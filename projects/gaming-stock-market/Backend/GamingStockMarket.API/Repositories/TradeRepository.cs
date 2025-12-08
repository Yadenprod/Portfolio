using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;

namespace GamingStockMarket.API.Repositories
{
    public class TradeRepository : BaseRepository<Trade>, ITradeRepository
    {
        public TradeRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Trade>> GetUserTradesAsync(int userId)
        {
            return await _context.Trades
                .Where(t => t.BuyOrder.UserId == userId || t.SellOrder.UserId == userId)
                .OrderByDescending(t => t.CreatedAt)
                .ToListAsync();
        }

        public async Task<decimal> GetTotalVolumeForPlayerAsync(int playerId)
        {
            return await _context.Trades
                .Where(t => t.PlayerId == playerId)
                .SumAsync(t => t.Shares);
        }
    }
}
