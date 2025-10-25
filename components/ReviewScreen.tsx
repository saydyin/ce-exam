import { useState, FC } from 'react';
import { Question } from '../types';
import { Button } from './common/Button';
import { Card } from './common/Card';
import { SECTIONS } from '../constants';
import { ImageZoomModal } from './common/ImageZoomModal';

interface ReviewScreenProps {
  sectionName: string;
  questions: Question[];
  answers: (string | null)[];
  onBack: () => void;
}

export const ReviewScreen: FC<ReviewScreenProps> = ({ sectionName, questions, answers, onBack }) => {
  const [zoomedImage, setZoomedImage] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 p-4 sm:p-6 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="flex justify-between items-center mb-6 pb-4 border-b border-gray-200 dark:border-gray-700">
          <div>
            <h1 className="text-3xl font-bold">Review Answers</h1>
            <p className="text-lg text-gray-500 dark:text-gray-400">{SECTIONS[sectionName as keyof typeof SECTIONS].title}</p>
          </div>
          <Button onClick={onBack} variant="secondary">Back</Button>
        </header>

        <div className="space-y-6">
          {questions.map((q, index) => {
            const userAnswer = answers[index];
            const isCorrect = userAnswer === q.correct_answer;
            return (
              <Card key={index}>
                <div className="mb-4">
                  <p className="font-bold text-lg">Question {index + 1}</p>
                   {q.group_id && (
                    <p className="text-sm font-semibold text-purple-600 dark:text-purple-400 mt-1">
                      Situation: {q.group_id}
                    </p>
                  )}
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
                <div className="space-y-3 mb-4">
                  {q.choices.map((choice, choiceIndex) => {
                    const choiceLetter = String.fromCharCode(65 + choiceIndex);
                    const isUserAnswer = userAnswer === choiceLetter;
                    const isCorrectAnswer = q.correct_answer === choiceLetter;
                    
                    let choiceClasses = "border-2 rounded-lg p-3 flex items-start";
                    if (isCorrectAnswer) {
                        choiceClasses += " bg-green-100 dark:bg-green-900 border-green-500";
                    } else if (isUserAnswer && !isCorrect) {
                        choiceClasses += " bg-red-100 dark:bg-red-900 border-red-500";
                    } else {
                        choiceClasses += " bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700";
                    }

                    return (
                      <div key={choiceIndex} className={choiceClasses}>
                        <span className="font-bold mr-3">{choiceLetter}.</span>
                        <span>{choice}</span>
                      </div>
                    );
                  })}
                </div>
                
                <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                    <p className="font-bold">Your Answer: <span className={isCorrect ? 'text-green-500' : 'text-red-500'}>{userAnswer || "Not Answered"}</span></p>
                    <p className="font-bold">Correct Answer: <span className="text-green-500">{q.correct_answer}</span></p>
                    {q.explanation && (
                        <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
                           <p className="font-semibold">Explanation:</p>
                           <p className="text-sm">{q.explanation}</p>
                        </div>
                    )}
                </div>
              </Card>
            );
          })}
        </div>
        {zoomedImage && <ImageZoomModal src={zoomedImage} alt="Zoomed figure" onClose={() => setZoomedImage(null)} />}
      </div>
    </div>
  );
};