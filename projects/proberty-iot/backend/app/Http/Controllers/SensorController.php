<?php

namespace App\Http\Controllers;

use App\Models\Sensor;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class SensorController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return response()->json(Sensor::with('equipment')->get());
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        $data = $request->validate([
            'equipment_id' => 'required|exists:equipment,id',
            'type' => 'required|string|max:255',
            'value' => 'nullable|numeric',
            'unit' => 'nullable|string|max:50',
            'last_update' => 'nullable|date',
        ]);
        $sensor = Sensor::create($data);
        return response()->json($sensor, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Sensor $sensor)
    {
        return response()->json($sensor->load('equipment'));
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Sensor $sensor)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Sensor $sensor)
    {
        $data = $request->validate([
            'equipment_id' => 'sometimes|required|exists:equipment,id',
            'type' => 'sometimes|required|string|max:255',
            'value' => 'nullable|numeric',
            'unit' => 'nullable|string|max:50',
            'last_update' => 'nullable|date',
        ]);
        $sensor->update($data);
        return response()->json($sensor);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Sensor $sensor)
    {
        $sensor->delete();
        return response()->json(null, 204);
    }
}
