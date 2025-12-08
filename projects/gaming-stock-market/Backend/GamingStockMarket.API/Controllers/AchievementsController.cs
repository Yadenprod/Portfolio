using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Extensions;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using GamingStockMarket.API.Services.Interfaces; // Added for IAchievementService

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class AchievementsController : ControllerBase
    {
        private readonly IAchievementService _achievementService;
        private readonly ILogger<AchievementsController> _logger;

        public AchievementsController(IAchievementService achievementService, ILogger<AchievementsController> logger)
        {
            _achievementService = achievementService;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<Models.Achievement>>> GetUserAchievements()
        {
            try
            {
                var userId = User.GetUserId();
                var achievements = await _achievementService.GetUserAchievementsAsync(userId);
                return Ok(achievements);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting achievements for user {UserId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<Models.Achievement>> GetAchievementById(int id)
        {
            try
            {
                var userId = User.GetUserId();
                var achievement = await _achievementService.GetAchievementByIdAsync(id);
                if (achievement == null || achievement.UserId != userId) return NotFound(new { message = "Achievement not found or unauthorized." });
                return Ok(achievement);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting achievement {AchievementId} for user {UserId}", id, User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }
    }
}
