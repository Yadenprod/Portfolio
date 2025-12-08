import { useState } from 'react';
import Head from 'next/head';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { signIn, useSession } from 'next-auth/react';
import { useEffect } from 'react';

export default function Login() {
  const router = useRouter();
  const { data: session, status } = useSession();
  const { callbackUrl } = router.query;
  const redirectUrl = typeof callbackUrl === 'string' ? callbackUrl : '/dashboard';

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // Перенаправляем на callbackUrl если пользователь уже авторизован
  useEffect(() => {
    if (status === 'authenticated') {
      router.push(redirectUrl);
    }
  }, [status, router, redirectUrl]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Используем Next-Auth для входа
      const result = await signIn('credentials', {
        redirect: false,
        email: formData.email,
        password: formData.password,
      });

      if (result?.error) {
        throw new Error(result.error || 'Ошибка при входе');
      }

      // Успешный вход - перенаправляем пользователя
      router.push(redirectUrl);
    } catch (err: any) {
      setError(err.message || 'Ошибка при входе');
    } finally {
      setLoading(false);
    }
  };

  if (status === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cs-orange mb-2"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Head>
        <title>Вход | CS2 Панель управления</title>
        <meta name="description" content="Вход в панель управления аккаунтами CS2" />
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
          <h1 className="text-2xl font-bold mb-6">Вход в панель</h1>
          
          {error && (
            <div className="bg-red-900 bg-opacity-50 border border-red-800 rounded-md p-3 mb-4 text-sm">
              {error}
            </div>
          )}
          
          <form onSubmit={handleSubmit} className="space-y-4">
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
              />
            </div>
            
            <button
              type="submit"
              className="cs-button w-full"
              disabled={loading}
            >
              {loading ? 'Загрузка...' : 'Войти'}
            </button>
            
            <div className="text-center text-sm text-gray-400 mt-4">
              Нет аккаунта?{' '}
              <Link href="/register" className="text-cs-orange hover:underline">
                Зарегистрироваться
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