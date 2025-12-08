using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using System;
using System.Threading;
using System.Threading.Tasks;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Services.Interfaces;
using GamingStockMarket.API.Repositories;

namespace GamingStockMarket.API.BackgroundServices
{
    public class PriceUpdateService : BackgroundService
    {
        private readonly IServiceProvider _serviceProvider;
        private readonly ILogger<PriceUpdateService> _logger;
        private readonly TimeSpan _updateInterval = TimeSpan.FromMinutes(5);

        public PriceUpdateService(IServiceProvider serviceProvider, ILogger<PriceUpdateService> logger)
        {
            _serviceProvider = serviceProvider;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Price Update Service started.");

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    using (var scope = _serviceProvider.CreateScope())
                    {
                        var priceCalculator = scope.ServiceProvider.GetRequiredService<IPriceCalculator>();
                        var playerRepository = scope.ServiceProvider.GetRequiredService<IPlayerRepository>();
                        var teamRepository = scope.ServiceProvider.GetRequiredService<ITeamRepository>();
                        var priceHistoryRepository = scope.ServiceProvider.GetRequiredService<IPriceHistoryRepository>();

                        // Update player prices
                        var players = await playerRepository.GetActivePlayersByGameAsync("");
                        foreach (var player in players)
                        {
                            var newPrice = await priceCalculator.CalculatePlayerPriceAsync(player.Id);
                            if (Math.Abs(newPrice - player.CurrentPrice) > 0.01m) // Check for significant change
                            {
                                var oldPrice = player.CurrentPrice;
                                player.CurrentPrice = newPrice;
                                await playerRepository.UpdateAsync(player);

                                await priceHistoryRepository.AddAsync(new Models.PriceHistory
                                {
                                    PlayerId = player.Id,
                                    Price = newPrice,
                                    Volume = 0, // Volume updated by trading engine
                                    RecordedAt = DateTime.UtcNow
                                });
                                _logger.LogInformation($"Player {player.Name} price updated: ${oldPrice:F2} -> ${newPrice:F2}");
                            }
                        }

                        // Update team prices
                        var teams = await teamRepository.GetActiveTeamsByGameAsync("");
                        foreach (var team in teams)
                        {
                            var newPrice = await priceCalculator.CalculateTeamPriceAsync(team.Id);
                            if (Math.Abs(newPrice - team.CurrentPrice) > 0.01m) // Check for significant change
                            {
                                var oldPrice = team.CurrentPrice;
                                team.CurrentPrice = newPrice;
                                await teamRepository.UpdateAsync(team);

                                await priceHistoryRepository.AddAsync(new Models.PriceHistory
                                {
                                    TeamId = team.Id,
                                    Price = newPrice,
                                    Volume = 0, // Volume updated by trading engine
                                    RecordedAt = DateTime.UtcNow
                                });
                                _logger.LogInformation($"Team {team.Name} price updated: ${oldPrice:F2} -> ${newPrice:F2}");
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error occurred in Price Update Service.");
                }

                await Task.Delay(_updateInterval, stoppingToken);
            }

            _logger.LogInformation("Price Update Service stopped.");
        }
    }
}
