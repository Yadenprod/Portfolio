<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddTelegramFieldsToUsersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('users', function (Blueprint $table) {
            $table->string('name')->nullable()->after('id');
            $table->string('email')->nullable()->after('name');
            $table->string('password')->nullable()->after('email');
            $table->string('username')->nullable()->after('password');
            $table->string('telegram_id')->nullable()->after('username');
            $table->decimal('balance', 10, 2)->default(0)->after('telegram_id');
            $table->string('referral_code')->nullable()->after('balance');
            $table->unsignedBigInteger('referred_by')->nullable()->after('referral_code');
            
            $table->index('telegram_id');
            $table->index('referral_code');
            $table->foreign('referred_by')->references('id')->on('users')->onDelete('set null');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('users', function (Blueprint $table) {
            $table->dropForeign(['referred_by']);
            $table->dropIndex(['telegram_id']);
            $table->dropIndex(['referral_code']);
            $table->dropColumn([
                'name', 'email', 'password', 'username', 'telegram_id',
                'balance', 'referral_code', 'referred_by'
            ]);
        });
    }
}
