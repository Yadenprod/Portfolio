<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PromoCode extends Model
{
    protected $fillable = [
        'code',
        'reward',
        'is_active',
        'max_uses',
        'used_count',
    ];

    protected $casts = [
        'reward' => 'decimal:2',
        'is_active' => 'boolean',
    ];

    public function users()
    {
        return $this->belongsToMany(User::class, 'user_promo_codes', 'promo_code_id', 'user_id')
            ->withTimestamps();
    }
}
