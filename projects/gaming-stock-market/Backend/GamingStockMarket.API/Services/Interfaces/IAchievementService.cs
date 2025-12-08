using GamingStockMarket.API.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IAchievementService
    {
        Task<IEnumerable<Achievement>> GetUserAchievementsAsync(int userId);
        Task<Achievement?> GetAchievementByIdAsync(int achievementId);
        Task GrantAchievementAsync(int userId, AchievementType type, decimal? reward = null, string? relatedData = null);
        Task CheckAndGrantAchievementsAsync(int userId);
    }
}
