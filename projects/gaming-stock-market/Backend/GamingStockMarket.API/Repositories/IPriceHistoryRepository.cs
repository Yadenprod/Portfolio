using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface IPriceHistoryRepository : IBaseRepository<PriceHistory>
    {
        Task<IEnumerable<PriceHistory>> GetPriceHistoryForPlayerAsync(int playerId, int days = 30);
        Task<IEnumerable<PriceHistory>> GetPriceHistoryForTeamAsync(int teamId, int days = 30);
    }
}
