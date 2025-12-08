import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Player {
  id: number;
  name: string;
  game: string;
  teamName?: string;
  currentPrice: number;
  popularityScore: number;
  isActive: boolean;
}

const PlayerManagement: React.FC = () => {
  const [players, setPlayers] = useState<Player[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchPlayers();
  }, []);

  const fetchPlayers = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Player[]>('http://localhost:5000/api/admin/players'); // Adjust API endpoint
      setPlayers(response.data);
    } catch (err) {
      setError('Failed to fetch players.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTogglePlayerStatus = async (playerId: number, currentStatus: boolean) => {
    try {
      await axios.put(`http://localhost:5000/api/admin/players/${playerId}/toggle-status`, { isActive: !currentStatus }); // Adjust API endpoint
      fetchPlayers(); 
    } catch (err) {
      setError('Failed to toggle player status.');
      console.error(err);
    }
  };

  if (loading) return <div className="text-center text-white">Loading players...</div>;
  if (error) return <div className="text-center text-red-500">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-indigo-400">Player Management</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-gray-800 rounded-lg shadow-md">
          <thead>
            <tr className="bg-gray-700">
              <th className="py-3 px-4 text-left">ID</th>
              <th className="py-3 px-4 text-left">Name</th>
              <th className="py-3 px-4 text-left">Game</th>
              <th className="py-3 px-4 text-left">Team</th>
              <th className="py-3 px-4 text-left">Price</th>
              <th className="py-3 px-4 text-left">Popularity</th>
              <th className="py-3 px-4 text-left">Status</th>
              <th className="py-3 px-4 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {players.map((player) => (
              <tr key={player.id} className="border-b border-gray-700 last:border-b-0">
                <td className="py-3 px-4">{player.id}</td>
                <td className="py-3 px-4">{player.name}</td>
                <td className="py-3 px-4">{player.game}</td>
                <td className="py-3 px-4">{player.teamName || 'N/A'}</td>
                <td className="py-3 px-4">{player.currentPrice.toFixed(2)}</td>
                <td className="py-3 px-4">{player.popularityScore}</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${player.isActive ? 'bg-green-500' : 'bg-red-500'}`}>
                    {player.isActive ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <button
                    onClick={() => handleTogglePlayerStatus(player.id, player.isActive)}
                    className={`px-4 py-2 rounded-md text-white ${player.isActive ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}`}
                  >
                    {player.isActive ? 'Deactivate' : 'Activate'}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PlayerManagement;
