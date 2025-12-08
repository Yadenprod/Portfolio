<?php

namespace App\Http\Controllers;

use App\Models\MaintenanceRequest;
use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class MaintenanceRequestController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return response()->json(MaintenanceRequest::with(['equipment', 'user', 'assignedEngineer'])->get());
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
            'user_id' => 'required|exists:users,id',
            'description' => 'required|string',
            'status' => 'nullable|string',
            'assigned_to' => 'nullable|exists:users,id',
            'closed_at' => 'nullable|date',
        ]);
        $requestModel = MaintenanceRequest::create($data);
        return response()->json($requestModel, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(MaintenanceRequest $maintenanceRequest)
    {
        return response()->json($maintenanceRequest->load(['equipment', 'user', 'assignedEngineer']));
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(MaintenanceRequest $maintenanceRequest)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, MaintenanceRequest $maintenanceRequest)
    {
        $data = $request->validate([
            'equipment_id' => 'sometimes|required|exists:equipment,id',
            'user_id' => 'sometimes|required|exists:users,id',
            'description' => 'sometimes|required|string',
            'status' => 'nullable|string',
            'assigned_to' => 'nullable|exists:users,id',
            'closed_at' => 'nullable|date',
        ]);
        $maintenanceRequest->update($data);
        return response()->json($maintenanceRequest);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(MaintenanceRequest $maintenanceRequest)
    {
        $maintenanceRequest->delete();
        return response()->json(null, 204);
    }
}
