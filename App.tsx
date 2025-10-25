import { useEffect } from 'react';
import { useAppState } from './hooks/useAppState';
import { MainMenu } from './components/MainMenu';
import { InstructionsScreen } from './components/InstructionsScreen';
import { ExamScreen } from './components/ExamScreen';
import { ResultsScreen } from './components/ResultsScreen';
import { FinalResultsScreen } from './components/FinalResultsScreen';
import { SettingsScreen } from './components/SettingsScreen';
import { BookmarksScreen } from './components/BookmarksScreen';
import { AnalyticsScreen } from './components/AnalyticsScreen';
import { ReviewScreen } from './components/ReviewScreen';
import { LoadingSpinner } from './components/common/LoadingSpinner';

const App = () => {
  const app = useAppState();

  // Theme toggle
  useEffect(() => {
    const root = window.document.documentElement;
    if (app.settings.theme === 'dark') {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
  }, [app.settings.theme]);

  const renderContent = () => {
    switch (app.view) {
      case 'loading':
        return (
          <div className="flex flex-col items-center justify-center h-screen bg-gray-50 dark:bg-gray-900">
            <LoadingSpinner size="lg" />
            <p className="mt-4 text-gray-600 dark:text-gray-300">
              Preparing Your Exam...
            </p>
          </div>
        );

      case 'main-menu':
        return (
          <MainMenu
            key={app.resetToken} // ✅ force remount after reset
            results={app.results}
            startExam={app.startExam}
            startFullMockExam={app.startFullMockExam}
            resetExam={app.resetExam}
            setView={app.setView}
            reviewSection={app.reviewSection}
          />
        );

      case 'instructions':
        return (
          <InstructionsScreen
            section={app.currentSection!}
            onStart={() => app.setView('exam')}
            onBack={() => app.setView('main-menu')}
          />
        );

      case 'exam':
        return (
          <ExamScreen
            section={app.currentSection!}
            questions={app.currentQuestions}
            initialAnswers={app.answers[app.currentSection!.name] || []}
            initialTime={app.initialTime}
            onSubmit={app.submitSection}
            onPause={app.pauseSection}
            onSelectAnswer={app.selectAnswer}
            settings={app.settings}
            toggleBookmark={app.toggleBookmark}
            isBookmarked={app.isBookmarked}
          />
        );

      case 'results':
        return (
          <ResultsScreen
            section={app.currentSection!}
            result={app.results[app.currentSection!.name]}
            onNextSection={app.nextSection}
            onReviewAll={() => app.reviewSection(app.currentSection!.name)}
          />
        );

      case 'final-results':
        return (
          <FinalResultsScreen
            results={app.results}
            onRestart={app.resetExam}
            onMainMenu={() => app.setView('main-menu')}
            onReview={app.reviewSection}
          />
        );

      case 'settings':
        return (
          <SettingsScreen
            settings={app.settings}
            onUpdateSettings={app.updateSettings}
            onBack={() => app.setView('main-menu')}
          />
        );

      case 'bookmarks':
        return (
          <BookmarksScreen
            bookmarks={app.bookmarks}
            reviewSection={app.reviewSection}
            goToQuestion={app.goToQuestion}
            clearBookmarks={app.clearBookmarks}
            onBack={() => app.setView('main-menu')} // ✅ back button works
          />
        );

      case 'analytics':
        return (
          <AnalyticsScreen
            results={app.results}
            onBack={() => app.setView('main-menu')} // ✅ back button works
            onReview={app.reviewSection}
          />
        );

      case 'review':
        return (
          <ReviewScreen
            sectionName={app.reviewingSection!}
            questions={app.examQuestions.filter(
              (q) => q.section === app.reviewingSection
            )}
            answers={app.answers[app.reviewingSection!] || []}
            onBack={app.backFromReview}
          />
        );

      default:
        return <div className="p-6 text-center">Unknown state</div>;
    }
  };

  return (
    <div
      className={`font-sans bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen ${
        app.settings.fontSize === 'small'
          ? 'text-sm'
          : app.settings.fontSize === 'large'
          ? 'text-lg'
          : 'text-base'
      }`}
    >
      {renderContent()}
    </div>
  );
};

export default App;
