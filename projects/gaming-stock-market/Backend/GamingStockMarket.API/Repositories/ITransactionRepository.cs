using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Repositories
{
    public interface ITransactionRepository : IBaseRepository<Transaction>
    {
        Task<IEnumerable<Transaction>> GetUserTransactionsAsync(int userId, TransactionType? type = null, string? status = null, int pageNumber = 1, int pageSize = 10);
        Task<Transaction?> GetByExternalTransactionIdAsync(string externalId);
    }
}
