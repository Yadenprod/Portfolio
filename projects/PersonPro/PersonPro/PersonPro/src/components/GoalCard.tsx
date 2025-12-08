import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  TouchableOpacity, 
  ProgressBarAndroid,
  Platform,
  ViewStyle
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { Goal, GoalCategory } from '../types';
import { useApp } from '../context/AppContext';
import { spacing, borderRadius, shadows, typography } from '../utils/theme';

// Для iOS используем прогресс-бар с react-native-paper
let ProgressBar: any = ProgressBarAndroid;
// Функция для импорта модуля для iOS будет реализована позже

interface GoalCardProps {
  goal: Goal;
  onPress: (goalId: string) => void;
  style?: ViewStyle;
  compact?: boolean;
}

const GoalCard: React.FC<GoalCardProps> = ({ 
  goal, 
  onPress, 
  style, 
  compact = false 
}) => {
  const { theme } = useApp();
  const isDark = theme === 'dark';

  // Получаем иконку и цвет для категории
  const getCategoryInfo = (category: GoalCategory) => {
    const categoryInfo = {
      health: { icon: 'favorite', color: '#F44336' },
      fitness: { icon: 'fitness-center', color: '#FF9800' },
      career: { icon: 'work', color: '#2196F3' },
      education: { icon: 'school', color: '#9C27B0' },
      finance: { icon: 'attach-money', color: '#4CAF50' },
      personal: { icon: 'person', color: '#03A9F4' },
      relationships: { icon: 'people', color: '#E91E63' },
      mental: { icon: 'psychology', color: '#673AB7' },
    };
    
    return categoryInfo[category];
  };

  const categoryInfo = getCategoryInfo(goal.category);
  
  // Получаем русское название категории
  const getCategoryName = (category: GoalCategory): string => {
    const translations: Record<GoalCategory, string> = {
      health: 'Здоровье',
      fitness: 'Фитнес',
      career: 'Карьера',
      education: 'Образование',
      finance: 'Финансы',
      personal: 'Личное развитие',
      relationships: 'Отношения',
      mental: 'Ментальное здоровье',
    };
    
    return translations[category];
  };

  // Форматируем дату
  const formatDate = (date: Date): string => {
    const options: Intl.DateTimeFormatOptions = { 
      day: 'numeric', 
      month: 'long', 
      year: 'numeric' 
    };
    return new Date(date).toLocaleDateString('ru-RU', options);
  };

  // Получаем количество выполненных задач
  const completedTasks = goal.tasks.filter(task => task.completed).length;
  const totalTasks = goal.tasks.length;

  return (
    <TouchableOpacity
      style={[
        styles.container,
        isDark ? styles.containerDark : styles.containerLight,
        shadows.md,
        compact ? styles.compactContainer : {},
        style,
      ]}
      onPress={() => onPress(goal.id)}
      activeOpacity={0.8}
    >
      <View style={styles.header}>
        <View style={[styles.categoryBadge, { backgroundColor: categoryInfo.color + '20' }]}>
          <MaterialIcons 
            name={categoryInfo.icon as any} 
            size={16} 
            color={categoryInfo.color} 
          />
          <Text 
            style={[
              styles.categoryText, 
              { color: categoryInfo.color },
              compact ? { fontSize: 10 } : {}
            ]}
          >
            {getCategoryName(goal.category)}
          </Text>
        </View>
        
        <Text 
          style={[
            styles.date, 
            isDark ? styles.textDark : styles.textLight,
            compact ? { fontSize: 10 } : {}
          ]}
        >
          до {formatDate(goal.targetDate)}
        </Text>
      </View>

      <Text 
        style={[
          styles.title, 
          isDark ? styles.textDark : styles.textLight,
          compact ? { fontSize: 16, marginVertical: spacing.xs } : {}
        ]}
        numberOfLines={compact ? 1 : 2}
      >
        {goal.title}
      </Text>

      {!compact && (
        <Text 
          style={[styles.description, isDark ? styles.textDark : styles.textLight]}
          numberOfLines={2}
        >
          {goal.description}
        </Text>
      )}

      <View style={styles.progressContainer}>
        <View style={styles.progressInfo}>
          <Text 
            style={[
              styles.progressText, 
              isDark ? styles.textDark : styles.textLight,
              compact ? { fontSize: 12 } : {}
            ]}
          >
            Прогресс: {goal.progress}%
          </Text>
          {!compact && totalTasks > 0 && (
            <Text 
              style={[styles.tasksText, isDark ? styles.textDark : styles.textLight]}
            >
              Задачи: {completedTasks}/{totalTasks}
            </Text>
          )}
        </View>
        
        <ProgressBar
          styleAttr="Horizontal"
          indeterminate={false}
          progress={goal.progress / 100}
          color={categoryInfo.color}
          style={styles.progressBar}
        />
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginVertical: spacing.sm,
    width: '100%',
  },
  compactContainer: {
    padding: spacing.sm,
    marginVertical: spacing.xs,
  },
  containerLight: {
    backgroundColor: '#FFF',
  },
  containerDark: {
    backgroundColor: '#1E1E1E',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: spacing.xs,
  },
  categoryBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs / 2,
    borderRadius: borderRadius.pill,
  },
  categoryText: {
    fontSize: 12,
    fontWeight: '500' as any,
    marginLeft: spacing.xs,
  },
  date: {
    fontSize: 12,
    opacity: 0.7,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold' as any,
    marginVertical: spacing.sm,
  },
  description: {
    fontSize: 14,
    opacity: 0.8,
    marginBottom: spacing.md,
  },
  progressContainer: {
    marginTop: spacing.sm,
  },
  progressInfo: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.xs,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '500' as any,
  },
  tasksText: {
    fontSize: 14,
    opacity: 0.7,
  },
  progressBar: {
    height: 6,
    borderRadius: borderRadius.pill,
  },
  textLight: {
    color: '#121212',
  },
  textDark: {
    color: '#FFFFFF',
  },
});

export default GoalCard; 