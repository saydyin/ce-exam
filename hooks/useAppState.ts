import { useState, useEffect, useCallback, useMemo } from 'react';
import {
  Question,
  Settings,
  AnswerSheet,
  SectionResults,
  Bookmark,
  WrongAnswerInfo,
  AppView,
} from '../types';
import { SECTIONS } from '../constants';
import { generateExam } from '../services/examGenerator';

const defaultSettings: Settings = {
  theme: 'light',
  fontSize: 'medium',
  autoSave: true,
  studyMode: false,
  keyboardShortcuts: true,
  navigationMode: 'scroll',
};

const EXAM_STATE_KEY = 'examAppState';
const EXAM_SETTINGS_KEY = 'examAppSettings';

export const useAppState = () => {
  const [view, setView] = useState<AppView>('loading');
  const [examQuestions, setExamQuestions] = useState<Question[]>([]);
  const [currentSectionIndex, setCurrentSectionIndex] = useState<number | null>(null);
  const [answers, setAnswers] = useState<AnswerSheet>({});
  const [results, setResults] = useState<SectionResults>({});
  const [timeSpent, setTimeSpent] = useState<{ [section: string]: number }>({});
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [settings, setSettings] = useState<Settings>(defaultSettings);
  const [isFullMockExam, setIsFullMockExam] = useState(false);
  const [reviewingSection, setReviewingSection] = useState<string | null>(null);
  const [examLocked, setExamLocked] = useState(false);
  const [resetToken, setResetToken] = useState(0);

  const sectionOrder = useMemo(() => Object.keys(SECTIONS), []);

  // ✅ Initialization effect to leave "loading"
  useEffect(() => {
    const init = async () => {
      try {
        const response = await fetch('/data/question_bank.json');
        const questionBank: Question[] = await response.json();
        const generatedQuestions = await generateExam(questionBank);
        setExamQuestions(generatedQuestions);
        setView('main-menu'); // ✅ leave loading state
      } catch (error) {
        console.error('❌ Failed to initialize exam:', error);
        setView('main-menu'); // fallback
      }
    };

    if (view === 'loading') {
      init();
    }
  }, [view]);

  // ✅ Reset exam data
  const resetExam = useCallback(
    async ({ soft = false, skipView = false }: { soft?: boolean; skipView?: boolean } = {}) => {
      setAnswers({});
      setResults({});
      setTimeSpent({});
      if (!soft) setBookmarks([]);
      setCurrentSectionIndex(null);
      setIsFullMockExam(false);
      setExamLocked(false);
      setReviewingSection(null);

      localStorage.removeItem(EXAM_STATE_KEY);

      try {
        const response = await fetch('/data/question_bank.json');
        const questionBank: Question[] = await response.json();
        const generatedQuestions = await generateExam(questionBank);
        setExamQuestions(generatedQuestions);

        if (!skipView) setView('main-menu');
      } catch (error) {
        console.error('❌ Failed to regenerate exam after reset:', error);
        if (!skipView) setView('main-menu');
      }

      setResetToken((t) => t + 1);
    },
    []
  );

  // ✅ Full mock exam resets first
  const startFullMockExam = useCallback(async () => {
    await resetExam({ soft: false, skipView: true });
    setCurrentSectionIndex(0);
    setIsFullMockExam(true);
    setView('instructions');
  }, [resetExam]);

  // Start a single section
  const startExam = useCallback(
    (sectionName: string) => {
      const sectionIndex = sectionOrder.findIndex((s) => s === sectionName);
      if (sectionIndex === -1 || results[sectionName]) return;
      setCurrentSectionIndex(sectionIndex);
      setIsFullMockExam(false);
      setView('instructions');
    },
    [results, sectionOrder]
  );

  // Answer selection
  const selectAnswer = useCallback(
    (questionIndex: number, choice: string) => {
      if (currentSectionIndex === null) return;
      const sectionName = sectionOrder[currentSectionIndex];
      setAnswers((prev) => {
        const currentAnswers = prev[sectionName] || [];
        const newAnswers = [...currentAnswers];
        newAnswers[questionIndex] = choice;
        return { ...prev, [sectionName]: newAnswers };
      });
    },
    [currentSectionIndex, sectionOrder]
  );

  // Submit section
  const submitSection = useCallback(() => {
    if (currentSectionIndex === null) return;
    const sectionName = sectionOrder[currentSectionIndex];
    const sectionQuestions = examQuestions.filter((q) => q.section === sectionName);
    const sectionAnswers = answers[sectionName] || [];
    let correctCount = 0;
    const wrongAnswers: WrongAnswerInfo[] = [];

    sectionQuestions.forEach((q, i) => {
      const userAnswer = sectionAnswers[i] || null;
      if (userAnswer === q.correct_answer) {
        correctCount++;
      } else {
        wrongAnswers.push({
          number: i + 1,
          stem: q.stem,
          user_answer: userAnswer,
          correct_answer: q.correct_answer,
          choices: q.choices,
          explanation: q.explanation,
          figure: q.figure,
        });
      }
    });

    const result = {
      score_pct: (correctCount / sectionQuestions.length) * 100,
      correct: correctCount,
      total: sectionQuestions.length,
      wrong: wrongAnswers,
    };

    const updatedResults = { ...results, [sectionName]: result };
    setResults(updatedResults);
    setView('results');

    if (sectionOrder.every((s) => updatedResults[s])) {
      setExamLocked(true);
    }
  }, [currentSectionIndex, examQuestions, answers, results, sectionOrder]);

  // Pause section
  const pauseSection = useCallback(
    (timeLeft: number) => {
      if (currentSectionIndex === null) return;
      const sectionName = sectionOrder[currentSectionIndex];
      const sectionTime = SECTIONS[sectionName as keyof typeof SECTIONS].time;
      const timeElapsed = sectionTime - timeLeft;
      setTimeSpent((prev) => ({
        ...prev,
        [sectionName]: (prev[sectionName] || 0) + timeElapsed,
      }));
      setCurrentSectionIndex(null);
      setView('main-menu');
    },
    [currentSectionIndex, sectionOrder]
  );

  // Next section
  const nextSection = useCallback(() => {
    if (isFullMockExam && currentSectionIndex !== null && currentSectionIndex < sectionOrder.length - 1) {
      setCurrentSectionIndex((prev) => prev! + 1);
      setView('instructions');
    } else {
      setView('final-results');
      setExamLocked(true);
    }
  }, [isFullMockExam, currentSectionIndex, sectionOrder]);

  // Settings
  const updateSettings = useCallback((newSettings: Partial<Settings>) => {
    setSettings((prev) => {
      const updated = { ...prev, ...newSettings };
      try {
        localStorage.setItem(EXAM_SETTINGS_KEY, JSON.stringify(updated));
      } catch (error) {
        console.error('Failed to save settings to localStorage', error);
      }
      return updated;
    });
  }, []);

  // Bookmarks
  const toggleBookmark = useCallback(
    (index: number) => {
      if (currentSectionIndex === null) return;
      const sectionName = sectionOrder[currentSectionIndex];
      const id = `${sectionName}-${index}`;
      setBookmarks((prev) => {
        const exists = prev.some((b) => b.id === id);
        if (exists) {
          return prev.filter((b) => b.id !== id);
        }
        return [
          ...prev,
          {
            id,
            section: sectionName,
            questionIndex: index,
            timestamp: new Date().toISOString(),
          },
        ];
      });
    },
    [currentSectionIndex, sectionOrder]
  );

  const isBookmarked = useCallback(
    (index: number): boolean => {
      if (currentSectionIndex === null) return false;
      const sectionName = sectionOrder[currentSectionIndex];
      const id = `${sectionName}-${index}`;
      return bookmarks.some((b) => b.id === id);
    },
    [currentSectionIndex, sectionOrder, bookmarks]
  );

  const clearBookmarks = useCallback(() => {
    setBookmarks([]);
  }, []);

  const getQuestionById = useCallback(
    (section: string, index: number): Question | undefined => {
      const sectionQuestions = examQuestions.filter((q) => q.section === section);
      return sectionQuestions[index];
    },
    [examQuestions]
  );

  const goToQuestion = useCallback(
    (section: string, index: number) => {
      const sectionIndex = sectionOrder.findIndex((s) => s === section);
      if (sectionIndex === -1) return;
      setCurrentSectionIndex(sectionIndex);
      setIsFullMockExam(false);
      setView('exam');
    },
    [sectionOrder]
  );

  // Review
  const reviewSection = useCallback((sectionName: string) => {
    setReviewingSection(sectionName);
    setView('review');
  }, []);

  const backFromReview = useCallback(() => {
    setReviewingSection(null);
    const allSectionsDone = sectionOrder.every((s) => results[s]);
    if (allSectionsDone) {
      setView('final-results');
    } else if (Object.keys(results).length > 0) {
      setView('analytics');
    } else {
      setView('main-menu');
    }
  }, [results, sectionOrder]);

  // ✅ Return everything needed by App.tsx and screens
  return {
    view,
    setView,
    examQuestions,
    currentSection:
      currentSectionIndex !== null
        ? SECTIONS[sectionOrder[currentSectionIndex] as keyof typeof SECTIONS]
        : null,
    currentQuestions:
      currentSectionIndex !== null
        ? examQuestions.filter(
            (q) => q.section === sectionOrder[currentSectionIndex]
          )
        : [],
    answers,
    results,
    initialTime:
      currentSectionIndex !== null
        ? SECTIONS[sectionOrder[currentSectionIndex] as keyof typeof SECTIONS]
            .time -
          (timeSpent[sectionOrder[currentSectionIndex]] || 0)
        : undefined,
    settings,
    bookmarks,
    reviewingSection,
    examLocked,
    sectionOrder,
    startExam,
    startFullMockExam,
    resetExam,
    selectAnswer,
    submitSection,
    pauseSection,
    nextSection,
    updateSettings,
    toggleBookmark,
    isBookmarked,
    clearBookmarks,
    getQuestionById,
    goToQuestion,
    reviewSection,
    backFromReview,
    resetToken,
  };
};
