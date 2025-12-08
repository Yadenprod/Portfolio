'use client';

import React, { useState } from 'react';
import { useBetSlip } from '@/context/BetSlipContext';

export const BetSlip = () => {
  const { selections, removeSelection, clearSelections } = useBetSlip();
  const [stake, setStake] = useState('10'); // Default stake

  if (selections.length === 0) {
    return null; // Don't show the slip if it's empty
  }

  const totalOdds = selections.reduce((acc, sel) => acc * sel.outcome.price, 1);
  const potentialWinnings = (parseFloat(stake) * totalOdds).toFixed(2);

  const handlePlaceBet = () => {
    alert(`Bet placed!\nStake: $${stake}\nTotal Odds: ${totalOdds.toFixed(2)}\nPotential Winnings: $${potentialWinnings}`);
    clearSelections();
  };

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t-2 border-blue-500 shadow-lg p-4 z-20">
      <h2 className="text-lg font-bold mb-2">Bet Slip</h2>
      <div className="space-y-2 mb-3">
        {selections.map(selection => (
          <div key={`${selection.eventId}-${selection.outcome.name}`} className="flex justify-between items-center bg-gray-100 p-2 rounded">
            <div>
              <p className="text-sm font-semibold">{selection.outcome.name}</p>
              <p className="text-xs text-gray-500">{selection.eventTitle}</p>
            </div>
            <div className="flex items-center gap-4">
                <p className="font-bold">{selection.outcome.price.toFixed(2)}</p>
                <button onClick={() => removeSelection(selection.outcome.name, selection.eventId)} className="text-red-500 hover:text-red-700">
                    &times;
                </button>
            </div>
          </div>
        ))}
      </div>
      
      <div className="space-y-3">
        <div className="flex justify-between items-center">
            <label htmlFor="stake" className="font-semibold">Stake:</label>
            <input 
                type="number" 
                id="stake" 
                value={stake}
                onChange={(e) => setStake(e.target.value)}
                className="w-24 p-1 border rounded text-right"
            />
        </div>
        <div className="flex justify-between items-center text-lg font-bold">
            <p>Total Odds:</p>
            <p>{totalOdds.toFixed(2)}</p>
        </div>
        <div className="flex justify-between items-center text-lg font-bold">
            <p>Potential Winnings:</p>
            <p>${potentialWinnings}</p>
        </div>
        <button 
            onClick={handlePlaceBet}
            className="w-full bg-green-500 text-white font-bold py-3 rounded hover:bg-green-600 transition-colors"
        >
            Place Bet
        </button>
      </div>
    </div>
  );
};
