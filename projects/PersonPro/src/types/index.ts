export type GoalCategory = 
  | 'health'
  | 'fitness'
  | 'career'
  | 'education'
  | 'finance'
  | 'personal'
  | 'social'
  | 'hobby'
  | 'relationships'
  | 'mental';

export interface Task {
  id: string;
  title: string;
  completed: boolean;
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  category: GoalCategory;
  progress: number;
  targetDate: Date;
  tasks: Task[];
  createdAt: Date;
}

export interface User {
  id: string;
  name: string;
  email: string;
  photoUrl?: string;
  stats: {
    dailyStreak: number;
    totalHours: number;
    startDate: Date;
    weeklyActivity: number[];
  };
}

export interface AIRecommendation {
  id: string;
  title: string;
  description: string;
  category: GoalCategory;
  impact: 'high' | 'medium' | 'low';
  createdAt: Date;
} 