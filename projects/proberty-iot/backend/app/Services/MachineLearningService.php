<?php

namespace App\Services;

use App\Models\Equipment;
use App\Models\Sensor;
use Illuminate\Support\Facades\Log;
use Phpml\Classification\KNearestNeighbors;
use Phpml\FeatureExtraction\TokenCountVectorizer;
use Phpml\Tokenization\WhitespaceTokenizer;
use Phpml\ModelManager;

class MachineLearningService
{
    private $modelPath;

    public function __construct()
    {
        $this->modelPath = storage_path('ml_models/equipment_health_predictor.model');
    }

    public function trainMaintenancePredictor()
    {
        // Собираем исторические данные о состоянии оборудования
        $trainingData = $this->collectTrainingData();

        $samples = $trainingData['samples'];
        $labels = $trainingData['labels'];

        $classifier = new KNearestNeighbors();
        $classifier->train($samples, $labels);

        // Сохраняем обученную модель
        $modelManager = new ModelManager();
        $modelManager->saveToFile($classifier, $this->modelPath);

        Log::info('ML Model trained', [
            'samples_count' => count($samples),
            'model_path' => $this->modelPath
        ]);

        return true;
    }

    private function collectTrainingData()
    {
        $equipments = Equipment::with('sensors', 'maintenanceRequests')->get();
        
        $samples = [];
        $labels = [];

        foreach ($equipments as $equipment) {
            $sensors = $equipment->sensors;
            $maintenanceRequests = $equipment->maintenanceRequests;

            // Извлекаем признаки из датчиков
            $sensorFeatures = $sensors->map(function($sensor) {
                return [
                    'type' => $this->encodeSensorType($sensor->type),
                    'value' => $sensor->value,
                    'last_update' => strtotime($sensor->updated_at)
                ];
            })->toArray();

            // Агрегируем признаки
            $sample = array_merge(
                $this->aggregateSensorFeatures($sensorFeatures),
                [
                    'age' => now()->diffInDays($equipment->created_at),
                    'maintenance_frequency' => $maintenanceRequests->count()
                ]
            );

            $samples[] = $sample;
            
            // Метка - требуется ли обслуживание
            $labels[] = $maintenanceRequests->where('status', 'critical')->count() > 0 ? 'need_maintenance' : 'ok';
        }

        return [
            'samples' => $samples,
            'labels' => $labels
        ];
    }

    private function aggregateSensorFeatures($sensorFeatures)
    {
        $aggregated = [
            'temperature_avg' => 0,
            'pressure_avg' => 0,
            'humidity_avg' => 0
        ];

        $counts = [
            'temperature' => 0,
            'pressure' => 0,
            'humidity' => 0
        ];

        foreach ($sensorFeatures as $sensor) {
            switch($sensor['type']) {
                case 1: // temperature
                    $aggregated['temperature_avg'] += $sensor['value'];
                    $counts['temperature']++;
                    break;
                case 2: // pressure
                    $aggregated['pressure_avg'] += $sensor['value'];
                    $counts['pressure']++;
                    break;
                case 3: // humidity
                    $aggregated['humidity_avg'] += $sensor['value'];
                    $counts['humidity']++;
                    break;
            }
        }

        // Усредняем
        foreach ($aggregated as $key => &$value) {
            $type = explode('_', $key)[0];
            $value = $counts[$type] > 0 ? $value / $counts[$type] : 0;
        }

        return $aggregated;
    }

    private function encodeSensorType($type)
    {
        return match($type) {
            'temperature' => 1,
            'pressure' => 2,
            'humidity' => 3,
            default => 0
        };
    }

    public function predictMaintenanceNeed($equipmentId)
    {
        try {
            $equipment = Equipment::findOrFail($equipmentId);
            $sensors = $equipment->sensors;

            // Если модель не обучена, обучаем
            if (!file_exists($this->modelPath)) {
                $this->trainMaintenancePredictor();
            }

            $modelManager = new ModelManager();
            $classifier = $modelManager->restoreFromFile($this->modelPath);

            $sensorFeatures = $sensors->map(function($sensor) {
                return [
                    'type' => $this->encodeSensorType($sensor->type),
                    'value' => $sensor->value,
                    'last_update' => strtotime($sensor->updated_at)
                ];
            })->toArray();

            $sample = array_merge(
                $this->aggregateSensorFeatures($sensorFeatures),
                [
                    'age' => now()->diffInDays($equipment->created_at),
                    'maintenance_frequency' => $equipment->maintenanceRequests->count()
                ]
            );

            $prediction = $classifier->predict($sample);

            Log::info('Maintenance prediction', [
                'equipment_id' => $equipmentId,
                'prediction' => $prediction
            ]);

            return $prediction === 'need_maintenance';

        } catch (\Exception $e) {
            Log::error('ML Prediction Error', [
                'equipment_id' => $equipmentId,
                'error' => $e->getMessage()
            ]);

            return false;
        }
    }
}
