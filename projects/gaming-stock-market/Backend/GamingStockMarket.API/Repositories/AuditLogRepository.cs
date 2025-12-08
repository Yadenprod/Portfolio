using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;

namespace GamingStockMarket.API.Repositories
{
    public class AuditLogRepository : BaseRepository<AuditLog>, IAuditLogRepository
    {
        public AuditLogRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task LogActivityAsync(int userId, string activityType, string details)
        {
            await AddAsync(new AuditLog
            {
                UserId = userId,
                Action = activityType, // Исправлено на Action
                Details = details,
                Timestamp = DateTime.UtcNow
            });
        }

        public async Task<IEnumerable<AuditLog>> GetAuditLogsForUserAsync(int userId)
        {
            return await _context.AuditLogs.Where(al => al.UserId == userId).ToListAsync();
        }
    }
}
