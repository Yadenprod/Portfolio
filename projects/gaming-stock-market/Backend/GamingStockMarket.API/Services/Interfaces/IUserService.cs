using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface IUserService
    {
        Task<User> RegisterAsync(string username, string email, string password);
        Task<User> LoginAsync(string username, string password);
        Task SetRefreshTokenAsync(int userId, string refreshToken);
        Task VerifyEmailAsync(string token);
        Task GeneratePasswordResetTokenAsync(string email);
        Task ResetPasswordAsync(string token, string newPassword);
        Task<User?> GetByIdAsync(int userId);
        Task<IEnumerable<User>> GetAllUsersAsync(int pageNumber, int pageSize);
        Task UpdateUserAsync(int userId, UpdateUserRequest request);
    }
}
