using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;

namespace GamingStockMarket.API.Repositories
{
    public class OrderRepository : BaseRepository<Order>, IOrderRepository
    {
        public OrderRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Order>> GetActiveOrdersAsync(int? playerId = null, OrderType? type = null)
        {
            var query = _context.Orders.Where(o => o.Status == OrderStatus.Pending);

            if (playerId.HasValue)
            {
                query = query.Where(o => o.PlayerId == playerId.Value);
            }
            if (type.HasValue)
            {
                query = query.Where(o => o.Type == type.Value);
            }

            return await query.ToListAsync();
        }

        public async Task<IEnumerable<Order>> GetOrdersByUserIdAsync(int userId)
        {
            return await _context.Orders.Where(o => o.UserId == userId).ToListAsync();
        }
    }
}
