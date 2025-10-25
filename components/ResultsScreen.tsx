import type { FC } from 'react';
import { Section, SectionResult } from '../types';
import { Button } from './common/Button';
import { Card } from './common/Card';
import { SECTIONS } from '../constants';
import { ImageZoomModal } from './common/ImageZoomModal';
import { useState } from 'react';

interface ResultsScreenProps {
  section: Section;
  result: SectionResult;
  onNextSection: () => void;
  onReviewAll: () => void;
}

export const ResultsScreen: FC<ResultsScreenProps> = ({ section, result, onNextSection, onReviewAll }) => {
  const [zoomedImage, setZoomedImage] = useState<string | null>(null);
  const passed = result.score_pct >= 70;

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 p-4 sm:p-6 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-6">
          <h1 className="text-3xl font-bold">Section Results: {section.title}</h1>
        </header>

        <Card className="text-center mb-6">
          <p className={`text-6xl font-bold ${passed ? 'text-green-500' : 'text-red-500'}`}>{result.score_pct.toFixed(2)}%</p>
          <p className="text-2xl font-semibold text-gray-700 dark:text-gray-300">{result.correct} / {result.total} Correct</p>
          <p className={`mt-2 text-xl font-bold ${passed ? 'text-green-500' : 'text-red-500'}`}>{passed ? 'PASSED' : 'FAILED'}</p>
        </Card>
        
        <div className="flex flex-col sm:flex-row justify-center gap-4 mb-8">
            <Button onClick={onReviewAll}>Review All Questions</Button>
            <Button onClick={onNextSection} variant="primary">
                Continue
            </Button>
        </div>

        {result.wrong.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-4 text-center">Incorrect Answers Review</h2>
            <div className="space-y-6">
              {result.wrong.map((wrong, idx) => (
                <Card key={idx}>
                   <div className="mb-4">
                     <p className="font-bold text-lg">Question {wrong.number}</p>
                   </div>
                   <p className="mb-4 whitespace-pre-wrap">{wrong.stem}</p>
                   {wrong.figure && (
                     <div className="mb-4">
                       <img 
                         src={wrong.figure} 
                         alt={`Figure for question ${wrong.number}`} 
                         className="max-w-sm h-auto rounded-lg mx-auto cursor-zoom-in"
                         onClick={() => setZoomedImage(wrong.figure)}
                       />
                     </div>
                   )}
                   <div className="space-y-3 mb-4">
                     {wrong.choices.map((choice, choiceIndex) => {
                       const choiceLetter = String.fromCharCode(65 + choiceIndex);
                       const isUserAnswer = wrong.user_answer === choiceLetter;
                       const isCorrectAnswer = wrong.correct_answer === choiceLetter;
                       
                       let choiceClasses = "border-2 rounded-lg p-3 flex items-start text-left w-full";
                       if (isCorrectAnswer) {
                           choiceClasses += " bg-green-100 dark:bg-green-900 border-green-500 text-green-800 dark:text-green-200";
                       } else if (isUserAnswer) {
                           choiceClasses += " bg-red-100 dark:bg-red-900 border-red-500 text-red-800 dark:text-red-200";
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
                   <div className="mt-4 p-4 bg-gray-100 dark:bg-gray-800 rounded-lg text-left">
                       <p className="font-bold text-red-600 dark:text-red-400">Your Answer: {wrong.user_answer || "Not Answered"}</p>
                       <p className="font-bold text-green-600 dark:text-green-400">Correct Answer: {wrong.correct_answer}</p>
                       {wrong.explanation && (
                           <div className="mt-2 pt-2 border-t border-gray-200 dark:border-gray-700">
                              <p className="font-semibold">Explanation:</p>
                              <p className="text-sm">{wrong.explanation}</p>
                           </div>
                       )}
                   </div>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
      {zoomedImage && <ImageZoomModal src={zoomedImage} alt="Zoomed figure" onClose={() => setZoomedImage(null)} />}
    </div>
  );
};
