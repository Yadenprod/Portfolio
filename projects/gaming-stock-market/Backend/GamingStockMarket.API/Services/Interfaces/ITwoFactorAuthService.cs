using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface ITwoFactorAuthService
    {
        Task<string> GenerateSetupCodeAsync(int userId);
        Task<bool> VerifyCodeAsync(int userId, string code);
        Task<bool> IsTwoFactorEnabledAsync(int userId);
        Task EnableTwoFactorAuthAsync(int userId, string secret);
        Task DisableTwoFactorAuthAsync(int userId);
    }
}
