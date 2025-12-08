<template>
  <div class="admin-login">
    <div class="login-card">
      <div class="login-header">
        <h2 class="login-title">🔐 Админ-панель</h2>
        <p class="login-subtitle">Введите пароль для доступа</p>
      </div>

      <form @submit.prevent="login" class="login-form">
        <div class="form-group">
          <label class="form-label">Пароль администратора</label>
          <div class="password-input-container">
            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              required
              class="password-input"
              placeholder="Введите пароль..."
            />
            <button
              type="button"
              @click="showPassword = !showPassword"
              class="password-toggle"
            >
              {{ showPassword ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="login-btn"
        >
          <span v-if="loading">⏳ Вход...</span>
          <span v-else>🚪 Войти</span>
        </button>
      </form>

      <div v-if="error" class="error-message">
        <span>❌</span>
        {{ error }}
      </div>

      <div class="login-footer">
        <p class="footer-text">Доступ только для администраторов</p>
        <button @click="$emit('close')" class="back-btn">
          ← Назад
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AdminLogin',
  data() {
    return {
      password: '',
      showPassword: false,
      loading: false,
      error: null,
      // В реальном приложении пароль должен храниться в защищенном месте
      adminPassword: 'admin123' // Для демонстрации
    }
  },
  methods: {
    async login() {
      if (!this.password) {
        this.error = 'Введите пароль'
        return
      }

      this.loading = true
      this.error = null

      // Имитация задержки API запроса
      await new Promise(resolve => setTimeout(resolve, 1000))

      if (this.password === this.adminPassword) {
        // Успешный вход
        localStorage.setItem('admin_auth', 'true')
        localStorage.setItem('admin_login_time', new Date().toISOString())

        this.$emit('login-success')

        this.$emit('show-notification', {
          type: 'success',
          title: 'Добро пожаловать!',
          message: 'Вы успешно вошли в админ-панель'
        })
      } else {
        this.error = 'Неверный пароль'
        this.password = ''
      }

      this.loading = false
    }
  }
}
</script>

<style scoped>
.admin-login {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 20px;
}

.login-card {
  background: white;
  border-radius: 20px;
  padding: 40px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-title {
  font-size: 2rem;
  font-weight: 700;
  color: #212529;
  margin-bottom: 10px;
}

.login-subtitle {
  font-size: 0.9rem;
  color: #6c757d;
  margin: 0;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  color: #212529;
  margin-bottom: 8px;
}

.password-input-container {
  position: relative;
}

.password-input {
  width: 100%;
  padding: 15px 50px 15px 15px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background: #f8f9fa;
}

.password-input:focus {
  outline: none;
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.password-toggle {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  padding: 5px;
  border-radius: 5px;
  transition: all 0.2s ease;
}

.password-toggle:hover {
  background: rgba(102, 126, 234, 0.1);
}

.login-btn {
  width: 100%;
  padding: 15px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 15px;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8d7da;
  color: #721c24;
  padding: 12px 15px;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-bottom: 20px;
  border: 1px solid #f5c6cb;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #e9ecef;
}

.footer-text {
  font-size: 0.8rem;
  color: #6c757d;
  margin-bottom: 15px;
}

.back-btn {
  background: #6c757d;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.back-btn:hover {
  background: #5a6268;
  transform: translateY(-1px);
}

/* Адаптивность */
@media (max-width: 480px) {
  .admin-login {
    padding: 15px;
  }

  .login-card {
    padding: 30px 20px;
  }

  .login-title {
    font-size: 1.5rem;
  }

  .password-input {
    padding: 12px 40px 12px 12px;
    font-size: 0.9rem;
  }
}
</style>
