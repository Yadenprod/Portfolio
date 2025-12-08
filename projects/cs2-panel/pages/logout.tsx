import { useEffect } from 'react';
import { signOut } from 'next-auth/react';
import { useRouter } from 'next/router';
import Head from 'next/head';

export default function Logout() {
  const router = useRouter();
  
  useEffect(() => {
    // Выполняем выход из системы
    const performSignOut = async () => {
      await signOut({ redirect: false });
      // После выхода перенаправляем на страницу входа
      router.push('/login');
    };
    
    performSignOut();
  }, [router]);
  
  return (
    <div className="min-h-screen flex items-center justify-center bg-cs-dark">
      <Head>
        <title>Выход из системы | CS2 Панель</title>
        <meta name="description" content="Выход из системы" />
      </Head>
      <div className="text-center">
        <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-cs-orange mb-4"></div>
        <p className="text-lg">Выход из системы...</p>
      </div>
    </div>
  );
} 