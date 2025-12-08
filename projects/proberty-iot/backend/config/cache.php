<?php

use Illuminate\Support\Str;

return [
    'default' => env('CACHE_DRIVER', 'redis'),
    'stores' => [
        'redis' => [
            'driver' => 'redis',
            'connection' => 'cache',
        ],
        'database' => [
            'driver' => 'database',
            'table' => 'cache',
            'connection' => null,
        ],
    ],
    'prefix' => env('CACHE_PREFIX', 'iiot_dashboard'),
    'model_cache' => [
        'equipment' => [
            'ttl' => 3600, // 1 час
            'keys' => ['id', 'name', 'location']
        ],
        'sensors' => [
            'ttl' => 300, // 5 минут
            'keys' => ['id', 'type', 'equipment_id']
        ]
    ]
];
