<?php

namespace App\Http\Controllers;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

use App\Models\Payment;
use App\Models\User;
use App\Models\Setting;
use App\Models\ReferralProfit;
use App\Models\Promocode;
use App\Models\PromocodeActivation;
use DB;

class PaymentController extends Controller
{
    public function init()
    {
        $data = Payment::where('user_id', $this->user->id)
            ->where('status', 1)
            ->orderBy('id', 'desc')
            ->limit(15)
            ->get();
        return ['payments' => $data];
    }

    public function create(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'amount' => 'required|numeric',
        ]);

        if($validator->fails()) {
            return [
                'error' => true,
                'message' => $validator->errors()->first()
            ];
        }

        switch($request->system) {
            case 'Freekassa':
                $payment = (object) $this->createOrder($request);

                if($payment->error) {
                    return [
                        'error' => true,
                        'message' => $payment->message
                    ];
                }

                $sign = md5($this->config->kassa_id.':'.$payment->sum.':'.$this->config->kassa_secret1.':RUB:'.$payment->id);
        
                $data = [
                    'm'        => $this->config->kassa_id,
                    'oa'       => $payment->sum,
                    'o'        => $payment->id,
                    'currency' => 'RUB',
                    's'        => $sign
                ];
        
                $url = "https://pay.freekassa.ru/?".http_build_query($data);
            break;
            case 'qiwi':
                $payment = (object) $this->createOrder($request);

                if($payment->error) {
                    return [
                        'error' => true,
                        'message' => $payment->message
                    ];
                }

                $bot_id = $this->config->vlito_id;
                $pay_id = $payment->id;
                $amount = $payment->sum;
                $secret_key = $this->config->vlito_secret;
            
                $arr_sign = array(
                    $bot_id,
                    $pay_id,
                    $amount,
                    $secret_key
                );
            
                $sign = hash('sha256', implode(':', $arr_sign));
        
                $data = [
                    'bot_id' => $bot_id,
                    'amount' => $amount,
                    'pay_id' => $pay_id,
                    'sign' => $sign,
                    'method' => 'qiwi',
                ];
        
                $response = $this->getParams('https://vlito.ru/paying/?' . http_build_query($data), ['pay']);

                if(!isset($response['pay'])) {
                    return [
                        'error' => true,
                        'message' => 'Проверьте настройки Vlito'
                    ];
                }

                $data = [
                    'pay' => $response['pay'],
                    'success_url' => urlencode('https://' . $_SERVER['HTTP_HOST']),
                    'price' => $amount,
                    'method' => 'qiwi'
                ];

                $url = 'https://vlito.ru/paying/?' . http_build_query($data);
            break;
            default:
                return [
                    'error' => true,
                    'message' => 'Выберите способ оплаты'
                ];
            break;
        }

        return [
            'url' => $url
        ];
    }

    public function handleVlito(Request $request)
    {
        if(!in_array($this->getIp(), ['185.178.44.168', '92.63.102.210'])) {
            return 'wrong ip';
        }

        $payment = Payment::query()->find($request->pay_id);

        if(!$payment) {
            return 'payment not found';
        }

        if($payment->status) {
            return 'payment already paid';
        }

        if($payment->sum > $request->amount) {
            return 'wrong sum';
        }

        $incrementSum = $payment->bonus != 0
            ? $payment->sum + (($payment->sum * $payment->bonus) / 100)
            : $payment->sum;

        $user = User::find($payment->user_id);
        $user->increment('balance', $incrementSum);
        $user->increment('wager', $incrementSum * 2);
    
        if(!is_null($user->referral_use)) {
            $this->setReferralProfit($user->id, $payment->sum);
        }

        $payment->status = 1;
        $payment->method = 'Vlito';
        $payment->save();

        Transaction::create([
            'user_id' => $this->user->id,
            'action'  => 'Пополнение счета',
            'amount'  => $incrementSum,
            'type'    => 'up'
        ]);

        return 'YES'; 
    }

    public function handle(Request $request)
    {
        $sign = md5($this->config->kassa_id.':'.$request->AMOUNT.':'.$this->config->kassa_secret2.':'.$request->MERCHANT_ORDER_ID);
        if ($sign != $request->SIGN) return 'wrong sign';

        $payment = Payment::find($request->MERCHANT_ORDER_ID);

        if(!$payment) {
            return 'payment not found';
        }

        if($payment->status) {
            return 'payment already paid';
        }

        $incrementSum = $payment->bonus != 0
            ? $payment->sum + (($payment->sum * $payment->bonus) / 100)
            : $payment->sum;

        $user = User::find($payment->user_id);
        $user->increment('balance', $incrementSum);
        $user->increment('wager', $incrementSum * 2);
    
        if(!is_null($user->referral_use)) {
            $this->setReferralProfit($user->id, $payment->sum);
        }

        $payment->status = 1;
        $payment->method = 'FK';
        $payment->save();

        Transaction::create([
            'user_id' => $this->user->id,
            'action'  => 'Пополнение счета',
            'amount'  => $incrementSum,
            'type'    => 'up'
        ]);

        return 'YES';
    }

    private function createOrder($request, $bonus = 0)
    {
        if($request->amount < $this->config->min_payment_sum) {
            return [
                'error' => true,
                'message' => 'Минимальная сумма пополнения ' . $this->config->min_payment_sum . ' руб'
            ];
        }
        
        $code = $request->code;

        if(isset($code)) {
            $promo = Promocode::where('name', $code)->lockForUpdate()->first();

            if (!$promo) {
                return [
                    'error' => true,
                    'message' => 'Промокод не найден'
                ];
            }
    
            if($promo->type != 'deposit') {
                return [
                    'error' => true,
                    'message' => 'Этот промокод нужно активировать во вкладке "Бонусы"'
                ];
            }

            if($request->amount > 1000) {
                return [
                    'error' => true,
                    'message' => 'Максимальная сумма пополнения при использовании промокода - 1000р'
                ];
            }
    
            $allUsed = PromocodeActivation::where('promo_id', $promo->id)->count('id');
    
            if ($allUsed >= $promo->activation) {
                return [
                    'error' => true,
                    'message' => 'Промокод закончился'
                ];
            }
    
            $used = PromocodeActivation::where([['promo_id', $promo->id], ['user_id', $this->user->id]])->first();
    
            if ($used) {
                return [
                    'error' => true,
                    'message' => 'Вы уже использовали этот код'
                ];
            }

            PromocodeActivation::create([
                'promo_id' => $promo->id,
                'user_id' => $this->user->id
            ]);

            $bonus += $promo->sum;
        }

        $payment = Payment::create([
            'user_id' => $this->user->id,
            'sum' => $request->amount,
            'bonus' => $bonus
        ]);

        return $payment;
    }

    private function setReferralProfit($user_id, $amount)
    {
        $user = User::find($user_id);
        $amount = $amount / 100;
        
        DB::beginTransaction();
    
        @$referral_1_lvl = User::find($user->referral_use);

        if(!is_null($referral_1_lvl)) {
            $percent = 10;

            if($referral_1_lvl->ref_1_lvl > 0) {
                $percent = $referral_1_lvl->ref_1_lvl;
            }

            $referral_1_lvl->increment('referral_balance', $amount * $percent);

            ReferralProfit::create([
                'from_id' => $user->id,
                'ref_id' => $referral_1_lvl->id,
                'amount' => $amount * $percent,
                'level' => 1
            ]);
        }

        DB::commit();

        return true;
    }

    private function getParams($url, $params = []): array
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        
        $html = curl_exec($ch);
        curl_close($ch);
        
        @$DOM = new \DOMDocument;
        @$DOM->loadHTML($html);

        $inputs = $DOM->getElementsByTagName('input');
        $response = [];

        foreach($inputs as $input)
        {
            $name = $input->getAttribute('name');

            if(in_array($name, $params) && !isset($response[$name])) 
            {
                $response[$name] = $input->getAttribute('value');
            }
        }

        return $response;
    }
}