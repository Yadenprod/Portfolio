using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using GamingStockMarket.API.Services.Interfaces; // Added for IPriceCalculator

namespace GamingStockMarket.API.Services
{
    public class PriceCalculator : IPriceCalculator
    {
        private readonly IPlayerRepository _playerRepository;
        private readonly ITeamRepository _teamRepository;
        private readonly IMatchRepository _matchRepository;
        private readonly IPriceHistoryRepository _priceHistoryRepository;
        private readonly ILogger<PriceCalculator> _logger;

        public PriceCalculator(IPlayerRepository playerRepository, ITeamRepository teamRepository, 
                               IMatchRepository matchRepository, IPriceHistoryRepository priceHistoryRepository,
                               ILogger<PriceCalculator> logger)
        {
            _playerRepository = playerRepository;
            _teamRepository = teamRepository;
            _matchRepository = matchRepository;
            _priceHistoryRepository = priceHistoryRepository;
            _logger = logger;
        }

        public async Task<decimal> CalculatePlayerPriceAsync(int playerId)
        {
            var player = await _playerRepository.GetByIdAsync(playerId);
            if (player == null) throw new Exception($"Player with ID {playerId} not found.");

            var recentMatches = (await _matchRepository.GetRecentMatchesAsync(playerId: playerId, count: 10)).ToList();
            var priceHistory = (await _priceHistoryRepository.GetPriceHistoryForPlayerAsync(playerId: playerId, days: 7)).ToList();

            var basePrice = player.BasePrice;
            
            // Factor 1: Recent Performance (40% weight)
            var performanceMultiplier = CalculatePerformanceMultiplier(recentMatches);
            
            // Factor 2: Tournament Success (30% weight)
            var tournamentMultiplier = CalculateTournamentMultiplier(recentMatches);
            
            // Factor 3: Popularity (20% weight) - Simplified, in real app would fetch from external APIs
            var popularityMultiplier = CalculatePopularityMultiplier(player.PopularityScore);
            
            // Factor 4: Team Factor (10% weight)
            var teamMultiplier = await CalculateTeamFactorMultiplier(player.Team); // Assuming player.Team is string for now

            // Factor 5: Trading Volume (dynamic factor) - Simple moving average of price changes
            var volumeMultiplier = CalculateTradingVolumeMultiplier(priceHistory);

            // Factor 6: Market Volatility (dynamic factor)
            var volatilityMultiplier = CalculateVolatilityMultiplier(priceHistory);

            var finalPrice = basePrice * performanceMultiplier * tournamentMultiplier * 
                             popularityMultiplier * teamMultiplier * volumeMultiplier * volatilityMultiplier;

            // Add protection against sharp price jumps (e.g., limit daily change to 100%)
            var maxChange = player.CurrentPrice * 1.0m; // Allow 100% up/down for now, refine later
            if (finalPrice > player.CurrentPrice + maxChange) finalPrice = player.CurrentPrice + maxChange;
            if (finalPrice < player.CurrentPrice - maxChange) finalPrice = player.CurrentPrice - maxChange;

            _logger.LogInformation($"Calculated price for player {player.Name}: {finalPrice:F2}");

            return finalPrice;
        }

        public async Task<decimal> CalculateTeamPriceAsync(int teamId)
        {
            var team = await _teamRepository.GetByIdAsync(teamId);
            if (team == null) throw new Exception($"Team with ID {teamId} not found.");

            var recentMatches = (await _matchRepository.GetRecentMatchesAsync(teamId: teamId, count: 10)).ToList();
            var priceHistory = (await _priceHistoryRepository.GetPriceHistoryForTeamAsync(teamId: teamId, days: 7)).ToList();

            var basePrice = team.BasePrice;

            // Factors (similar to player, but team-focused)
            var performanceMultiplier = CalculatePerformanceMultiplier(recentMatches); // Based on team match results
            var tournamentMultiplier = CalculateTournamentMultiplier(recentMatches);
            var popularityMultiplier = 1.0m; // Placeholder for team popularity
            var volumeMultiplier = CalculateTradingVolumeMultiplier(priceHistory);
            var volatilityMultiplier = CalculateVolatilityMultiplier(priceHistory);

            var finalPrice = basePrice * performanceMultiplier * tournamentMultiplier * 
                             popularityMultiplier * volumeMultiplier * volatilityMultiplier;

            // Add protection against sharp price jumps
            var maxChange = team.CurrentPrice * 1.0m; 
            if (finalPrice > team.CurrentPrice + maxChange) finalPrice = team.CurrentPrice + maxChange;
            if (finalPrice < team.CurrentPrice - maxChange) finalPrice = team.CurrentPrice - maxChange;

            _logger.LogInformation($"Calculated price for team {team.Name}: {finalPrice:F2}");

            return finalPrice;
        }

        private decimal CalculatePerformanceMultiplier(List<Models.Match> matches)
        {
            decimal multiplier = 1.0m;
            foreach (var match in matches)
            {
                if (match.Result == "WIN") multiplier *= 1.05m; // +5%
                else if (match.Result == "LOSS") multiplier *= 0.95m; // -5%

                if (match.PlayerRating > 1.3m) multiplier *= 1.02m; // +2% for high rating
                else if (match.PlayerRating < 0.8m) multiplier *= 0.98m; // -2% for low rating

                if (match.IsMVP) multiplier *= 1.03m; // +3% for MVP
            }
            return multiplier;
        }

        private decimal CalculateTournamentMultiplier(List<Models.Match> matches)
        {
            decimal multiplier = 1.0m;
            foreach (var match in matches.Where(m => m.TournamentTier.HasValue))
            {
                switch (match.TournamentTier.Value)
                {
                    case 1: // Major
                        multiplier *= 1.15m; // Significant boost
                        break;
                    case 2: // Tier 1
                        multiplier *= 1.07m; // Moderate boost
                        break;
                    case 3: // Tier 2
                        multiplier *= 1.03m; // Small boost
                        break;
                }
            }
            return multiplier;
        }

        private decimal CalculatePopularityMultiplier(int popularityScore)
        {
            // Simplified: 0.1% for every 1000 popularity points
            return 1.0m + (popularityScore / 1000m * 0.001m);
        }

        private async Task<decimal> CalculateTeamFactorMultiplier(string? teamName)
        {
            if (string.IsNullOrEmpty(teamName)) return 1.0m;

            var topTeams = (await _teamRepository.GetAllAsync()).OrderByDescending(t => t.Ranking).Take(5).Select(t => t.Name).ToList();

            if (topTeams.Contains(teamName)) return 1.10m; // Top 5 team: +10%

            return 1.0m;
        }

        private decimal CalculateTradingVolumeMultiplier(List<Models.PriceHistory> priceHistory)
        {
            if (priceHistory.Count < 2) return 1.0m;

            // Simple example: average of recent price changes
            decimal totalChange = 0;
            for (int i = 1; i < priceHistory.Count; i++)
            {
                totalChange += Math.Abs(priceHistory[i].Price - priceHistory[i - 1].Price);
            }
            var averageChange = totalChange / (priceHistory.Count - 1);

            // If average change is high, price is more sensitive to volume (example logic)
            return 1.0m + (averageChange * 0.1m); 
        }

        private decimal CalculateVolatilityMultiplier(List<Models.PriceHistory> priceHistory)
        {
            if (priceHistory.Count < 2) return 1.0m;

            // Simple example: standard deviation of recent prices
            var prices = priceHistory.Select(ph => (double)ph.Price).ToList();
            var average = prices.Average();
            var sumOfSquaresOfDifferences = prices.Select(val => (val - average) * (val - average)).Sum();
            var standardDeviation = Math.Sqrt(sumOfSquaresOfDifferences / prices.Count);

            // Higher volatility means higher multiplier (more dynamic pricing)
            return 1.0m + (decimal)standardDeviation * 0.05m; 
        }
    }
}
