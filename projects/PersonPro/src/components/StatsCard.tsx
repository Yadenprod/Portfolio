import React from 'react';
import { View, Text, StyleSheet, Dimensions } from 'react-native';
import { LineChart } from 'react-native-chart-kit';
import { MaterialIcons } from '@expo/vector-icons';
import { GoalCategory } from '../types';

interface StatsCardProps {
  category: GoalCategory;
  title: string;
  currentValue: number;
  previousValue: number;
  data: number[];
  labels: string[];
}

const { width } = Dimensions.get('window');

const getCategoryIcon = (category: GoalCategory): string => {
  switch (category) {
    case 'health':
      return 'favorite';
    case 'fitness':
      return 'fitness-center';
    case 'career':
      return 'work';
    case 'education':
      return 'school';
    case 'finance':
      return 'account-balance';
    case 'personal':
      return 'person';
    case 'social':
      return 'people';
    case 'hobby':
      return 'sports-esports';
    default:
      return 'star';
  }
};

const getCategoryColor = (category: GoalCategory): string => {
  switch (category) {
    case 'health':
      return '#FF6B6B';
    case 'fitness':
      return '#4ECDC4';
    case 'career':
      return '#45B7D1';
    case 'education':
      return '#96CEB4';
    case 'finance':
      return '#FFEEAD';
    case 'personal':
      return '#D4A5A5';
    case 'social':
      return '#9B59B6';
    case 'hobby':
      return '#3498DB';
    default:
      return '#95A5A6';
  }
};

const calculatePercentageChange = (current: number, previous: number): number => {
  if (previous === 0) return 0;
  return ((current - previous) / previous) * 100;
};

export const StatsCard: React.FC<StatsCardProps> = ({
  category,
  title,
  currentValue,
  previousValue,
  data,
  labels,
}) => {
  const percentageChange = calculatePercentageChange(currentValue, previousValue);
  const isPositive = percentageChange >= 0;
  const iconColor = getCategoryColor(category);

  const chartConfig = {
    backgroundGradientFrom: '#ffffff',
    backgroundGradientTo: '#ffffff',
    color: (opacity = 1) => iconColor,
    strokeWidth: 2,
    barPercentage: 0.5,
    useShadowColorFromDataset: false,
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View style={styles.titleContainer}>
          <MaterialIcons name={getCategoryIcon(category)} size={24} color={iconColor} />
          <Text style={styles.title}>{title}</Text>
        </View>
        <View style={styles.valueContainer}>
          <Text style={styles.currentValue}>{currentValue}</Text>
          <Text style={[styles.percentageChange, { color: isPositive ? '#2ECC71' : '#E74C3C' }]}>
            {isPositive ? '+' : ''}{percentageChange.toFixed(1)}%
          </Text>
        </View>
      </View>
      <LineChart
        data={{
          labels,
          datasets: [{ data }],
        }}
        width={width - 40}
        height={220}
        chartConfig={chartConfig}
        bezier
        style={styles.chart}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#ffffff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
  valueContainer: {
    alignItems: 'flex-end',
  },
  currentValue: {
    fontSize: 24,
    fontWeight: '700',
  },
  percentageChange: {
    fontSize: 14,
    fontWeight: '500',
  },
  chart: {
    marginVertical: 8,
    borderRadius: 16,
  },
}); 