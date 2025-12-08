import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Dimensions,
} from 'react-native';
import { useApp } from '../../context/AppContext';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { StatsCard } from '../../components/StatsCard';
import { GoalCategory } from '../../types';

const { width } = Dimensions.get('window');

const generateMockData = (count: number): number[] => {
  return Array.from({ length: count }, () => Math.floor(Math.random() * 100));
};

const generateMockLabels = (count: number): string[] => {
  return Array.from({ length: count }, (_, i) => `Week ${i + 1}`);
};

const StatsScreen = () => {
  const { user, goals } = useApp();

  const completedGoals = goals.filter(goal => goal.progress === 100).length;
  const inProgressGoals = goals.filter(goal => goal.progress > 0 && goal.progress < 100).length;
  const notStartedGoals = goals.filter(goal => goal.progress === 0).length;

  const getCategoryStats = () => {
    const stats: Record<string, { count: number; totalProgress: number }> = {};
    
    goals.forEach(goal => {
      if (!stats[goal.category]) {
        stats[goal.category] = { count: 0, totalProgress: 0 };
      }
      stats[goal.category].count++;
      stats[goal.category].totalProgress += goal.progress;
    });

    return stats;
  };

  const categoryStats = getCategoryStats();

  const getGoalsByCategory = (category: GoalCategory) => {
    return goals.filter(goal => goal.category === category);
  };

  const getCompletionRate = (category: GoalCategory) => {
    const categoryGoals = getGoalsByCategory(category);
    if (categoryGoals.length === 0) return 0;
    const completedGoals = categoryGoals.filter(goal => goal.isCompleted);
    return (completedGoals.length / categoryGoals.length) * 100;
  };

  const statsData = [
    {
      category: 'health' as GoalCategory,
      title: 'Health Goals',
      currentValue: getCompletionRate('health'),
      previousValue: 60, // Mock previous value
      data: generateMockData(8),
      labels: generateMockLabels(8),
    },
    {
      category: 'fitness' as GoalCategory,
      title: 'Fitness Goals',
      currentValue: getCompletionRate('fitness'),
      previousValue: 45,
      data: generateMockData(8),
      labels: generateMockLabels(8),
    },
    {
      category: 'career' as GoalCategory,
      title: 'Career Goals',
      currentValue: getCompletionRate('career'),
      previousValue: 70,
      data: generateMockData(8),
      labels: generateMockLabels(8),
    },
    {
      category: 'education' as GoalCategory,
      title: 'Education Goals',
      currentValue: getCompletionRate('education'),
      previousValue: 55,
      data: generateMockData(8),
      labels: generateMockLabels(8),
    },
  ];

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#1a1a1a', '#2d2d2d']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>Статистика</Text>
      </LinearGradient>

      <ScrollView style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Общая статистика</Text>
          <View style={styles.statsGrid}>
            <View style={styles.statCard}>
              <MaterialIcons name="flag" size={24} color="#6200EE" />
              <Text style={styles.statNumber}>{goals.length}</Text>
              <Text style={styles.statLabel}>Всего целей</Text>
            </View>
            <View style={styles.statCard}>
              <MaterialIcons name="check-circle" size={24} color="#4CAF50" />
              <Text style={styles.statNumber}>{completedGoals}</Text>
              <Text style={styles.statLabel}>Выполнено</Text>
            </View>
            <View style={styles.statCard}>
              <MaterialIcons name="trending-up" size={24} color="#FFC107" />
              <Text style={styles.statNumber}>{inProgressGoals}</Text>
              <Text style={styles.statLabel}>В процессе</Text>
            </View>
            <View style={styles.statCard}>
              <MaterialIcons name="schedule" size={24} color="#FF5722" />
              <Text style={styles.statNumber}>{notStartedGoals}</Text>
              <Text style={styles.statLabel}>Не начато</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Прогресс по категориям</Text>
          {Object.entries(categoryStats).map(([category, stats]) => (
            <View key={category} style={styles.categoryProgress}>
              <View style={styles.categoryHeader}>
                <MaterialIcons
                  name={
                    category === 'health'
                      ? 'favorite'
                      : category === 'fitness'
                      ? 'fitness-center'
                      : category === 'career'
                      ? 'work'
                      : category === 'education'
                      ? 'school'
                      : category === 'finance'
                      ? 'attach-money'
                      : category === 'personal'
                      ? 'person'
                      : category === 'relationships'
                      ? 'people'
                      : 'psychology'
                  }
                  size={20}
                  color="#6200EE"
                />
                <Text style={styles.categoryName}>
                  {category === 'health'
                    ? 'Здоровье'
                    : category === 'fitness'
                    ? 'Фитнес'
                    : category === 'career'
                    ? 'Карьера'
                    : category === 'education'
                    ? 'Образование'
                    : category === 'finance'
                    ? 'Финансы'
                    : category === 'personal'
                    ? 'Личное'
                    : category === 'relationships'
                    ? 'Отношения'
                    : 'Психология'}
                </Text>
                <Text style={styles.categoryStats}>
                  {stats.count} целей
                </Text>
              </View>
              <View style={styles.progressBar}>
                <View
                  style={[
                    styles.progressFill,
                    {
                      width: `${(stats.totalProgress / stats.count)}%`,
                    },
                  ]}
                />
              </View>
              <Text style={styles.progressText}>
                {Math.round(stats.totalProgress / stats.count)}% в среднем
              </Text>
            </View>
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Достижения</Text>
          <View style={styles.achievementCard}>
            <MaterialIcons name="emoji-events" size={24} color="#FFD700" />
            <View style={styles.achievementContent}>
              <Text style={styles.achievementTitle}>Страйк!</Text>
              <Text style={styles.achievementDescription}>
                {user.stats.dailyStreak} дней подряд
              </Text>
            </View>
          </View>
          <View style={styles.achievementCard}>
            <MaterialIcons name="timer" size={24} color="#6200EE" />
            <View style={styles.achievementContent}>
              <Text style={styles.achievementTitle}>Время в пути</Text>
              <Text style={styles.achievementDescription}>
                {user.stats.totalHours} часов работы над целями
              </Text>
            </View>
          </View>
          <View style={styles.achievementCard}>
            <MaterialIcons name="calendar-today" size={24} color="#4CAF50" />
            <View style={styles.achievementContent}>
              <Text style={styles.achievementTitle}>Старт</Text>
              <Text style={styles.achievementDescription}>
                С {format(new Date(user.stats.startDate), 'd MMMM yyyy', { locale: ru })}
              </Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Статистика по категориям</Text>
          <ScrollView style={styles.statsScrollView}>
            {statsData.map((stat, index) => (
              <StatsCard
                key={index}
                category={stat.category}
                title={stat.title}
                currentValue={stat.currentValue}
                previousValue={stat.previousValue}
                data={stat.data}
                labels={stat.labels}
              />
            ))}
          </ScrollView>
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#121212',
  },
  header: {
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerTitle: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  section: {
    marginBottom: 30,
  },
  sectionTitle: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  statCard: {
    width: (width - 60) / 2,
    backgroundColor: '#1E1E1E',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    alignItems: 'center',
  },
  statNumber: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
    marginVertical: 5,
  },
  statLabel: {
    color: '#aaa',
    fontSize: 14,
  },
  categoryProgress: {
    backgroundColor: '#1E1E1E',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  categoryName: {
    color: '#fff',
    fontSize: 16,
    marginLeft: 10,
    flex: 1,
  },
  categoryStats: {
    color: '#aaa',
    fontSize: 14,
  },
  progressBar: {
    height: 6,
    backgroundColor: '#333',
    borderRadius: 3,
    marginBottom: 5,
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#6200EE',
    borderRadius: 3,
  },
  progressText: {
    color: '#aaa',
    fontSize: 12,
    textAlign: 'right',
  },
  achievementCard: {
    flexDirection: 'row',
    backgroundColor: '#1E1E1E',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    alignItems: 'center',
  },
  achievementContent: {
    marginLeft: 15,
    flex: 1,
  },
  achievementTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  achievementDescription: {
    color: '#aaa',
    fontSize: 14,
  },
  statsScrollView: {
    flex: 1,
  },
});

export default StatsScreen; 