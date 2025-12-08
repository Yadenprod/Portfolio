using GamingStockMarket.API.Data;
using GamingStockMarket.API.Models;
using Microsoft.EntityFrameworkCore;

namespace GamingStockMarket.API.Repositories
{
    public class TransactionRepository : BaseRepository<Transaction>, ITransactionRepository
    {
        public TransactionRepository(ApplicationDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Transaction>> GetUserTransactionsAsync(int userId, TransactionType? type = null, string? status = null, int pageNumber = 1, int pageSize = 10)
        {
            var query = _context.Transactions.Where(t => t.UserId == userId);

            if (type.HasValue)
            {
                query = query.Where(t => t.Type == type.Value);
            }

            if (!string.IsNullOrEmpty(status))
            {
                query = query.Where(t => t.Status == status);
            }

            return await query
                .Skip((pageNumber - 1) * pageSize)
                .Take(pageSize)
                .ToListAsync();
        }

        public async Task<Transaction?> GetByExternalTransactionIdAsync(string externalId)
        {
            return await _context.Transactions.FirstOrDefaultAsync(t => t.ExternalTransactionId == externalId);
        }
    }
}
