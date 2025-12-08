import { User, Goal, AIRecommendation, GoalCategory } from '../types';

/**
 * Генерирует AI рекомендации на основе данных пользователя и его целей
 */
export const generateAIRecommendations = (user: User, goals: Goal[]): AIRecommendation[] => {
  const categoryProgress = analyzeUserProgress(user, goals);
  const recommendations: AIRecommendation[] = [];

  // Генерация рекомендаций для каждой категории
  Object.entries(categoryProgress).forEach(([category, progress]) => {
    const impact = determineImpact(progress);
    
    // Генерация рекомендаций на основе прогресса
    if (progress < 30) {
      recommendations.push({
        id: Date.now().toString(),
        title: getRecommendationTitle(category as GoalCategory, 'low'),
        description: getRecommendationDescription(category as GoalCategory, 'low'),
        category: category as GoalCategory,
        impact,
        createdAt: new Date(),
      });
    } else if (progress < 70) {
      recommendations.push({
        id: Date.now().toString(),
        title: getRecommendationTitle(category as GoalCategory, 'medium'),
        description: getRecommendationDescription(category as GoalCategory, 'medium'),
        category: category as GoalCategory,
        impact,
        createdAt: new Date(),
      });
    } else {
      recommendations.push({
        id: Date.now().toString(),
        title: getRecommendationTitle(category as GoalCategory, 'high'),
        description: getRecommendationDescription(category as GoalCategory, 'high'),
        category: category as GoalCategory,
        impact,
        createdAt: new Date(),
      });
    }
  });

  return recommendations;
};

/**
 * Создает новую рекомендацию с уникальным ID и текущей датой
 */
const createRecommendation = (
  title: string,
  description: string,
  category: GoalCategory,
  impact: 'low' | 'medium' | 'high'
): AIRecommendation => {
  return {
    id: Date.now().toString(),
    title,
    description,
    category,
    impact,
    createdAt: new Date(),
  };
};

/**
 * Переводит категорию цели на русский язык
 */
const translateCategory = (category: GoalCategory): string => {
  const translations: Record<GoalCategory, string> = {
    health: 'здоровье',
    fitness: 'физическая форма',
    career: 'карьера',
    education: 'образование',
    finance: 'финансы',
    personal: 'личное развитие',
    relationships: 'отношения',
    mental: 'ментальное здоровье',
  };
  
  return translations[category];
};

// Функция для анализа прогресса пользователя
const analyzeUserProgress = (user: User, goals: Goal[]): Record<GoalCategory, number> => {
  const categoryProgress: Record<GoalCategory, number> = {
    health: 0,
    fitness: 0,
    career: 0,
    education: 0,
    finance: 0,
    personal: 0,
    relationships: 0,
    mental: 0,
  };

  // Анализ прогресса по категориям
  goals.forEach(goal => {
    const category = goal.category;
    categoryProgress[category] += goal.progress;
  });

  // Нормализация значений
  Object.keys(categoryProgress).forEach(category => {
    categoryProgress[category as GoalCategory] = Math.min(
      Math.round((categoryProgress[category as GoalCategory] / goals.length) * 100),
      100
    );
  });

  return categoryProgress;
};

// Функция для определения приоритета рекомендации
const determineImpact = (progress: number): 'high' | 'medium' | 'low' => {
  if (progress < 30) return 'high';
  if (progress < 70) return 'medium';
  return 'low';
};

// Функции для генерации заголовков и описаний рекомендаций
const getRecommendationTitle = (category: GoalCategory, progress: 'low' | 'medium' | 'high'): string => {
  const titles: Record<GoalCategory, Record<'low' | 'medium' | 'high', string>> = {
    health: {
      low: 'Начните заботиться о здоровье',
      medium: 'Продолжайте улучшать здоровье',
      high: 'Поддерживайте здоровый образ жизни',
    },
    fitness: {
      low: 'Начните регулярные тренировки',
      medium: 'Увеличьте интенсивность тренировок',
      high: 'Оптимизируйте программу тренировок',
    },
    career: {
      low: 'Развивайте профессиональные навыки',
      medium: 'Повышайте квалификацию',
      high: 'Достигайте новых карьерных высот',
    },
    education: {
      low: 'Начните обучение новым навыкам',
      medium: 'Углубляйте знания',
      high: 'Применяйте знания на практике',
    },
    finance: {
      low: 'Начните планировать бюджет',
      medium: 'Оптимизируйте финансовые потоки',
      high: 'Инвестируйте в будущее',
    },
    personal: {
      low: 'Развивайте личные качества',
      medium: 'Совершенствуйте себя',
      high: 'Станьте примером для других',
    },
    relationships: {
      low: 'Улучшайте коммуникацию',
      medium: 'Укрепляйте отношения',
      high: 'Создавайте крепкие связи',
    },
    mental: {
      low: 'Начните заботиться о ментальном здоровье',
      medium: 'Развивайте осознанность',
      high: 'Практикуйте медитацию',
    },
  };

  return titles[category][progress];
};

const getRecommendationDescription = (category: GoalCategory, progress: 'low' | 'medium' | 'high'): string => {
  const descriptions: Record<GoalCategory, Record<'low' | 'medium' | 'high', string>> = {
    health: {
      low: 'Начните с малого: 10 минут утренней зарядки, правильное питание и достаточный сон помогут вам улучшить здоровье.',
      medium: 'Продолжайте развивать здоровые привычки: добавьте силовые тренировки и следите за питанием.',
      high: 'Вы достигли отличных результатов! Продолжайте поддерживать здоровый образ жизни и делитесь опытом с другими.',
    },
    fitness: {
      low: 'Начните с простых упражнений: ходьба, бег или йога помогут вам войти в ритм тренировок.',
      medium: 'Попробуйте новые виды тренировок: кроссфит, плавание или велоспорт для разнообразия.',
      high: 'Вы в отличной форме! Попробуйте поставить новые спортивные цели или участвовать в соревнованиях.',
    },
    career: {
      low: 'Определите свои сильные стороны и начните развивать профессиональные навыки через курсы и практику.',
      medium: 'Ищите возможности для роста: новые проекты, менторство или участие в профессиональных сообществах.',
      high: 'Вы достигли значительных успехов! Подумайте о наставничестве или создании собственного проекта.',
    },
    education: {
      low: 'Начните с изучения основ интересующей вас области через онлайн-курсы и книги.',
      medium: 'Углубляйте знания через практику, участие в проектах и общение с экспертами.',
      high: 'Применяйте знания на практике и делитесь опытом с другими через блоги или преподавание.',
    },
    finance: {
      low: 'Начните с ведения бюджета и создания финансовой подушки безопасности.',
      medium: 'Изучите основы инвестирования и начните формировать инвестиционный портфель.',
      high: 'Оптимизируйте инвестиционный портфель и рассмотрите возможности пассивного дохода.',
    },
    personal: {
      low: 'Начните с самоанализа и определения областей для личностного роста.',
      medium: 'Работайте над развитием эмоционального интеллекта и коммуникативных навыков.',
      high: 'Станьте наставником для других и помогайте им в личностном развитии.',
    },
    relationships: {
      low: 'Начните с улучшения коммуникации в ближайшем окружении.',
      medium: 'Расширяйте круг общения и развивайте эмпатию.',
      high: 'Создавайте крепкие связи и поддерживайте здоровые отношения.',
    },
    mental: {
      low: 'Начните с простых практик осознанности и медитации.',
      medium: 'Развивайте эмоциональный интеллект и учитесь управлять стрессом.',
      high: 'Практикуйте продвинутые техники медитации и делитесь опытом с другими.',
    },
  };

  return descriptions[category][progress];
}; 