import api from 'api/api';
import type { PlayerResponse, TeamResponse } from 'types/api';

export const playerApi = {
  getAllPlayers: (game?: string, searchTerm?: string, pageNumber?: number, pageSize?: number) => 
    api.get<PlayerResponse[]>('/Players', { params: { game, searchTerm, pageNumber, pageSize } }),
  getPlayerById: (id: number) => api.get<PlayerResponse>(`/Players/${id}`),
  getAllTeams: (game?: string, searchTerm?: string, pageNumber?: number, pageSize?: number) => 
    api.get<TeamResponse[]>('/Players/teams', { params: { game, searchTerm, pageNumber, pageSize } }),
  getTeamById: (id: number) => api.get<TeamResponse>(`/Players/teams/${id}`),
};
