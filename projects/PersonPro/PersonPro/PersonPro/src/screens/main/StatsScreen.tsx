import React, { useContext } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Dimensions,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { AppContext } from '../../context/AppContext';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';
import { LineChart, PieChart } from 'react-native-chart-kit';
import { Ionicons } from '@expo/vector-icons';

const { width } = Dimensions.get('window');

export const StatsScreen = () => {
  const { user, goals } = useContext(AppContext);

  // Подготовка данных для графика активности
  const activityData = {
    labels: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
    datasets: [
      {
        data: user.stats.weeklyActivity,
        color: (opacity = 1) => `rgba(134, 65, 244, ${opacity})`,
        strokeWidth: 2,
      },
    ],
  };

  // Подготовка данных для круговой диаграммы категорий
  const categoryData = goals.reduce((acc, goal) => {
    acc[goal.category] = (acc[goal.category] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  const pieData = Object.entries(categoryData).map(([category, value]) => ({
    name: category,
    population: value,
    color: getCategoryColor(category),
    legendFontColor: '#7F7F7F',
    legendFontSize: 12,
  }));

  // Функция для получения цвета категории
  const getCategoryColor = (category: string): string => {
    const colors: Record<string, string> = {
      health: '#4CAF50',
      fitness: '#2196F3',
      career: '#FF9800',
      education: '#9C27B0',
      finance: '#F44336',
      personal: '#00BCD4',
      relationships: '#E91E63',
      mental: '#8BC34A',
    };
    return colors[category] || '#607D8B';
  };

  // Функция для получения иконки категории
  const getCategoryIcon = (category: string): keyof typeof Ionicons.glyphMap => {
    const icons: Record<string, keyof typeof Ionicons.glyphMap> = {
      health: 'medkit',
      fitness: 'fitness',
      career: 'briefcase',
      education: 'school',
      finance: 'wallet',
      personal: 'person',
      relationships: 'people',
      mental: 'brain',
    };
    return icons[category] || 'help';
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#6A11CB', '#2575FC']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>Статистика</Text>
      </LinearGradient>

      <ScrollView style={styles.content}>
        {/* График активности */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Активность за неделю</Text>
          <LineChart
            data={activityData}
            width={width - 40}
            height={220}
            chartConfig={{
              backgroundColor: '#ffffff',
              backgroundGradientFrom: '#ffffff',
              backgroundGradientTo: '#ffffff',
              decimalPlaces: 0,
              color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
              style: {
                borderRadius: 16,
              },
            }}
            bezier
            style={styles.chart}
          />
        </View>

        {/* Круговая диаграмма категорий */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Распределение целей</Text>
          <PieChart
            data={pieData}
            width={width - 40}
            height={220}
            chartConfig={{
              color: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
            }}
            accessor="population"
            backgroundColor="transparent"
            paddingLeft="15"
            absolute
          />
        </View>

        {/* Общая статистика */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Общая статистика</Text>
          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Ionicons name="trophy" size={24} color="#FFD700" />
              <Text style={styles.statValue}>{goals.filter(g => g.progress === 100).length}</Text>
              <Text style={styles.statLabel}>Достигнуто целей</Text>
            </View>
            <View style={styles.statItem}>
              <Ionicons name="time" size={24} color="#4CAF50" />
              <Text style={styles.statValue}>{user.stats.totalHours}ч</Text>
              <Text style={styles.statLabel}>Потрачено времени</Text>
            </View>
            <View style={styles.statItem}>
              <Ionicons name="calendar" size={24} color="#2196F3" />
              <Text style={styles.statValue}>
                {format(new Date(user.stats.startDate), 'dd MMMM yyyy', { locale: ru })}
              </Text>
              <Text style={styles.statLabel}>Дата начала</Text>
            </View>
          </View>
        </View>

        {/* Прогресс по категориям */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Прогресс по категориям</Text>
          {Object.entries(categoryData).map(([category, count]) => (
            <View key={category} style={styles.categoryItem}>
              <View style={styles.categoryHeader}>
                <Ionicons name={getCategoryIcon(category)} size={24} color={getCategoryColor(category)} />
                <Text style={styles.categoryName}>{category}</Text>
              </View>
              <View style={styles.progressBar}>
                <View
                  style={[
                    styles.progressFill,
                    {
                      width: `${(count / goals.length) * 100}%`,
                      backgroundColor: getCategoryColor(category),
                    },
                  ]}
                />
              </View>
              <Text style={styles.categoryCount}>{count} целей</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
  },
  header: {
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  section: {
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    padding: 16,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 16,
    color: '#333333',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 10,
  },
  statItem: {
    alignItems: 'center',
    flex: 1,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    marginVertical: 5,
    color: '#333333',
  },
  statLabel: {
    fontSize: 12,
    color: '#666666',
    textAlign: 'center',
  },
  categoryItem: {
    marginBottom: 16,
  },
  categoryHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  categoryName: {
    fontSize: 16,
    marginLeft: 8,
    color: '#333333',
  },
  progressBar: {
    height: 8,
    backgroundColor: '#E0E0E0',
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  categoryCount: {
    fontSize: 12,
    color: '#666666',
    marginTop: 4,
  },
}); 