using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface IAchievementRepository : IBaseRepository<Achievement>
    {
        Task<IEnumerable<Achievement>> GetAchievementsForUserAsync(int userId);
        Task<Achievement?> GetAchievementByNameAsync(string name);
    }
}
