import { createSlice, type PayloadAction } from '@reduxjs/toolkit';

export interface Achievement {
  id: number;
  name: string;
  description: string;
  achievedAt: string | null;
  rewardAmount: number;
  type: string;
}

interface AchievementState {
  achievements: Achievement[];
  loading: boolean;
  error: string | null;
}

const initialState: AchievementState = {
  achievements: [],
  loading: false,
  error: null,
};

const achievementSlice = createSlice({
  name: 'achievement',
  initialState,
  reducers: {
    fetchAchievementsStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    fetchAchievementsSuccess: (state, action: PayloadAction<Achievement[]>) => {
      state.achievements = action.payload;
      state.loading = false;
    },
    fetchAchievementsFailure: (state, action: PayloadAction<string>) => {
      state.loading = false;
      state.error = action.payload;
    },
  },
});

export const { fetchAchievementsStart, fetchAchievementsSuccess, fetchAchievementsFailure } = achievementSlice.actions;
export default achievementSlice.reducer;
