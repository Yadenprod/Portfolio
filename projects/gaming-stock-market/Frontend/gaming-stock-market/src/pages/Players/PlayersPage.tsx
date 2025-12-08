import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store';
import { fetchPlayersStart, fetchPlayersSuccess, fetchPlayersFailure } from 'slices/playerSlice';
import { playerApi } from 'api/playerApi';
import Card from 'components/Card';
import LoadingSpinner from 'components/LoadingSpinner';
import type { Player } from 'slices/playerSlice';

const PlayersPage: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { players, loading, error } = useSelector((state: RootState) => state.player);

  useEffect(() => {
    const getPlayers = async () => {
      dispatch(fetchPlayersStart());
      try {
        const response = await playerApi.getAllPlayers();
        dispatch(fetchPlayersSuccess(response.data));
      } catch (err: any) {
        dispatch(fetchPlayersFailure(err.response?.data?.message || 'Failed to fetch players.'));
      }
    };
    getPlayers();
  }, [dispatch]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">All Players</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {players.map((player: Player) => (
          <Card key={player.id} item={player} type="player" />
        ))}
      </div>
    </div>
  );
};

export default PlayersPage;
