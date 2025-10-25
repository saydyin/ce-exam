import type { FC } from 'react';
import { Section } from '../types';
import { Button } from './common/Button';
import { Card } from './common/Card';
import { PRC_INSTRUCTIONS, MOTIVATIONAL_QUOTES } from '../constants';

interface InstructionsScreenProps {
  section: Section;
  onStart: () => void;
  onBack: () => void;
}

export const InstructionsScreen: FC<InstructionsScreenProps> = ({ section, onStart, onBack }) => {
  const randomQuote = MOTIVATIONAL_QUOTES[Math.floor(Math.random() * MOTIVATIONAL_QUOTES.length)];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
      <Card className="max-w-2xl w-full">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-purple-600 dark:text-purple-400">Instructions</h1>
          <p className="mt-2 text-lg font-semibold">{section.title}</p>
        </div>

        <div className="mt-6 p-4 bg-yellow-50 dark:bg-gray-700 border-l-4 border-yellow-400 dark:border-yellow-500">
          <p className="font-bold">Please read the following instructions carefully:</p>
          <ul className="mt-2 list-disc list-inside space-y-1 text-gray-700 dark:text-gray-300">
            {PRC_INSTRUCTIONS.map((instruction, index) => (
              <li key={index}>{instruction}</li>
            ))}
             <li>This section has <strong>{section.total} questions</strong>.</li>
            <li>You have <strong>{section.time / 3600} hours</strong> to complete this section.</li>
          </ul>
        </div>
        
        <div className="mt-6 text-center italic text-gray-500 dark:text-gray-400">
          <p>"{randomQuote}"</p>
        </div>

        <div className="mt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
          <Button onClick={onBack} variant="secondary">Back to Main Menu</Button>
          <Button onClick={onStart} size="lg">Start Exam Section</Button>
        </div>
      </Card>
    </div>
  );
};
