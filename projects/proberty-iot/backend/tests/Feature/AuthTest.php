<?php

namespace Tests\Feature;

use App\Models\User;
use App\Models\Role;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    protected function setUp(): void
    {
        parent::setUp();
        $this->seed(); // Применяем сидеры для создания ролей
    }

    public function test_user_can_register()
    {
        $role = Role::where('name', 'оператор')->first();
        $userData = [
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
            'role_id' => $role->id
        ];

        $response = $this->postJson('/api/register', $userData);
        $response->assertStatus(201);
        $response->assertJsonStructure(['user', 'token']);
        $this->assertDatabaseHas('users', ['email' => 'test@example.com']);
    }

    public function test_user_can_login()
    {
        $role = Role::where('name', 'оператор')->first();
        $user = User::factory()->create([
            'role_id' => $role->id,
            'password' => bcrypt('password123')
        ]);

        $response = $this->postJson('/api/login', [
            'email' => $user->email,
            'password' => 'password123'
        ]);

        $response->assertStatus(200);
        $response->assertJsonStructure(['token']);
    }

    public function test_user_role_access_control()
    {
        $adminRole = Role::where('name', 'админ')->first();
        $operatorRole = Role::where('name', 'оператор')->first();

        $admin = User::factory()->create(['role_id' => $adminRole->id]);
        $operator = User::factory()->create(['role_id' => $operatorRole->id]);

        // Тест доступа администратора к ресурсам ролей
        $this->actingAs($admin);
        $this->getJson('/api/roles')->assertStatus(200);

        // Тест запрета доступа оператора к ресурсам ролей
        $this->actingAs($operator);
        $this->getJson('/api/roles')->assertStatus(403);
    }

    public function test_user_logout()
    {
        $role = Role::where('name', 'оператор')->first();
        $user = User::factory()->create(['role_id' => $role->id]);

        $token = $user->createToken('test-token');
        $this->actingAs($user);

        $response = $this->postJson('/api/logout');

        $response->assertStatus(200);
        $response->assertJson(['message' => 'Successfully logged out']);

        // Проверяем, что токен больше не действителен
        $this->assertDatabaseMissing('personal_access_tokens', [
            'id' => $token->accessToken->id
        ]);
    }
}
