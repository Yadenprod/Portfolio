using Microsoft.Extensions.Logging;
using System.Threading.Tasks;
using GamingStockMarket.API.Services.Interfaces; // Added for ITwoFactorAuthService

namespace GamingStockMarket.API.Services
{
    public class TwoFactorAuthService : ITwoFactorAuthService
    {
        private readonly ILogger<TwoFactorAuthService> _logger;

        public TwoFactorAuthService(ILogger<TwoFactorAuthService> logger)
        {
            _logger = logger;
        }

        public Task<string> GenerateSetupCodeAsync(int userId)
        {
            _logger.LogInformation($"Generating 2FA setup code for user {userId}. (Dummy implementation)");
            return Task.FromResult("DUMMY_2FA_CODE");
        }

        public Task<bool> VerifyCodeAsync(int userId, string code)
        {
            _logger.LogInformation($"Verifying 2FA code for user {userId}. Code: {code}. (Dummy implementation)");
            return Task.FromResult(true); // Simulate success
        }

        public Task<bool> IsTwoFactorEnabledAsync(int userId)
        {
            _logger.LogInformation($"Checking 2FA status for user {userId}. (Dummy implementation)");
            return Task.FromResult(false); // Simulate not enabled by default
        }

        public Task EnableTwoFactorAuthAsync(int userId, string setupCode)
        {
            _logger.LogInformation($"Enabling 2FA for user {userId} with code {setupCode}. (Dummy implementation)");
            return Task.CompletedTask;
        }

        public Task DisableTwoFactorAuthAsync(int userId)
        {
            _logger.LogInformation($"Disabling 2FA for user {userId}. (Dummy implementation)");
            return Task.CompletedTask;
        }
    }
}
