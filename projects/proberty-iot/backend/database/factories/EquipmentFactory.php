<?php
namespace Database\Factories;
use Illuminate\Database\Eloquent\Factories\Factory;
class EquipmentFactory extends Factory
{
    protected $model = \App\Models\Equipment::class;
    public function definition()
    {
        return [
            'name' => $this->faker->company . ' ' . $this->faker->word,
            'location' => $this->faker->city,
            'status' => $this->faker->randomElement(['working', 'attention', 'critical'])
        ];
    }
}
