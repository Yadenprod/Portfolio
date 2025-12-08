<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\EquipmentController;
use App\Http\Controllers\SensorController;
use App\Http\Controllers\MaintenanceRequestController;
use App\Http\Controllers\RoleController;
use App\Http\Controllers\ExternalApiController;
use App\Http\Controllers\AuthController;

Route::middleware(['auth:sanctum', 'ensureuserrole:админ,инженер,оператор'])->group(function () {
    Route::apiResources([
        'equipment' => EquipmentController::class,
        'sensors' => SensorController::class,
        'maintenance-requests' => MaintenanceRequestController::class,
    ]);
});

Route::middleware(['auth:sanctum', 'ensureuserrole:админ'])->apiResource('roles', RoleController::class);

Route::post('register', [AuthController::class, 'register']);
Route::post('login', [AuthController::class, 'login']);
Route::middleware('auth:sanctum')->post('logout', [AuthController::class, 'logout']);
Route::middleware('auth:sanctum')->get('me', [AuthController::class, 'me']);

Route::get('external/simulate-sensor', [ExternalApiController::class, 'simulateSensor']);
Route::get('external/weather', [ExternalApiController::class, 'weather']);

// DEMO: Публичные GET-роуты для фронта без авторизации
Route::get('equipment', [EquipmentController::class, 'index']);
Route::get('sensors', [SensorController::class, 'index']);
Route::get('maintenance-requests', [MaintenanceRequestController::class, 'index']);