import React, { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Button, Text, Card, TextInput, List } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';

// Временные данные для демонстрации
const carBrands = [
  'Toyota',
  'Honda',
  'BMW',
  'Mercedes-Benz',
  'Audi',
  'Volkswagen',
  'Ford',
  'Chevrolet',
];

const CarSearchScreen = () => {
  const navigation = useNavigation();
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedBrand, setSelectedBrand] = useState('');
  const [selectedModel, setSelectedModel] = useState('');

  const filteredBrands = carBrands.filter(brand =>
    brand.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleBrandSelect = (brand: string) => {
    setSelectedBrand(brand);
    setSelectedModel('');
  };

  const handleModelSelect = (model: string) => {
    setSelectedModel(model);
    navigation.navigate('CarDetails', {
      brand: selectedBrand,
      model: model,
    });
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Text variant="titleLarge" style={styles.title}>
            Выберите автомобиль
          </Text>
          
          <TextInput
            label="Поиск марки"
            value={searchQuery}
            onChangeText={setSearchQuery}
            style={styles.searchInput}
          />

          {!selectedBrand ? (
            <View style={styles.brandList}>
              {filteredBrands.map((brand) => (
                <List.Item
                  key={brand}
                  title={brand}
                  onPress={() => handleBrandSelect(brand)}
                  right={props => <List.Icon {...props} icon="chevron-right" />}
                />
              ))}
            </View>
          ) : (
            <View>
              <Button
                mode="outlined"
                onPress={() => setSelectedBrand('')}
                style={styles.backButton}
              >
                Назад к маркам
              </Button>
              
              <Text variant="titleMedium" style={styles.subtitle}>
                Выберите модель {selectedBrand}
              </Text>
              
              {/* Здесь будет список моделей выбранной марки */}
              <List.Item
                title="Model 1"
                onPress={() => handleModelSelect('Model 1')}
                right={props => <List.Icon {...props} icon="chevron-right" />}
              />
              <List.Item
                title="Model 2"
                onPress={() => handleModelSelect('Model 2')}
                right={props => <List.Icon {...props} icon="chevron-right" />}
              />
            </View>
          )}
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
  subtitle: {
    marginTop: 20,
    marginBottom: 10,
  },
  searchInput: {
    marginBottom: 10,
  },
  brandList: {
    marginTop: 10,
  },
  backButton: {
    marginTop: 10,
  },
});

export default CarSearchScreen; 