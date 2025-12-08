import { User, Goal, Task, GoalCategory, AIRecommendation, Statistics } from '../types';

// Вспомогательная функция для создания ID
const generateId = (): string => Math.random().toString(36).substring(2, 15);

// Создание тестовых задач
const createTasks = (count: number, completed = false): Task[] => {
  return Array(count).fill(0).map((_, index) => ({
    id: generateId(),
    title: `Задача ${index + 1}`,
    completed: index === 0 ? completed : Math.random() > 0.7,
    createdAt: new Date(Date.now() - Math.floor(Math.random() * 10000000)),
  }));
};

// Создание тестовых целей
const createGoals = (): Goal[] => {
  const categories: GoalCategory[] = [
    'health', 'fitness', 'career', 'education', 
    'finance', 'personal', 'relationships', 'mental'
  ];
  
  return categories.map((category, index) => {
    const progress = Math.floor(Math.random() * 100);
    return {
      id: generateId(),
      title: getCategoryTitle(category),
      description: getCategoryDescription(category),
      category,
      targetDate: new Date(Date.now() + (30 + Math.floor(Math.random() * 90)) * 86400000),
      progress,
      tasks: createTasks(3 + Math.floor(Math.random() * 5), progress > 50),
      createdAt: new Date(Date.now() - Math.floor(Math.random() * 10000000)),
      updatedAt: new Date(Date.now() - Math.floor(Math.random() * 1000000)),
    };
  });
};

// Получение заголовков целей по категориям
const getCategoryTitle = (category: GoalCategory): string => {
  const titles: Record<GoalCategory, string> = {
    health: 'Улучшить здоровье',
    fitness: 'Начать заниматься спортом регулярно',
    career: 'Выучить новый навык для работы',
    education: 'Прочитать 12 книг за год',
    finance: 'Создать финансовый план',
    personal: 'Научиться медитировать',
    relationships: 'Больше времени проводить с семьей',
    mental: 'Снизить уровень стресса',
  };
  
  return titles[category];
};

// Получение описаний целей по категориям
const getCategoryDescription = (category: GoalCategory): string => {
  const descriptions: Record<GoalCategory, string> = {
    health: 'Улучшить общее состояние здоровья через правильное питание и регулярные чекапы.',
    fitness: 'Заниматься спортом минимум 3 раза в неделю по 30 минут.',
    career: 'Изучить новый язык программирования или технологию, которая поможет в работе.',
    education: 'Прочитать минимум одну книгу в месяц для расширения кругозора.',
    finance: 'Создать финансовый план, бюджет и начать откладывать 15% дохода.',
    personal: 'Практиковать медитацию каждый день по 10 минут для улучшения осознанности.',
    relationships: 'Выделить минимум один вечер в неделю для качественного времени с семьей.',
    mental: 'Разработать стратегии управления стрессом и регулярно их практиковать.',
  };
  
  return descriptions[category];
};

// Создание статистики
const createStatistics = (): Statistics => {
  return {
    dailyStreak: Math.floor(Math.random() * 30),
    totalCompletedGoals: Math.floor(Math.random() * 15),
    totalCompletedTasks: Math.floor(Math.random() * 100),
    categoriesProgress: {
      health: Math.floor(Math.random() * 100),
      fitness: Math.floor(Math.random() * 100),
      career: Math.floor(Math.random() * 100),
      education: Math.floor(Math.random() * 100),
      finance: Math.floor(Math.random() * 100),
      personal: Math.floor(Math.random() * 100),
      relationships: Math.floor(Math.random() * 100),
      mental: Math.floor(Math.random() * 100),
    },
    weeklyActivity: Array(7).fill(0).map(() => Math.floor(Math.random() * 5)),
  };
};

// Создание рекомендаций ИИ
const createAIRecommendations = (): AIRecommendation[] => {
  const recommendations: AIRecommendation[] = [
    {
      id: generateId(),
      title: 'Медитация для снижения стресса',
      description: 'Начните день с 10-минутной медитации. Это поможет снизить уровень стресса и улучшит концентрацию в течение дня.',
      category: 'mental',
      impact: 'high',
      createdAt: new Date(),
    },
    {
      id: generateId(),
      title: 'Утренняя зарядка',
      description: 'Добавьте в свое утреннее расписание 15-минутную зарядку. Это зарядит вас энергией на весь день и улучшит общую физическую форму.',
      category: 'fitness',
      impact: 'medium',
      createdAt: new Date(),
    },
    {
      id: generateId(),
      title: 'Читайте перед сном',
      description: 'Замените просмотр соцсетей перед сном на чтение книги в течение 20 минут. Это улучшит качество сна и поможет достичь вашей цели по чтению книг.',
      category: 'education',
      impact: 'medium',
      createdAt: new Date(),
    },
    {
      id: generateId(),
      title: 'Обучение новому навыку',
      description: 'Уделите 30 минут в день изучению нового навыка, который поможет в карьере. Последовательность - ключ к успеху.',
      category: 'career',
      impact: 'high',
      createdAt: new Date(),
    },
    {
      id: generateId(),
      title: 'Семейное время',
      description: 'Выделите воскресенье для семейного досуга без гаджетов. Это укрепит ваши отношения и создаст ценные воспоминания.',
      category: 'relationships',
      impact: 'low',
      createdAt: new Date(),
    },
  ];
  
  return recommendations;
};

// Создание тестового пользователя
export const createMockUser = (): User => {
  const goals = createGoals();
  
  return {
    id: generateId(),
    name: 'Александр',
    email: 'user@example.com',
    photoUrl: 'https://example.com/profile.jpg',
    goals,
    stats: createStatistics(),
    joinedDate: new Date(Date.now() - 30 * 86400000),
  };
};

// Экспортируем готовые данные
export const mockUser = createMockUser();
export const mockGoals = mockUser.goals;
export const mockRecommendations = createAIRecommendations(); 