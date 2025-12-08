using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface ITeamRepository : IBaseRepository<Team>
    {
        Task<Team?> GetByIdWithPlayersAsync(int id);
        Task<IEnumerable<Team>> GetActiveTeamsByGameAsync(string game);
    }
}
