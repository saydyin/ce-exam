import type { FC } from 'react';
import { Button } from './common/Button';
import { Card } from './common/Card';
import { SECTIONS } from '../constants';
import type { SectionResults } from '../types';

interface MainMenuProps {
  results: { [section: string]: SectionResults };
  startExam: (sectionName: string) => void;
  startFullMockExam: () => void;
  resetExam: () => void;
  setView: (view: string) => void;
  reviewSection: (sectionName: string) => void;
}

export const MainMenu: FC<MainMenuProps> = ({
  results,
  startExam,
  startFullMockExam,
  resetExam,
  setView,
  reviewSection,
}) => {
  const completedCount = Object.keys(results).length;
  const totalSections = Object.keys(SECTIONS).length;

  return (
    <div className="p-6 space-y-8 max-w-5xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl font-bold">Civil Engineering Exam Simulator</h1>
        <p className="text-gray-600 dark:text-gray-400">
          {completedCount}/{totalSections} sections completed
        </p>
      </div>

      {/* Section Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {Object.values(SECTIONS).map((section, idx) => {
          const result = results?.[section.name];
          const isCompleted = result && Number.isFinite(result.score_pct);

          return (
            <Card key={section.name} className="p-5 flex flex-col justify-between">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <span>{['📐','🏗️','📊','🧱','🌉','💧'][idx % 6]}</span>
                  {section.name}
                </h2>
                {isCompleted && (
                  <span className="text-sm font-medium text-green-600">
                    {result.score_pct.toFixed(1)}%
                  </span>
                )}
              </div>

              <p className="text-sm text-gray-500 mb-4">{section.description}</p>

              {isCompleted ? (
                <Button
                  variant="secondary"
                  className="w-full"
                  onClick={() => reviewSection(section.name)}
                >
                  Review Section
                </Button>
              ) : (
                <Button
                  variant="primary"
                  className="w-full"
                  onClick={() => startExam(section.name)}
                >
                  Start Section
                </Button>
              )}

              {isCompleted && (
                <div className="mt-3 h-2 bg-gray-200 rounded">
                  <div
                    className="h-2 bg-green-500 rounded"
                    style={{ width: `${result.score_pct}%` }}
                  />
                </div>
              )}
            </Card>
          );
        })}
      </div>

      {/* Full Mock Exam */}
      <div className="flex justify-center">
        <Button variant="primary" size="lg" onClick={startFullMockExam}>
          🚀 Start Full Mock Exam
        </Button>
      </div>

      {/* Navigation Buttons */}
      <div className="flex justify-center gap-4">
        <Button variant="secondary" onClick={() => setView('settings')}>
          ⚙️ Settings
        </Button>
        <Button variant="secondary" onClick={() => setView('bookmarks')}>
          🔖 Bookmarks
        </Button>
        <Button variant="secondary" onClick={() => setView('analytics')}>
          📊 Analytics
        </Button>
      </div>

      {/* Reset Exam Data */}
      <div className="flex justify-center">
        <Button
          variant="danger"
          onClick={() => {
            if (
              window.confirm(
                'Are you sure you want to reset all exam data? This cannot be undone.'
              )
            ) {
              resetExam();
            }
          }}
        >
          🗑️ Reset Exam Data
        </Button>
      </div>
    </div>
  );
};
