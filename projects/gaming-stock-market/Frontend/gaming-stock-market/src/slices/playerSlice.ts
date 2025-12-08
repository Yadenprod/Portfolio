import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface Player {
  id: number;
  name: string;
  game: string;
  team?: string;
  currentPrice: number;
  rating?: number;
  popularityScore: number;
}

export interface Team {
  id: number;
  name: string;
  game: string;
  currentPrice: number;
  ranking?: number;
}

interface PlayerState {
  players: Player[];
  teams: Team[];
  selectedPlayer: Player | null;
  selectedTeam: Team | null;
  loading: boolean;
  error: string | null;
}

const initialState: PlayerState = {
  players: [],
  teams: [],
  selectedPlayer: null,
  selectedTeam: null,
  loading: false,
  error: null,
};

const playerSlice = createSlice({
  name: 'player',
  initialState,
  reducers: {
    fetchPlayersStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchPlayersSuccess: (state, action: PayloadAction<Player[]>) => {
      state.players = action.payload;
      state.loading = false;
    },
    fetchPlayersFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    fetchTeamsStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchTeamsSuccess: (state, action: PayloadAction<Team[]>) => {
      state.teams = action.payload;
      state.loading = false;
    },
    fetchTeamsFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
    setSelectedPlayer: (state, action: PayloadAction<Player | null>) => {
      state.selectedPlayer = action.payload;
    },
    setSelectedTeam: (state, action: PayloadAction<Team | null>) => {
      state.selectedTeam = action.payload;
    },
  },
});

export const {
  fetchPlayersStart, fetchPlayersSuccess, fetchPlayersFailure,
  fetchTeamsStart, fetchTeamsSuccess, fetchTeamsFailure,
  setSelectedPlayer, setSelectedTeam,
} = playerSlice.actions;

export default playerSlice.reducer;
