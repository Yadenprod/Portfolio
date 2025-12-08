<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\MinesController;
use App\Http\Controllers\DiceController;
use App\Http\Controllers\WheelController;
use App\Http\Controllers\SlotsController;
use App\Http\Controllers\ChatController;
use App\Http\Controllers\PromoController;
use App\Http\Controllers\BonusController;
use App\Http\Controllers\ReferralController;
use App\Http\Controllers\PaymentController;
use App\Http\Controllers\WithdrawController;
use App\Http\Controllers\FakeController;

use App\Http\Controllers\Admin\AdminController;
use App\Http\Controllers\Admin\AntiminusController;
use App\Http\Controllers\Admin\BotsController;
use App\Http\Controllers\Admin\DepositsController;
use App\Http\Controllers\Admin\IndexController;
use App\Http\Controllers\Admin\PromocodeController;
use App\Http\Controllers\Admin\SettingsController;
use App\Http\Controllers\Admin\UsersController;
use App\Http\Controllers\Admin\WithdrawsController;


Route::get('/r/{unique_id}', [ReferralController::class, 'setReferral']);

Route::group(['prefix' => 'slots'], function() {
    //Route::get('/parse', [SlotsController::class, 'parse']);
    Route::post('/init', [SlotsController::class, 'init']);
    Route::post('/loadGame', [SlotsController::class, 'loadGame']);
    Route::post('/callback', [SlotsController::class, 'callback']);
});

Route::group(['prefix' => 'user'], function() {
    Route::post('/init', [UserController::class, 'init']);
    Route::post('/updateBalance', [UserController::class, 'updateBalance']);
    Route::get('/logout', [UserController::class, 'logout']);
});

Route::group(['prefix' => 'withdraw', 'middleware' => 'auth'], function () {
    Route::post('/create', [WithdrawController::class, 'create']);
    Route::post('/decline', [WithdrawController::class, 'decline']);
    Route::post('/init', [WithdrawController::class, 'init']);
});

Route::group(['prefix' => 'payment', 'middleware' => 'auth'], function () {
    Route::post('/create', [PaymentController::class, 'create']);
    Route::post('/init', [PaymentController::class, 'init']);
});

Route::group(['prefix' => 'referral', 'middleware' => 'auth'], function () {
    Route::post('/get', [ReferralController::class, 'init']);
});

Route::group(['prefix' => 'promo', 'middleware' => 'auth'], function () {
    Route::post('/activate', [PromoController::class, 'activate']);
});

Route::group(['prefix' => 'bonus', 'middleware' => 'auth'], function () {
    Route::post('/take', [BonusController::class, 'take']);
});

Route::group(['prefix' => 'chat'], function() {
    Route::post('/init', [ChatController::class, 'init']);

    Route::group(['middleware' => 'auth'], function() {
        Route::post('/send', [ChatController::class, 'send']);
        Route::post('/delete', [ChatController::class, 'delete']);
        Route::post('/ban', [ChatController::class, 'mute']);
    });
});

Route::group(['prefix' => 'dice', 'middleware' => 'auth'], function() {
	Route::post('/bet', [DiceController::class, 'bet']);
});

Route::group(['prefix' => 'wheel'], function() {
	Route::post('/init', [WheelController::class, 'init']);
	Route::post('/bet', [WheelController::class, 'bet'])->middleware('auth');
});

Route::group(['prefix' => 'mines', 'middleware' => 'auth'], function() {
    Route::post('/init', [MinesController::class, 'init']);
    Route::post('/start', [MinesController::class, 'createGame']);
    Route::post('/open', [MinesController::class, 'openPath']);
    Route::post('/take', [MinesController::class, 'take']);
});

Route::group(['prefix' => 'auth/vkontakte'], function() {
    Route::get('/', [AuthController::class, 'redirect']);
    Route::get('/handle', [AuthController::class, 'handle']);
});

Route::group(['prefix' => 'admin', 'namespace' => 'Admin', 'middleware' => 'auth'], function () {
    Route::group(['middleware' => 'access:admin'], function () {
        Route::post('/load', [AdminController::class, 'load']);
        Route::get('/', [IndexController::class, 'index'])->name('admin.index');
        Route::get('/users', [UsersController::class, 'index'])->name('admin.users');
        Route::get('/bots', [BotsController::class, 'index'])->name('admin.bots');
        Route::post('/versionUpdate', [AdminController::class, 'versionUpdate']);
        Route::post('/getUserByMonth', [IndexController::class, 'getUserByMonth']);
        Route::post('/getDepsByMonth', [IndexController::class, 'getDepsByMonth']);

        Route::group(['prefix' => 'promocodes'], function () {
            Route::get('/', [PromocodeController::class, 'index'])->name('admin.promocodes');
            Route::get('/create', [PromocodeController::class, 'create'])->name('admin.promocodes.create');
            Route::post('/create', [PromocodeController::class, 'createPost']);
            Route::get('/delete/{id}', [PromocodeController::class, 'delete'])->name('admin.promocodes.delete');
        });

        Route::group(['prefix' => 'users'], function () {
            Route::get('/edit/{id}', [UsersController::class, 'edit'])->name('admin.users.edit');
            Route::post('/edit/{id}', [UsersController::class, 'editPost']);
            Route::get('/delete/{id}', [UsersController::class, 'delete'])->name('admin.users.delete');
            Route::post('/checker', [UsersController::class, 'checker']);
        });

        Route::group(['prefix' => 'bots'], function () {
            Route::get('/create', [BotsController::class, 'create'])->name('admin.bots.create');
            Route::post('/create', [BotsController::class, 'createPost']);
            Route::get('/edit/{id}', [BotsController::class, 'edit'])->name('admin.bots.edit');
            Route::post('/edit/{id}', [BotsController::class, 'editPost']);
            Route::get('/delete/{id}', [BotsController::class, 'delete'])->name('admin.bots.delete');
        });

        Route::group(['prefix' => 'settings'], function () {
            Route::get('/', [SettingsController::class, 'index'])->name('admin.settings');
            Route::post('/', [SettingsController::class, 'save']);
        });

        Route::group(['prefix' => 'antiminus'], function () {
            Route::get('/', [AntiminusController::class, 'index'])->name('admin.antiminus');
            Route::post('/', [AntiminusController::class, 'save']);
        });

        Route::group(['prefix' => 'withdraws'], function () {
            Route::get('/', [WithdrawsController::class, 'index'])->name('admin.withdraws');
            Route::post('/get', [WithdrawsController::class, 'getById']);
            Route::post('/send', [WithdrawsController::class, 'send']);
            Route::post('/decline', [WithdrawsController::class, 'decline']);
        });

        Route::group(['prefix' => 'deposits'], function () {
            Route::get('/', [DepositsController::class, 'index'])->name('admin.deposits');
        });

        Route::post('/getMerchant', [IndexController::class, 'getMerchant']);
    });
});

Route::group(['prefix' => 'api', 'middleware' => 'serverAccess'], function() {
    Route::post('/getTimer', function() {
        return \App\Models\Setting::query()->find(1)->bot_timer;
    });
    Route::post('/fake', [FakeController::class, 'fake']);

	Route::group(['prefix' => 'wheel'], function () {
		Route::any('/slider', [WheelController::class, 'getSlider']);
		Route::any('/create', [WheelController::class, 'createGame']);
		Route::any('/getStatus', [WheelController::class, 'getStatus']);
	});
});

Route::get('/{any}', function () {
    return view('app');
})->where('any', '.*');
