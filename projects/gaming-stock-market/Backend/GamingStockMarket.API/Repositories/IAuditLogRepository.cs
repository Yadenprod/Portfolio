using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface IAuditLogRepository : IBaseRepository<AuditLog>
    {
        Task LogActivityAsync(int userId, string activityType, string details);
        Task<IEnumerable<AuditLog>> GetAuditLogsForUserAsync(int userId);
    }
}
