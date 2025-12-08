<?php
namespace Database\Factories;
use Illuminate\Database\Eloquent\Factories\Factory;
use App\Models\User;
class MaintenanceRequestFactory extends Factory
{
    protected $model = \App\Models\MaintenanceRequest::class;
    public function definition()
    {
        return [
            'equipment_id' => \App\Models\Equipment::factory(),
            'user_id' => User::factory(),
            'status' => $this->faker->randomElement(['pending', 'in_progress', 'completed', 'critical']),
            'description' => $this->faker->sentence,
            'created_at' => $this->faker->dateTimeBetween('-1 month', 'now'),
        ];
    }
}
