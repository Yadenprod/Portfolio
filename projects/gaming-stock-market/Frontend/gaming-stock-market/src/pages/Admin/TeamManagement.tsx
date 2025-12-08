import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Team {
  id: number;
  name: string;
  game: string;
  ranking: number;
  isActive: boolean;
}

const TeamManagement: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Team[]>('http://localhost:5000/api/admin/teams'); // Adjust API endpoint
      setTeams(response.data);
    } catch (err) {
      setError('Failed to fetch teams.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleTeamStatus = async (teamId: number, currentStatus: boolean) => {
    try {
      await axios.put(`http://localhost:5000/api/admin/teams/${teamId}/toggle-status`, { isActive: !currentStatus }); // Adjust API endpoint
      fetchTeams(); 
    } catch (err) {
      setError('Failed to toggle team status.');
      console.error(err);
    }
  };

  if (loading) return <div className="text-center text-white">Loading teams...</div>;
  if (error) return <div className="text-center text-red-500">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-indigo-400">Team Management</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-gray-800 rounded-lg shadow-md">
          <thead>
            <tr className="bg-gray-700">
              <th className="py-3 px-4 text-left">ID</th>
              <th className="py-3 px-4 text-left">Name</th>
              <th className="py-3 px-4 text-left">Game</th>
              <th className="py-3 px-4 text-left">Ranking</th>
              <th className="py-3 px-4 text-left">Status</th>
              <th className="py-3 px-4 text-left">Actions</th>
            </tr>
          </thead>
          <tbody>
            {teams.map((team) => (
              <tr key={team.id} className="border-b border-gray-700 last:border-b-0">
                <td className="py-3 px-4">{team.id}</td>
                <td className="py-3 px-4">{team.name}</td>
                <td className="py-3 px-4">{team.game}</td>
                <td className="py-3 px-4">{team.ranking}</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${team.isActive ? 'bg-green-500' : 'bg-red-500'}`}>
                    {team.isActive ? 'Active' : 'Inactive'}
                  </span>
                </td>
                <td className="py-3 px-4">
                  <button
                    onClick={() => handleToggleTeamStatus(team.id, team.isActive)}
                    className={`px-4 py-2 rounded-md text-white ${team.isActive ? 'bg-red-600 hover:bg-red-700' : 'bg-green-600 hover:bg-green-700'}`}
                  >
                    {team.isActive ? 'Deactivate' : 'Activate'}
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

export default TeamManagement;
