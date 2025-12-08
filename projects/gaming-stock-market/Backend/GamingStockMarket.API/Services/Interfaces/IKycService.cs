using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IKycService
    {
        Task<bool> InitiateKycVerificationAsync(int userId);
        Task<bool> CheckKycStatusAsync(int userId);
    }
}
