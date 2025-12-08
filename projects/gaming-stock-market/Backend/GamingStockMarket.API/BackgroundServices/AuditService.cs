using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace GamingStockMarket.API.BackgroundServices
{
    public class AuditService : BackgroundService
    {
        private readonly ILogger<AuditService> _logger;
        private readonly TimeSpan _processInterval = TimeSpan.FromMinutes(10); // Process audit logs periodically

        public AuditService(ILogger<AuditService> logger)
        {
            _logger = logger;
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            _logger.LogInformation("Audit Service started.");

            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    // TODO: Implement audit log processing here
                    // This service would process raw audit log entries, potentially enriching them
                    // and moving them to a long-term storage or analytics system.
                    _logger.LogInformation("Audit Service: processing audit logs...");
                }
                catch (Exception ex)
                {
                    _logger.LogError(ex, "Error occurred in Audit Service.");
                }

                await Task.Delay(_processInterval, stoppingToken);
            }

            _logger.LogInformation("Audit Service stopped.");
        }
    }
}
