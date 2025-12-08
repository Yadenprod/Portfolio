import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

// Маршруты, требующие аутентификации
const protectedRoutes = ['/dashboard', '/api/accounts'];

export async function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;
  
  // Проверка, требует ли маршрут аутентификации
  const isProtectedRoute = protectedRoutes.some(route => 
    path === route || path.startsWith(`${route}/`)
  );
  
  if (isProtectedRoute) {
    const token = await getToken({ 
      req: request, 
      secret: process.env.NEXTAUTH_SECRET
    });
    
    // Если пользователь не аутентифицирован, перенаправляем на страницу входа
    if (!token) {
      const url = new URL('/login', request.url);
      url.searchParams.set('callbackUrl', path);
      return NextResponse.redirect(url);
    }
  }
  
  return NextResponse.next();
}

// Конфигурация для определения, какие маршруты обрабатывать middleware
export const config = {
  matcher: [
    '/dashboard/:path*',
    '/api/accounts/:path*',
  ],
}; 