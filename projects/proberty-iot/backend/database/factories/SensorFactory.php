<?php
namespace Database\Factories;
use Illuminate\Database\Eloquent\Factories\Factory;
class SensorFactory extends Factory
{
    protected $model = \App\Models\Sensor::class;
    public function definition()
    {
        return [
            'type' => $this->faker->randomElement(['temperature', 'pressure', 'humidity']),
            'status' => $this->faker->randomElement(['active', 'inactive', 'error']),
            'value' => $this->faker->randomFloat(2, 0, 100),
            'unit' => $this->faker->randomElement(['°C', 'hPa', '%']),
        ];
    }
}
