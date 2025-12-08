import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import tradingReducer from './slices/tradingSlice';
import playerReducer from './slices/playerSlice';
import notificationReducer from './slices/notificationSlice';
import achievementReducer from './slices/achievementSlice';

export const store = configureStore({
  reducer: {
    auth: authReducer,
    trading: tradingReducer,
    player: playerReducer,
    notification: notificationReducer,
    achievement: achievementReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
