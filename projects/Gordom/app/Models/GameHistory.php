<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class GameHistory extends Model
{
    protected $fillable = [
        'user_id',
        'game',
        'amount',
        'win',
        'multiplier',
        'result',
        'chance',
    ];

    protected $casts = [
        'amount' => 'decimal:2',
        'multiplier' => 'decimal:2',
        'win' => 'boolean',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
