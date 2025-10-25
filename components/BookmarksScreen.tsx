import type { FC } from 'react';
import { Button } from './common/Button';
import type { Bookmark } from '../types';

interface BookmarksScreenProps {
  bookmarks: Bookmark[];
  reviewSection: (sectionName: string) => void;
  goToQuestion: (section: string, index: number) => void;
  clearBookmarks: () => void;
  onBack?: () => void; // <-- add this
}

export const BookmarksScreen: FC<BookmarksScreenProps> = ({
  bookmarks,
  reviewSection,
  goToQuestion,
  clearBookmarks,
  onBack,
}) => {
  return (
    <div className="p-6 space-y-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold text-center">🔖 Bookmarked Questions</h1>

      {bookmarks.length === 0 ? (
        <p className="text-center text-gray-500">No bookmarks yet.</p>
      ) : (
        <ul className="space-y-2">
          {bookmarks.map((b) => (
            <li key={b.id} className="flex justify-between items-center border p-2 rounded">
              <span>{b.section} — Q{b.questionIndex + 1}</span>
              <Button variant="secondary" onClick={() => goToQuestion(b.section, b.questionIndex)}>
                Go
              </Button>
            </li>
          ))}
        </ul>
      )}

      <div className="flex justify-center gap-4">
        <Button variant="danger" onClick={clearBookmarks}>
          Clear All
        </Button>
        {onBack && (
          <Button variant="secondary" onClick={onBack}>
            ⬅️ Back
          </Button>
        )}
      </div>
    </div>
  );
};
