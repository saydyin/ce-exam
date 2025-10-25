import { forwardRef, type ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  // FIX: Add `id` prop to allow attaching an ID to the card element.
  id?: string;
}

// FIX: The Card component was a standard functional component and could not accept a ref. It is now wrapped in `forwardRef` so that it can receive a ref and forward it to the underlying div element. This is necessary for the `ExamScreen` to scroll to specific questions.
export const Card = forwardRef<HTMLDivElement, CardProps>(({ children, className = '', id }, ref) => {
  return (
    <div ref={ref} id={id} className={`bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 ${className}`}>
      {children}
    </div>
  );
});

Card.displayName = 'Card';
