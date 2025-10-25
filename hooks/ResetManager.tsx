// src/hooks/ResetManager.tsx
import { useCallback } from 'react';
import { Question } from '../types';
import { generateExam } from '../services/examGenerator';

const EXAM_STATE_KEY = 'examAppState';

interface ResetManagerProps {
  setAnswers: React.Dispatch<React.SetStateAction<any>>;
  setResults: React.Dispatch<React.SetStateAction<any>>;
  setTimeSpent: React.Dispatch<React.SetStateAction<any>>;
  setBookmarks: React.Dispatch<React.SetStateAction<any>>;
  setCurrentSectionIndex: React.Dispatch<React.SetStateAction<number | null>>;
  setIsFullMockExam: React.Dispatch<React.SetStateAction<boolean>>;
  setExamLocked: React.Dispatch<React.SetStateAction<boolean>>;
  setReviewingSection: React.Dispatch<React.SetStateAction<string | null>>;
  setExamQuestions: React.Dispatch<React.SetStateAction<Question[]>>;
  setView: React.Dispatch<React.SetStateAction<string>>;
  setResetToken: React.Dispatch<React.SetStateAction<number>>;
}

export function useResetManager({
  setAnswers,
  setResults,
  setTimeSpent,
  setBookmarks,
  setCurrentSectionIndex,
  setIsFullMockExam,
  setExamLocked,
  setReviewingSection,
  setExamQuestions,
  setView,
  setResetToken,
}: ResetManagerProps) {
  const resetExam = useCallback(async () => {
    console.log('🔄 Resetting exam…');

    // Clear all state
    setAnswers({});
    setResults({});
    setTimeSpent({});
    setBookmarks([]);
    setCurrentSectionIndex(null);
    setIsFullMockExam(false);
    setExamLocked(false);
    setReviewingSection(null);

    // Clear localStorage
    localStorage.removeItem(EXAM_STATE_KEY);

    // Regenerate questions
    try {
      const response = await fetch('/data/question_bank.json');
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const questionBank: Question[] = await response.json();
      const generatedQuestions = await generateExam(questionBank);
      setExamQuestions(generatedQuestions);
    } catch (error) {
      console.error('❌ Failed to regenerate exam after reset:', error);
    }

    // Force MainMenu remount
    setResetToken((t) => t + 1);
    setView('main-menu');
  }, [
    setAnswers,
    setResults,
    setTimeSpent,
    setBookmarks,
    setCurrentSectionIndex,
    setIsFullMockExam,
    setExamLocked,
    setReviewingSection,
    setExamQuestions,
    setView,
    setResetToken,
  ]);

  return { resetExam };
}
