import React from 'react';
import { 
  View, 
  Text, 
  StyleSheet, 
  Image, 
  StatusBar, 
  SafeAreaView, 
  Dimensions,
  ImageBackground 
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { AuthStackParamList } from '../../navigation/AppNavigator';
import Button from '../../components/Button';
import { spacing, typography, borderRadius } from '../../utils/theme';

type WelcomeScreenNavigationProp = StackNavigationProp<
  AuthStackParamList,
  'Welcome'
>;

const WelcomeScreen = () => {
  const navigation = useNavigation<WelcomeScreenNavigationProp>();

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      
      <ImageBackground 
        source={require('../../assets/images/welcome_bg.png')} 
        style={styles.backgroundImage}
        resizeMode="cover"
      >
        <View style={styles.overlay}>
          <View style={styles.logoContainer}>
            <Image 
              // Заглушка - в реальном приложении будет реальный логотип
              source={require('../../assets/images/logo.png')} 
              style={styles.logo}
              resizeMode="contain"
            />
            <Text style={styles.appName}>PersonPro</Text>
          </View>
          
          <View style={styles.content}>
            <Text style={styles.title}>Стань лучшей версией себя</Text>
            
            <Text style={styles.description}>
              Поставь цели, отслеживай прогресс и получай персональные рекомендации от искусственного интеллекта
            </Text>
            
            <View style={styles.featureRow}>
              <View style={styles.featureItem}>
                <Text style={styles.featureTitle}>Умный анализ</Text>
                <Text style={styles.featureDescription}>
                  ИИ анализирует вашу статистику и предлагает действия
                </Text>
              </View>
              
              <View style={styles.featureItem}>
                <Text style={styles.featureTitle}>Потрясающий UI</Text>
                <Text style={styles.featureDescription}>
                  Интерфейс будущего в вашем телефоне
                </Text>
              </View>
            </View>
          </View>
          
          <View style={styles.buttonsContainer}>
            <Button 
              title="Войти" 
              onPress={() => navigation.navigate('Login')} 
              variant="primary" 
              size="large"
              fullWidth
            />
            
            <Button 
              title="Зарегистрироваться" 
              onPress={() => navigation.navigate('Register')} 
              variant="outline" 
              size="large"
              fullWidth
              style={styles.registerButton}
            />
          </View>
        </View>
      </ImageBackground>
    </SafeAreaView>
  );
};

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  backgroundImage: {
    width: '100%',
    height: '100%',
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.65)',
    padding: spacing.lg,
    justifyContent: 'space-between',
  },
  logoContainer: {
    alignItems: 'center',
    marginTop: height * 0.05,
  },
  logo: {
    width: 80,
    height: 80,
  },
  appName: {
    color: '#FFFFFF',
    fontSize: 28,
    fontWeight: 'bold',
    marginTop: spacing.sm,
  },
  content: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: spacing.xl,
  },
  title: {
    color: '#FFFFFF',
    fontSize: 32,
    fontWeight: 'bold',
    textAlign: 'center',
    marginBottom: spacing.lg,
  },
  description: {
    color: '#FFFFFF',
    fontSize: 16,
    textAlign: 'center',
    marginBottom: spacing.xl,
    opacity: 0.9,
    lineHeight: 24,
  },
  featureRow: {
    flexDirection: 'row',
    width: '100%',
    justifyContent: 'space-between',
    marginTop: spacing.md,
  },
  featureItem: {
    width: '48%',
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    borderRadius: borderRadius.md,
    padding: spacing.md,
  },
  featureTitle: {
    color: '#FFFFFF',
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: spacing.xs,
  },
  featureDescription: {
    color: '#FFFFFF',
    fontSize: 14,
    opacity: 0.8,
    lineHeight: 20,
  },
  buttonsContainer: {
    marginTop: spacing.xl,
    marginBottom: height * 0.05,
  },
  registerButton: {
    marginTop: spacing.md,
    borderColor: '#FFFFFF',
  },
});

export default WelcomeScreen; 