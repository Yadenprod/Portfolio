import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { Goal } from '../types';
import ProgressBar from './ProgressBar';

interface GoalCardProps {
  goal: Goal;
  onPress: () => void;
  onComplete: () => void;
}

const GoalCard: React.FC<GoalCardProps> = ({ goal, onPress, onComplete }) => {
  const getCategoryIcon = (category: string) => {
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
        return 'sports';
      default:
        return 'flag';
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'health':
        return '#FF5252';
      case 'fitness':
        return '#4CAF50';
      case 'career':
        return '#2196F3';
      case 'education':
        return '#9C27B0';
      case 'finance':
        return '#FFC107';
      case 'personal':
        return '#FF9800';
      case 'social':
        return '#00BCD4';
      case 'hobby':
        return '#E91E63';
      default:
        return '#6200EE';
    }
  };

  const progress = goal.tasks.length > 0
    ? goal.tasks.filter(task => task.completed).length / goal.tasks.length
    : 0;

  return (
    <TouchableOpacity
      style={[styles.container, { borderLeftColor: getCategoryColor(goal.category) }]}
      onPress={onPress}
    >
      <View style={styles.header}>
        <View style={styles.titleContainer}>
          <MaterialIcons
            name={getCategoryIcon(goal.category)}
            size={24}
            color={getCategoryColor(goal.category)}
          />
          <Text style={styles.title} numberOfLines={1}>
            {goal.title}
          </Text>
        </View>
        <TouchableOpacity onPress={onComplete}>
          <MaterialIcons
            name={progress === 1 ? 'check-circle' : 'radio-button-unchecked'}
            size={24}
            color={progress === 1 ? '#4CAF50' : '#757575'}
          />
        </TouchableOpacity>
      </View>

      {goal.description && (
        <Text style={styles.description} numberOfLines={2}>
          {goal.description}
        </Text>
      )}

      <View style={styles.progressContainer}>
        <ProgressBar
          progress={progress}
          color={getCategoryColor(goal.category)}
        />
        <Text style={styles.progressText}>
          {Math.round(progress * 100)}%
        </Text>
      </View>

      <View style={styles.footer}>
        <Text style={styles.date}>
          {new Date(goal.targetDate).toLocaleDateString()}
        </Text>
        <Text style={styles.taskCount}>
          {goal.tasks.filter(task => task.completed).length}/{goal.tasks.length} задач
        </Text>
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#FFFFFF',
    borderRadius: 8,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  titleContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    marginRight: 8,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
    color: '#212121',
  },
  description: {
    fontSize: 14,
    color: '#757575',
    marginBottom: 12,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  progressText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#757575',
  },
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  date: {
    fontSize: 12,
    color: '#9E9E9E',
  },
  taskCount: {
    fontSize: 12,
    color: '#9E9E9E',
  },
});

export default GoalCard; 