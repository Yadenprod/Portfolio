<?php

namespace App\Http\Controllers;

use App\Models\Equipment;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;
use Illuminate\Support\Facades\Log;

class EquipmentController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return response()->json(Equipment::with(['sensors', 'maintenanceRequests'])->get());
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
        Log::info('Создание нового оборудования', [
            'user_id' => auth()->id(),
            'equipment_data' => $request->all()
        ]);
        
        $data = $request->validate([
            'name' => 'required|string|max:255',
            'location' => 'nullable|string|max:255',
            'description' => 'nullable|string',
        ]);
        $equipment = Equipment::create($data);
        return response()->json($equipment, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Equipment $equipment)
    {
        return response()->json($equipment->load(['sensors', 'maintenanceRequests']));
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Equipment $equipment)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, Equipment $equipment)
    {
        Log::info('Обновление оборудования', [
            'user_id' => auth()->id(),
            'equipment_id' => $equipment->id,
            'update_data' => $request->all()
        ]);
        
        $data = $request->validate([
            'name' => 'sometimes|required|string|max:255',
            'location' => 'nullable|string|max:255',
            'description' => 'nullable|string',
        ]);
        $equipment->update($data);
        return response()->json($equipment);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Equipment $equipment)
    {
        Log::warning('Удаление оборудования', [
            'user_id' => auth()->id(),
            'equipment_id' => $equipment->id
        ]);
        
        $equipment->delete();
        return response()->json(null, 204);
    }
}
