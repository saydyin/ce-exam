import type { FC } from 'react';
import { SectionResults } from '../types';
import { SECTIONS } from '../constants';
import { Button } from './common/Button';
import { Card } from './common/Card';

interface AnalyticsScreenProps {
  results: SectionResults;
  onBack: () => void;
  onReview: (sectionName: string) => void;
}

export const AnalyticsScreen: FC<AnalyticsScreenProps> = ({ results, onBack, onReview }) => {
  const hasResults = Object.keys(results).length > 0;
  
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 sm:p-6 md:p-8">
      <div className="max-w-5xl mx-auto">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Performance Analytics</h1>
          <Button onClick={onBack} variant="secondary">Back</Button>
        </header>

        {hasResults ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {Object.keys(results).map(sectionName => {
                    const result = results[sectionName];
                    const section = SECTIONS[sectionName as keyof typeof SECTIONS];
                    const passed = result.score_pct >= 70;
                    return (
                        <Card key={sectionName} className="flex flex-col">
                            <h2 className="text-xl font-bold mb-1">{section.title}</h2>
                            <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">{section.name}</p>

                            <div className="text-center my-4">
                                <p className={`text-5xl font-bold ${passed ? 'text-green-500' : 'text-red-500'}`}>{result.score_pct.toFixed(2)}%</p>
                                <p className="font-semibold text-gray-600 dark:text-gray-300">{result.correct} / {result.total} Correct</p>
                            </div>
                            
                            <div className="space-y-2 text-sm">
                                <div className="flex justify-between"><span className="font-medium">Correct Answers:</span> <span>{result.correct}</span></div>
                                <div className="flex justify-between"><span className="font-medium">Incorrect Answers:</span> <span>{result.wrong.length}</span></div>
                                <div className="flex justify-between"><span className="font-medium">Unanswered:</span> <span>{result.total - result.correct - result.wrong.length}</span></div>
                            </div>
                            
                            <div className="mt-auto pt-6">
                                <Button onClick={() => onReview(sectionName)} className="w-full">Review Wrong Answers</Button>
                            </div>
                        </Card>
                    );
                })}
            </div>
        ) : (
          <Card className="text-center py-12">
            <h2 className="text-xl font-semibold text-gray-700 dark:text-gray-300">No Analytics Available</h2>
            <p className="mt-2 text-gray-500 dark:text-gray-400">Complete at least one exam section to see your performance analytics.</p>
          </Card>
        )}
      </div>
    </div>
  );
};
