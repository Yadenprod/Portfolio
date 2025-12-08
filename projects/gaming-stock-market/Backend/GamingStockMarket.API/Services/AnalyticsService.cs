using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Services.Interfaces; // Added for IAnalyticsService
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using GamingStockMarket.API.Repositories;

namespace GamingStockMarket.API.Services
{
    public class AnalyticsService : IAnalyticsService
    {
        private readonly IUserRepository _userRepository;
        private readonly ITradeRepository _tradeRepository;
        private readonly ILogger<AnalyticsService> _logger;

        public AnalyticsService(IUserRepository userRepository, ITradeRepository tradeRepository, ILogger<AnalyticsService> logger)
        {
            _userRepository = userRepository;
            _tradeRepository = tradeRepository;
            _logger = logger;
        }

        public async Task<AnalyticsResponse> GetOverallAnalyticsAsync()
        {
            var totalUsers = (await _userRepository.GetAllAsync()).Count();
            var activeUsers = (await _userRepository.GetAllAsync()).Count(u => u.IsActive && u.LastLoginAt.HasValue && u.LastLoginAt.Value > DateTime.UtcNow.AddDays(-30)); // Active in last 30 days
            
            // Simplified total trading volume - sum of all trade amounts
            var allTrades = await _tradeRepository.GetAllAsync();
            var totalTradingVolume = allTrades.Sum(t => t.Shares * t.Price);

            return new AnalyticsResponse
            {
                TotalUsers = totalUsers,
                ActiveUsers = activeUsers,
                TotalTradingVolume = totalTradingVolume,
                DailyTradingVolume = new List<DailyMetric>(), // To be populated by other methods
                DailyNewUsers = new List<DailyMetric>() // To be populated by other methods
            };
        }

        public async Task<IEnumerable<DailyMetric>> GetDailyTradingVolumeAsync(int days)
        {
            var startDate = DateTime.UtcNow.AddDays(-days);
            var trades = (await _tradeRepository.GetAllAsync()).Where(t => t.CreatedAt >= startDate).ToList();

            var dailyVolume = trades
                .GroupBy(t => t.CreatedAt.Date)
                .Select(g => new DailyMetric
                {
                    Date = g.Key,
                    Value = g.Sum(t => t.Shares * t.Price)
                })
                .OrderBy(d => d.Date)
                .ToList();

            return dailyVolume;
        }

        public async Task<IEnumerable<DailyMetric>> GetDailyNewUsersAsync(int days)
        {
            var startDate = DateTime.UtcNow.AddDays(-days);
            var users = (await _userRepository.GetAllAsync()).Where(u => u.CreatedAt >= startDate).ToList();

            var dailyNewUsers = users
                .GroupBy(u => u.CreatedAt.Date)
                .Select(g => new DailyMetric
                {
                    Date = g.Key,
                    Value = g.Count()
                })
                .OrderBy(d => d.Date)
                .ToList();

            return dailyNewUsers;
        }
    }
}
