import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  ScrollView, 
  TouchableOpacity, 
  Switch,
  Linking,
  Alert,
  SafeAreaView,
  StatusBar
} from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import { useApp } from '../../context/AppContext';
import { spacing, borderRadius } from '../../utils/theme';

interface SettingsItemProps {
  icon: React.ComponentProps<typeof MaterialIcons>['name'];
  title: string;
  subtitle?: string;
  onPress?: () => void;
  rightComponent?: React.ReactNode;
  showArrow?: boolean;
}

const SettingsScreen = () => {
  const { theme, toggleTheme, user } = useApp();
  const isDark = theme === 'dark';

  const SettingsItem: React.FC<SettingsItemProps> = ({ 
    icon, 
    title, 
    subtitle, 
    onPress, 
    rightComponent, 
    showArrow = true 
  }) => (
    <TouchableOpacity 
      style={[styles.settingsItem, isDark ? styles.settingsItemDark : styles.settingsItemLight]} 
      onPress={onPress}
      disabled={!onPress}
    >
      <View style={[styles.iconContainer, isDark ? styles.iconContainerDark : styles.iconContainerLight]}>
        <MaterialIcons name={icon} size={22} color={isDark ? '#BB86FC' : '#6200EE'} />
      </View>
      
      <View style={styles.settingsItemContent}>
        <Text style={[styles.settingsItemTitle, isDark ? styles.textDark : styles.textLight]}>
          {title}
        </Text>
        
        {subtitle && (
          <Text style={[styles.settingsItemSubtitle, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
            {subtitle}
          </Text>
        )}
      </View>
      
      <View style={styles.settingsItemRight}>
        {rightComponent}
        
        {onPress && showArrow && (
          <MaterialIcons 
            name="chevron-right" 
            size={22} 
            color={isDark ? '#777777' : '#AAAAAA'} 
          />
        )}
      </View>
    </TouchableOpacity>
  );

  const handleClearData = () => {
    Alert.alert(
      'Очистить все данные',
      'Вы уверены, что хотите удалить все данные приложения? Это действие нельзя отменить.',
      [
        {
          text: 'Отмена',
          style: 'cancel',
        },
        {
          text: 'Очистить',
          onPress: () => {
            // В реальном приложении здесь будет логика очистки данных
            Alert.alert('Данные очищены', 'Все данные приложения успешно удалены.');
          },
          style: 'destructive',
        },
      ]
    );
  };

  const handleLogout = () => {
    Alert.alert(
      'Выйти из аккаунта',
      'Вы уверены, что хотите выйти из аккаунта?',
      [
        {
          text: 'Отмена',
          style: 'cancel',
        },
        {
          text: 'Выйти',
          onPress: () => {
            // В реальном приложении здесь будет логика выхода из аккаунта
          },
          style: 'destructive',
        },
      ]
    );
  };

  return (
    <SafeAreaView style={[styles.container, isDark ? styles.containerDark : styles.containerLight]}>
      <StatusBar barStyle={isDark ? 'light-content' : 'dark-content'} />
      
      <View style={styles.header}>
        <Text style={[styles.title, isDark ? styles.textDark : styles.textLight]}>
          Настройки
        </Text>
      </View>
      
      <ScrollView style={styles.scrollView}>
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
            ПРОФИЛЬ
          </Text>
          
          <SettingsItem
            icon="account-circle"
            title="Личные данные"
            subtitle="Имя, email, фото профиля"
            onPress={() => {
              // Навигация на экран редактирования профиля
            }}
          />
          
          <SettingsItem
            icon="notifications"
            title="Уведомления"
            subtitle="Настройка уведомлений и напоминаний"
            onPress={() => {
              // Навигация на экран настроек уведомлений
            }}
          />
        </View>
        
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
            ПРИЛОЖЕНИЕ
          </Text>
          
          <SettingsItem
            icon="dark-mode"
            title="Темная тема"
            subtitle="Изменить оформление приложения"
            rightComponent={
              <Switch
                value={isDark}
                onValueChange={toggleTheme}
                trackColor={{ false: '#CCCCCC', true: '#9E77E9' }}
                thumbColor={isDark ? '#BB86FC' : '#FFFFFF'}
              />
            }
            showArrow={false}
          />
          
          <SettingsItem
            icon="language"
            title="Язык"
            subtitle="Русский"
            onPress={() => {
              // Навигация на экран выбора языка
            }}
          />
          
          <SettingsItem
            icon="sync"
            title="Синхронизация данных"
            subtitle="Настройка резервного копирования"
            onPress={() => {
              // Навигация на экран настроек синхронизации
            }}
          />
        </View>
        
        <View style={styles.section}>
          <Text style={[styles.sectionTitle, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
            О ПРИЛОЖЕНИИ
          </Text>
          
          <SettingsItem
            icon="info"
            title="О PersonPro"
            subtitle={`Версия 1.0.0`}
            onPress={() => {
              // Показать информацию о приложении
            }}
          />
          
          <SettingsItem
            icon="policy"
            title="Политика конфиденциальности"
            onPress={() => {
              // Открыть политику конфиденциальности
              Linking.openURL('https://example.com/privacy-policy');
            }}
          />
          
          <SettingsItem
            icon="description"
            title="Условия использования"
            onPress={() => {
              // Открыть условия использования
              Linking.openURL('https://example.com/terms');
            }}
          />
          
          <SettingsItem
            icon="support"
            title="Поддержка"
            subtitle="Задать вопрос или сообщить о проблеме"
            onPress={() => {
              // Открыть поддержку
              Linking.openURL('mailto:support@example.com');
            }}
          />
        </View>
        
        <View style={styles.section}>
          <SettingsItem
            icon="delete-forever"
            title="Очистить все данные"
            subtitle="Удалить все ваши данные из приложения"
            onPress={handleClearData}
            showArrow={false}
          />
          
          <SettingsItem
            icon="logout"
            title="Выйти из аккаунта"
            onPress={handleLogout}
            showArrow={false}
          />
        </View>
        
        <View style={styles.footer}>
          <Text style={[styles.footerText, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
            PersonPro © {new Date().getFullYear()}
          </Text>
          <Text style={[styles.footerText, isDark ? styles.textDarkSecondary : styles.textLightSecondary]}>
            Разработано с ❤️
          </Text>
        </View>
      </ScrollView>
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
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  scrollView: {
    flex: 1,
  },
  section: {
    marginBottom: spacing.lg,
  },
  sectionTitle: {
    fontSize: 13,
    fontWeight: 'bold',
    marginHorizontal: spacing.lg,
    marginVertical: spacing.sm,
  },
  settingsItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    marginBottom: 1,
  },
  settingsItemLight: {
    backgroundColor: '#FFFFFF',
  },
  settingsItemDark: {
    backgroundColor: '#1E1E1E',
  },
  iconContainer: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: spacing.md,
  },
  iconContainerLight: {
    backgroundColor: '#F0E5FF',
  },
  iconContainerDark: {
    backgroundColor: '#2C1E47',
  },
  settingsItemContent: {
    flex: 1,
  },
  settingsItemTitle: {
    fontSize: 16,
    fontWeight: '500',
  },
  settingsItemSubtitle: {
    fontSize: 14,
    marginTop: 2,
  },
  settingsItemRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  footer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.xl,
  },
  footerText: {
    fontSize: 12,
    marginBottom: spacing.xs,
  },
  textLight: {
    color: '#121212',
  },
  textDark: {
    color: '#FFFFFF',
  },
  textLightSecondary: {
    color: '#757575',
  },
  textDarkSecondary: {
    color: '#BBBBBB',
  },
});

export default SettingsScreen; 