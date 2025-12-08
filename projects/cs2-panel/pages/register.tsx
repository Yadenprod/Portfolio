import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';

export default function Register() {
  const router = useRouter();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Пароли не совпадают');
      setLoading(false);
      return;
    }

    try {
      const res = await fetch('/api/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.message || 'Ошибка при регистрации');
      }

      // Редирект на страницу входа после успешной регистрации
      router.push('/login');
    } catch (err: any) {
      setError(err.message || 'Ошибка при регистрации');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>Регистрация | CS2 Панель управления</title>
        <meta name="description" content="Регистрация в панели управления аккаунтами CS2" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="bg-cs-dark border-b border-gray-800 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold text-cs-orange">
            CS2 Панель
          </Link>
        </div>
      </header>

      <main className="flex-grow container mx-auto p-4 flex items-center justify-center">
        <div className="cs-card w-full max-w-md">
          <h1 className="text-2xl font-bold mb-6">Регистрация</h1>
          
          {error && (
            <div className="bg-red-900 bg-opacity-50 border border-red-800 rounded-md p-3 mb-4 text-sm">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1">Имя</label>
              <input
                type="text"
                name="name"
                value={formData.name}
                onChange={handleChange}
                className="cs-input w-full"
                placeholder="Ваше имя"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="cs-input w-full"
                placeholder="your@email.com"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">Пароль</label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="cs-input w-full"
                placeholder="********"
                required
                minLength={6}
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium mb-1">Подтвердите пароль</label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="cs-input w-full"
                placeholder="********"
                required
                minLength={6}
              />
            </div>
            
            <button
              type="submit"
              className="cs-button w-full"
              disabled={loading}
            >
              {loading ? 'Загрузка...' : 'Зарегистрироваться'}
            </button>
            
            <div className="text-center text-sm text-gray-400 mt-4">
              Уже есть аккаунт?{' '}
              <Link href="/login" className="text-cs-orange hover:underline">
                Войти
              </Link>
            </div>
          </form>
        </div>
      </main>

      <footer className="bg-cs-dark border-t border-gray-800 p-4 text-center text-gray-400">
        <div className="container mx-auto">
          <p>© {new Date().getFullYear()} CS2 Панель управления. Все права защищены.</p>
        </div>
      </footer>
    </div>
  );
} 