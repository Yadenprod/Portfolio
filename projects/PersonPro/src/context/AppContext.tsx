import React, { createContext, useContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Goal, User, Task, AIRecommendation, GoalCategory } from '../types';

interface AppContextType {
  user: User;
  goals: Goal[];
  recommendations: AIRecommendation[];
  isDarkMode: boolean;
  toggleDarkMode: () => void;
  addGoal: (goal: Omit<Goal, 'id' | 'createdAt'>) => void;
  updateGoal: (goalId: string, updates: Partial<Goal>) => void;
  deleteGoal: (goalId: string) => void;
  addTask: (goalId: string, task: Omit<Task, 'id'>) => void;
  updateTask: (goalId: string, taskId: string, completed: boolean) => void;
  deleteTask: (goalId: string, taskId: string) => void;
  updateUser: (updates: Partial<User>) => void;
  isLoading: boolean;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

const STORAGE_KEYS = {
  USER: '@PersonPro:user',
  GOALS: '@PersonPro:goals',
  RECOMMENDATIONS: '@PersonPro:recommendations',
  DARK_MODE: '@PersonPro:darkMode',
};

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [user, setUser] = useState<User>({
    id: '1',
    name: 'Пользователь',
    email: 'user@example.com',
    stats: {
      dailyStreak: 0,
      totalHours: 0,
      startDate: new Date(),
      weeklyActivity: [0, 0, 0, 0, 0, 0, 0],
    },
  });
  const [goals, setGoals] = useState<Goal[]>([]);
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [userData, goalsData, recommendationsData, darkModeData] = await Promise.all([
        AsyncStorage.getItem(STORAGE_KEYS.USER),
        AsyncStorage.getItem(STORAGE_KEYS.GOALS),
        AsyncStorage.getItem(STORAGE_KEYS.RECOMMENDATIONS),
        AsyncStorage.getItem(STORAGE_KEYS.DARK_MODE),
      ]);

      if (userData) {
        setUser(JSON.parse(userData));
      }
      if (goalsData) {
        setGoals(JSON.parse(goalsData));
      }
      if (recommendationsData) {
        setRecommendations(JSON.parse(recommendationsData));
      }
      if (darkModeData) {
        setIsDarkMode(JSON.parse(darkModeData));
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const saveData = async (key: string, data: any) => {
    try {
      await AsyncStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
      console.error(`Error saving ${key}:`, error);
    }
  };

  const toggleDarkMode = () => {
    setIsDarkMode(prev => {
      const newValue = !prev;
      saveData(STORAGE_KEYS.DARK_MODE, newValue);
      return newValue;
    });
  };

  const addGoal = (goalData: Omit<Goal, 'id' | 'createdAt'>) => {
    const newGoal: Goal = {
      ...goalData,
      id: Date.now().toString(),
      createdAt: new Date(),
    };
    setGoals(prev => {
      const newGoals = [...prev, newGoal];
      saveData(STORAGE_KEYS.GOALS, newGoals);
      return newGoals;
    });
  };

  const updateGoal = (goalId: string, updates: Partial<Goal>) => {
    setGoals(prev => {
      const newGoals = prev.map(goal =>
        goal.id === goalId ? { ...goal, ...updates } : goal
      );
      saveData(STORAGE_KEYS.GOALS, newGoals);
      return newGoals;
    });
  };

  const deleteGoal = (goalId: string) => {
    setGoals(prev => {
      const newGoals = prev.filter(goal => goal.id !== goalId);
      saveData(STORAGE_KEYS.GOALS, newGoals);
      return newGoals;
    });
  };

  const addTask = (goalId: string, taskData: Omit<Task, 'id'>) => {
    const newTask: Task = {
      ...taskData,
      id: Date.now().toString(),
    };
    setGoals(prev => {
      const newGoals = prev.map(goal =>
        goal.id === goalId
          ? { ...goal, tasks: [...goal.tasks, newTask] }
          : goal
      );
      saveData(STORAGE_KEYS.GOALS, newGoals);
      return newGoals;
    });
  };

  const updateTask = (goalId: string, taskId: string, completed: boolean) => {
    setGoals(prev => {
      const newGoals = prev.map(goal =>
        goal.id === goalId
          ? {
              ...goal,
              tasks: goal.tasks.map(task =>
                task.id === taskId ? { ...task, completed } : task
              ),
            }
          : goal
      );
      saveData(STORAGE_KEYS.GOALS, newGoals);
      return newGoals;
    });
  };

  const deleteTask = (goalId: string, taskId: string) => {
    setGoals(prev => {
      const newGoals = prev.map(goal =>
        goal.id === goalId
          ? {
              ...goal,
              tasks: goal.tasks.filter(task => task.id !== taskId),
            }
          : goal
      );
      saveData(STORAGE_KEYS.GOALS, newGoals);
      return newGoals;
    });
  };

  const updateUser = (updates: Partial<User>) => {
    setUser(prev => {
      const newUser = { ...prev, ...updates };
      saveData(STORAGE_KEYS.USER, newUser);
      return newUser;
    });
  };

  return (
    <AppContext.Provider
      value={{
        user,
        goals,
        recommendations,
        isDarkMode,
        toggleDarkMode,
        addGoal,
        updateGoal,
        deleteGoal,
        addTask,
        updateTask,
        deleteTask,
        updateUser,
        isLoading,
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