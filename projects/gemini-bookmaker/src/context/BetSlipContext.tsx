
'use client';

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Event, Outcome } from '@/lib/mockEvents';

export type BetSelection = {
  eventId: string;
  eventTitle: string;
  marketKey: string;
  outcome: Outcome;
};

type BetSlipContextType = {
  selections: BetSelection[];
  addSelection: (selection: BetSelection) => void;
  removeSelection: (outcomeName: string, eventId: string) => void;
  clearSelections: () => void;
  isOutcomeSelected: (outcomeName: string, eventId: string) => boolean;
};

const BetSlipContext = createContext<BetSlipContextType | undefined>(undefined);

export const BetSlipProvider = ({ children }: { children: ReactNode }) => {
  const [selections, setSelections] = useState<BetSelection[]>([]);

  const addSelection = (selection: BetSelection) => {
    setSelections(prev => {
      // If an outcome from the same event is already selected, replace it.
      const filtered = prev.filter(s => s.eventId !== selection.eventId);
      return [...filtered, selection];
    });
  };

  const removeSelection = (outcomeName: string, eventId: string) => {
    setSelections(prev => prev.filter(s => !(s.outcome.name === outcomeName && s.eventId === eventId)));
  };

  const clearSelections = () => {
    setSelections([]);
  };

  const isOutcomeSelected = (outcomeName: string, eventId: string) => {
    return selections.some(s => s.outcome.name === outcomeName && s.eventId === eventId);
  };

  return (
    <BetSlipContext.Provider value={{ selections, addSelection, removeSelection, clearSelections, isOutcomeSelected }}>
      {children}
    </BetSlipContext.Provider>
  );
};

export const useBetSlip = () => {
  const context = useContext(BetSlipContext);
  if (context === undefined) {
    throw new Error('useBetSlip must be used within a BetSlipProvider');
  }
  return context;
};
