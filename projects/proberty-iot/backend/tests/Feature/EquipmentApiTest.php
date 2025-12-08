<?php

namespace Tests\Feature;

use Tests\TestCase;
use App\Models\Equipment;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

class EquipmentApiTest extends TestCase
{
    use RefreshDatabase;

    public function test_equipment_route_access()
    {
        $this->seed();
        $user = User::where('email', 'admin@example.com')->first();
        $this->actingAs($user, 'sanctum');
        $response = $this->getJson('/api/equipment');
        $response->dump();
        $response->assertStatus(200);
    }

    public function test_equipment_crud()
    {
        $this->seed();
        $user = User::where('email', 'admin@example.com')->first();
        $this->actingAs($user, 'sanctum');

        // Create
        $response = $this->postJson('/api/equipment', [
            'name' => 'Test Equipment',
            'location' => 'Test Location',
            'description' => 'Test Desc',
        ]);
        $response->assertStatus(201);
        $id = $response->json('id');

        // Read
        $response = $this->getJson('/api/equipment/' . $id);
        $response->assertStatus(200)->assertJson(['name' => 'Test Equipment']);

        // Update
        $response = $this->putJson('/api/equipment/' . $id, [
            'name' => 'Updated Equipment',
        ]);
        $response->assertStatus(200)->assertJson(['name' => 'Updated Equipment']);

        // Delete
        $response = $this->deleteJson('/api/equipment/' . $id);
        $response->assertStatus(204);
    }
}
