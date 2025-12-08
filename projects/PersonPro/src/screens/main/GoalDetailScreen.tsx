import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  TextInput,
  Alert,
} from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import { MaterialIcons } from '@expo/vector-icons';
import { useApp } from '../../context/AppContext';
import { LinearGradient } from 'expo-linear-gradient';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

const GoalDetailScreen = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { goalId } = route.params as { goalId: string };
  const { goals, updateGoal, deleteGoal, addTask, updateTask, deleteTask } = useApp();
  
  const goal = goals.find(g => g.id === goalId);
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [isEditing, setIsEditing] = useState(false);
  const [editedTitle, setEditedTitle] = useState(goal?.title || '');
  const [editedDescription, setEditedDescription] = useState(goal?.description || '');

  if (!goal) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>Цель не найдена</Text>
      </View>
    );
  }

  const handleAddTask = () => {
    if (!newTaskTitle.trim()) return;

    addTask(goalId, {
      title: newTaskTitle.trim(),
      completed: false,
    });

    setNewTaskTitle('');
  };

  const handleUpdateGoal = () => {
    if (!editedTitle.trim()) return;

    updateGoal(goalId, {
      title: editedTitle.trim(),
      description: editedDescription.trim(),
    });

    setIsEditing(false);
  };

  const handleDeleteGoal = () => {
    Alert.alert(
      'Удалить цель',
      'Вы уверены, что хотите удалить эту цель?',
      [
        {
          text: 'Отмена',
          style: 'cancel',
        },
        {
          text: 'Удалить',
          style: 'destructive',
          onPress: () => {
            deleteGoal(goalId);
            navigation.goBack();
          },
        },
      ],
    );
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

  return (
    <View style={styles.container}>
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
          <View style={styles.headerTitle}>
            <MaterialIcons
              name={getCategoryIcon(goal.category)}
              size={24}
              color={getCategoryColor(goal.category)}
            />
            {isEditing ? (
              <TextInput
                style={styles.titleInput}
                value={editedTitle}
                onChangeText={setEditedTitle}
                placeholder="Название цели"
                placeholderTextColor="#666"
              />
            ) : (
              <Text style={styles.title}>{goal.title}</Text>
            )}
          </View>
          <TouchableOpacity
            style={styles.menuButton}
            onPress={() => setIsEditing(!isEditing)}
          >
            <MaterialIcons
              name={isEditing ? 'save' : 'edit'}
              size={24}
              color="#fff"
            />
          </TouchableOpacity>
        </View>
      </LinearGradient>

      <ScrollView style={styles.content}>
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Описание</Text>
          {isEditing ? (
            <TextInput
              style={styles.descriptionInput}
              value={editedDescription}
              onChangeText={setEditedDescription}
              placeholder="Описание цели"
              placeholderTextColor="#666"
              multiline
            />
          ) : (
            <Text style={styles.description}>{goal.description}</Text>
          )}
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Прогресс</Text>
          <View style={styles.progressBar}>
            <View
              style={[
                styles.progressFill,
                {
                  width: `${goal.progress}%`,
                  backgroundColor: getCategoryColor(goal.category),
                },
              ]}
            />
          </View>
          <Text style={styles.progressText}>{goal.progress}% выполнено</Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Целевая дата</Text>
          <Text style={styles.dateText}>
            {format(new Date(goal.targetDate), 'd MMMM yyyy', { locale: ru })}
          </Text>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Задачи</Text>
          {goal.tasks.map((task) => (
            <View key={task.id} style={styles.taskItem}>
              <TouchableOpacity
                style={styles.taskCheckbox}
                onPress={() => updateTask(goalId, task.id, !task.completed)}
              >
                <MaterialIcons
                  name={task.completed ? 'check-box' : 'check-box-outline-blank'}
                  size={24}
                  color={task.completed ? '#6200EE' : '#666'}
                />
              </TouchableOpacity>
              <Text
                style={[
                  styles.taskTitle,
                  task.completed && styles.completedTask,
                ]}
              >
                {task.title}
              </Text>
              <TouchableOpacity
                style={styles.deleteTaskButton}
                onPress={() => deleteTask(goalId, task.id)}
              >
                <MaterialIcons name="delete" size={20} color="#666" />
              </TouchableOpacity>
            </View>
          ))}
        </View>

        <View style={styles.addTaskContainer}>
          <TextInput
            style={styles.addTaskInput}
            value={newTaskTitle}
            onChangeText={setNewTaskTitle}
            placeholder="Новая задача"
            placeholderTextColor="#666"
          />
          <TouchableOpacity
            style={styles.addTaskButton}
            onPress={handleAddTask}
            disabled={!newTaskTitle.trim()}
          >
            <MaterialIcons name="add" size={24} color="#fff" />
          </TouchableOpacity>
        </View>
      </ScrollView>

      {isEditing && (
        <View style={styles.editActions}>
          <TouchableOpacity
            style={[styles.editButton, styles.saveButton]}
            onPress={handleUpdateGoal}
          >
            <Text style={styles.editButtonText}>Сохранить</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.editButton, styles.deleteButton]}
            onPress={handleDeleteGoal}
          >
            <Text style={styles.editButtonText}>Удалить цель</Text>
          </TouchableOpacity>
        </View>
      )}
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
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  backButton: {
    padding: 10,
  },
  headerTitle: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
    marginLeft: 10,
  },
  title: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    marginLeft: 10,
  },
  titleInput: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
    marginLeft: 10,
    flex: 1,
  },
  menuButton: {
    padding: 10,
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
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
  },
  description: {
    color: '#aaa',
    fontSize: 16,
    lineHeight: 24,
  },
  descriptionInput: {
    color: '#fff',
    fontSize: 16,
    lineHeight: 24,
    backgroundColor: '#1E1E1E',
    borderRadius: 10,
    padding: 15,
    minHeight: 100,
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
  dateText: {
    color: '#aaa',
    fontSize: 16,
  },
  taskItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E1E1E',
    borderRadius: 10,
    padding: 15,
    marginBottom: 10,
  },
  taskCheckbox: {
    marginRight: 10,
  },
  taskTitle: {
    color: '#fff',
    fontSize: 16,
    flex: 1,
  },
  completedTask: {
    textDecorationLine: 'line-through',
    color: '#666',
  },
  deleteTaskButton: {
    padding: 5,
  },
  addTaskContainer: {
    flexDirection: 'row',
    marginBottom: 20,
  },
  addTaskInput: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    borderRadius: 10,
    padding: 15,
    color: '#fff',
    fontSize: 16,
    marginRight: 10,
  },
  addTaskButton: {
    backgroundColor: '#6200EE',
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
  },
  editActions: {
    flexDirection: 'row',
    padding: 20,
    backgroundColor: '#1E1E1E',
  },
  editButton: {
    flex: 1,
    padding: 15,
    borderRadius: 10,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  saveButton: {
    backgroundColor: '#6200EE',
  },
  deleteButton: {
    backgroundColor: '#FF3B30',
  },
  editButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  errorText: {
    color: '#fff',
    fontSize: 16,
    textAlign: 'center',
    marginTop: 20,
  },
});

export default GoalDetailScreen; 