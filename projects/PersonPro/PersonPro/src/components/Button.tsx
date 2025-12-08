import React from 'react';
import { 
  TouchableOpacity, 
  Text, 
  StyleSheet, 
  ActivityIndicator, 
  ViewStyle, 
  TextStyle, 
  TouchableOpacityProps 
} from 'react-native';
import { useApp } from '../context/AppContext';
import { spacing, borderRadius, typography } from '../utils/theme';

interface ButtonProps extends TouchableOpacityProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline' | 'text';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
  disabled?: boolean;
  fullWidth?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'medium',
  loading = false,
  disabled = false,
  fullWidth = false,
  icon,
  iconPosition = 'left',
  style,
  textStyle,
  ...rest
}) => {
  const { theme } = useApp();
  const isDark = theme === 'dark';

  // Получаем стили в зависимости от варианта кнопки
  const getVariantStyles = (): { container: ViewStyle; text: TextStyle } => {
    switch (variant) {
      case 'primary':
        return {
          container: {
            backgroundColor: isDark ? '#BB86FC' : '#6200EE',
          },
          text: {
            color: '#FFF',
          },
        };
      case 'secondary':
        return {
          container: {
            backgroundColor: isDark ? '#2E2E2E' : '#E0E0E0',
          },
          text: {
            color: isDark ? '#FFFFFF' : '#121212',
          },
        };
      case 'outline':
        return {
          container: {
            backgroundColor: 'transparent',
            borderWidth: 1,
            borderColor: isDark ? '#BB86FC' : '#6200EE',
          },
          text: {
            color: isDark ? '#BB86FC' : '#6200EE',
          },
        };
      case 'text':
        return {
          container: {
            backgroundColor: 'transparent',
          },
          text: {
            color: isDark ? '#BB86FC' : '#6200EE',
          },
        };
      default:
        return {
          container: {
            backgroundColor: isDark ? '#BB86FC' : '#6200EE',
          },
          text: {
            color: '#FFF',
          },
        };
    }
  };

  // Получаем стили в зависимости от размера кнопки
  const getSizeStyles = (): { container: ViewStyle; text: TextStyle } => {
    switch (size) {
      case 'small':
        return {
          container: {
            paddingHorizontal: spacing.md,
            paddingVertical: spacing.xs,
            minHeight: 32,
          },
          text: {
            fontSize: 12,
            fontWeight: '500' as TextStyle['fontWeight'],
            letterSpacing: 0.4,
            textTransform: 'uppercase' as TextStyle['textTransform'],
          },
        };
      case 'medium':
        return {
          container: {
            paddingHorizontal: spacing.lg,
            paddingVertical: spacing.sm,
            minHeight: 44,
          },
          text: {
            fontSize: 14,
            fontWeight: '500' as TextStyle['fontWeight'],
            letterSpacing: 0.5,
            textTransform: 'uppercase' as TextStyle['textTransform'],
          },
        };
      case 'large':
        return {
          container: {
            paddingHorizontal: spacing.xl,
            paddingVertical: spacing.md,
            minHeight: 56,
          },
          text: {
            fontSize: 16,
            fontWeight: '500' as TextStyle['fontWeight'],
            letterSpacing: 0.6,
            textTransform: 'uppercase' as TextStyle['textTransform'],
          },
        };
      default:
        return {
          container: {
            paddingHorizontal: spacing.lg,
            paddingVertical: spacing.sm,
            minHeight: 44,
          },
          text: {
            fontSize: 14,
            fontWeight: '500' as TextStyle['fontWeight'],
            letterSpacing: 0.5,
            textTransform: 'uppercase' as TextStyle['textTransform'],
          },
        };
    }
  };

  const variantStyles = getVariantStyles();
  const sizeStyles = getSizeStyles();

  const containerStyles = [
    styles.container,
    variantStyles.container,
    sizeStyles.container,
    fullWidth && styles.fullWidth,
    disabled && styles.disabledContainer,
    style,
  ];

  const textStyles = [
    styles.text,
    variantStyles.text,
    sizeStyles.text,
    disabled && styles.disabledText,
    textStyle,
  ];

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.7}
      style={containerStyles}
      {...rest}
    >
      {loading ? (
        <ActivityIndicator color={variantStyles.text.color} size="small" />
      ) : (
        <>
          {icon && iconPosition === 'left' && icon}
          <Text style={textStyles}>{title}</Text>
          {icon && iconPosition === 'right' && icon}
        </>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: borderRadius.md,
    gap: spacing.sm,
  },
  fullWidth: {
    width: '100%',
  },
  text: {
    textAlign: 'center',
  },
  disabledContainer: {
    opacity: 0.5,
  },
  disabledText: {
    opacity: 0.8,
  },
});

export default Button; 