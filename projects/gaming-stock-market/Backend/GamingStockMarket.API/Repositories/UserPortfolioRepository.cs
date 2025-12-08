using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;

namespace GamingStockMarket.API.Repositories
{
    public class UserPortfolioRepository : BaseRepository<UserPortfolio>, IUserPortfolioRepository
    {
        public UserPortfolioRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<UserPortfolio>> GetUserPortfolioAsync(int userId)
        {
            return await _context.UserPortfolios
                .Where(up => up.UserId == userId)
                .Include(up => up.Player)
                .ThenInclude(p => p.Team)
                .ToListAsync();
        }

        public async Task<UserPortfolio?> GetUserPortfolioItemAsync(int userId, int playerId)
        {
            return await _context.UserPortfolios
                .FirstOrDefaultAsync(up => up.UserId == userId && up.PlayerId == playerId);
        }
    }
}
