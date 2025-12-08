using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface IPlayerRepository : IBaseRepository<Player>
    {
        Task<Player?> GetByIdWithDetailsAsync(int id);
        Task<IEnumerable<Player>> GetActivePlayersByGameAsync(string game);
        Task<IEnumerable<Player>> GetAllPlayersWithDetailsAsync();
    }
}
