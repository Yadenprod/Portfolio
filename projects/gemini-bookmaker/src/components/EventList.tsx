
'use client';

import React from 'react';
import { mockEvents } from '@/lib/mockEvents';
import { useBetSlip } from '@/context/BetSlipContext';

export const EventList = () => {
  const { addSelection, isOutcomeSelected } = useBetSlip();

  return (
    <div className="space-y-4">
      {mockEvents.map(event => {
        const market = event.markets.find(m => m.key === 'h2h');
        if (!market) return null;

        return (
          <div key={event.id} className="bg-white rounded-lg shadow p-4">
            <div className="flex justify-between items-center mb-3">
              <p className="font-semibold text-gray-800">{event.homeTeam} vs {event.awayTeam}</p>
              <p className="text-sm text-gray-500">{event.startTime.toLocaleTimeString()}</p>
            </div>
            <div className="grid grid-cols-3 gap-2 text-center">
              {market.outcomes.map(outcome => {
                const isSelected = isOutcomeSelected(outcome.name, event.id);
                return (
                  <button
                    key={outcome.name}
                    onClick={() => addSelection({
                      eventId: event.id,
                      eventTitle: `${event.homeTeam} vs ${event.awayTeam}`,
                      marketKey: market.key,
                      outcome: outcome,
                    })}
                    className={`p-2 rounded-md transition-colors ${isSelected ? 'bg-blue-500 text-white' : 'bg-gray-200 hover:bg-gray-300'}`}>
                    <span className="block text-sm text-gray-600">{outcome.name}</span>
                    <span className="font-bold text-lg">{outcome.price.toFixed(2)}</span>
                  </button>
                );
              })}
            </div>
          </div>
        );
      })}
    </div>
  );
};
