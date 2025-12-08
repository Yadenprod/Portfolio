using GamingStockMarket.API.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface ITradingService
    {
        Task<Order> PlaceOrderAsync(Order order);
        Task CancelOrderAsync(int orderId, int userId);
        Task<(List<Order> BuyOrders, List<Order> SellOrders)> GetOrderBookAsync(int? playerId = null, int? teamId = null);
        Task<List<UserPortfolio>> GetUserPortfolioAsync(int userId);
        Task<IEnumerable<Trade>> GetTradeHistoryAsync(int? userId = null, int? playerId = null, int? teamId = null, int pageNumber = 1, int pageSize = 10);
        Task<decimal> CalculateCommissionAsync(decimal amount, int userId);
        Task ExecuteTradeAsync(Order buyOrder, Order sellOrder, int shares, decimal tradePrice);
        Task<bool> ApplyStopLossAsync(int userId, int? playerId, int? teamId, decimal stopLossPrice);
        Task<bool> ApplyTakeProfitAsync(int userId, int? playerId, int? teamId, decimal takeProfitPrice);
    }
}
