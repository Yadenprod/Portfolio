using GamingStockMarket.API.DTOs;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IAnalyticsService
    {
        Task<AnalyticsResponse> GetOverallAnalyticsAsync();
        Task<IEnumerable<DailyMetric>> GetDailyTradingVolumeAsync(int days);
        Task<IEnumerable<DailyMetric>> GetDailyNewUsersAsync(int days);
    }
}
