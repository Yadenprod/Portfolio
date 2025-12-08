import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  SafeAreaView,
  StatusBar,
  Alert,
  ActivityIndicator,
  Image
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { MainStackParamList } from '../../navigation/AppNavigator';
import { useApp } from '../../context/AppContext';
import { AIRecommendation } from '../../types';
import Button from '../../components/Button';
import { spacing, borderRadius, shadows } from '../../utils/theme';
import { LinearGradient } from 'expo-linear-gradient';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

type AIRecommendationsScreenNavigationProp = StackNavigationProp<
  MainStackParamList,
  'AIRecommendations'
>;

const AIRecommendationsScreen = () => {
  const navigation = useNavigation<AIRecommendationsScreenNavigationProp>();
  const { recommendations, theme, user, goals } = useApp();
  const isDark = theme === 'dark';
  
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [filter, setFilter] = useState<'all' | 'high' | 'medium' | 'low'>('all');
  
  const onRefresh = React.useCallback(() => {
    setRefreshing(true);
    // Здесь будет логика обновления рекомендаций
    setTimeout(() => {
      setRefreshing(false);
    }, 1000);
  }, []);
  
  // Фильтрация рекомендаций
  const filteredRecommendations = filter === 'all' 
    ? recommendations 
    : recommendations.filter(rec => rec.impact === filter);
  
  // Получение цвета и текста для приоритета
  const getImpactInfo = (impact: 'high' | 'medium' | 'low') => {
    switch (impact) {
      case 'high':
        return {
          color: '#F44336',
          bgColor: 'rgba(244, 67, 54, 0.1)',
          text: 'Высокий приоритет'
        };
      case 'medium':
        return {
          color: '#FF9800',
          bgColor: 'rgba(255, 152, 0, 0.1)',
          text: 'Средний приоритет'
        };
      case 'low':
        return {
          color: '#4CAF50',
          bgColor: 'rgba(76, 175, 80, 0.1)',
          text: 'Низкий приоритет'
        };
    }
  };
  
  // Функция для применения рекомендации
  const handleApplyRecommendation = (recommendation: AIRecommendation) => {
    setLoading(true);
    
    // Имитация обработки запроса
    setTimeout(() => {
      setLoading(false);
      Alert.alert(
        'Рекомендация применена',
        'Рекомендация была успешно добавлена в ваши цели.',
        [{ text: 'OK' }]
      );
    }, 1500);
  };
  
  // Функция для генерации новых рекомендаций
  const handleRefreshRecommendations = () => {
    setLoading(true);
    
    // Имитация запроса к ИИ
    setTimeout(() => {
      setLoading(false);
      Alert.alert(
        'Рекомендации обновлены',
        'ИИ создал новые персонализированные рекомендации на основе ваших данных.',
        [{ text: 'Отлично!' }]
      );
    }, 2000);
  };

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

  const getImpactLabel = (impact: string) => {
    const labels: Record<string, string> = {
      high: 'Высокий приоритет',
      medium: 'Средний приоритет',
      low: 'Низкий приоритет',
    };
    return labels[impact] || 'Приоритет';
  };

  return (
    <SafeAreaView style={[styles.container, isDark ? styles.containerDark : styles.containerLight]}>
      <StatusBar barStyle={isDark ? 'light-content' : 'dark-content'} />
      
      <LinearGradient
        colors={['#1a1a1a', '#2d2d2d']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <TouchableOpacity
            style={styles.backButton}
            onPress={() => navigation.goBack()}
          >
            <MaterialIcons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text style={styles.title}>Рекомендации ИИ</Text>
          <View style={styles.placeholder} />
        </View>
      </LinearGradient>
      
      <View style={styles.filterContainer}>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'all' && styles.activeFilter]}
          onPress={() => setFilter('all')}
        >
          <Text style={[styles.filterText, filter === 'all' && styles.activeFilterText]}>
            Все
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'high' && styles.activeFilter]}
          onPress={() => setFilter('high')}
        >
          <Text style={[styles.filterText, filter === 'high' && styles.activeFilterText]}>
            Высокие
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'medium' && styles.activeFilter]}
          onPress={() => setFilter('medium')}
        >
          <Text style={[styles.filterText, filter === 'medium' && styles.activeFilterText]}>
            Средние
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterButton, filter === 'low' && styles.activeFilter]}
          onPress={() => setFilter('low')}
        >
          <Text style={[styles.filterText, filter === 'low' && styles.activeFilterText]}>
            Низкие
          </Text>
        </TouchableOpacity>
      </View>
      
      <ScrollView
        style={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      >
        {filteredRecommendations.length === 0 ? (
          <View style={styles.emptyContainer}>
            <MaterialIcons 
              name="lightbulb"
              size={60}
              color={isDark ? '#555555' : '#CCCCCC'}
            />
            <Text style={[styles.emptyText, isDark ? styles.textDark : styles.textLight]}>
              Рекомендаций не найдено
            </Text>
            <Text style={[styles.emptySubtext, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
              Нажмите на кнопку обновления, чтобы получить новые рекомендации от ИИ
            </Text>
          </View>
        ) : (
          <>
            <View style={styles.aiContainer}>
              <View style={[styles.aiCard, isDark ? styles.aiCardDark : styles.aiCardLight]}>
                <View style={styles.aiHeader}>
                  <View style={styles.aiIconContainer}>
                    <MaterialIcons name="psychology" size={24} color="#FFFFFF" />
                  </View>
                  <View>
                    <Text style={[styles.aiTitle, isDark ? styles.textDark : styles.textLight]}>
                      ИИ-ассистент
                    </Text>
                    <Text style={[styles.aiSubtitle, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
                      Персональный анализ
                    </Text>
                  </View>
                </View>
                
                <Text style={[styles.aiMessage, isDark ? styles.textDark : styles.textLight]}>
                  Основываясь на анализе ваших целей и активности, я подготовил для вас несколько рекомендаций, которые помогут вам стать лучшей версией себя.
                </Text>
              </View>
            </View>
            
            {filteredRecommendations.map(recommendation => {
              const impactInfo = getImpactInfo(recommendation.impact as 'high' | 'medium' | 'low');
              
              return (
                <View 
                  key={recommendation.id} 
                  style={[styles.recommendationCard, isDark ? styles.cardDark : styles.cardLight]}
                >
                  <View style={styles.recommendationHeader}>
                    <View style={styles.categoryIcon}>
                      <MaterialIcons
                        name={getCategoryIcon(recommendation.category)}
                        size={24}
                        color={getCategoryColor(recommendation.category)}
                      />
                    </View>
                    <View style={styles.recommendationInfo}>
                      <Text style={[styles.recommendationTitle, isDark ? styles.textDark : styles.textLight]}>
                        {recommendation.title}
                      </Text>
                      <Text style={[styles.recommendationDate, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
                        {format(new Date(recommendation.createdAt), 'd MMMM yyyy', {
                          locale: ru,
                        })}
                      </Text>
                    </View>
                    <View
                      style={[
                        styles.impactBadge,
                        { backgroundColor: getImpactColor(recommendation.impact) },
                      ]}
                    >
                      <Text style={[styles.impactText, { color: impactInfo.color }]}>
                        {getImpactLabel(recommendation.impact as 'high' | 'medium' | 'low')}
                      </Text>
                    </View>
                  </View>
                  
                  <Text style={[styles.recommendationDescription, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
                    {recommendation.description}
                  </Text>
                  
                  <View style={styles.recommendationActions}>
                    <Button
                      title="Применить"
                      onPress={() => handleApplyRecommendation(recommendation)}
                      variant="primary"
                      size="small"
                      loading={loading}
                    />
                    
                    <TouchableOpacity style={styles.dismissButton}>
                      <Text style={[styles.dismissButtonText, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
                        Скрыть
                      </Text>
                    </TouchableOpacity>
                  </View>
                </View>
              );
            })}
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  containerLight: {
    backgroundColor: '#F8F9FA',
  },
  containerDark: {
    backgroundColor: '#121212',
  },
  header: {
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  backButton: {
    padding: 10,
  },
  title: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  placeholder: {
    width: 44,
  },
  filterContainer: {
    flexDirection: 'row',
    padding: 10,
    backgroundColor: '#1E1E1E',
  },
  filterButton: {
    flex: 1,
    padding: 10,
    alignItems: 'center',
    borderRadius: 20,
    marginHorizontal: 5,
  },
  activeFilter: {
    backgroundColor: '#6200EE',
  },
  filterText: {
    color: '#666',
    fontSize: 14,
  },
  activeFilterText: {
    color: '#fff',
  },
  content: {
    flex: 1,
    padding: 20,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: spacing.xl * 2,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: spacing.md,
  },
  emptySubtext: {
    fontSize: 14,
    textAlign: 'center',
    marginTop: spacing.sm,
    paddingHorizontal: spacing.xl,
  },
  aiContainer: {
    marginBottom: spacing.lg,
  },
  aiCard: {
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    ...shadows.md,
  },
  aiCardLight: {
    backgroundColor: '#FFFFFF',
  },
  aiCardDark: {
    backgroundColor: '#1E1E1E',
  },
  aiHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.md,
  },
  aiIconContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#6200EE',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  aiTitle: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  aiSubtitle: {
    fontSize: 12,
  },
  aiMessage: {
    fontSize: 14,
    lineHeight: 20,
  },
  recommendationCard: {
    borderRadius: borderRadius.lg,
    padding: spacing.md,
    marginBottom: spacing.md,
    ...shadows.md,
  },
  cardLight: {
    backgroundColor: '#FFFFFF',
  },
  cardDark: {
    backgroundColor: '#1E1E1E',
  },
  recommendationHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: spacing.sm,
  },
  categoryIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#2C2C2C',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  recommendationInfo: {
    flex: 1,
  },
  recommendationTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: spacing.sm,
  },
  recommendationDate: {
    fontSize: 12,
  },
  impactBadge: {
    paddingHorizontal: spacing.sm,
    paddingVertical: spacing.xs / 2,
    borderRadius: 4,
  },
  impactText: {
    fontSize: 12,
    fontWeight: '500',
  },
  recommendationDescription: {
    fontSize: 14,
    marginBottom: spacing.md,
    lineHeight: 20,
  },
  recommendationActions: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  dismissButton: {
    marginLeft: spacing.md,
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.sm,
  },
  dismissButtonText: {
    fontSize: 14,
  },
  textLight: {
    color: '#121212',
  },
  textDark: {
    color: '#FFFFFF',
  },
  textLightSecondary: {
    color: '#757575',
  },
  textDarkSecondary: {
    color: '#BBBBBB',
  },
});

export default AIRecommendationsScreen; 