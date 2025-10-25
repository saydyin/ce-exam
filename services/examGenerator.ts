import { Question } from '../types';
import { SECTION_REQUIREMENTS } from '../constants';

const shuffleArray = <T>(array: T[]): T[] => {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
};

/**
 * Generate exam questions grouped by group_id, ensuring:
 * - Groups stay together
 * - "Situation" items appear first in group
 * - No "Situation" question appears near the very end (e.g., #49–#50)
 */
export const generateExam = async (questionBank: Question[]): Promise<Question[]> => {
  const generatedQuestions: Question[] = [];

  // Group questions by section
  const questionsBySection: Record<string, Question[]> = {};
  for (const question of questionBank) {
    if (!questionsBySection[question.section]) questionsBySection[question.section] = [];
    questionsBySection[question.section].push(question);
  }

  for (const sectionName in SECTION_REQUIREMENTS) {
    const requirements = SECTION_REQUIREMENTS[sectionName as keyof typeof SECTION_REQUIREMENTS];
    const sectionQuestions = questionsBySection[sectionName] || [];

    // === Group by group_id ===
    const groupMap: Record<string, Question[]> = {};
    for (const q of sectionQuestions) {
      const groupKey = q.group_id || `single-${Math.random().toString(36).substring(2, 8)}`;
      if (!groupMap[groupKey]) groupMap[groupKey] = [];
      groupMap[groupKey].push(q);
    }

    // === Within each group: "Situation" first ===
    const grouped = Object.values(groupMap).map(group => {
      const situation = group.find(q => q.stem.trim().startsWith('Situation'));
      if (situation) {
        const rest = group.filter(q => q !== situation);
        return [situation, ...rest];
      }
      return group;
    });

    // === Shuffle the groups (not individual questions) ===
    let shuffledGroups = shuffleArray(grouped);

    // === Flatten groups ===
    let orderedQuestions = shuffledGroups.flat();

    // === Post-flatten fix: prevent "Situation" in last few questions ===
    const checkLastN = 5;
    const badIndex = orderedQuestions
      .slice(-checkLastN)
      .findIndex(q => q.stem.trim().startsWith('Situation'));

    if (badIndex !== -1) {
      const situationQ = orderedQuestions[orderedQuestions.length - checkLastN + badIndex];
      const situationGroupId = situationQ.group_id;

      // Remove all questions from same group
      const remaining = orderedQuestions.filter(q => q.group_id !== situationGroupId);
      const movedGroup = orderedQuestions.filter(q => q.group_id === situationGroupId);

      // Insert the group into the middle
      const insertPos = Math.floor(remaining.length / 2);
      remaining.splice(insertPos, 0, ...movedGroup);

      orderedQuestions = remaining;
    }

    // === Trim to required number per section ===
    const finalQuestions = orderedQuestions.slice(0, requirements.total);

    generatedQuestions.push(...finalQuestions);
  }

  return generatedQuestions;
};
