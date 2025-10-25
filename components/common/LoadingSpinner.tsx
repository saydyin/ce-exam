import type { FC } from 'react';
import { ThemeIcon } from './icons';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
}

export const LoadingSpinner: FC<LoadingSpinnerProps> = ({ size = 'md' }) => {
  const sizeClasses = {
    sm: 'w-6 h-6',
    md: 'w-10 h-10',
    lg: 'w-16 h-16',
  };

  return (
    <div className="flex justify-center items-center">
      <ThemeIcon className={`animate-spin text-purple-600 dark:text-purple-400 ${sizeClasses[size]}`} />
    </div>
  );
};