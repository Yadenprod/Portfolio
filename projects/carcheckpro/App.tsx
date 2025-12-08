import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Provider as PaperProvider } from 'react-native-paper';
import { StatusBar } from 'expo-status-bar';

// Screens
import HomeScreen from './src/screens/HomeScreen';
import CarSearchScreen from './src/screens/CarSearchScreen';
import CarDetailsScreen from './src/screens/CarDetailsScreen';

const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <PaperProvider>
      <NavigationContainer>
        <StatusBar style="auto" />
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen 
            name="Home" 
            component={HomeScreen} 
            options={{ title: 'Проверка авто' }}
          />
          <Stack.Screen 
            name="CarSearch" 
            component={CarSearchScreen} 
            options={{ title: 'Поиск автомобиля' }}
          />
          <Stack.Screen 
            name="CarDetails" 
            component={CarDetailsScreen} 
            options={{ title: 'Детали автомобиля' }}
          />
        </Stack.Navigator>
      </NavigationContainer>
    </PaperProvider>
  );
} 