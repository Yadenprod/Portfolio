import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Button, Text, Card } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';

const HomeScreen = () => {
  const navigation = useNavigation();

  return (
    <View style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="headlineMedium" style={styles.title}>
            Проверка автомобиля
          </Text>
          <Text variant="bodyLarge" style={styles.description}>
            Узнайте о типичных проблемах и уязвимых местах автомобиля перед покупкой
          </Text>
        </Card.Content>
      </Card>

      <Button
        mode="contained"
        onPress={() => navigation.navigate('CarSearch')}
        style={styles.button}
      >
        Начать проверку
      </Button>

      <Card style={styles.infoCard}>
        <Card.Content>
          <Text variant="titleMedium">Как это работает?</Text>
          <Text variant="bodyMedium" style={styles.infoText}>
            1. Выберите марку и модель автомобиля{'\n'}
            2. Укажите поколение и год выпуска{'\n'}
            3. Получите подробный отчет о типичных проблемах{'\n'}
            4. Следуйте рекомендациям по проверке
          </Text>
        </Card.Content>
      </Card>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#f5f5f5',
  },
  card: {
    marginBottom: 20,
  },
  title: {
    textAlign: 'center',
    marginBottom: 10,
  },
  description: {
    textAlign: 'center',
    marginBottom: 10,
  },
  button: {
    marginVertical: 20,
  },
  infoCard: {
    marginTop: 20,
  },
  infoText: {
    marginTop: 10,
    lineHeight: 24,
  },
});

export default HomeScreen; 