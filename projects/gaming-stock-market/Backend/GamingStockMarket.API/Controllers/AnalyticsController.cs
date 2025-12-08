using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.Services.Interfaces;
using GamingStockMarket.API.DTOs;
using Microsoft.AspNetCore.Authorization;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize(Roles = "Admin")] // Only administrators can access analytics
    public class AnalyticsController : ControllerBase
    {
        private readonly IAnalyticsService _analyticsService;
        private readonly ILogger<AnalyticsController> _logger;

        public AnalyticsController(IAnalyticsService analyticsService, ILogger<AnalyticsController> logger)
        {
            _analyticsService = analyticsService;
            _logger = logger;
        }

        [HttpGet("overall")]
        public async Task<ActionResult<AnalyticsResponse>> GetOverallAnalytics()
        {
            try
            {
                var analytics = await _analyticsService.GetOverallAnalyticsAsync();
                return Ok(analytics);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting overall analytics.");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpGet("daily-trading-volume")]
        public async Task<ActionResult<IEnumerable<DailyMetric>>> GetDailyTradingVolume([FromQuery] int days = 7)
        {
            try
            {
                var data = await _analyticsService.GetDailyTradingVolumeAsync(days);
                return Ok(data);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting daily trading volume.");
                return StatusCode(500, "Internal server error");
            }
        }

        [HttpGet("daily-new-users")]
        public async Task<ActionResult<IEnumerable<DailyMetric>>> GetDailyNewUsers([FromQuery] int days = 7)
        {
            try
            {
                var data = await _analyticsService.GetDailyNewUsersAsync(days);
                return Ok(data);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting daily new users.");
                return StatusCode(500, "Internal server error");
            }
        }
    }
}
