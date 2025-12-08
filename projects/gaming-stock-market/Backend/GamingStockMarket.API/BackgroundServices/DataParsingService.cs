using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using System;
using System.Threading;
using System.Threading.Tasks;
using GamingStockMarket.API.Services; // Added for CSGOParser
using GamingStockMarket.API.Services.Interfaces; // Added for IDataParser

namespace GamingStockMarket.API.BackgroundServices
{
    public class DataParsingService : BackgroundService
    {
        private readonly IServiceProvider _serviceProvider;
        private readonly ILogger<DataParsingService> _logger;
        private readonly TimeSpan _updateInterval = TimeSpan.FromHours(1); // Hourly data parsing

        public DataParsingService(IServiceProvider serviceProvider, ILogger<DataParsingService> logger)
        {
            _serviceProvider = serviceProvider;
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Data Parsing Service started.");

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    using (var scope = _serviceProvider.CreateScope())
                    {
                        var csgoParser = scope.ServiceProvider.GetRequiredService<CSGOParser>();
                        // Add other parsers here (e.g., Dota2Parser, ValorantParser)

                        await csgoParser.UpdatePlayerDataAsync();
                        await csgoParser.UpdateMatchesAsync();
                        await csgoParser.UpdateTeamDataAsync();
                    }
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error occurred in Data Parsing Service.");
                }

                await Task.Delay(_updateInterval, stoppingToken);
            }

            _logger.LogInformation("Data Parsing Service stopped.");
        }
    }
}
