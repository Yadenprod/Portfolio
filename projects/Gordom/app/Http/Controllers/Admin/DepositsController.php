<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;

class DepositsController extends Controller
{
    public function index()
    {
        return view('admin.deposits.index');
    }
}
