<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TelegramAuthController;
use App\Http\Controllers\WalletController;
use App\Http\Controllers\PromoController;
use App\Http\Controllers\ReferralController;
use App\Http\Controllers\HistoryController;
use App\Http\Controllers\GameController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

// Telegram Web App API routes
Route::prefix('auth')->group(function () {
    Route::post('/telegram/me', [TelegramAuthController::class, 'me']);
});

Route::prefix('wallet')->group(function () {
    Route::post('/deposit', [WalletController::class, 'deposit']);
    Route::post('/withdraw', [WalletController::class, 'withdraw']);
});

Route::prefix('promo')->group(function () {
    Route::post('/activate', [PromoController::class, 'activate']);
});

Route::prefix('referrals')->group(function () {
    Route::get('/stats', [ReferralController::class, 'stats']);
});

Route::get('/history', [HistoryController::class, 'index']);

Route::prefix('games')->group(function () {
    Route::post('/dice/bet', [GameController::class, 'diceBet']);
    Route::post('/wheel/bet', [GameController::class, 'wheelBet']);
    Route::post('/mines/bet', [GameController::class, 'minesBet']);
    Route::post('/slots/bet', [GameController::class, 'slotsBet']);
});
