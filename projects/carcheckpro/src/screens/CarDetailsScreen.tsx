import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Text, List, Divider, Button } from 'react-native-paper';
import { useRoute } from '@react-navigation/native';

// Временные данные для демонстрации
const commonProblems = [
  {
    title: 'Двигатель',
    problems: [
      'Проблемы с маслосъемными колпачками',
      'Течь масла из-под клапанной крышки',
      'Проблемы с гидрокомпенсаторами',
    ],
  },
  {
    title: 'Трансмиссия',
    problems: [
      'Износ сцепления',
      'Проблемы с синхронизаторами',
      'Течь масла из коробки передач',
    ],
  },
  {
    title: 'Подвеска',
    problems: [
      'Износ шаровых опор',
      'Проблемы с сайлентблоками',
      'Износ амортизаторов',
    ],
  },
];

const checkPoints = [
  {
    title: 'Внешний осмотр',
    points: [
      'Проверка кузова на наличие ржавчины',
      'Осмотр лакокрасочного покрытия',
      'Проверка состояния стекол',
    ],
  },
  {
    title: 'Проверка двигателя',
    points: [
      'Проверка уровня масла',
      'Осмотр на наличие течей',
      'Проверка работы двигателя на холодную',
    ],
  },
  {
    title: 'Проверка ходовой',
    points: [
      'Проверка люфтов в подвеске',
      'Осмотр состояния шин',
      'Проверка работы тормозов',
    ],
  },
];

const CarDetailsScreen = () => {
  const route = useRoute();
  const { brand, model } = route.params as { brand: string; model: string };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="headlineMedium" style={styles.title}>
            {brand} {model}
          </Text>
          
          <Text variant="titleLarge" style={styles.sectionTitle}>
            Типичные проблемы
          </Text>
          
          {commonProblems.map((section, index) => (
            <View key={index}>
              <Text variant="titleMedium" style={styles.subsectionTitle}>
                {section.title}
              </Text>
              {section.problems.map((problem, pIndex) => (
                <List.Item
                  key={pIndex}
                  title={problem}
                  left={props => <List.Icon {...props} icon="alert" />}
                />
              ))}
              {index < commonProblems.length - 1 && <Divider />}
            </View>
          ))}

          <Text variant="titleLarge" style={styles.sectionTitle}>
            Что проверить при осмотре
          </Text>
          
          {checkPoints.map((section, index) => (
            <View key={index}>
              <Text variant="titleMedium" style={styles.subsectionTitle}>
                {section.title}
              </Text>
              {section.points.map((point, pIndex) => (
                <List.Item
                  key={pIndex}
                  title={point}
                  left={props => <List.Icon {...props} icon="check-circle" />}
                />
              ))}
              {index < checkPoints.length - 1 && <Divider />}
            </View>
          ))}

          <Button
            mode="contained"
            onPress={() => {}}
            style={styles.button}
          >
            Сохранить отчет
          </Button>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  card: {
    margin: 16,
  },
  title: {
    textAlign: 'center',
    marginBottom: 20,
  },
  sectionTitle: {
    marginTop: 20,
    marginBottom: 10,
  },
  subsectionTitle: {
    marginTop: 10,
    marginBottom: 5,
  },
  button: {
    marginTop: 20,
  },
});

export default CarDetailsScreen; 