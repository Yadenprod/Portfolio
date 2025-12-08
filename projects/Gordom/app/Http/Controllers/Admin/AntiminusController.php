<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

use App\Models\Profit;
use App\Models\Setting;

class AntiminusController extends Controller
{
    public function index()
    {
        return view('admin.antiminus.index');
    }

    public function save(Request $request)
    {
        Profit::find(1)->update($request->all());
        Setting::find(1)->update([
            'antiminus' => $request->antiminus
        ]);

        return redirect()->back()->withSuccess('Сохранено');
    }
}