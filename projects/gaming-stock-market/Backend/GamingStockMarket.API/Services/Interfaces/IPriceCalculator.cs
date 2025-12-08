using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IPriceCalculator
    {
        Task<decimal> CalculatePlayerPriceAsync(int playerId);
        Task<decimal> CalculateTeamPriceAsync(int teamId);
    }
}
