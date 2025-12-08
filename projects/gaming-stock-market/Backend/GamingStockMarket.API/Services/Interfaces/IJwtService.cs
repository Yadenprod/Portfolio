using GamingStockMarket.API.Models;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IJwtService
    {
        string GenerateJwtToken(User user);
        string GenerateRefreshToken();
        Task<(User user, string newToken, string newRefreshToken)> RefreshTokenAsync(string refreshToken);
    }
}
