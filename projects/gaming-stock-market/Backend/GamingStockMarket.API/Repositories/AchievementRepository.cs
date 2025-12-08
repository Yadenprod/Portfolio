using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Repositories
{
    public class AchievementRepository : BaseRepository<Achievement>, IAchievementRepository
    {
        public AchievementRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Achievement>> GetAchievementsForUserAsync(int userId)
        {
            return await _context.Achievements
                .Where(a => a.UserId == userId)
                .ToListAsync();
        }

        public async Task<Achievement?> GetAchievementByNameAsync(string name)
        {
            return await _context.Achievements.FirstOrDefaultAsync(a => a.Name == name);
        }
    }
}
