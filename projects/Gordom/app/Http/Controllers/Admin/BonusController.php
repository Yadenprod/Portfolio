<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\BonusLevel;

class BonusController extends Controller
{
    public function index()
    {
        return view('admin.bonus.index');
    }

    public function create(Request $request)
    {
        BonusLevel::create($request->all());
        return redirect()->back()->withSucess('Уровень создан');
    }

    public function delete($id)
    {
        $bonus = BonusLevel::find($id);

        if(!$bonus) {
            return redirect()->back()->withError('Уровень уже удален');
        }

        $bonus->delete();
        return redirect()->back()->withSuccess('Уровень удален');
    }
}