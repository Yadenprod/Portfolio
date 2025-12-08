import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store'; // Updated path
import { fetchAchievementsStart, fetchAchievementsSuccess, fetchAchievementsFailure } from 'slices/achievementSlice'; // Updated path
import { achievementApi } from 'api/achievementApi'; // Updated path
import LoadingSpinner from 'components/LoadingSpinner'; // Updated path
import type { Achievement } from 'slices/achievementSlice'; // Updated path

const AchievementsPage: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { achievements, loading, error } = useSelector((state: RootState) => state.achievement);

  useEffect(() => {
    const getAchievements = async () => {
      dispatch(fetchAchievementsStart());
      try {
        const response = await achievementApi.getUserAchievements();
        dispatch(fetchAchievementsSuccess(response.data));
      } catch (err: any) {
        dispatch(fetchAchievementsFailure(err.response?.data?.message || 'Failed to fetch achievements.'));
      }
    };
    getAchievements();
  }, [dispatch]);

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">My Achievements</h1>
      {achievements.length === 0 ? (
        <p className="text-gray-400 text-center">No achievements yet.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {achievements.map((achievement: Achievement) => (
            <div key={achievement.id} className={`bg-gray-800 p-6 rounded-lg shadow-lg ${achievement.achievedAt ? 'border-l-4 border-green-500' : 'border-l-4 border-gray-600'}`}>
              <h2 className="text-xl font-semibold text-white mb-2">{achievement.name}</h2>
              <p className="text-gray-300 mb-3">{achievement.description}</p>
              {achievement.achievedAt ? (
                <p className="text-green-400 text-sm">Achieved on: {new Date(achievement.achievedAt).toLocaleDateString()}</p>
              ) : (
                <p className="text-gray-500 text-sm">Not yet achieved</p>
              )}
              {achievement.rewardAmount && (
                <p className="text-yellow-400 text-sm">Reward: ${achievement.rewardAmount.toFixed(2)}</p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AchievementsPage;
