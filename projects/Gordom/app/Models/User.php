<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsToMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class User extends Authenticatable
{
    protected $guarded = [];

    protected $fillable = [
        'name',
        'email',
        'password',
        'username',
        'telegram_id',
        'balance',
        'referral_code',
        'referred_by',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'balance' => 'decimal:2',
    ];

    public function transactions(): HasMany
    {
        return $this->hasMany(Transaction::class);
    }

    public function gameHistory(): HasMany
    {
        return $this->hasMany(GameHistory::class);
    }

    public function usedPromoCodes(): BelongsToMany
    {
        return $this->belongsToMany(PromoCode::class, 'user_promo_codes', 'user_id', 'promo_code_id')
            ->withTimestamps();
    }

    public function referrer(): BelongsTo
    {
        return $this->belongsTo(User::class, 'referred_by');
    }

    public function referrals(): HasMany
    {
        return $this->hasMany(User::class, 'referred_by');
    }
}
