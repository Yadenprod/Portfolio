import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialIcons } from '@expo/vector-icons';

// Screens
import DashboardScreen from '../screens/main/DashboardScreen';
import NewGoalScreen from '../screens/main/NewGoalScreen';
import GoalDetailScreen from '../screens/main/GoalDetailScreen';
import AIRecommendationsScreen from '../screens/main/AIRecommendationsScreen';
import StatsScreen from '../screens/main/StatsScreen';

export type RootStackParamList = {
  MainTabs: undefined;
  NewGoal: undefined;
  GoalDetail: { goalId: string };
  AIRecommendations: undefined;
};

export type MainTabParamList = {
  Dashboard: undefined;
  Stats: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

const MainTabs = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;

          if (route.name === 'Dashboard') {
            iconName = focused ? 'dashboard' : 'dashboard';
          } else if (route.name === 'Stats') {
            iconName = focused ? 'analytics' : 'analytics';
          }

          return <MaterialIcons name={iconName as any} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#6200EE',
        tabBarInactiveTintColor: 'gray',
        headerShown: false,
      })}
    >
      <Tab.Screen name="Dashboard" component={DashboardScreen} />
      <Tab.Screen name="Stats" component={StatsScreen} />
    </Tab.Navigator>
  );
};

const AppNavigator = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: {
            backgroundColor: '#1a1a1a',
          },
          headerTintColor: '#fff',
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="MainTabs" 
          component={MainTabs} 
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="NewGoal" 
          component={NewGoalScreen} 
          options={{ title: 'Новая цель' }}
        />
        <Stack.Screen 
          name="GoalDetail" 
          component={GoalDetailScreen} 
          options={{ title: 'Детали цели' }}
        />
        <Stack.Screen 
          name="AIRecommendations" 
          component={AIRecommendationsScreen} 
          options={{ title: 'Рекомендации ИИ' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigator; 