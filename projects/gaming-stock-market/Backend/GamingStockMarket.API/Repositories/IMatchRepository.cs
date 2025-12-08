using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface IMatchRepository : IBaseRepository<Match>
    {
        Task<IEnumerable<Match>> GetRecentMatchesAsync(int? playerId = null, int? teamId = null, int count = 10);
        Task<IEnumerable<Match>> GetMatchesByPlayerIdAsync(int playerId);
        Task<IEnumerable<Match>> GetMatchesByTeamIdAsync(int teamId);
    }
}
