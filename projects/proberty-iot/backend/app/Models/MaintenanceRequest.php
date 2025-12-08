<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class MaintenanceRequest extends Model
{
    use HasFactory;

    protected $fillable = [
        'equipment_id',
        'user_id',
        'description',
        'status',
        'assigned_to',
        'closed_at',
    ];

    public function equipment()
    {
        return $this->belongsTo(Equipment::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function assignedEngineer()
    {
        return $this->belongsTo(User::class, 'assigned_to');
    }
}
