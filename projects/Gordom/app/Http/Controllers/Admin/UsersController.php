<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\User;
use App\Models\ReferralProfit;
use Illuminate\Http\Request;

class UsersController extends Controller
{
    public function index()
    {
        return view('admin.users.index');
    }

    public function edit($id)
    {
        $user = User::query()->find($id);
        if (!$user) {
            return redirect()->back()->with('error', 'Пользователь не найден!');
        }
        
        return view('admin.users.edit', compact('user'));
    }

    public function editPost($id, Request $r)
    {
        $user = User::query()->find($id);

        if (!$user) {
            return redirect()->back()->with('error', 'Пользователь не найден!');
        }

        if ($user->password !== $r->get('password')) {
            $user->update([
                'password' => hash('sha256', $r->get('password'))
            ]);
        }

        User::query()->find($id)->update($r->all());

        return redirect('/admin/users/edit/' . $id)->with('success', 'Данные пользователя обновлены!');
    }

    public function delete($id)
    {
        User::query()->find($id)->delete();

        return redirect()->back()->with('success', 'Пользователь удален');
    }

    public function checker(Request $request)
    {
        $user = User::find($request->user_id);

        $multi = User::query()
            ->orWhere('used_ip', $user->used_ip)
            ->orWhere('created_ip', $user->created_ip)
            ->get();

        return [
            'user' => $user,
            'list' => collect($multi)->where('id', '!=', $user->id)->values()
        ];
    }
}
