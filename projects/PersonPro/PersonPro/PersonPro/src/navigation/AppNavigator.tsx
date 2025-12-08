import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialIcons } from '@expo/vector-icons';
import { useApp } from '../context/AppContext';
import { lightTheme, darkTheme } from '../utils/theme';

// Экраны аутентификации
import WelcomeScreen from '../screens/auth/WelcomeScreen';
import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';

// Основные экраны
import DashboardScreen from '../screens/main/DashboardScreen';
import GoalsScreen from '../screens/main/GoalsScreen';
import GoalDetailScreen from '../screens/main/GoalDetailScreen';
import NewGoalScreen from '../screens/main/NewGoalScreen';
import ProfileScreen from '../screens/main/ProfileScreen';
import AIRecommendationsScreen from '../screens/main/AIRecommendationsScreen';
import StatsScreen from '../screens/main/StatsScreen';
import SettingsScreen from '../screens/main/SettingsScreen';

// Типы для стеков навигации
export type AuthStackParamList = {
  Welcome: undefined;
  Login: undefined;
  Register: undefined;
};

export type MainStackParamList = {
  Dashboard: undefined;
  GoalDetail: { goalId: string };
  NewGoal: undefined;
  AIRecommendations: undefined;
  Settings: undefined;
};

export type ProfileStackParamList = {
  Profile: undefined;
  Stats: undefined;
  Settings: undefined;
};

export type TabParamList = {
  Home: undefined;
  Goals: undefined;
  Profile: undefined;
};

// Создаем навигационные стеки
const AuthStack = createStackNavigator<AuthStackParamList>();
const MainStack = createStackNavigator<MainStackParamList>();
const ProfileStack = createStackNavigator<ProfileStackParamList>();
const Tab = createBottomTabNavigator<TabParamList>();

// Стек аутентификации
const AuthNavigator = () => (
  <AuthStack.Navigator
    screenOptions={{
      headerShown: false,
    }}
  >
    <AuthStack.Screen name="Welcome" component={WelcomeScreen} />
    <AuthStack.Screen name="Login" component={LoginScreen} />
    <AuthStack.Screen name="Register" component={RegisterScreen} />
  </AuthStack.Navigator>
);

// Основной стек (вкладка Home)
const HomeNavigator = () => (
  <MainStack.Navigator>
    <MainStack.Screen
      name="Dashboard"
      component={DashboardScreen}
      options={{ headerShown: false }}
    />
    <MainStack.Screen
      name="GoalDetail"
      component={GoalDetailScreen}
      options={{ title: 'Цель' }}
    />
    <MainStack.Screen
      name="NewGoal"
      component={NewGoalScreen}
      options={{ title: 'Новая цель' }}
    />
    <MainStack.Screen
      name="AIRecommendations"
      component={AIRecommendationsScreen}
      options={{ title: 'ИИ рекомендации' }}
    />
    <MainStack.Screen
      name="Settings"
      component={SettingsScreen}
      options={{ title: 'Настройки' }}
    />
  </MainStack.Navigator>
);

// Стек профиля
const ProfileNavigator = () => (
  <ProfileStack.Navigator>
    <ProfileStack.Screen
      name="Profile"
      component={ProfileScreen}
      options={{ headerShown: false }}
    />
    <ProfileStack.Screen
      name="Stats"
      component={StatsScreen}
      options={{ title: 'Статистика' }}
    />
    <ProfileStack.Screen
      name="Settings"
      component={SettingsScreen}
      options={{ title: 'Настройки' }}
    />
  </ProfileStack.Navigator>
);

// Навигация по вкладкам
const TabNavigator = () => (
  <Tab.Navigator
    screenOptions={({ route }) => ({
      tabBarIcon: ({ color, size }) => {
        let iconName: React.ComponentProps<typeof MaterialIcons>['name'] = 'home';

        if (route.name === 'Home') {
          iconName = 'dashboard';
        } else if (route.name === 'Goals') {
          iconName = 'flag';
        } else if (route.name === 'Profile') {
          iconName = 'person';
        }

        return <MaterialIcons name={iconName} size={size} color={color} />;
      },
      headerShown: false,
      tabBarActiveTintColor: '#6200EE',
      tabBarInactiveTintColor: 'gray',
      tabBarLabelStyle: {
        fontSize: 12,
      },
    })}
  >
    <Tab.Screen 
      name="Home" 
      component={HomeNavigator} 
      options={{ title: 'Главная' }}
    />
    <Tab.Screen 
      name="Goals" 
      component={GoalsScreen} 
      options={{ title: 'Цели' }}
    />
    <Tab.Screen 
      name="Profile" 
      component={ProfileNavigator} 
      options={{ title: 'Профиль' }}
    />
  </Tab.Navigator>
);

// Основной навигатор приложения
export const AppNavigator = () => {
  const { user, isLoading, theme } = useApp();
  
  if (isLoading) {
    // В реальном приложении здесь был бы экран загрузки
    return null;
  }
  
  return (
    <NavigationContainer theme={theme === 'dark' ? darkTheme : lightTheme}>
      {user ? <TabNavigator /> : <AuthNavigator />}
    </NavigationContainer>
  );
}; 