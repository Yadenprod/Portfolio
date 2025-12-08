using GamingStockMarket.API.DTOs;
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
    public class TradingService : ITradingService
    {
        private readonly IOrderRepository _orderRepository;
        private readonly IUserRepository _userRepository;
        private readonly IPlayerRepository _playerRepository;
        private readonly ITeamRepository _teamRepository;
        private readonly ITradeRepository _tradeRepository;
        private readonly IUserPortfolioRepository _userPortfolioRepository;
        private readonly ITransactionRepository _transactionRepository;
        private readonly ILogger<TradingService> _logger;
        private readonly OrderBook _orderBook; // Injected OrderBook
        private readonly IAchievementService _achievementService; // Added for achievement service

        public TradingService(IOrderRepository orderRepository, IUserRepository userRepository, 
                              IPlayerRepository playerRepository, ITeamRepository teamRepository,
                              ITradeRepository tradeRepository, IUserPortfolioRepository userPortfolioRepository,
                              ITransactionRepository transactionRepository, ILogger<TradingService> logger,
                              OrderBook orderBook, IAchievementService achievementService)
        {
            _orderRepository = orderRepository;
            _userRepository = userRepository;
            _playerRepository = playerRepository;
            _teamRepository = teamRepository;
            _tradeRepository = tradeRepository;
            _userPortfolioRepository = userPortfolioRepository;
            _transactionRepository = transactionRepository;
            _logger = logger;
            _orderBook = orderBook;
            _achievementService = achievementService; // Initialize achievement service

            // Subscribe to OrderBook's OnTradeExecuted event
            _orderBook.OnTradeExecuted += HandleTradeExecutedAsync;
        }

        public async Task<Order> PlaceOrderAsync(Order order)
        {
            // 1. Validate order
            await ValidateOrder(order);

            // 2. Deduct/Reserve balance for BUY orders
            var user = await _userRepository.GetByIdAsync(order.UserId);
            if (user == null) throw new Exception("User not found");

            if (order.Type == OrderType.Buy)
            {
                var totalCost = order.Shares * order.Price;
                if (user.Balance < totalCost) throw new Exception("Insufficient balance");
                user.Balance -= totalCost; // Reserve funds
                await _userRepository.UpdateAsync(user);

                await _transactionRepository.AddAsync(new Transaction
                {
                    UserId = user.Id,
                    Type = TransactionType.TradeBuy,
                    Amount = totalCost,
                    Status = "PENDING",
                    Notes = $"Reserved for buy order {order.Id}"
                });
            }

            // 3. Save order to DB
            await _orderRepository.AddAsync(order);

            // 4. Add to in-memory OrderBook
            _orderBook.AddOrder(order);

            _logger.LogInformation($"Order placed: {order.Type} {order.Shares} shares at ${order.Price} for User {order.UserId}");

            // Check for achievements after placing an order
            await _achievementService.CheckAndGrantAchievementsAsync(order.UserId);

            return order;
        }

        public async Task CancelOrderAsync(int orderId, int userId)
        {
            var order = await _orderRepository.GetByIdAsync(orderId);
            if (order == null || order.UserId != userId) throw new Exception("Order not found or unauthorized");
            if (order.Status != OrderStatus.Pending) throw new Exception("Only pending orders can be cancelled");

            order.Status = OrderStatus.Cancelled;
            await _orderRepository.UpdateAsync(order);

            // Refund reserved balance for BUY orders
            if (order.Type == OrderType.Buy)
            {
                var user = await _userRepository.GetByIdAsync(userId);
                if (user == null) throw new Exception("User not found");

                user.Balance += (order.Shares - order.FilledShares) * order.Price; // Refund unfiilled part
                await _userRepository.UpdateAsync(user);

                await _transactionRepository.AddAsync(new Transaction
                {
                    UserId = user.Id,
                    Type = TransactionType.TradeBuy,
                    Amount = (order.Shares - order.FilledShares) * order.Price,
                    Status = "COMPLETED",
                    Notes = $"Refund for cancelled buy order {order.Id}"
                });
            }

            _logger.LogInformation($"Order cancelled: {orderId} by User {userId}");
        }

        public async Task<(List<Order> BuyOrders, List<Order> SellOrders)> GetOrderBookAsync(int? playerId = null, int? teamId = null)
        {
            var buyOrders = await _orderRepository.GetActiveOrdersAsync(playerId, OrderType.Buy);
            var sellOrders = await _orderRepository.GetActiveOrdersAsync(playerId, OrderType.Sell);

            return (buyOrders.ToList(), sellOrders.ToList());
        }

        public async Task<List<UserPortfolio>> GetUserPortfolioAsync(int userId)
        {
            var portfolio = await _userPortfolioRepository.GetUserPortfolioAsync(userId);
            return portfolio.ToList();
        }

        public async Task<IEnumerable<Trade>> GetTradeHistoryAsync(int? userId = null, int? playerId = null, int? teamId = null, int pageNumber = 1, int pageSize = 10)
        {
            if (!userId.HasValue) throw new Exception("UserId is required for GetTradeHistoryAsync.");
            return await _tradeRepository.GetUserTradesAsync(userId.Value);
        }

        public async Task<decimal> CalculateCommissionAsync(decimal amount, int userId)
        {
            var user = await _userRepository.GetByIdAsync(userId);
            if (user == null) throw new Exception("User not found");

            // Commission based on user level (example logic)
            return user.Level switch
            {
                4 => amount * 0.005m, // Master: 0.5%
                3 => amount * 0.01m,  // Expert: 1%
                2 => amount * 0.015m, // Trader: 1.5%
                _ => amount * 0.02m   // Novice: 2%
            };
        }

        public async Task ExecuteTradeAsync(Order buyOrder, Order sellOrder, int shares, decimal tradePrice)
        {
            // Get buyers and sellers
            var buyer = await _userRepository.GetByIdAsync(buyOrder.UserId);
            var seller = await _userRepository.GetByIdAsync(sellOrder.UserId);

            if (buyer == null) throw new Exception($"Buyer with ID {buyOrder.UserId} not found.");
            if (seller == null) throw new Exception($"Seller with ID {sellOrder.UserId} not found.");

            // Calculate commission
            var commission = await CalculateCommissionAsync(shares * tradePrice, seller.Id); // Commission usually from seller

            // Update balances
            buyer.Balance -= (shares * tradePrice); // Already reserved in PlaceOrder, so deduct it fully
            seller.Balance += (shares * tradePrice - commission);

            await _userRepository.UpdateAsync(buyer);
            await _userRepository.UpdateAsync(seller);

            // Create Trade record
            var trade = new Trade
            {
                BuyOrderId = buyOrder.Id,
                SellOrderId = sellOrder.Id,
                BuyOrder = buyOrder,
                SellOrder = sellOrder,
                PlayerId = buyOrder.PlayerId,
                TeamId = buyOrder.TeamId,
                Shares = shares,
                Price = tradePrice,
                Commission = commission,
                CreatedAt = DateTime.UtcNow
            };
            await _tradeRepository.AddAsync(trade);

            // Update orders status
            buyOrder.FilledShares += shares;
            sellOrder.FilledShares += shares;

            if (buyOrder.RemainingShares == 0)
                buyOrder.Status = OrderStatus.Filled;
            else
                buyOrder.Status = OrderStatus.PartiallyFilled;

            if (sellOrder.RemainingShares == 0)
                sellOrder.Status = OrderStatus.Filled;
            else
                sellOrder.Status = OrderStatus.PartiallyFilled;

            await _orderRepository.UpdateAsync(buyOrder);
            await _orderRepository.UpdateAsync(sellOrder);

            // Update UserPortfolio
            await UpdateUserPortfolio(buyer.Id, buyOrder.PlayerId, buyOrder.TeamId, shares, tradePrice, OrderType.Buy);
            await UpdateUserPortfolio(seller.Id, sellOrder.PlayerId, sellOrder.TeamId, shares, tradePrice, OrderType.Sell);

            // Record transactions
            await _transactionRepository.AddAsync(new Transaction
            {
                UserId = buyer.Id,
                Type = TransactionType.TradeBuy,
                Amount = shares * tradePrice,
                Status = "COMPLETED",
                Notes = $"Buy trade {trade.Id}"
            });
            await _transactionRepository.AddAsync(new Transaction
            {
                UserId = seller.Id,
                Type = TransactionType.TradeSell,
                Amount = shares * tradePrice - commission,
                Status = "COMPLETED",
                Notes = $"Sell trade {trade.Id}"
            });
            if (commission > 0)
            {
                await _transactionRepository.AddAsync(new Transaction
                {
                    UserId = seller.Id,
                    Type = TransactionType.Commission,
                    Amount = commission,
                    Status = "COMPLETED",
                    Notes = $"Commission for trade {trade.Id}"
                });
            }

            _logger.LogInformation($"Trade {trade.Id} executed between User {buyer.Id} and User {seller.Id} for {shares} shares at ${tradePrice}");

            // Check for achievements after executing a trade
            await _achievementService.CheckAndGrantAchievementsAsync(buyer.Id);
            await _achievementService.CheckAndGrantAchievementsAsync(seller.Id);
        }

        private async Task ValidateOrder(Order order)
        {
            if (order.Shares <= 0 || order.Price <= 0) throw new Exception("Invalid order parameters");

            if (order.PlayerId.HasValue && order.TeamId.HasValue) throw new Exception("Order cannot be for both player and team.");
            if (!order.PlayerId.HasValue && !order.TeamId.HasValue) throw new Exception("Order must be for either a player or a team.");

            if (order.PlayerId.HasValue)
            {
                var player = await _playerRepository.GetByIdAsync(order.PlayerId.Value);
                if (player == null) throw new Exception("Player not found.");
                if (!player.IsActive) throw new Exception("Player is not active for trading.");
            }

            if (order.TeamId.HasValue)
            {
                var team = await _teamRepository.GetByIdAsync(order.TeamId.Value);
                if (team == null) throw new Exception("Team not found.");
                if (!team.IsActive) throw new Exception("Team is not active for trading.");
            }

            // Additional validation for SELL orders: user must own enough shares
            if (order.Type == OrderType.Sell)
            {
                var holding = await _userPortfolioRepository.GetUserPortfolioItemAsync(order.UserId, order.PlayerId.GetValueOrDefault());
                if (holding == null || holding.Shares < order.Shares) throw new Exception("Insufficient shares to sell.");
            }
        }

        private async Task UpdateUserPortfolio(int userId, int? playerId, int? teamId, int shares, decimal price, OrderType orderType)
        {
            var holding = await _userPortfolioRepository.GetUserPortfolioItemAsync(userId, playerId.GetValueOrDefault());

            if (orderType == OrderType.Buy)
            {
                if (holding == null)
                {
                    await _userPortfolioRepository.AddAsync(new UserPortfolio
                    {
                        UserId = userId,
                        PlayerId = playerId,
                        TeamId = teamId,
                        Shares = shares,
                        AveragePrice = price,
                        CreatedAt = DateTime.UtcNow,
                        UpdatedAt = DateTime.UtcNow
                    });
                }
                else
                {
                    holding.AveragePrice = ((holding.AveragePrice * holding.Shares) + (price * shares)) / (holding.Shares + shares);
                    holding.Shares += shares;
                    holding.UpdatedAt = DateTime.UtcNow;
                    await _userPortfolioRepository.UpdateAsync(holding);
                }
            }
            else if (orderType == OrderType.Sell)
            {
                if (holding == null || holding.Shares < shares) throw new Exception("Error: Selling more shares than owned.");

                holding.Shares -= shares;
                holding.UpdatedAt = DateTime.UtcNow;

                if (holding.Shares == 0)
                {
                    await _userPortfolioRepository.DeleteAsync(holding); // If all shares sold, remove from portfolio
                }
                else
                {
                    await _userPortfolioRepository.UpdateAsync(holding);
                }
            }
        }

        // Dummy implementation for now, will be implemented fully later
        public Task<bool> ApplyStopLossAsync(int userId, int? playerId, int? teamId, decimal stopLossPrice)
        {
            _logger.LogInformation($"Applying stop-loss for user {userId} on asset (PlayerId: {playerId}, TeamId: {teamId}) at price {stopLossPrice}");
            return Task.FromResult(true);
        }

        public Task<bool> ApplyTakeProfitAsync(int userId, int? playerId, int? teamId, decimal takeProfitPrice)
        {
            _logger.LogInformation($"Applying take-profit for user {userId} on asset (PlayerId: {playerId}, TeamId: {teamId}) at price {takeProfitPrice}");
            return Task.FromResult(true);
        }

        private async Task HandleTradeExecutedAsync(Order buyOrder, Order sellOrder, int shares, decimal tradePrice)
        {
            await ExecuteTradeAsync(buyOrder, sellOrder, shares, tradePrice);
        }
    }
}
