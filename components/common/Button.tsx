import type { FC, ButtonHTMLAttributes, ReactNode } from 'react';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: 'primary' | 'secondary' | 'text' | 'danger' | 'danger_text';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export const Button: FC<ButtonProps> = ({ children, variant = 'primary', size = 'md', className = '', ...props }) => {
  const baseClasses = 'inline-flex items-center justify-center font-bold rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed gap-2';

  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-sm',
    lg: 'px-8 py-3 text-base',
  };

  const variantClasses = {
    primary: 'bg-purple-600 text-white hover:bg-purple-700 focus:ring-purple-500',
    secondary: 'bg-purple-100 text-purple-700 hover:bg-purple-200 dark:bg-gray-700 dark:text-gray-200 dark:hover:bg-gray-600 focus:ring-purple-500',
    text: 'text-purple-600 hover:bg-purple-100 dark:text-purple-400 dark:hover:bg-gray-700 focus:ring-purple-500',
    danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
    danger_text: 'text-red-600 hover:bg-red-100 dark:text-red-400 dark:hover:bg-gray-700 focus:ring-red-500',
  };

  return (
    <button
      className={`${baseClasses} ${sizeClasses[size]} ${variantClasses[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};