<?php

namespace App\Http\Controllers\Admin;

use App\Models\Setting;
use App\Models\User;
use App\Models\Withdraw;
use App\Models\Payment;
use App\Models\Promocode;
use App\Models\PromocodeActivation;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use DB;
use Yajra\DataTables\DataTables;

class AdminController extends Controller
{
    public function versionUpdate() {
        Setting::where('id', 1)->update([
            'file_version' => time()
        ]);
        return response()->json(['success' => true, 'msg' => 'Версия обновлена!']);
    }

    public function load(Request $request)
    {
        switch($request->type) {

            case 'users':
                return datatables(User::query())->toJson();
            break;

            case 'bots':
                return datatables(User::query()->where('is_bot', '=', 1))->toJson();
            break;

            case 'promocodes':
                $promocodes = Promocode::where('name', '!=', '')
                    ->leftJoin('promocode_activations', function ($join) {
                        $join->on('promocodes.id', '=', 'promocode_activations.promo_id');
                    })
                    ->select('promocodes.*', DB::raw('count(promocode_activations.id) as activated'))
                    ->groupBy('promocodes.id');

                return Datatables::of($promocodes)->make(true);
            break;
            
            case 'bonus':
                return datatables(BonusLevel::all())->toJson();
            break;

            case 'withdraws':
                $withdraws = Withdraw::where('status', $request->status)
                    ->join('users', 'users.id', '=', 'withdraws.user_id')
                    ->select('users.id as user_id', 'users.username as username', 'withdraws.*')
                    ->get();

                return Datatables::of($withdraws)->make(true);
            break;

            case 'deposits':
                $deposits = Payment::where('status', 1)
                    ->join('users', 'users.id', '=', 'payments.user_id')
                    ->select('users.id as user_id', 'users.username as username', 'payments.*')
                    ->get();

                return Datatables::of($deposits)->make(true);
            break;
        }
    }
}
