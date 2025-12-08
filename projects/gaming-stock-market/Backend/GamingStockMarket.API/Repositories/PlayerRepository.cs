using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;

namespace GamingStockMarket.API.Repositories
{
    public class PlayerRepository : BaseRepository<Player>, IPlayerRepository
    {
        public PlayerRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<Player?> GetByIdWithDetailsAsync(int id)
        {
            return await _context.Players
                .Include(p => p.Team)
                .FirstOrDefaultAsync(p => p.Id == id);
        }

        public async Task<IEnumerable<Player>> GetActivePlayersByGameAsync(string game)
        {
            return await _context.Players
                .Where(p => p.Game == game && p.IsActive)
                .ToListAsync();
        }

        public async Task<IEnumerable<Player>> GetAllPlayersWithDetailsAsync()
        {
            return await _context.Players
                .Include(p => p.Team)
                .ToListAsync();
        }
    }
}
