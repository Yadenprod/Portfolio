import React, { useState } from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  FlatList, 
  TouchableOpacity,
  SafeAreaView,
  StatusBar,
  TextInput,
  RefreshControl,
  Alert
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { MainStackParamList } from '../../navigation/AppNavigator';
import { useApp } from '../../context/AppContext';
import GoalCard from '../../components/GoalCard';
import { GoalCategory } from '../../types';
import { spacing, borderRadius, shadows } from '../../utils/theme';

type GoalsScreenNavigationProp = StackNavigationProp<
  MainStackParamList,
  'Dashboard'
>;

// Категории для фильтрации
const categories: { label: string; value: GoalCategory | 'all' }[] = [
  { label: 'Все', value: 'all' },
  { label: 'Здоровье', value: 'health' },
  { label: 'Фитнес', value: 'fitness' },
  { label: 'Карьера', value: 'career' },
  { label: 'Образование', value: 'education' },
  { label: 'Финансы', value: 'finance' },
  { label: 'Личное развитие', value: 'personal' },
  { label: 'Отношения', value: 'relationships' },
  { label: 'Ментальное здоровье', value: 'mental' },
];

const GoalsScreen = () => {
  const navigation = useNavigation<GoalsScreenNavigationProp>();
  const { goals, theme, deleteGoal } = useApp();
  const isDark = theme === 'dark';
  
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<GoalCategory | 'all'>('all');
  const [sortBy, setSortBy] = useState<'progress' | 'date'>('date');
  const [refreshing, setRefreshing] = useState(false);
  
  // Фильтруем и сортируем цели
  const filteredGoals = goals.filter(goal => {
    const matchesSearch = goal.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         goal.description.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesCategory = selectedCategory === 'all' || goal.category === selectedCategory;
    
    return matchesSearch && matchesCategory;
  }).sort((a, b) => {
    if (sortBy === 'progress') {
      return b.progress - a.progress;
    } else {
      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    }
  });

  const handleGoalPress = (goalId: string) => {
    navigation.navigate('GoalDetail', { goalId });
  };

  const handleAddGoalPress = () => {
    navigation.navigate('NewGoal');
  };

  const handleDeleteGoal = (goalId: string) => {
    Alert.alert(
      'Удалить цель',
      'Вы уверены, что хотите удалить эту цель? Это действие нельзя отменить.',
      [
        {
          text: 'Отмена',
          style: 'cancel',
        },
        {
          text: 'Удалить',
          onPress: () => deleteGoal(goalId),
          style: 'destructive',
        },
      ]
    );
  };
  
  const onRefresh = () => {
    setRefreshing(true);
    // Имитация загрузки данных
    setTimeout(() => {
      setRefreshing(false);
    }, 1000);
  };

  return (
    <SafeAreaView style={[styles.container, isDark ? styles.containerDark : styles.containerLight]}>
      <StatusBar barStyle={isDark ? 'light-content' : 'dark-content'} />
      
      <View style={styles.header}>
        <Text style={[styles.title, isDark ? styles.textDark : styles.textLight]}>
          Ваши цели
        </Text>
        
        <TouchableOpacity 
          style={[styles.sortButton, isDark ? styles.buttonDark : styles.buttonLight]} 
          onPress={() => setSortBy(sortBy === 'date' ? 'progress' : 'date')}
        >
          <MaterialIcons 
            name={sortBy === 'date' ? 'access-time' : 'trending-up'} 
            size={20} 
            color={isDark ? '#FFFFFF' : '#121212'} 
          />
          <Text style={[styles.sortButtonText, isDark ? styles.textDark : styles.textLight]}>
            {sortBy === 'date' ? 'По дате' : 'По прогрессу'}
          </Text>
        </TouchableOpacity>
      </View>
      
      <View style={[styles.searchContainer, isDark ? styles.searchContainerDark : styles.searchContainerLight]}>
        <MaterialIcons name="search" size={20} color={isDark ? '#BBBBBB' : '#757575'} />
        <TextInput
          style={[styles.searchInput, isDark ? styles.textDark : styles.textLight]}
          placeholder="Поиск целей..."
          placeholderTextColor={isDark ? '#777777' : '#AAAAAA'}
          value={searchQuery}
          onChangeText={setSearchQuery}
        />
        {searchQuery.length > 0 && (
          <TouchableOpacity onPress={() => setSearchQuery('')}>
            <MaterialIcons name="close" size={20} color={isDark ? '#BBBBBB' : '#757575'} />
          </TouchableOpacity>
        )}
      </View>
      
      <View style={styles.categoriesContainer}>
        <FlatList
          horizontal
          showsHorizontalScrollIndicator={false}
          data={categories}
          keyExtractor={(item) => item.value}
          renderItem={({ item }) => (
            <TouchableOpacity
              style={[
                styles.categoryButton,
                isDark ? styles.categoryButtonDark : styles.categoryButtonLight,
                selectedCategory === item.value && (
                  isDark ? styles.categoryButtonActiveDark : styles.categoryButtonActiveLight
                ),
              ]}
              onPress={() => setSelectedCategory(item.value)}
            >
              <Text 
                style={[
                  styles.categoryButtonText,
                  isDark ? styles.textDark : styles.textLight,
                  selectedCategory === item.value && styles.categoryButtonTextActive,
                ]}
              >
                {item.label}
              </Text>
            </TouchableOpacity>
          )}
          contentContainerStyle={styles.categoriesList}
        />
      </View>
      
      {filteredGoals.length === 0 ? (
        <View style={styles.emptyContainer}>
          <MaterialIcons 
            name="flag"
            size={60}
            color={isDark ? '#555555' : '#CCCCCC'}
          />
          <Text style={[styles.emptyText, isDark ? styles.textDark : styles.textLight]}>
            {searchQuery 
              ? 'Целей по вашему запросу не найдено'
              : selectedCategory !== 'all'
                ? 'В этой категории пока нет целей'
                : 'У вас пока нет целей'
            }
          </Text>
          <TouchableOpacity 
            style={[styles.emptyButton, isDark ? styles.emptyButtonDark : styles.emptyButtonLight]}
            onPress={handleAddGoalPress}
          >
            <Text style={styles.emptyButtonText}>Создать цель</Text>
          </TouchableOpacity>
        </View>
      ) : (
        <FlatList
          data={filteredGoals}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <GoalCard 
              goal={item} 
              onPress={handleGoalPress}
              onLongPress={() => handleDeleteGoal(item.id)}
            />
          )}
          contentContainerStyle={styles.goalsList}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              colors={['#6200EE']}
              tintColor={isDark ? '#BB86FC' : '#6200EE'}
            />
          }
        />
      )}
      
      <TouchableOpacity 
        style={[styles.fab, isDark ? styles.fabDark : styles.fabLight]} 
        onPress={handleAddGoalPress}
      >
        <MaterialIcons name="add" size={24} color="#FFFFFF" />
      </TouchableOpacity>
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
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  sortButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    borderRadius: borderRadius.md,
    ...shadows.sm,
  },
  buttonLight: {
    backgroundColor: '#FFFFFF',
  },
  buttonDark: {
    backgroundColor: '#2C2C2C',
  },
  sortButtonText: {
    marginLeft: spacing.xs,
    fontSize: 14,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: spacing.md,
    marginHorizontal: spacing.lg,
    marginBottom: spacing.md,
    borderRadius: borderRadius.md,
    height: 44,
    ...shadows.sm,
  },
  searchContainerLight: {
    backgroundColor: '#FFFFFF',
  },
  searchContainerDark: {
    backgroundColor: '#2C2C2C',
  },
  searchInput: {
    flex: 1,
    marginLeft: spacing.xs,
    height: '100%',
    fontSize: 16,
  },
  categoriesContainer: {
    marginBottom: spacing.md,
  },
  categoriesList: {
    paddingHorizontal: spacing.lg,
  },
  categoryButton: {
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
    marginRight: spacing.sm,
    borderRadius: borderRadius.sm,
  },
  categoryButtonLight: {
    backgroundColor: '#FFFFFF',
  },
  categoryButtonDark: {
    backgroundColor: '#2C2C2C',
  },
  categoryButtonActiveLight: {
    backgroundColor: '#EDE7F6',
  },
  categoryButtonActiveDark: {
    backgroundColor: '#4A148C',
  },
  categoryButtonText: {
    fontSize: 14,
  },
  categoryButtonTextActive: {
    color: '#6200EE',
    fontWeight: 'bold',
  },
  goalsList: {
    paddingHorizontal: spacing.lg,
    paddingBottom: spacing.xxl,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: spacing.xl,
  },
  emptyText: {
    fontSize: 16,
    textAlign: 'center',
    marginTop: spacing.md,
    marginBottom: spacing.lg,
  },
  emptyButton: {
    paddingHorizontal: spacing.lg,
    paddingVertical: spacing.md,
    borderRadius: borderRadius.md,
    ...shadows.md,
  },
  emptyButtonLight: {
    backgroundColor: '#6200EE',
  },
  emptyButtonDark: {
    backgroundColor: '#BB86FC',
  },
  emptyButtonText: {
    color: '#FFFFFF',
    fontWeight: 'bold',
    fontSize: 16,
  },
  fab: {
    position: 'absolute',
    right: spacing.lg,
    bottom: spacing.lg,
    width: 56,
    height: 56,
    borderRadius: 28,
    justifyContent: 'center',
    alignItems: 'center',
    ...shadows.lg,
  },
  fabLight: {
    backgroundColor: '#6200EE',
  },
  fabDark: {
    backgroundColor: '#BB86FC',
  },
  textLight: {
    color: '#121212',
  },
  textDark: {
    color: '#FFFFFF',
  },
});

export default GoalsScreen; 