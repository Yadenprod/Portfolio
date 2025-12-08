using GamingStockMarket.API.Models;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IPaymentService
    {
        Task<Models.Transaction> CreateDepositAsync(int userId, decimal amount, string currency, string paymentMethodId);
        Task<Models.Transaction> CreateWithdrawalAsync(int userId, decimal amount, string currency, string withdrawalMethodDetails);
        Task HandleStripeWebhookAsync(string json, string stripeSignature, string webhookSecret);
    }
}
