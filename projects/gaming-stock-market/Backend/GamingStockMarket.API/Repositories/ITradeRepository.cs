using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface ITradeRepository : IBaseRepository<Trade>
    {
        Task<IEnumerable<Trade>> GetUserTradesAsync(int userId);
        Task<decimal> GetTotalVolumeForPlayerAsync(int playerId);
    }
}
