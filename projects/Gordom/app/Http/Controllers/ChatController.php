<?php

namespace App\Http\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Redis;

use Carbon\Carbon;
use App\Models\User;
use App\Models\Message;
use Auth;
use DB;
use Cache;

class ChatController extends Controller
{
    public function __construct()
    {
        parent::__construct();
        $this->redis = Redis::connection();
    }

    public function init()
    {
        $messages = Message::orderBy('created_at', 'desc')->limit(20)->get();
        return $messages;
    }

    public function send(Request $request)
    {
        $validator = Validator::make($request->all(), [
            'message' => 'required|min:1|max:100',
        ]);

        if($validator->fails()) {
            return [
                'error' => true,
                'message' => $validator->errors()->first()
            ];
        }

        if(Cache::has('message.' . $this->user->id)) {
            return [
                'error' => true,
                'message' => 'Не так часто'
            ];
        }
        
        if($this->user->chat_mute >= time()) {
            return [
                'error' => true,
                'message' => 'Вы заблокированы в чате до ' . date('Y-m-d H:i:s', $this->user->chat_mute) . '<br>Причина: ' . $this->user->chat_mute_reason
            ];
        }

        $data = [
            'user_id' => $this->user->id,
            'avatar' => $this->user->avatar,
            'login' => $this->user->username,
            'text' => $request->message,
            'time' => date('H:i'),
            'role' => $this->getRole()
        ];

        $this->messageSend($data);

        $expiresAt = Carbon::now()->addSeconds(2);
        Cache::put('message.' . $this->user->id, '', $expiresAt);

        return ['message' => 'Сообщение отправлено'];
    }

    private function getRole()
    {
        if($this->user->is_admin) {
            return 'admin';
        }

        if($this->user->is_moderator) {
            return 'moderator';
        }

        if($this->user->is_youtuber) {
            return 'youtuber';
        }

        return '';
    }

    private function messageSend($data)
    {
        $message = Message::create($data);
        $data['id'] = $message->id;

        $this->redis->publish('chat.message', json_encode($data));
    }

    public function delete(Request $request)
    {
        if(!$this->user->is_admin && !$this->user->is_moderator) {
            return [
                'error' => true,
                'message' => 'Недостаточно прав'
            ];
        }

        $message = Message::find($request->id);
        $user = User::find($message->user_id);

        if(!$message) {
            return [
                'error' => true,
                'message' => 'Сообщение не найдено'
            ];
        }

        if(!$this->user->is_admin && $user->is_admin) {
            return [
                'error' => true,
                'message' => 'Недостаточно прав'
            ];
        }

        if(!$this->user->is_admin && $user->is_moderator) {
            return [
                'error' => true,
                'message' => 'Недостаточно прав'
            ];
        }

        $message->delete();
        $this->redis->publish('chat.delete', json_encode([
            'id' => $request->id
        ]));

        return [
            'message' => 'Сообщение удалено'
        ];
    }

    public function mute(Request $request)
    {
        if(!$this->user->is_admin && !$this->user->is_moderator) {
            return [
                'error' => true,
                'message' => 'Недостаточно прав'
            ];
        }

        $validator = Validator::make($request->all(), [
            'time' => 'required|numeric|min:1|max:999',
            'reason' => 'required|min:1|max:100',
        ]);

        if($validator->fails()) {
            return [
                'error' => true,
                'message' => $validator->errors()->first()
            ];
        }

        $user = User::find($request->user_id);

        if(!$user) {
            return [
                'error' => true,
                'message' => 'Пользователь не найден'
            ];
        }

        if(!$this->user->is_admin && $user->is_admin) {
            return [
                'error' => true,
                'message' => 'Недостаточно прав'
            ];
        }

        if(!$this->user->is_admin && $user->is_moderator) {
            return [
                'error' => true,
                'message' => 'Недостаточно прав'
            ];
        }

        if($user->id === $this->user->id) {
            return [
                'error' => true,
                'message' => 'Вы не можете заблокировать себя'
            ];
        }

        if($user->chat_mute > time()) {
            return [
                'error' => true,
                'message' => 'Пользователь уже заблокирован'
            ];
        }

        $user->chat_mute = time() + (60 * $request->time);
        $user->chat_mute_reason = $request->reason;
        $user->save();

        $data = [
            'user_id' => 0,
            'avatar' => '/images/system.svg',
            'login' => 'Система',
            'text' => 'Игрок "'.$user->username.'" был заблокирован. Причина: ' . $request->reason,
            'time' => date('H:i')
        ];

        $this->messageSend($data);
        
        return [
            'message' => 'Пользователь заблокирован'
        ];
    }
}