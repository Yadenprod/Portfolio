using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System;
using GamingStockMarket.API.Services.Interfaces; // Added for ITradingService

namespace GamingStockMarket.API.Services
{
    public class OrderBook
    {
        private readonly SortedDictionary<decimal, List<Order>> _buyOrders;
        private readonly SortedDictionary<decimal, List<Order>> _sellOrders;
        private readonly ILogger<OrderBook> _logger;
        public event Func<Order, Order, int, decimal, Task>? OnTradeExecuted;

        public OrderBook(ILogger<OrderBook> logger)
        {
            // Descending order for buy prices (highest buy price first)
            _buyOrders = new SortedDictionary<decimal, List<Order>>(Comparer<decimal>.Create((x, y) => y.CompareTo(x)));
            // Ascending order for sell prices (lowest sell price first)
            _sellOrders = new SortedDictionary<decimal, List<Order>>();
            _logger = logger;
        }

        public void AddOrder(Order order)
        {
            var orders = order.Type == OrderType.Buy ? _buyOrders : _sellOrders;

            if (!orders.ContainsKey(order.Price))
                orders[order.Price] = new List<Order>();

            orders[order.Price].Add(order);
            _logger.LogInformation($"Order added to order book: {order.Type} {order.Shares} shares at ${order.Price} for User {order.UserId}");

            TryMatchOrders();
        }

        private void TryMatchOrders()
        {
            while (_buyOrders.Count > 0 && _sellOrders.Count > 0)
            {
                var bestBuyPrice = _buyOrders.Keys.First();
                var bestSellPrice = _sellOrders.Keys.First();

                if (bestBuyPrice >= bestSellPrice)
                {
                    ExecuteTrade(bestBuyPrice, bestSellPrice);
                }
                else
                {
                    break; // No match found
                }
            }
        }

        private void ExecuteTrade(decimal buyPrice, decimal sellPrice)
        {
            var buyOrderList = _buyOrders[buyPrice];
            var sellOrderList = _sellOrders[sellPrice];

            // Take the oldest orders first (price-time priority)
            var buyOrder = buyOrderList.First();
            var sellOrder = sellOrderList.First();

            var tradePrice = buyPrice; // Can be buyPrice, sellPrice, or midpoint. Using buyPrice for now.
            var tradeShares = Math.Min(buyOrder.RemainingShares, sellOrder.RemainingShares);

            // Execute trade via TradingService
            OnTradeExecuted?.Invoke(buyOrder, sellOrder, tradeShares, tradePrice).Wait();

            // Update orders in order book (not in DB yet, TradingService handles DB updates)
            buyOrder.FilledShares += tradeShares;
            sellOrder.FilledShares += tradeShares;

            if (buyOrder.RemainingShares == 0)
            {
                buyOrderList.Remove(buyOrder);
                if (buyOrderList.Count == 0)
                    _buyOrders.Remove(buyPrice);
            }

            if (sellOrder.RemainingShares == 0)
            {
                sellOrderList.Remove(sellOrder);
                if (sellOrderList.Count == 0)
                    _sellOrders.Remove(sellPrice);
            }

            _logger.LogInformation($"Trade executed in order book: {tradeShares} shares at ${tradePrice}");
        }

        public (List<Order> buyOrders, List<Order> sellOrders) GetOrderBookForAsset(int? playerId, int? teamId)
        {
            // This method would need to filter orders based on playerId or teamId if the OrderBook held all orders.
            // For this simplified in-memory OrderBook, we'll return all orders and assume filtering happens at a higher level.
            // In a real system, OrderBook might be per-asset or use more sophisticated filtering.
            return (_buyOrders.SelectMany(kv => kv.Value).ToList(), _sellOrders.SelectMany(kv => kv.Value).ToList());
        }
    }

    // Custom comparer for descending order in SortedDictionary
    public class ReverseComparer<T> : IComparer<T>
    {
        public int Compare(T? x, T? y)
        {
            return Comparer<T>.Default.Compare(y, x);
        }
    }
}
