using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Repositories
{
    public class MatchRepository : BaseRepository<Models.Match>, IMatchRepository
    {
        public MatchRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Models.Match>> GetRecentMatchesAsync(int? playerId = null, int? teamId = null, int count = 10)
        {
            var query = _context.Matches.AsQueryable();

            if (playerId.HasValue)
            {
                query = query.Where(m => m.PlayerId == playerId.Value);
            }

            if (teamId.HasValue)
            {
                query = query.Where(m => m.TeamId == teamId.Value);
            }

            return await query.OrderByDescending(m => m.MatchDate).Take(count).ToListAsync();
        }

        public async Task<IEnumerable<Models.Match>> GetMatchesByPlayerIdAsync(int playerId)
        {
            return await _context.Matches.Where(m => m.PlayerId == playerId).ToListAsync();
        }

        public async Task<IEnumerable<Models.Match>> GetMatchesByTeamIdAsync(int teamId)
        {
            return await _context.Matches.Where(m => m.TeamId == teamId).ToListAsync();
        }
    }
}
