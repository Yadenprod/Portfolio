import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Animated,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { MaterialIcons } from '@expo/vector-icons';
import { useApp } from '../../context/AppContext';
import { GoalCategory } from '../../types';
import { LinearGradient } from 'expo-linear-gradient';

const DashboardScreen = () => {
  const navigation = useNavigation();
  const { user, goals, recommendations } = useApp();
  const fadeAnim = new Animated.Value(0);

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start();
  }, []);

  const getCategoryIcon = (category: GoalCategory) => {
    const icons: Record<GoalCategory, string> = {
      health: 'favorite',
      fitness: 'fitness-center',
      career: 'work',
      education: 'school',
      finance: 'attach-money',
      personal: 'person',
      relationships: 'people',
      mental: 'psychology',
    };
    return icons[category];
  };

  const getCategoryColor = (category: GoalCategory) => {
    const colors: Record<GoalCategory, string> = {
      health: '#FF6B6B',
      fitness: '#4ECDC4',
      career: '#45B7D1',
      education: '#96CEB4',
      finance: '#FFEEAD',
      personal: '#D4A5A5',
      relationships: '#9B59B6',
      mental: '#3498DB',
    };
    return colors[category];
  };

  return (
    <Animated.View style={[styles.container, { opacity: fadeAnim }]}>
      <LinearGradient
        colors={['#1a1a1a', '#2d2d2d']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View style={styles.userInfo}>
            <Image
              source={{ uri: user?.photoUrl || 'https://via.placeholder.com/50' }}
              style={styles.avatar}
            />
            <View>
              <Text style={styles.greeting}>Привет, {user?.name}!</Text>
              <Text style={styles.stats}>
                Дней подряд: {user?.stats.dailyStreak} 🔥
              </Text>
            </View>
          </View>
          <TouchableOpacity
            style={styles.aiButton}
            onPress={() => navigation.navigate('AIRecommendations')}
          >
            <MaterialIcons name="psychology" size={24} color="#fff" />
          </TouchableOpacity>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Ваши цели</Text>
          {goals.map((goal) => (
            <TouchableOpacity
              key={goal.id}
              style={styles.goalCard}
              onPress={() => navigation.navigate('GoalDetail', { goalId: goal.id })}
            >
              <View style={styles.goalHeader}>
                <MaterialIcons
                  name={getCategoryIcon(goal.category)}
                  size={24}
                  color={getCategoryColor(goal.category)}
                />
                <Text style={styles.goalTitle}>{goal.title}</Text>
              </View>
              <View style={styles.progressBar}>
                <View
                  style={[
                    styles.progressFill,
                    { width: `${goal.progress}%`, backgroundColor: getCategoryColor(goal.category) },
                  ]}
                />
              </View>
              <Text style={styles.progressText}>{goal.progress}% выполнено</Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Рекомендации ИИ</Text>
          {recommendations.slice(0, 3).map((rec) => (
            <View key={rec.id} style={styles.recommendationCard}>
              <MaterialIcons
                name={getCategoryIcon(rec.category)}
                size={24}
                color={getCategoryColor(rec.category)}
              />
              <View style={styles.recommendationContent}>
                <Text style={styles.recommendationTitle}>{rec.title}</Text>
                <Text style={styles.recommendationDescription}>
                  {rec.description}
                </Text>
              </View>
            </View>
          ))}
        </View>
      </ScrollView>

      <TouchableOpacity
        style={styles.addButton}
        onPress={() => navigation.navigate('NewGoal')}
      >
        <MaterialIcons name="add" size={30} color="#fff" />
      </TouchableOpacity>
    </Animated.View>
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
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  userInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  avatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    marginRight: 15,
  },
  greeting: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
  stats: {
    color: '#aaa',
    fontSize: 14,
  },
  aiButton: {
    backgroundColor: '#6200EE',
    padding: 10,
    borderRadius: 25,
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
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  goalCard: {
    backgroundColor: '#1E1E1E',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
  },
  goalHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  goalTitle: {
    color: '#fff',
    fontSize: 18,
    marginLeft: 10,
    flex: 1,
  },
  progressBar: {
    height: 8,
    backgroundColor: '#333',
    borderRadius: 4,
    marginBottom: 5,
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  progressText: {
    color: '#aaa',
    fontSize: 12,
    textAlign: 'right',
  },
  recommendationCard: {
    backgroundColor: '#1E1E1E',
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
    flexDirection: 'row',
    alignItems: 'center',
  },
  recommendationContent: {
    flex: 1,
    marginLeft: 15,
  },
  recommendationTitle: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  recommendationDescription: {
    color: '#aaa',
    fontSize: 14,
  },
  addButton: {
    position: 'absolute',
    right: 20,
    bottom: 20,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#6200EE',
    justifyContent: 'center',
    alignItems: 'center',
    elevation: 5,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
});

export default DashboardScreen; 