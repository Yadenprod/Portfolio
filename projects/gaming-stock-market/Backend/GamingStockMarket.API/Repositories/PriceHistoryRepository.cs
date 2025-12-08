using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Repositories
{
    public class PriceHistoryRepository : BaseRepository<PriceHistory>, IPriceHistoryRepository
    {
        public PriceHistoryRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<PriceHistory>> GetPriceHistoryForPlayerAsync(int playerId, int days = 30)
        {
            return await _context.PriceHistory
                .Where(ph => ph.PlayerId == playerId && ph.RecordedAt >= DateTime.UtcNow.AddDays(-days))
                .OrderBy(ph => ph.RecordedAt)
                .ToListAsync();
        }

        public async Task<IEnumerable<PriceHistory>> GetPriceHistoryForTeamAsync(int teamId, int days = 30)
        {
            return await _context.PriceHistory
                .Where(ph => ph.TeamId == teamId && ph.RecordedAt >= DateTime.UtcNow.AddDays(-days))
                .OrderBy(ph => ph.RecordedAt)
                .ToListAsync();
        }
    }
}
