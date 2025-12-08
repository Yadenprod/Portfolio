using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface IUserPortfolioRepository : IBaseRepository<UserPortfolio>
    {
        Task<IEnumerable<UserPortfolio>> GetUserPortfolioAsync(int userId);
        Task<UserPortfolio?> GetUserPortfolioItemAsync(int userId, int playerId);
    }
}
