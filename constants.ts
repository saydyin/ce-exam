import { Section } from './types';

// FIX: Define a type for the SECTIONS object to ensure type safety.
type SectionRecord = Record<"AMSTHEC" | "HPGE" | "PSAD", Section>;

// FIX: Create the SECTIONS constant with data for each exam section.
export const SECTIONS: SectionRecord = {
  AMSTHEC: {
    name: "AMSTHEC",
    title: "Mathematics, Surveying & Transportation Engineering",
    total: 75,
    time: 5 * 60 * 60, // 5 hours
  },
  HPGE: {
    name: "HPGE",
    title: "Hydraulics & Geotechnical Engineering",
    total: 50,
    time: 4 * 60 * 60, // 4 hours
  },
  PSAD: {
    name: "PSAD",
    title: "Structural Design & Construction",
    total: 75,
    time: 5 * 60 * 60, // 5 hours
  }
};

// FIX: Create the SECTION_REQUIREMENTS constant used by the exam generator.
export const SECTION_REQUIREMENTS = {
  AMSTHEC: { total: 75 },
  HPGE: { total: 50 },
  PSAD: { total: 75 },
};

export const SECTION_WEIGHTS = {
  AMSTHEC: 0.35,
  HPGE: 0.30,
  PSAD: 0.35,
};

// FIX: Create the PRC_INSTRUCTIONS constant.
export const PRC_INSTRUCTIONS = [
  "Read each question carefully.",
  "Choose the best answer from the given choices.",
  "Shade the corresponding letter on your answer sheet.",
  "Avoid erasures. Make sure of your answer before shading.",
  "Do not use any electronic devices during the examination.",
  "You are not allowed to leave the room once the exam has started."
];

// FIX: Create the MOTIVATIONAL_QUOTES constant.
export const MOTIVATIONAL_QUOTES = [
  "The secret of getting ahead is getting started.",
  "Believe you can and you're halfway there.",
  "It does not matter how slowly you go as long as you do not stop.",
  "Success is the sum of small efforts, repeated day in and day out.",
  "The future belongs to those who believe in the beauty of their dreams."
];