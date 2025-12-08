<?php

namespace App\Services;

use App\Models\Equipment;
use App\Models\Sensor;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Log;

class EquipmentMonitoringService
{
    public function getEquipmentStatus($equipmentId)
    {
        return Cache::remember("equipment_status_{$equipmentId}", 300, function () use ($equipmentId) {
            $equipment = Equipment::findOrFail($equipmentId);
            $sensors = $equipment->sensors;

            $status = [
                'overall_health' => $this->calculateOverallHealth($sensors),
                'critical_sensors' => $this->findCriticalSensors($sensors),
                'last_maintenance' => $equipment->maintenanceRequests()->latest()->first()
            ];

            Log::info("Equipment status check", [
                'equipment_id' => $equipmentId,
                'overall_health' => $status['overall_health']
            ]);

            return $status;
        });
    }

    private function calculateOverallHealth($sensors)
    {
        if ($sensors->isEmpty()) return 'unknown';

        $criticalCount = $sensors->filter(function ($sensor) {
            return $this->isSensorCritical($sensor);
        })->count();

        $healthPercentage = 100 - ($criticalCount / $sensors->count() * 100);
        
        return match(true) {
            $healthPercentage >= 90 => 'excellent',
            $healthPercentage >= 70 => 'good',
            $healthPercentage >= 50 => 'warning',
            default => 'critical'
        };
    }

    private function findCriticalSensors($sensors)
    {
        return $sensors->filter(function ($sensor) {
            return $this->isSensorCritical($sensor);
        })->map(function ($sensor) {
            return [
                'id' => $sensor->id,
                'type' => $sensor->type,
                'value' => $sensor->value,
                'unit' => $sensor->unit
            ];
        })->values();
    }

    private function isSensorCritical($sensor)
    {
        return match($sensor->type) {
            'temperature' => $sensor->value < -10 || $sensor->value > 100,
            'pressure' => $sensor->value < 800 || $sensor->value > 1200,
            'humidity' => $sensor->value < 10 || $sensor->value > 90,
            default => false
        };
    }

    public function predictMaintenanceNeed($equipmentId)
    {
        $status = $this->getEquipmentStatus($equipmentId);
        
        if ($status['overall_health'] === 'critical') {
            Log::warning("Maintenance recommended", [
                'equipment_id' => $equipmentId,
                'critical_sensors' => $status['critical_sensors']
            ]);
            
            return true;
        }

        return false;
    }
}
