import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { AIRecommendation } from '../types';

interface RecommendationCardProps {
  recommendation: AIRecommendation;
  onApply: () => void;
  onDismiss: () => void;
}

const RecommendationCard: React.FC<RecommendationCardProps> = ({
  recommendation,
  onApply,
  onDismiss,
}) => {
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
        return 'lightbulb';
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

  return (
    <View style={[styles.container, { borderLeftColor: getCategoryColor(recommendation.category) }]}>
      <View style={styles.header}>
        <View style={styles.titleContainer}>
          <MaterialIcons
            name={getCategoryIcon(recommendation.category)}
            size={24}
            color={getCategoryColor(recommendation.category)}
          />
          <Text style={styles.title}>
            {recommendation.title}
          </Text>
        </View>
        <TouchableOpacity onPress={onDismiss}>
          <MaterialIcons
            name="close"
            size={24}
            color="#757575"
          />
        </TouchableOpacity>
      </View>

      <Text style={styles.description}>
        {recommendation.description}
      </Text>

      <View style={styles.footer}>
        <Text style={styles.date}>
          {new Date(recommendation.date).toLocaleDateString()}
        </Text>
        <TouchableOpacity
          style={[styles.applyButton, { backgroundColor: getCategoryColor(recommendation.category) }]}
          onPress={onApply}
        >
          <Text style={styles.applyButtonText}>Применить</Text>
        </TouchableOpacity>
      </View>
    </View>
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
  footer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  date: {
    fontSize: 12,
    color: '#9E9E9E',
  },
  applyButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 4,
  },
  applyButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '500',
  },
});

export default RecommendationCard; 