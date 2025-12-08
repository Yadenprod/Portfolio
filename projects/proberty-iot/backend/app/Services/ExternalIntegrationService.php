<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use App\Models\Equipment;
use App\Models\Sensor;

class ExternalIntegrationService
{
    // Интеграция с ERP системой
    public function syncEquipmentWithERP()
    {
        try {
            $erpEndpoint = config('services.erp.endpoint');
            $apiKey = config('services.erp.api_key');

            $equipments = Equipment::all();
            $syncData = $equipments->map(function($equipment) {
                return [
                    'id' => $equipment->id,
                    'name' => $equipment->name,
                    'location' => $equipment->location,
                    'status' => $this->getEquipmentStatus($equipment)
                ];
            });

            $response = Http::withHeaders([
                'Authorization' => "Bearer {$apiKey}",
                'Content-Type' => 'application/json'
            ])->post($erpEndpoint . '/equipment/sync', $syncData->toArray());

            if ($response->successful()) {
                Log::info('ERP Sync Successful', [
                    'synced_equipment_count' => $syncData->count()
                ]);
                return true;
            }

            Log::error('ERP Sync Failed', [
                'response' => $response->body()
            ]);
            return false;

        } catch (\Exception $e) {
            Log::error('ERP Integration Error', [
                'message' => $e->getMessage()
            ]);
            return false;
        }
    }

    // Интеграция с ModBus протоколом
    public function readModBusSensors($equipmentId)
    {
        try {
            $equipment = Equipment::findOrFail($equipmentId);
            $modbusConfig = config('services.modbus');

            $client = new \ModbusTcpClient\Client(
                $modbusConfig['host'], 
                $modbusConfig['port']
            );

            $temperatureRegister = $client->readHoldingRegisters(
                $equipment->modbus_address, 
                0, 
                2  // Чтение 2 регистров для температуры
            );

            $pressureRegister = $client->readHoldingRegisters(
                $equipment->modbus_address, 
                2, 
                2  // Чтение 2 регистров для давления
            );

            $temperature = $this->convertModbusValue($temperatureRegister);
            $pressure = $this->convertModbusValue($pressureRegister);

            $this->updateSensorData($equipment, $temperature, $pressure);

            Log::info('ModBus Data Read', [
                'equipment_id' => $equipmentId,
                'temperature' => $temperature,
                'pressure' => $pressure
            ]);

            return true;

        } catch (\Exception $e) {
            Log::error('ModBus Integration Error', [
                'equipment_id' => $equipmentId,
                'message' => $e->getMessage()
            ]);
            return false;
        }
    }

    private function getEquipmentStatus(Equipment $equipment)
    {
        $sensors = $equipment->sensors;
        $criticalSensors = $sensors->filter(function($sensor) {
            return $sensor->value > 90 || $sensor->value < 10;
        });

        return $criticalSensors->count() > 0 ? 'critical' : 'normal';
    }

    private function convertModbusValue($registerData)
    {
        // Преобразование значений ModBus в физические величины
        // Реализация зависит от конкретного оборудования
        return $registerData / 10.0;
    }

    private function updateSensorData(Equipment $equipment, $temperature, $pressure)
    {
        Sensor::updateOrCreate([
            'equipment_id' => $equipment->id,
            'type' => 'temperature'
        ], [
            'value' => $temperature,
            'unit' => '°C'
        ]);

        Sensor::updateOrCreate([
            'equipment_id' => $equipment->id,
            'type' => 'pressure'
        ], [
            'value' => $pressure,
            'unit' => 'hPa'
        ]);
    }
}
