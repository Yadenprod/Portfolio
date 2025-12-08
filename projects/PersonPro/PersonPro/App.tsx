import React from 'react';
import { StatusBar } from 'react-native';
import { AppProvider } from './src/context/AppContext';
import AppNavigator from './src/navigation/AppNavigator';
import { SafeAreaProvider } from 'react-native-safe-area-context';

const App = () => {
  return (
    <SafeAreaProvider>
      <AppProvider>
        <StatusBar barStyle="light-content" />
        <AppNavigator />
      </AppProvider>
    </SafeAreaProvider>
  );
};

export default App; 