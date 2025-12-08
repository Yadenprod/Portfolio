import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { User, Goal, Task, AIRecommendation, GoalCategory, Statistics } from '../types';
import { generateAIRecommendations } from '../services/aiService';
import { mockUser, mockGoals, mockRecommendations } from '../utils/mockData';

interface AppContextType {
  user: User | null;
  goals: Goal[];
  recommendations: AIRecommendation[];
  isLoading: boolean;
  theme: 'light' | 'dark';
  setUser: (user: User | null) => void;
  addGoal: (goal: Omit<Goal, 'id' | 'createdAt' | 'updatedAt'>) => void;
  updateGoal: (goalId: string, updates: Partial<Goal>) => void;
  deleteGoal: (goalId: string) => void;
  addTask: (goalId: string, task: Omit<Task, 'id' | 'createdAt'>) => void;
  updateTask: (goalId: string, taskId: string, completed: boolean) => void;
  deleteTask: (goalId: string, taskId: string) => void;
  toggleTheme: () => void;
}

const defaultStats: Statistics = {
  dailyStreak: 0,
  totalCompletedGoals: 0,
  totalCompletedTasks: 0,
  categoriesProgress: {
    health: 0,
    fitness: 0,
    career: 0,
    education: 0,
    finance: 0,
    personal: 0,
    relationships: 0,
    mental: 0,
  },
  weeklyActivity: [0, 0, 0, 0, 0, 0, 0],
};

const AppContext = createContext<AppContextType | undefined>(undefined);

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(mockUser);
  const [goals, setGoals] = useState<Goal[]>(mockGoals);
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>(mockRecommendations);
  const [isLoading, setIsLoading] = useState(false);
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(false);
      } catch (error) {
        console.error('Error loading data from AsyncStorage', error);
        setIsLoading(false);
      }
    };
    
    loadData();
  }, []);

  useEffect(() => {
    if (user && goals.length > 0) {
    }
  }, [user, goals]);

  useEffect(() => {
    const saveData = async () => {
      try {
      } catch (error) {
        console.error('Error saving data to AsyncStorage', error);
      }
    };
    
    if (!isLoading) saveData();
  }, [user, goals, theme, isLoading]);

  const addGoal = (goalData: Omit<Goal, 'id' | 'createdAt' | 'updatedAt'>) => {
    const newGoal: Goal = {
      ...goalData,
      id: Date.now().toString(),
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    setGoals(prevGoals => [...prevGoals, newGoal]);
    
    if (user) {
      const updatedStats = { ...user.stats };
      updatedStats.categoriesProgress[goalData.category] += 1;
      
      setUser({
        ...user,
        goals: [...user.goals, newGoal],
        stats: updatedStats,
      });
    }
  };

  const updateGoal = (goalId: string, updates: Partial<Goal>) => {
    setGoals(prevGoals => 
      prevGoals.map(goal => 
        goal.id === goalId 
          ? { ...goal, ...updates, updatedAt: new Date() } 
          : goal
      )
    );
    
    if (user) {
      setUser({
        ...user,
        goals: user.goals.map(goal => 
          goal.id === goalId 
            ? { ...goal, ...updates, updatedAt: new Date() } 
            : goal
        ),
      });
    }
  };

  const deleteGoal = (goalId: string) => {
    setGoals(prevGoals => prevGoals.filter(goal => goal.id !== goalId));
    
    if (user) {
      setUser({
        ...user,
        goals: user.goals.filter(goal => goal.id !== goalId),
      });
    }
  };

  const addTask = (goalId: string, taskData: Omit<Task, 'id' | 'createdAt'>) => {
    const newTask: Task = {
      ...taskData,
      id: Date.now().toString(),
      createdAt: new Date(),
    };
    
    setGoals(prevGoals => 
      prevGoals.map(goal => 
        goal.id === goalId
          ? {
              ...goal,
              tasks: [...goal.tasks, newTask],
              updatedAt: new Date(),
            }
          : goal
      )
    );
    
    if (user) {
      setUser({
        ...user,
        goals: user.goals.map(goal => 
          goal.id === goalId
            ? {
                ...goal,
                tasks: [...goal.tasks, newTask],
                updatedAt: new Date(),
              }
            : goal
        ),
      });
    }
  };

  const updateTask = (goalId: string, taskId: string, completed: boolean) => {
    setGoals(prevGoals => 
      prevGoals.map(goal => 
        goal.id === goalId
          ? {
              ...goal,
              tasks: goal.tasks.map(task => 
                task.id === taskId ? { ...task, completed } : task
              ),
              updatedAt: new Date(),
            }
          : goal
      )
    );
    
    if (completed && user) {
      const updatedStats = { ...user.stats };
      updatedStats.totalCompletedTasks += 1;
      
      const today = new Date().toDateString();
      const lastActive = new Date(user.stats.dailyStreak).toDateString();
      
      if (today !== lastActive) {
        updatedStats.dailyStreak += 1;
        
        const dayOfWeek = new Date().getDay();
        const weeklyActivity = [...updatedStats.weeklyActivity];
        weeklyActivity[dayOfWeek] += 1;
        updatedStats.weeklyActivity = weeklyActivity;
      }
      
      setUser({
        ...user,
        goals: user.goals.map(goal => 
          goal.id === goalId
            ? {
                ...goal,
                tasks: goal.tasks.map(task => 
                  task.id === taskId ? { ...task, completed } : task
                ),
                updatedAt: new Date(),
              }
            : goal
        ),
        stats: updatedStats,
      });
    }
  };

  const deleteTask = (goalId: string, taskId: string) => {
    setGoals(prevGoals => 
      prevGoals.map(goal => 
        goal.id === goalId
          ? {
              ...goal,
              tasks: goal.tasks.filter(task => task.id !== taskId),
              updatedAt: new Date(),
            }
          : goal
      )
    );
    
    if (user) {
      setUser({
        ...user,
        goals: user.goals.map(goal => 
          goal.id === goalId
            ? {
                ...goal,
                tasks: goal.tasks.filter(task => task.id !== taskId),
                updatedAt: new Date(),
              }
            : goal
        ),
      });
    }
  };

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
  };

  return (
    <AppContext.Provider
      value={{
        user,
        goals,
        recommendations,
        isLoading,
        theme,
        setUser,
        addGoal,
        updateGoal,
        deleteGoal,
        addTask,
        updateTask,
        deleteTask,
        toggleTheme,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export const useApp = () => {
  const context = useContext(AppContext);
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
}; 