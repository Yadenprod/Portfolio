<?php

namespace Database\Seeders;

use App\Models\User;
use App\Models\Role;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $adminRole = Role::firstOrCreate(['name' => 'админ']);
        $engineerRole = Role::firstOrCreate(['name' => 'инженер']);
        $operatorRole = Role::firstOrCreate(['name' => 'оператор']);

        User::factory()->create([
            'name' => 'Admin',
            'email' => 'admin@example.com',
            'password' => Hash::make('password'),
            'role_id' => $adminRole->id,
        ]);

        \App\Models\User::factory(10)->create();
        \App\Models\Equipment::factory()->count(10)->create()->each(function ($equipment) {
            \App\Models\Sensor::factory()->count(3)->create([
                'equipment_id' => $equipment->id,
            ]);
        });
        \App\Models\MaintenanceRequest::factory()->count(10)->create();
    }
}
