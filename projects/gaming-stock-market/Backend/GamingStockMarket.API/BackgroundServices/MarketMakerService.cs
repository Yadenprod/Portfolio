using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace GamingStockMarket.API.BackgroundServices
{
    public class MarketMakerService : BackgroundService
    {
        private readonly ILogger<MarketMakerService> _logger;
        private readonly TimeSpan _checkInterval = TimeSpan.FromMinutes(1);

        public MarketMakerService(ILogger<MarketMakerService> logger)
        {
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Market Maker Service started.");

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    // TODO: Implement market making logic here
                    // This service would place synthetic buy/sell orders to provide liquidity
                    // and stabilize prices, especially for less popular assets.
                    _logger.LogInformation("Market Maker Service: checking market liquidity...");
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error occurred in Market Maker Service.");
                }

                await Task.Delay(_checkInterval, stoppingToken);
            }

            _logger.LogInformation("Market Maker Service stopped.");
        }
    }
}
