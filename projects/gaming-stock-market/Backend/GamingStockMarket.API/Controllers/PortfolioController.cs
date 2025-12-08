using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Extensions;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using GamingStockMarket.API.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class PortfolioController : ControllerBase
    {
        private readonly ITradingService _tradingService;
        private readonly ITransactionRepository _transactionRepository;
        private readonly ILogger<PortfolioController> _logger;

        public PortfolioController(ITradingService tradingService, ITransactionRepository transactionRepository, ILogger<PortfolioController> logger)
        {
            _tradingService = tradingService;
            _transactionRepository = transactionRepository;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<PortfolioResponse>> GetUserPortfolio()
        {
            try
            {
                var userId = User.GetUserId();
                var portfolio = await _tradingService.GetUserPortfolioAsync(userId);
                // The TradingService.GetUserPortfolioAsync already calculates total value.
                // It also requires IUserService, IPlayerRepository, ITeamRepository to be injected into TradingService.
                // For now, PortfolioResponse already contains these details. No further calculation here.
                return Ok(portfolio);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting portfolio for user {UserId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("transactions")]
        public async Task<ActionResult<IEnumerable<Models.Transaction>>> GetUserTransactions(
            [FromQuery] Models.TransactionType? type = null, [FromQuery] string? status = null, 
            [FromQuery] int pageNumber = 1, [FromQuery] int pageSize = 10)
        {
            try
            {
                var userId = User.GetUserId();
                var transactions = await _transactionRepository.GetUserTransactionsAsync(userId, type, status, pageNumber, pageSize);
                return Ok(transactions);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting transactions for user {UserId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }
    }
}
