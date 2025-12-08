import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { useApp } from '../../context/AppContext';
import { MaterialIcons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

const AIRecommendationsScreen = () => {
  const { recommendations, goals, addGoal } = useApp();
  const [loading, setLoading] = useState(false);

  const getCategoryIcon = (category: string) => {
    const icons: Record<string, string> = {
      health: 'favorite',
      fitness: 'fitness-center',
      career: 'work',
      education: 'school',
      finance: 'attach-money',
      personal: 'person',
      relationships: 'people',
      mental: 'psychology',
    };
    return icons[category] || 'flag';
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      health: '#FF6B6B',
      fitness: '#4ECDC4',
      career: '#45B7D1',
      education: '#96CEB4',
      finance: '#FFEEAD',
      personal: '#D4A5A5',
      relationships: '#9B59B6',
      mental: '#3498DB',
    };
    return colors[category] || '#6200EE';
  };

  const getImpactColor = (impact: string) => {
    const colors: Record<string, string> = {
      high: '#FF3B30',
      medium: '#FF9500',
      low: '#34C759',
    };
    return colors[impact] || '#6200EE';
  };

  const handleAddGoal = (recommendation: any) => {
    addGoal({
      title: recommendation.title,
      description: recommendation.description,
      category: recommendation.category,
      targetDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000), // 30 дней от текущей даты
      progress: 0,
      tasks: [],
    });
  };

  const handleRefresh = async () => {
    setLoading(true);
    // Здесь будет логика обновления рекомендаций
    await new Promise(resolve => setTimeout(resolve, 1000));
    setLoading(false);
  };

  return (
    <View style={styles.container}>
      <LinearGradient
        colors={['#1a1a1a', '#2d2d2d']}
        style={styles.header}
      >
        <Text style={styles.headerTitle}>Рекомендации ИИ</Text>
        <TouchableOpacity
          style={styles.refreshButton}
          onPress={handleRefresh}
          disabled={loading}
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <MaterialIcons name="refresh" size={24} color="#fff" />
          )}
        </TouchableOpacity>
      </LinearGradient>

      <ScrollView style={styles.content}>
        {recommendations.map((recommendation) => (
          <View
            key={recommendation.id}
            style={styles.recommendationCard}
          >
            <View style={styles.recommendationHeader}>
              <View style={styles.categoryIcon}>
                <MaterialIcons
                  name={getCategoryIcon(recommendation.category)}
                  size={24}
                  color={getCategoryColor(recommendation.category)}
                />
              </View>
              <View style={styles.recommendationTitleContainer}>
                <Text style={styles.recommendationTitle}>
                  {recommendation.title}
                </Text>
                <View style={styles.impactContainer}>
                  <View
                    style={[
                      styles.impactDot,
                      { backgroundColor: getImpactColor(recommendation.impact) },
                    ]}
                  />
                  <Text style={styles.impactText}>
                    {recommendation.impact === 'high'
                      ? 'Высокий приоритет'
                      : recommendation.impact === 'medium'
                      ? 'Средний приоритет'
                      : 'Низкий приоритет'}
                  </Text>
                </View>
              </View>
            </View>

            <Text style={styles.recommendationDescription}>
              {recommendation.description}
            </Text>

            <View style={styles.recommendationFooter}>
              <Text style={styles.recommendationDate}>
                {format(new Date(recommendation.createdAt), 'd MMMM yyyy', {
                  locale: ru,
                })}
              </Text>
              <TouchableOpacity
                style={styles.addButton}
                onPress={() => handleAddGoal(recommendation)}
              >
                <MaterialIcons name="add" size={20} color="#fff" />
                <Text style={styles.addButtonText}>Добавить цель</Text>
              </TouchableOpacity>
            </View>
          </View>
        ))}

        {recommendations.length === 0 && (
          <View style={styles.emptyState}>
            <MaterialIcons name="psychology" size={48} color="#666" />
            <Text style={styles.emptyStateText}>
              Нет доступных рекомендаций
            </Text>
            <Text style={styles.emptyStateSubtext}>
              Нажмите кнопку обновления, чтобы получить новые рекомендации
            </Text>
          </View>
        )}
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  headerTitle: {
    color: '#fff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  refreshButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#6200EE',
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  recommendationCard: {
    backgroundColor: '#1E1E1E',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
  },
  recommendationHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  categoryIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#2D2D2D',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 10,
  },
  recommendationTitleContainer: {
    flex: 1,
  },
  recommendationTitle: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  impactContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  impactDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 5,
  },
  impactText: {
    color: '#aaa',
    fontSize: 12,
  },
  recommendationDescription: {
    color: '#aaa',
    fontSize: 14,
    lineHeight: 20,
    marginBottom: 15,
  },
  recommendationFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  recommendationDate: {
    color: '#666',
    fontSize: 12,
  },
  addButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#6200EE',
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
  },
  addButtonText: {
    color: '#fff',
    fontSize: 14,
    marginLeft: 5,
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 50,
  },
  emptyStateText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
  },
  emptyStateSubtext: {
    color: '#666',
    fontSize: 14,
    textAlign: 'center',
  },
});

export default AIRecommendationsScreen; 