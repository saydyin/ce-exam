import { useState, useEffect, useRef, FC, createRef } from 'react';
import { Question, Section, Settings } from '../types';
import { Button } from './common/Button';
import { Card } from './common/Card';
import { BookmarkIcon, CheckIcon, ChevronLeftIcon, ChevronRightIcon, PauseIcon, PlayIcon } from './common/icons';
import { ImageZoomModal } from './common/ImageZoomModal';

interface ExamScreenProps {
  section: Section;
  questions: Question[];
  initialAnswers: (string | null)[];
  initialTime: number | undefined;
  onSubmit: () => void;
  onPause: (timeLeft: number) => void;
  onSelectAnswer: (questionIndex: number, choice: string) => void;
  settings: Settings;
  toggleBookmark: (index: number) => void;
  isBookmarked: (index: number) => boolean;
}

const formatTime = (seconds: number) => {
  if (seconds < 0) seconds = 0;
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return [h, m, s].map(v => v.toString().padStart(2, '0')).join(':');
};

export const ExamScreen: FC<ExamScreenProps> = ({
  section,
  questions,
  initialAnswers,
  initialTime,
  onSubmit,
  onPause,
  onSelectAnswer,
  settings,
  toggleBookmark,
  isBookmarked,
}) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [timeLeft, setTimeLeft] = useState(initialTime ?? section.time);
  const [isPaused, setIsPaused] = useState(false);
  const [answers, setAnswers] = useState(initialAnswers);
  const [showConfirmSubmit, setShowConfirmSubmit] = useState(false);
  const [zoomedImage, setZoomedImage] = useState<string | null>(null);

  const questionRefs = useRef<React.RefObject<HTMLDivElement>[]>([]);
  questionRefs.current = questions.map((_, i) => questionRefs.current[i] ?? createRef<HTMLDivElement>());

  // Timer effect
  useEffect(() => {
    if (isPaused) return;

    if (timeLeft <= 0) {
      onSubmit();
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, isPaused, onSubmit]);
  
  // Scroll to current question
  useEffect(() => {
    if (settings.navigationMode === 'scroll') {
      questionRefs.current[currentQuestionIndex]?.current?.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
  }, [currentQuestionIndex, settings.navigationMode]);
  
  const handleSelectAnswer = (questionIndex: number, choice: string) => {
    onSelectAnswer(questionIndex, choice);
    // Update local state to re-render choices immediately
    setAnswers(prev => {
        const newAnswers = [...prev];
        newAnswers[questionIndex] = choice;
        return newAnswers;
    });
  };

  const unansweredQuestions = questions.length - answers.filter(Boolean).length;

  const renderQuestion = (q: Question, index: number) => {
    const userAnswer = answers[index];
    
    return (
      <Card key={index} ref={questionRefs.current[index]} id={`question-${index}`} className="mb-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <p className="font-bold text-lg">Question {index + 1}</p>
            {q.group_id && (
              <p className="text-sm font-semibold text-purple-600 dark:text-purple-400 mt-1">
                Situation: {q.group_id}
              </p>
            )}
          </div>
          <Button
            variant={isBookmarked(index) ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => toggleBookmark(index)}
            aria-label={isBookmarked(index) ? 'Remove bookmark' : 'Add bookmark'}
          >
            <BookmarkIcon />
          </Button>
        </div>
        <p className="mb-4 whitespace-pre-wrap">{q.stem}</p>
        {q.figure && (
          <div className="mb-4">
            <img
              src={q.figure}
              alt={`Figure for question ${index + 1}`}
              className="max-w-sm h-auto rounded-lg mx-auto cursor-zoom-in"
              onClick={() => setZoomedImage(q.figure)}
            />
          </div>
        )}
        <div className="space-y-3">
          {q.choices.map((choice, choiceIndex) => {
            const choiceLetter = String.fromCharCode(65 + choiceIndex);
            const isSelected = userAnswer === choiceLetter;
            return (
              <button
                key={choiceIndex}
                onClick={() => handleSelectAnswer(index, choiceLetter)}
                className={`w-full text-left border-2 rounded-lg p-3 flex items-start transition-colors ${
                  isSelected
                    ? 'border-purple-500 bg-purple-50 dark:bg-purple-900'
                    : 'border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <span className="font-bold mr-3">{choiceLetter}.</span>
                <span>{choice}</span>
              </button>
            );
          })}
        </div>
      </Card>
    );
  };
  
  return (
    <div className="flex flex-col h-screen">
      <header className="bg-white dark:bg-gray-800 shadow-md p-4 sticky top-0 z-10">
        <div className="container mx-auto flex justify-between items-center">
          <div>
            <h1 className="text-xl font-bold">{section.title}</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Question {currentQuestionIndex + 1} of {questions.length}
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-2xl font-mono bg-gray-100 dark:bg-gray-700 px-4 py-2 rounded-lg">
              {formatTime(timeLeft)}
            </div>
            <Button onClick={() => setIsPaused(!isPaused)} variant="secondary">
              {isPaused ? <PlayIcon/> : <PauseIcon />}
              {isPaused ? 'Resume' : 'Pause'}
            </Button>
            <Button onClick={() => setShowConfirmSubmit(true)} variant="primary">
              <CheckIcon /> Submit
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto bg-gray-100 dark:bg-gray-950 p-4 sm:p-6 md:p-8">
        <div className="container mx-auto max-w-4xl">
           {settings.navigationMode === 'scroll' ? (
             questions.map(renderQuestion)
           ) : (
             renderQuestion(questions[currentQuestionIndex], currentQuestionIndex)
           )}
        </div>
      </main>

      {settings.navigationMode === 'buttons' && (
        <footer className="bg-white dark:bg-gray-800 p-4 border-t dark:border-gray-700 sticky bottom-0">
          <div className="container mx-auto flex justify-between items-center">
            <Button onClick={() => setCurrentQuestionIndex(p => Math.max(0, p - 1))} disabled={currentQuestionIndex === 0}>
              <ChevronLeftIcon /> Previous
            </Button>
            <Button onClick={() => setCurrentQuestionIndex(p => Math.min(questions.length - 1, p + 1))} disabled={currentQuestionIndex === questions.length - 1}>
              Next <ChevronRightIcon />
            </Button>
          </div>
        </footer>
      )}

      {isPaused && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex flex-col justify-center items-center z-50">
          <h2 className="text-4xl font-bold text-white mb-4">Exam Paused</h2>
          <div className="flex gap-4">
             <Button onClick={() => setIsPaused(false)} size="lg">Resume Exam</Button>
             <Button onClick={() => onPause(timeLeft)} variant="secondary" size="lg">Save & Exit</Button>
          </div>
        </div>
      )}
      
      {showConfirmSubmit && (
         <div className="fixed inset-0 bg-black bg-opacity-75 flex flex-col justify-center items-center z-50 p-4">
            <Card className="max-w-md w-full text-center">
                <h2 className="text-2xl font-bold mb-4">Confirm Submission</h2>
                {unansweredQuestions > 0 && (
                    <p className="mb-4 text-yellow-600 dark:text-yellow-400">
                        You have {unansweredQuestions} unanswered question{unansweredQuestions > 1 ? 's' : ''}.
                    </p>
                )}
                <p className="mb-6">Are you sure you want to submit your answers for this section?</p>
                <div className="flex justify-center gap-4">
                    <Button onClick={() => setShowConfirmSubmit(false)} variant="secondary">Cancel</Button>
                    <Button onClick={onSubmit} variant="primary">Yes, Submit</Button>
                </div>
            </Card>
         </div>
      )}

      {zoomedImage && <ImageZoomModal src={zoomedImage} alt="Zoomed figure" onClose={() => setZoomedImage(null)} />}
    </div>
  );
};