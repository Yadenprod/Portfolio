using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Extensions;
using GamingStockMarket.API.Repositories;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using GamingStockMarket.API.Models; // Added for OrderStatus and Models.Player
using GamingStockMarket.API.Services.Interfaces; // Added for IUserService

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize(Roles = "Admin")] // Only administrators can access these endpoints
    public class AdminController : ControllerBase
    {
        private readonly IUserService _userService;
        private readonly IPlayerRepository _playerRepository;
        private readonly ITeamRepository _teamRepository;
        private readonly IOrderRepository _orderRepository;
        private readonly ITransactionRepository _transactionRepository;
        private readonly IAuditLogRepository _auditLogRepository;
        private readonly ILogger<AdminController> _logger;

        public AdminController(IUserService userService, IPlayerRepository playerRepository, ITeamRepository teamRepository,
                               IOrderRepository orderRepository, ITransactionRepository transactionRepository, IAuditLogRepository auditLogRepository,
                               ILogger<AdminController> logger)
        {
            _userService = userService;
            _playerRepository = playerRepository;
            _teamRepository = teamRepository;
            _orderRepository = orderRepository;
            _transactionRepository = transactionRepository;
            _auditLogRepository = auditLogRepository;
            _logger = logger;
        }

        // User Management
        [HttpGet("users")]
        public async Task<ActionResult<IEnumerable<Models.User>>> GetUsers([FromQuery] int pageNumber = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                var users = await _userService.GetAllUsersAsync(pageNumber, pageSize);
                return Ok(users);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting users by admin {AdminId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("users/{id}")]
        public async Task<ActionResult<Models.User>> GetUserById(int id)
        {
            try
            {
                var user = await _userService.GetByIdAsync(id);
                if (user == null) return NotFound(new { message = "User not found." });
                return Ok(user);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting user {UserId} by admin {AdminId}", id, User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpPut("users/{id}")]
        public async Task<ActionResult> UpdateUser(int id, [FromBody] UpdateUserRequest request)
        {
            try
            {
                await _userService.UpdateUserAsync(id, request);
                _logger.LogInformation("User {UserId} updated by admin {AdminId}", id, User.GetUserId());
                return Ok(new { message = "User updated successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating user {UserId} by admin {AdminId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        // Player Management
        [HttpPost("players")]
        public async Task<ActionResult<PlayerResponse>> CreatePlayer([FromBody] CreatePlayerRequest request)
        {
            try
            {
                var player = new Models.Player
                {
                    Name = request.Name,
                    Game = request.Game,
                    Team = request.Team,
                    BasePrice = request.BasePrice,
                    CurrentPrice = request.BasePrice, // Initial current price same as base price
                    LastUpdated = DateTime.UtcNow, // Использование LastUpdated вместо CreatedAt
                    IsActive = true,
                    Orders = new List<Models.Order>(), // Инициализация
                    Trades = new List<Models.Trade>(), // Инициализация
                    PortfolioHoldings = new List<Models.UserPortfolio>(), // Инициализация
                    Matches = new List<Models.Match>(), // Инициализация
                    PriceHistory = new List<Models.PriceHistory>() // Инициализация
                };
                await _playerRepository.AddAsync(player);
                _logger.LogInformation("Player {PlayerName} created by admin {AdminId}", player.Name, User.GetUserId());
                return CreatedAtAction(nameof(PlayersController.GetPlayerById), "Players", new { id = player.Id }, player); // Assuming PlayersController has GetPlayerById
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating player by admin {AdminId}", User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPut("players/{id}")]
        public async Task<ActionResult> UpdatePlayer(int id, [FromBody] UpdatePlayerRequest request)
        {
            try
            {
                var player = await _playerRepository.GetByIdAsync(id);
                if (player == null) return NotFound(new { message = "Player not found." });

                player.Name = request.Name;
                player.Game = request.Game;
                player.Team = request.Team;
                player.BasePrice = request.BasePrice;
                if (request.IsActive.HasValue) player.IsActive = request.IsActive.Value;
                player.LastUpdated = DateTime.UtcNow;

                await _playerRepository.UpdateAsync(player);
                _logger.LogInformation("Player {PlayerId} updated by admin {AdminId}", id, User.GetUserId());
                return Ok(new { message = "Player updated successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating player {PlayerId} by admin {AdminId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpDelete("players/{id}")]
        public async Task<ActionResult> DeletePlayer(int id)
        {
            try
            {
                var player = await _playerRepository.GetByIdAsync(id);
                if (player == null) return NotFound(new { message = "Player not found." });
                await _playerRepository.DeleteAsync(player);
                _logger.LogInformation("Player {PlayerId} deleted by admin {AdminId}", id, User.GetUserId());
                return Ok(new { message = "Player deleted successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting player {PlayerId} by admin {AdminId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        // Team Management
        [HttpPost("teams")]
        public async Task<ActionResult<TeamResponse>> CreateTeam([FromBody] CreateTeamRequest request)
        {
            try
            {
                var team = new Models.Team
                {
                    Name = request.Name,
                    Game = request.Game,
                    BasePrice = request.BasePrice,
                    CurrentPrice = request.BasePrice,
                    LastUpdated = DateTime.UtcNow, // Использование LastUpdated вместо CreatedAt
                    IsActive = true,
                    Orders = new List<Models.Order>(), // Инициализация
                    Trades = new List<Models.Trade>(), // Инициализация
                    PortfolioHoldings = new List<Models.UserPortfolio>(), // Инициализация
                    Matches = new List<Models.Match>(), // Инициализация
                    PriceHistory = new List<Models.PriceHistory>() // Инициализация
                };
                await _teamRepository.AddAsync(team);
                _logger.LogInformation("Team {TeamName} created by admin {AdminId}", team.Name, User.GetUserId());
                return CreatedAtAction(nameof(PlayersController.GetTeamById), "Players", new { id = team.Id }, team); // Assuming PlayersController has GetTeamById
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error creating team by admin {AdminId}", User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPut("teams/{id}")]
        public async Task<ActionResult> UpdateTeam(int id, [FromBody] UpdateTeamRequest request)
        {
            try
            {
                var team = await _teamRepository.GetByIdAsync(id);
                if (team == null) return NotFound(new { message = "Team not found." });

                team.Name = request.Name;
                team.Game = request.Game;
                team.BasePrice = request.BasePrice;
                if (request.IsActive.HasValue) team.IsActive = request.IsActive.Value;
                team.LastUpdated = DateTime.UtcNow;

                await _teamRepository.UpdateAsync(team);
                _logger.LogInformation("Team {TeamId} updated by admin {AdminId}", id, User.GetUserId());
                return Ok(new { message = "Team updated successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating team {TeamId} by admin {AdminId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpDelete("teams/{id}")]
        public async Task<ActionResult> DeleteTeam(int id)
        {
            try
            {
                var team = await _teamRepository.GetByIdAsync(id);
                if (team == null) return NotFound(new { message = "Team not found." });
                await _teamRepository.DeleteAsync(team);
                _logger.LogInformation("Team {TeamId} deleted by admin {AdminId}", id, User.GetUserId());
                return Ok(new { message = "Team deleted successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting team {TeamId} by admin {AdminId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        // Order Management
        [HttpGet("orders")]
        public async Task<ActionResult<IEnumerable<Models.Order>>> GetAllOrders([FromQuery] int pageNumber = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                var orders = await _orderRepository.GetAllAsync();
                return Ok(orders);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting all orders by admin {AdminId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpPut("orders/{id}/status")]
        public async Task<ActionResult> UpdateOrderStatus(int id, [FromBody] string status)
        {
            try
            {
                var order = await _orderRepository.GetByIdAsync(id);
                if (order == null) return NotFound(new { message = "Order not found." });

                if (!Enum.TryParse(status, true, out OrderStatus newStatus))
                {
                    return BadRequest(new { message = "Invalid order status." });
                }

                order.Status = newStatus;
                await _orderRepository.UpdateAsync(order);
                _logger.LogInformation("Order {OrderId} status updated to {NewStatus} by admin {AdminId}", id, newStatus, User.GetUserId());
                return Ok(new { message = "Order status updated successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error updating order {OrderId} status by admin {AdminId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        // Transaction Management
        [HttpGet("transactions")]
        public async Task<ActionResult<IEnumerable<Models.Transaction>>> GetAllTransactions([FromQuery] int pageNumber = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                var transactions = await _transactionRepository.GetAllAsync();
                return Ok(transactions);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting all transactions by admin {AdminId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        // Audit Logs
        [HttpGet("audit-logs")]
        public async Task<ActionResult<IEnumerable<Models.AuditLog>>> GetAuditLogs([FromQuery] int pageNumber = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                var auditLogs = await _auditLogRepository.GetAllAsync();
                return Ok(auditLogs);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting audit logs by admin {AdminId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }
    }
}
