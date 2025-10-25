import type { FC } from 'react';
import { SectionResults } from '../types';
import { Button } from './common/Button';
import { Card } from './common/Card';
import { SECTIONS, SECTION_WEIGHTS } from '../constants';

interface FinalResultsScreenProps {
  results: SectionResults;
  onRestart: () => void;
  onMainMenu: () => void;
  onReview: (sectionName: string) => void;
}

export const FinalResultsScreen: FC<FinalResultsScreenProps> = ({ results, onRestart, onMainMenu, onReview }) => {
  const allSections = Object.keys(SECTIONS);
  const completedSections = allSections.filter(s => results[s]);

  if (completedSections.length === 0) {
    return (
      <div className="flex items-center justify-center h-screen text-center p-4">
        <div>
          <h1 className="text-2xl font-bold mb-4">No Results Available</h1>
          <p className="text-gray-500 dark:text-gray-400 mb-6">You must complete at least one section to see the final results.</p>
          <Button onClick={onMainMenu}>Back to Main Menu</Button>
        </div>
      </div>
    );
  }

  const weightedSum = completedSections.reduce(
    (sum, section) => sum + (results[section]?.score_pct || 0) * SECTION_WEIGHTS[section as keyof typeof SECTION_WEIGHTS],
    0
  );
  
  const totalWeight = completedSections.reduce(
    (sum, section) => sum + SECTION_WEIGHTS[section as keyof typeof SECTION_WEIGHTS],
    0
  );
  
  const gwa = totalWeight > 0 ? weightedSum / totalWeight : 0;
  
  const allSectionsDone = allSections.every(s => results[s]);
  const hasFailingSection = allSectionsDone && completedSections.some(s => results[s].score_pct < 50);
  const passed = allSectionsDone && gwa >= 70 && !hasFailingSection;


  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-4 sm:p-6 md:p-8">
      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold">Final Examination Results</h1>
        </header>

        <Card className="p-6 bg-white dark:bg-gray-800 shadow-lg rounded-xl mb-8">
          <div className="text-center">
            <p className={`text-6xl font-bold ${passed ? 'text-green-500' : 'text-red-500'}`}>{gwa.toFixed(2)}%</p>
            <p className="text-2xl font-semibold text-gray-700 dark:text-gray-300">
              {allSectionsDone ? "General Weighted Average" : "Current Weighted Average"}
            </p>
            <p className={`mt-2 text-3xl font-bold ${passed ? 'text-green-500' : 'text-red-500'}`}>{passed ? 'PASSED' : 'FAILED'}</p>
            {allSectionsDone && <p className="text-sm mt-2 text-gray-500 dark:text-gray-400">Passing criteria: GWA of 70% and no section score below 50%.</p>}
            {hasFailingSection && <p className="text-sm mt-1 text-red-500">You failed because at least one section score was below 50%.</p>}
          </div>

          <table className="w-full mt-8 text-left border-collapse">
            <thead>
              <tr className="border-b-2 border-gray-300 dark:border-gray-700">
                <th className="py-3 px-3 font-semibold">Section</th>
                <th className="py-3 px-3 text-center font-semibold">Correct</th>
                <th className="py-3 px-3 text-center font-semibold">Total</th>
                <th className="py-3 px-3 text-center font-semibold">Score</th>
                <th className="py-3 px-3 text-center font-semibold">Action</th>
              </tr>
            </thead>
            <tbody>
              {allSections.map(sectionName => {
                const result = results[sectionName];
                const section = SECTIONS[sectionName as keyof typeof SECTIONS];
                if (!result) return null;
                const sectionPassed = result.score_pct >= 50;
                return (
                  <tr
                    // FIX: Type 'Section' is not assignable to type 'Key'. Use sectionName which is a string.
                    key={sectionName}
                    className="border-b border-gray-200 dark:border-gray-700"
                  >
                    <td className="py-3 px-3 font-medium">{section.name}</td>
                    <td className="py-3 px-3 text-center">{result.correct}</td>
                    <td className="py-3 px-3 text-center">{result.total}</td>
                    <td className={`py-3 px-3 text-center font-bold ${!sectionPassed && allSectionsDone ? 'text-red-500' : ''}`}>
                      {result.score_pct.toFixed(2)}%
                    </td>
                    <td className="py-3 px-3 text-center">
                       <Button onClick={() => onReview(sectionName)} variant="text" size="sm">View Results</Button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </Card>

        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <Button onClick={onMainMenu} variant="secondary">Back to Main Menu</Button>
          <Button onClick={onRestart}>Reset & Start New Exam</Button>
        </div>
      </div>
    </div>
  );
};