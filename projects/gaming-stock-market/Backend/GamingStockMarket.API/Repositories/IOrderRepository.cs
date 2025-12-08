using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface IOrderRepository : IBaseRepository<Order>
    {
        Task<IEnumerable<Order>> GetActiveOrdersAsync(int? playerId = null, OrderType? type = null);
        Task<IEnumerable<Order>> GetOrdersByUserIdAsync(int userId);
    }
}
