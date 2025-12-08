<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;

class SecurityHeadersMiddleware
{
    public function handle(Request $request, Closure $next): Response
    {
        $response = $next($request);

        // Политика безопасности содержимого
        $response->headers->set('Content-Security-Policy', implode('; ', [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'",
            "style-src 'self' 'unsafe-inline'",
            "img-src 'self' data:",
            "connect-src 'self'",
            "font-src 'self'",
            "object-src 'none'",
            "media-src 'self'",
            "frame-ancestors 'none'"
        ]));

        // Защита от clickjacking
        $response->headers->set('X-Frame-Options', 'DENY');

        // Предотвращение MIME-type sniffing
        $response->headers->set('X-Content-Type-Options', 'nosniff');

        // Защита от XSS
        $response->headers->set('X-XSS-Protection', '1; mode=block');

        // Политика referrer
        $response->headers->set('Referrer-Policy', 'strict-origin-when-cross-origin');

        // Политика безопасности транспорта
        $response->headers->set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');

        // Политика приватности
        $response->headers->set('Permissions-Policy', implode(', ', [
            'geolocation=(self)',
            'camera=(self)',
            'microphone=(self)',
            'payment=(self)'
        ]));

        return $response;
    }
}
