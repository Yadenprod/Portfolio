
'use client';

import React from 'react';
import { mockEvents, Event } from '@/lib/mockEvents';
import { useBetSlip } from '@/context/BetSlipContext';
import { FaFutbol, FaBasketballBall } from 'react-icons/fa';

const sportIcons: { [key: string]: React.ElementType } = {
  Football: FaFutbol,
  Basketball: FaBasketballBall,
};

// Group events by sport
const groupedEvents = mockEvents.reduce((acc, event) => {
  const sport = event.sport;
  if (!acc[sport]) {
    acc[sport] = [];
  }
  acc[sport].push(event);
  return acc;
}, {} as { [key: string]: Event[] });


export const EventList = () => {
  const { addSelection, isOutcomeSelected } = useBetSlip();

  return (
    <div>
      <h1 className="text-3xl font-bold text-white mb-6">Sports</h1>
      <div className="space-y-8">
        {Object.entries(groupedEvents).map(([sport, events]) => {
          const SportIcon = sportIcons[sport] || FaFutbol; // Default icon
          return (
            <div key={sport}>
              <div className="flex items-center mb-4">
                <SportIcon className="text-2xl text-gray-400 mr-3" />
                <h2 className="text-2xl font-bold text-white">{sport}</h2>
              </div>
              <div className="space-y-4">
                {events.map(event => {
                  const market = event.markets.find(m => m.key === 'h2h');
                  if (!market) return null;

                  return (
                    <div key={event.id} className="bg-gray-800 rounded-lg shadow-lg p-4 flex items-center">
                      <div className="flex-1 pr-4">
                        <p className="text-sm text-gray-400">{event.startTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                        <p className="text-lg font-bold text-white">{event.homeTeam}</p>
                        <p className="text-lg font-bold text-white">{event.awayTeam}</p>
                      </div>
                      <div className="grid grid-cols-3 gap-2 text-center w-64">
                        {market.outcomes.map(outcome => {
                          const isSelected = isOutcomeSelected(outcome.name, event.id);
                          const shortName = outcome.name === event.homeTeam ? '1' : outcome.name === event.awayTeam ? '2' : 'X';
                          return (
                            <button
                              key={outcome.name}
                              onClick={() => addSelection({
                                eventId: event.id,
                                eventTitle: `${event.homeTeam} vs ${event.awayTeam}`,
                                marketKey: market.key,
                                outcome: outcome,
                              })}
                              className={`p-3 rounded-md transition-colors ${isSelected ? 'bg-blue-600 text-white' : 'bg-gray-700 hover:bg-gray-600'}`}>
                              <span className="block text-sm text-gray-400">{shortName}</span>
                              <span className="font-bold text-md">{outcome.price.toFixed(2)}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
