using System.Threading.Tasks;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Services.Interfaces;
using Microsoft.Extensions.Logging;
using GamingStockMarket.API.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;

namespace GamingStockMarket.API.Services
{
    public class AchievementService : IAchievementService
    {
        private readonly IAchievementRepository _achievementRepository;
        private readonly IUserRepository _userRepository;
        private readonly ITradeRepository _tradeRepository;
        private readonly ITransactionRepository _transactionRepository;
        private readonly IUserPortfolioRepository _userPortfolioRepository; // Added for portfolio access
        private readonly ILogger<AchievementService> _logger;

        public AchievementService(IAchievementRepository achievementRepository, IUserRepository userRepository,
                                  ITradeRepository tradeRepository, ITransactionRepository transactionRepository,
                                  IUserPortfolioRepository userPortfolioRepository, // Added to constructor
                                  ILogger<AchievementService> logger)
        {
            _achievementRepository = achievementRepository;
            _userRepository = userRepository;
            _tradeRepository = tradeRepository;
            _transactionRepository = transactionRepository;
            _userPortfolioRepository = userPortfolioRepository; // Initialize
            _logger = logger;
        }

        public async Task<IEnumerable<Achievement>> GetUserAchievementsAsync(int userId)
        {
            return await _achievementRepository.GetAchievementsForUserAsync(userId);
        }

        public async Task<Achievement?> GetAchievementByIdAsync(int achievementId)
        {
            return await _achievementRepository.GetByIdAsync(achievementId);
        }

        public async Task GrantAchievementAsync(int userId, AchievementType type, decimal? reward = null, string? relatedData = null)
        {
            var existingAchievement = await _achievementRepository.GetAchievementByNameAsync(type.ToString());
            // Need to check if user *already has* this specific achievement, not just if it exists globally
            // This logic needs to be refined if UserAchievement is a separate join entity
            if (existingAchievement != null) 
            {
                var userAchievements = await _achievementRepository.GetAchievementsForUserAsync(userId);
                if (userAchievements.Any(a => a.Id == existingAchievement.Id))
                {
                    _logger.LogInformation($"User {userId} already has achievement {type}. Skipping.");
                    return; // User already has this achievement
                }
            }

            var achievement = new Achievement
            {
                UserId = userId,
                Type = type,
                Name = type.ToString(), // Simple name for now
                Description = GetAchievementDescription(type), // Helper method to get description
                AchievedAt = DateTime.UtcNow,
                RewardAmount = reward,
                RelatedData = relatedData
            };
            await _achievementRepository.AddAsync(achievement);

            // If there's a reward, add it to user's balance
            if (reward.HasValue && reward.Value > 0)
            {
                var user = await _userRepository.GetByIdAsync(userId);
                if (user != null)
                {
                    user.Balance += reward.Value;
                    await _userRepository.UpdateAsync(user);
                    await _transactionRepository.AddAsync(new Models.Transaction
                    {
                        UserId = userId,
                        Type = Models.TransactionType.Bonus,
                        Amount = reward.Value,
                        Status = "COMPLETED",
                        Notes = $"Achievement reward: {type}",
                        CreatedAt = DateTime.UtcNow,
                        CompletedAt = DateTime.UtcNow
                    });
                    _logger.LogInformation($"User {userId} granted {type} achievement with reward {reward.Value}.");
                }
            }
            else
            {
                _logger.LogInformation($"User {userId} granted {type} achievement.");
            }
        }

        public async Task CheckAndGrantAchievementsAsync(int userId)
        {
            // Check for FirstTrade
            var userTrades = await _tradeRepository.GetUserTradesAsync(userId);
            if (userTrades.Any() && !(await _achievementRepository.GetAchievementsForUserAsync(userId)).Any(a => a.Name == AchievementType.FirstTrade.ToString()))
            {
                await GrantAchievementAsync(userId, AchievementType.FirstTrade, 10m);
            }

            // Check for SuccessfulTrader (e.g., 10% profit overall)
            var portfolio = await _userPortfolioRepository.GetUserPortfolioAsync(userId); // Assuming this gives average buy price
            // This logic is complex and needs current prices to accurately calculate profit. Placeholder for now.
            decimal totalInvested = 0; // sum of (holding.Shares * holding.AveragePrice)
            decimal currentPortfolioValue = 0; // sum of (holding.Shares * current_market_price)
            // For demonstration, let's assume a simplified check.
            if (portfolio.Any() && (currentPortfolioValue > totalInvested * 1.10m) && !(await _achievementRepository.GetAchievementsForUserAsync(userId)).Any(a => a.Name == AchievementType.SuccessfulTrader.ToString()))
            {
                await GrantAchievementAsync(userId, AchievementType.SuccessfulTrader, 25m);
            }

            // Implement checks for other achievements (ExpertTrader, LegendTrader, TopTraderOfMonth, etc.)
            // This would involve more complex queries against trade history, portfolio, and potentially external data.
            _logger.LogInformation($"Checked achievements for user {userId}.");
        }

        private string GetAchievementDescription(AchievementType type)
        {
            return type switch
            {
                AchievementType.FirstTrade => "Make your first trade on the platform.",
                AchievementType.SuccessfulTrader => "Achieve 10% overall profit.",
                AchievementType.ExpertTrader => "Achieve 50% overall profit.",
                AchievementType.LegendTrader => "Achieve 100% overall profit.",
                AchievementType.TopTraderOfMonth => "Be among the top traders of the month.",
                AchievementType.ReferralBonus => "Successfully refer a friend.",
                AchievementType.DailyLoginStreak => "Log in for consecutive days.",
                _ => "No description available."
            };
        }
    }
}
