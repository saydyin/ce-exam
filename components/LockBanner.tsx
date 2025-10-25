import type { FC } from 'react';
import { Lock } from 'lucide-react';
import { Card } from './common/Card';

interface LockBannerProps {
  message?: string;
}

const LockBanner: FC<LockBannerProps> = ({
  message = 'Exam Locked — Please reset to take another attempt.',
}) => {
  return (
    <Card className="w-full p-4 bg-red-50 dark:bg-red-900/30 border border-red-300 dark:border-red-700 flex items-center justify-center space-x-2 rounded-xl">
      <Lock className="h-5 w-5 text-red-600 dark:text-red-400" />
      <span className="text-red-700 dark:text-red-300 font-medium">{message}</span>
    </Card>
  );
};

export default LockBanner;
