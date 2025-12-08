import api from 'api/api';
import type { AchievementResponse } from 'types/api';

export const achievementApi = {
  getUserAchievements: () => api.get<AchievementResponse[]>('/Achievement/user'),
};
