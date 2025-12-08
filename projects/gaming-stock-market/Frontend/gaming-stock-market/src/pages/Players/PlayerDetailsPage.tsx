import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store'; // Updated path
import { setSelectedPlayer } from 'slices/playerSlice'; // Updated path
import { playerApi } from 'api/playerApi'; // Updated path
import LoadingSpinner from 'components/LoadingSpinner'; // Updated path

const PlayerDetailsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch: AppDispatch = useDispatch();
  const { selectedPlayer, loading, error } = useSelector((state: RootState) => state.player);

  useEffect(() => {
    if (id) {
      const getPlayerDetails = async () => {
        // Note: Currently, loading and error states are for all players/teams, not specific details
        // You might want to extend playerSlice to handle loading/error for selectedPlayer/Team
        try {
          const response = await playerApi.getPlayerById(parseInt(id));
          dispatch(setSelectedPlayer(response.data));
        } catch (err: any) {
          console.error("Failed to fetch player details:", err);
          // Handle error, maybe set an error state specific to selected player
        }
      };
      getPlayerDetails();
    }
  }, [id, dispatch]);

  if (loading) return <LoadingSpinner />;
  // If there's a global error or specific error for selected player
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;
  if (!selectedPlayer) return <div className="text-center text-gray-400 mt-8">Player not found.</div>;

  return (
    <div className="p-4">
      <h1 className="text-4xl font-bold text-white mb-6">{selectedPlayer.name}</h1>
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
        <p className="text-gray-300 text-lg mb-2">Game: <span className="font-semibold text-white">{selectedPlayer.game}</span></p>
        {selectedPlayer.team && <p className="text-gray-300 text-lg mb-2">Team: <span className="font-semibold text-white">{selectedPlayer.team}</span></p>}
        <p className="text-gray-300 text-lg mb-2">Current Price: <span className="font-semibold text-green-400">${selectedPlayer.currentPrice.toFixed(2)}</span></p>
        {selectedPlayer.rating && <p className="text-gray-300 text-lg mb-2">Rating: <span className="font-semibold text-white">{selectedPlayer.rating.toFixed(2)}</span></p>}
        <p className="text-gray-300 text-lg mb-2">Popularity Score: <span className="font-semibold text-white">{selectedPlayer.popularityScore}</span></p>
      </div>

      {/* TODO: Add trading components, price charts, news, etc. */}
    </div>
  );
};

export default PlayerDetailsPage;
