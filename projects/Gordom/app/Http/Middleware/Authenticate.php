<?php

namespace App\Http\Middleware;
use Illuminate\Http\RedirectResponse;

use Closure;
use Auth;
use Cache;

class Authenticate
{
    /**
     * Handle an incoming request.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \Closure  $next
     * @return mixed
     */
    public function handle($request, Closure $next)
    {
        if($request->isMethod('post')) {
            if(Auth::guest()) {
                return response()->json([
                    'error' => true,
                    'message' => 'Вы не авторизованы'
                ]);
            }

            if(Auth::user()->ban && !$request->is(['*/init', '*/get', 'admin/*'])) {
                return response()->json([
                    'error' => true,
                    'message' => 'Ваш аккаунт заблокирован'
                ]);
            }
        }

        if(Auth::guest()) {
            return new RedirectResponse(url('/'));
        }

        return $next($request);
    }
}
