import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store';
import { fetchTeamsStart, fetchTeamsSuccess, fetchTeamsFailure } from 'slices/playerSlice';
import { playerApi } from 'api/playerApi';
import Card from 'components/Card';
import LoadingSpinner from 'components/LoadingSpinner';
import type { Team } from 'slices/playerSlice';

const TeamsPage: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { teams, loading, error } = useSelector((state: RootState) => state.player);

  useEffect(() => {
    const getTeams = async () => {
      dispatch(fetchTeamsStart());
      try {
        const response = await playerApi.getAllTeams();
        dispatch(fetchTeamsSuccess(response.data));
      } catch (err: any) {
        dispatch(fetchTeamsFailure(err.response?.data?.message || 'Failed to fetch teams.'));
      }
    };
    getTeams();
  }, [dispatch]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">All Teams</h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        {teams.map((team: Team) => (
          <Card key={team.id} item={team} type="team" />
        ))}
      </div>
    </div>
  );
};

export default TeamsPage;
