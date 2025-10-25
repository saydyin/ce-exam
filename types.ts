

export interface Question {
  stem: string;
  figure: string | null;
  choices: string[];
  correct_answer: string;
  section: string;
  difficulty: number;
  explanation?: string;
  group_id?: string;
  term?: boolean | string;
  isDummy?: boolean;
}

export interface Section {
  name: "AMSTHEC" | "HPGE" | "PSAD";
  title: string;
  total: number;
  time: number; // in seconds
}

export interface Settings {
  theme: 'light' | 'dark';
  fontSize: 'small' | 'medium' | 'large';
  autoSave: boolean;
  studyMode: boolean;
  keyboardShortcuts: boolean;
  navigationMode: 'buttons' | 'scroll';
}

export interface Bookmark {
  id: string;
  section: string;
  questionIndex: number;
  timestamp: string;
}

export interface AnswerSheet {
  [section: string]: (string | null)[];
}

export interface WrongAnswerInfo {
  number: number;
  stem: string;
  user_answer: string | null;
  correct_answer: string;
  choices: string[];
  explanation?: string;
  figure: string | null;
}

export interface SectionResult {
  score_pct: number;
  correct: number;
  total: number;
  wrong: WrongAnswerInfo[];
}

export interface SectionResults {
  [section: string]: SectionResult;
}

// FIX: Moved AppView here to be globally accessible.
export type AppView =
  | 'loading'
  | 'main-menu'
  | 'instructions'
  | 'exam'
  | 'results'
  | 'final-results'
  | 'settings'
  | 'bookmarks'
  | 'analytics'
  | 'review';
