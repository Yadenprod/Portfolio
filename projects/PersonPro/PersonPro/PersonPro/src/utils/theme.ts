import { AppTheme } from '../types';

export const lightTheme: AppTheme = {
  dark: false,
  colors: {
    primary: '#6200EE',  // Основной фиолетовый
    background: '#FFFFFF',
    card: '#F8F9FA',
    text: '#121212',
    border: '#E0E0E0',
    notification: '#FF9800',
    accent: '#03DAC6',  // Бирюзовый акцент
    success: '#4CAF50',
    warning: '#FFC107',
    error: '#F44336',
  },
};

export const darkTheme: AppTheme = {
  dark: true,
  colors: {
    primary: '#BB86FC',  // Светло-фиолетовый
    background: '#121212',
    card: '#1E1E1E',
    text: '#FFFFFF',
    border: '#333333',
    notification: '#FF9800',
    accent: '#03DAC6',  // Бирюзовый акцент
    success: '#4CAF50',
    warning: '#FFC107',
    error: '#F44336',
  },
};

// Градиенты для красивой визуализации
export const gradients = {
  primary: ['#6200EE', '#9F44D3'],
  success: ['#4CAF50', '#8BC34A'],
  warning: ['#FFC107', '#FFB300'],
  error: ['#F44336', '#E53935'],
  purple: ['#5E35B1', '#7B1FA2'],
  blue: ['#1976D2', '#0277BD'],
  cyan: ['#00ACC1', '#00838F'],
  gray: ['#757575', '#616161'],
};

// Размеры для обеспечения консистентности
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};

// Радиусы скругления
export const borderRadius = {
  sm: 4,
  md: 8,
  lg: 16,
  xl: 24,
  pill: 9999,
};

// Тени для элементов
export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.18,
    shadowRadius: 1.0,
    elevation: 1,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.22,
    shadowRadius: 2.22,
    elevation: 3,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.30,
    shadowRadius: 4.65,
    elevation: 8,
  },
};

// Типографика
export const typography = {
  h1: {
    fontSize: 32,
    fontWeight: 'bold',
    letterSpacing: 0.25,
  },
  h2: {
    fontSize: 24,
    fontWeight: 'bold',
    letterSpacing: 0,
  },
  h3: {
    fontSize: 20,
    fontWeight: '600',
    letterSpacing: 0.15,
  },
  subtitle1: {
    fontSize: 16,
    fontWeight: '600',
    letterSpacing: 0.15,
  },
  subtitle2: {
    fontSize: 14,
    fontWeight: '500',
    letterSpacing: 0.1,
  },
  body1: {
    fontSize: 16,
    fontWeight: 'normal',
    letterSpacing: 0.5,
  },
  body2: {
    fontSize: 14,
    fontWeight: 'normal',
    letterSpacing: 0.25,
  },
  button: {
    fontSize: 14,
    fontWeight: '500',
    letterSpacing: 1.25,
    textTransform: 'uppercase',
  },
  caption: {
    fontSize: 12,
    fontWeight: 'normal',
    letterSpacing: 0.4,
  },
  overline: {
    fontSize: 10,
    fontWeight: 'normal',
    letterSpacing: 1.5,
    textTransform: 'uppercase',
  },
}; 