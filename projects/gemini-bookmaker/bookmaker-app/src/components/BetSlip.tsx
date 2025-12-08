'use client';

import React, { useState } from 'react';
import { useBetSlip } from '@/context/BetSlipContext';
import { FaTrash } from 'react-icons/fa';

export const BetSlip = () => {
  const { selections, removeSelection, clearSelections } = useBetSlip();
  const [stake, setStake] = useState('10');

  const totalOdds = selections.reduce((acc, sel) => acc * sel.outcome.price, 1);
  const potentialWinnings = stake && parseFloat(stake) > 0 ? (parseFloat(stake) * totalOdds).toFixed(2) : '0.00';

  const handlePlaceBet = () => {
    alert(`Bet placed!\nStake: $${stake}\nTotal Odds: ${totalOdds.toFixed(2)}\nPotential Winnings: $${potentialWinnings}`);
    clearSelections();
    setStake('10');
  };

  return (
    <div className="flex flex-col h-full">
      <h2 className="text-xl font-bold mb-4 text-white">Bet Slip</h2>
      
      {selections.length === 0 ? (
        <div className="flex-1 flex items-center justify-center bg-gray-700 rounded-lg">
          <p className="text-gray-400">Your slip is empty</p>
        </div>
      ) : (
        <div className="flex-1 flex flex-col">
          {/* Selections List */}
          <div className="space-y-2 mb-4 flex-1 overflow-y-auto pr-1">
            {selections.map(selection => (
              <div key={`${selection.eventId}-${selection.outcome.name}`} className="bg-gray-700 p-3 rounded-lg shadow">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="text-sm font-semibold text-white">{selection.outcome.name}</p>
                    <p className="text-xs text-gray-400">{selection.eventTitle}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    <p className="font-bold text-white">{selection.outcome.price.toFixed(2)}</p>
                    <button onClick={() => removeSelection(selection.outcome.name, selection.eventId)} className="text-gray-400 hover:text-red-500 transition-colors">
                        <FaTrash />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Calculation Section */}
          <div className="bg-gray-900 p-4 rounded-lg">
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                  <label htmlFor="stake" className="font-semibold text-gray-300">Stake:</label>
                  <div className="relative">
                    <span className="absolute left-2 top-1/2 -translate-y-1/2 text-gray-400">$</span>
                    <input 
                        type="number" 
                        id="stake" 
                        value={stake}
                        onChange={(e) => setStake(e.target.value)}
                        className="w-28 p-2 pl-6 border-none bg-gray-700 text-white rounded-md text-right font-mono"
                    />
                  </div>
              </div>
              <div className="flex justify-between items-center text-md font-bold">
                  <p className="text-gray-300">Total Odds:</p>
                  <p className="text-white font-mono">x{totalOdds.toFixed(2)}</p>
              </div>
              <div className="flex justify-between items-center text-lg font-bold">
                  <p className="text-gray-300">Winnings:</p>
                  <p className="text-green-400 font-mono">${potentialWinnings}</p>
              </div>
              <button 
                  onClick={handlePlaceBet}
                  className="w-full bg-green-600 text-white font-bold py-3 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-500"
                  disabled={!stake || parseFloat(stake) <= 0}
              >
                  Place Bet
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
