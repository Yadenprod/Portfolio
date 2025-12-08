<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Factories\HasFactory;

class Sensor extends Model
{
    use HasFactory;

    protected $fillable = [
        'equipment_id',
        'type',
        'value',
        'unit',
        'last_update',
    ];

    public function equipment()
    {
        return $this->belongsTo(Equipment::class);
    }
}
