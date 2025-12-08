import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store';
import { setSelectedTeam } from 'slices/playerSlice';
import { playerApi } from 'api/playerApi';
import LoadingSpinner from 'components/LoadingSpinner';

const TeamDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch: AppDispatch = useDispatch();
  const { selectedTeam, loading, error } = useSelector((state: RootState) => state.player);

  useEffect(() => {
    if (id) {
      const getTeamDetails = async () => {
        try {
          const response = await playerApi.getTeamById(parseInt(id));
          dispatch(setSelectedTeam(response.data));
        } catch (err: any) {
          console.error("Failed to fetch team details:", err);
        }
      };
      getTeamDetails();
    }
  }, [id, dispatch]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;
  if (!selectedTeam) return <div className="text-center text-gray-400 mt-8">Team not found.</div>;

  return (
    <div className="p-4">
      <h1 className="text-4xl font-bold text-white mb-6">{selectedTeam.name}</h1>
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <p className="text-gray-300 text-lg mb-2">Game: <span className="font-semibold text-white">{selectedTeam.game}</span></p>
        <p className="text-gray-300 text-lg mb-2">Current Price: <span className="font-semibold text-green-400">${selectedTeam.currentPrice.toFixed(2)}</span></p>
        {selectedTeam.ranking && <p className="text-gray-300 text-lg mb-2">Ranking: <span className="font-semibold text-white">{selectedTeam.ranking}</span></p>}
      </div>

      {/* TODO: Add trading components, price charts, news, etc. */}
    </div>
  );
};

export default TeamDetailsPage;
