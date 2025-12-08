<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class ExternalApiController extends Controller
{
    // Эмуляция данных с датчика (рандомные значения)
    public function simulateSensor()
    {
        $types = ['temperature', 'pressure', 'humidity'];
        $type = $types[array_rand($types)];
        $value = match($type) {
            'temperature' => rand(-20, 120) + rand(0, 99)/100,
            'pressure' => rand(900, 1100) + rand(0, 99)/100,
            'humidity' => rand(0, 100) + rand(0, 99)/100,
        };
        $unit = match($type) {
            'temperature' => '°C',
            'pressure' => 'hPa',
            'humidity' => '%',
        };
        return response()->json([
            'type' => $type,
            'value' => $value,
            'unit' => $unit,
            'timestamp' => now(),
        ]);
    }

    // Получение прогноза погоды через публичный API (например, open-meteo.com)
    public function weather()
    {
        $lat = request('lat', '55.3552'); // Кемерово по умолчанию
        $lon = request('lon', '86.0878');
        $response = Http::get("https://api.open-meteo.com/v1/forecast", [
            'latitude' => $lat,
            'longitude' => $lon,
            'current_weather' => true,
        ]);
        if ($response->successful()) {
            return response()->json($response->json());
        }
        return response()->json(['error' => 'Weather API unavailable'], 503);
    }
}
