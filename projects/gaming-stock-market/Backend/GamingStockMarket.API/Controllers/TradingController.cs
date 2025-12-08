using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Extensions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using GamingStockMarket.API.Services.Interfaces; // Added for ITradingService, IUserService
using GamingStockMarket.API.Repositories; // Added for IPlayerRepository, ITeamRepository

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class TradingController : ControllerBase
    {
        private readonly ITradingService _tradingService;
        private readonly IUserService _userService; // Added
        private readonly IPlayerRepository _playerRepository; // Added
        private readonly ITeamRepository _teamRepository; // Added
        private readonly ILogger<TradingController> _logger;

        public TradingController(ITradingService tradingService, ILogger<TradingController> logger, IUserService userService, IPlayerRepository playerRepository, ITeamRepository teamRepository) // Updated constructor
        {
            _tradingService = tradingService;
            _logger = logger;
            _userService = userService; // Initialize
            _playerRepository = playerRepository; // Initialize
            _teamRepository = teamRepository; // Initialize
        }

        [HttpPost("place-order")]
        public async Task<ActionResult<OrderResponse>> PlaceOrder([FromBody] PlaceOrderRequest request)
        {
            try
            {
                var userId = User.GetUserId();
                var order = new Models.Order
                {
                    UserId = userId,
                    PlayerId = request.PlayerId,
                    TeamId = request.TeamId,
                    Type = request.Type,
                    Shares = request.Shares,
                    Price = request.Price,
                    Status = Models.OrderStatus.Pending,
                    CreatedAt = DateTime.UtcNow,
                    UpdatedAt = DateTime.UtcNow,
                    BuyTrades = new List<Models.Trade>(), // Инициализация
                    SellTrades = new List<Models.Trade>() // Инициализация
                };

                var result = await _tradingService.PlaceOrderAsync(order);

                return Ok(new OrderResponse
                {
                    OrderId = result.Id,
                    Status = result.Status,
                    FilledShares = result.FilledShares
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error placing order for user {UserId}", User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("cancel-order/{orderId}")]
        public async Task<ActionResult> CancelOrder(int orderId)
        {
            try
            {
                var userId = User.GetUserId();
                await _tradingService.CancelOrderAsync(orderId, userId);
                return Ok(new { message = "Order cancelled successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error cancelling order {OrderId} for user {UserId}", orderId, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpGet("order-book")]
        public async Task<ActionResult<OrderBookResponse>> GetOrderBook([FromQuery] int? playerId = null, [FromQuery] int? teamId = null)
        {
            try
            {
                var (buyOrders, sellOrders) = await _tradingService.GetOrderBookAsync(playerId, teamId);
                return Ok(new OrderBookResponse
                {
                    PlayerId = playerId,
                    TeamId = teamId,
                    BuyOrders = buyOrders.Select(o => new OrderDto
                    {
                        OrderId = o.Id,
                        UserId = o.UserId,
                        Price = o.Price,
                        Quantity = o.Shares,
                        Type = o.Type.ToString(),
                        CreatedAt = o.CreatedAt
                    }).ToList(),
                    SellOrders = sellOrders.Select(o => new OrderDto
                    {
                        OrderId = o.Id,
                        UserId = o.UserId,
                        Price = o.Price,
                        Quantity = o.Shares,
                        Type = o.Type.ToString(),
                        CreatedAt = o.CreatedAt
                    }).ToList()
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting order book (PlayerId: {PlayerId}, TeamId: {TeamId})", playerId, teamId);
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("portfolio")]
        public async Task<ActionResult<PortfolioResponse>> GetPortfolio()
        {
            try
            {
                var userId = User.GetUserId();
                var portfolioHoldings = await _tradingService.GetUserPortfolioAsync(userId);
                var user = await _userService.GetByIdAsync(userId); // Assuming IUserService is available
                if (user == null) return NotFound(new { message = "User not found." });

                // Calculate total value (simplified for now)
                decimal totalValue = user.Balance;
                foreach (var holding in portfolioHoldings)
                {
                    // Need current price for each asset
                    decimal currentPrice = 0;
                    if (holding.PlayerId.HasValue)
                    {
                        var player = await _playerRepository.GetByIdAsync(holding.PlayerId.Value); // Assuming IPlayerRepository
                        if (player != null) currentPrice = player.CurrentPrice;
                    }
                    else if (holding.TeamId.HasValue)
                    {
                        var team = await _teamRepository.GetByIdAsync(holding.TeamId.Value); // Assuming ITeamRepository
                        if (team != null) currentPrice = team.CurrentPrice;
                    }
                    totalValue += holding.Shares * currentPrice;
                }

                return Ok(new PortfolioResponse
                {
                    UserId = userId,
                    Balance = user.Balance,
                    Holdings = portfolioHoldings,
                    TotalValue = totalValue
                });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting portfolio for user {UserId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("trade-history")]
        public async Task<ActionResult<IEnumerable<Models.Trade>>> GetTradeHistory()
        {
            try
            {
                var userId = User.GetUserId();
                var tradeHistory = await _tradingService.GetTradeHistoryAsync(userId);
                return Ok(tradeHistory);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting trade history for user {UserId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpPost("stop-loss")]
        public async Task<ActionResult> SetStopLoss([FromBody] StopLossRequest request)
        {
            try
            {
                var userId = User.GetUserId();
                await _tradingService.ApplyStopLossAsync(userId, request.PlayerId, request.TeamId, request.StopLossPrice);
                return Ok(new { message = "Stop-loss set successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error setting stop-loss for user {UserId}", User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("take-profit")]
        public async Task<ActionResult> SetTakeProfit([FromBody] TakeProfitRequest request)
        {
            try
            {
                var userId = User.GetUserId();
                await _tradingService.ApplyTakeProfitAsync(userId, request.PlayerId, request.TeamId, request.TakeProfitPrice);
                return Ok(new { message = "Take-profit set successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error setting take-profit for user {UserId}", User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }
    }

    // DTOs for StopLoss and TakeProfit requests
    public class StopLossRequest
    {
        public int? PlayerId { get; set; }
        public int? TeamId { get; set; }
        [Required]
        [Range(0.01, 10000.00)]
        public decimal StopLossPrice { get; set; }
    }

    public class TakeProfitRequest
    {
        public int? PlayerId { get; set; }
        public int? TeamId { get; set; }
        [Required]
        [Range(0.01, 10000.00)]
        public decimal TakeProfitPrice { get; set; }
    }
}
