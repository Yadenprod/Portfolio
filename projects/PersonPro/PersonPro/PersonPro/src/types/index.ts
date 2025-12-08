export interface User {
  id: string;
  name: string;
  email: string;
  photoUrl?: string;
  goals: Goal[];
  stats: Statistics;
  joinedDate: Date;
}

export interface Goal {
  id: string;
  title: string;
  description: string;
  category: GoalCategory;
  targetDate: Date;
  progress: number; // 0-100
  tasks: Task[];
  createdAt: Date;
  updatedAt: Date;
}

export type GoalCategory = 
  | 'health'
  | 'fitness'
  | 'career'
  | 'education'
  | 'finance'
  | 'personal'
  | 'relationships'
  | 'mental';

export interface Task {
  id: string;
  title: string;
  completed: boolean;
  dueDate?: Date;
  createdAt: Date;
}

export interface Statistics {
  dailyStreak: number;
  totalCompletedGoals: number;
  totalCompletedTasks: number;
  categoriesProgress: Record<GoalCategory, number>;
  weeklyActivity: number[];
}

export interface AIRecommendation {
  id: string;
  title: string;
  description: string;
  category: GoalCategory;
  impact: 'low' | 'medium' | 'high';
  createdAt: Date;
}

export interface AppTheme {
  dark: boolean;
  colors: {
    primary: string;
    background: string;
    card: string;
    text: string;
    border: string;
    notification: string;
    accent: string;
    success: string;
    warning: string;
    error: string;
  };
} 