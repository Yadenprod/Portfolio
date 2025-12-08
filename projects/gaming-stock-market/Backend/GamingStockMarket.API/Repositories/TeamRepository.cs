using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;

namespace GamingStockMarket.API.Repositories
{
    public class TeamRepository : BaseRepository<Team>, ITeamRepository
    {
        public TeamRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<Team?> GetByIdWithPlayersAsync(int id)
        {
            return await _context.Teams
                .Include(t => t.Players)
                .FirstOrDefaultAsync(t => t.Id == id);
        }

        public async Task<IEnumerable<Team>> GetActiveTeamsByGameAsync(string game)
        {
            return await _context.Teams
                .Where(t => t.Game == game && t.IsActive)
                .ToListAsync();
        }
    }
}
