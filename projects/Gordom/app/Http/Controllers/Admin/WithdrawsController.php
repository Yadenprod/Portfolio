<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\Withdraw;
use App\Models\User;
use Illuminate\Http\Request;

class WithdrawsController extends Controller
{
    public function index()
    {
        return view('admin.withdraws.index');
    }

    public function decline(Request $request)
    {
        $withdraw = Withdraw::query()->find($request->id);

        if(!$withdraw) {
            return [
                'error' => 'Выплата отменена пользователем'
            ];
        }

        if($withdraw->status > 0) {
            return [
                'error' => 'Статус выплаты уже изменен ранее'
            ];
        }

        if($request->status == 2) {

            if($request->returnBalance == 1) {
                $user = User::where('id', $withdraw->user_id)->lockForUpdate()->first();
                $user->balance += $withdraw->sum;
                $user->save();
            }

            $withdraw->update([
                'status' => $request->status,
                'reason' => $request->reason
            ]);
        }
    }

    public function send(Request $request)
    {
        $id = $request->id;
        $status = $request->status;

        $withdraw = Withdraw::where('id', $id)->lockForUpdate()->first();

        if(!$withdraw) {
            return [
                'error' => true,
                'message' => 'Выплата отменена пользователем',
                'reload' => true
            ];
        }

        if($withdraw->status > 0) {
            return [
                'error' => true,
                'message' => 'Статус выплаты уже изменен ранее',
                'reload' => true
            ];
        }

        $currency = 0;

        switch($withdraw->system) {
            case 'fk':
                $currency = 133;
            break;
            case 'qiwi':
                $currency = 63;
            break;
            case 'card':
                $currency = 94;
            break;
        }
    
        $data = [
            'wallet_id' => $this->config->wallet_id,
            'order_id'  => $withdraw->id,
            'purse'     => $withdraw->wallet,
            'amount'    => $withdraw->sumWithCom,
            'desc'      => $this->config->wallet_desc,
            'currency'  => $currency,
            'sign'      => md5($this->config->wallet_id.$currency.$withdraw->sumWithCom.$withdraw->wallet.$this->config->wallet_secret),
            'action'    => 'cashout',
        ];
    
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, 'https://fkwallet.com/api_v1.php');
        curl_setopt($ch, CURLOPT_HEADER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
        curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 0);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
        curl_setopt($ch, CURLOPT_POST, 1);
        curl_setopt($ch, CURLOPT_TIMEOUT, 10);
        curl_setopt($ch, CURLOPT_CONNECTTIMEOUT, 10);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        $result = trim(curl_exec($ch));
        $c_errors = curl_error($ch);
        curl_close($ch);
    
        $data = json_decode($result, true);
    
        if($data['status'] == 'error') {
            return [
                'error' => true,
                'message' => $data['desc']
            ];
        }

        $withdraw->update([
            'status' => ($withdraw->system !== 'fk') ? 3 : 1,
        ]);

        return [
            'message' => 'Выплата отправлена',
            'status' => $withdraw->status
        ];
    }

    public function getById(Request $request)
    {
        $withdraw = Withdraw::where('withdraws.id', $request->id)
            ->join('users', 'users.id', '=', 'withdraws.user_id')
            ->select('users.username as username', 'withdraws.*')
            ->first();
        return $withdraw;
    }
}
