using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using GamingStockMarket.API.Services.Interfaces;

namespace GamingStockMarket.API.Services
{
    public class UserService : IUserService
    {
        private readonly IUserRepository _userRepository;
        private readonly IJwtService _jwtService;
        private readonly IEmailService _emailService;
        private readonly ILogger<UserService> _logger;
        private readonly IAchievementService _achievementService;

        public UserService(IUserRepository userRepository, IJwtService jwtService,
                           IEmailService emailService, ILogger<UserService> logger,
                           IAchievementService achievementService)
        {
            _userRepository = userRepository;
            _jwtService = jwtService;
            _emailService = emailService;
            _logger = logger;
            _achievementService = achievementService;
        }

        public async Task<User> RegisterAsync(string username, string email, string password)
        {
            if (await _userRepository.GetByUsernameAsync(username) != null) throw new Exception("Username already exists.");
            if (await _userRepository.GetByEmailAsync(email) != null) throw new Exception("Email already registered.");

            // Hash password (using BCrypt or similar)
            var passwordHash = BCrypt.Net.BCrypt.HashPassword(password); // Requires BCrypt.Net-Next package

            var user = new User
            {
                Username = username,
                Email = email,
                PasswordHash = passwordHash,
                VerificationToken = GenerateVerificationToken(),
                VerificationTokenExpires = DateTime.UtcNow.AddDays(7),
                CreatedAt = DateTime.UtcNow,
                LastLoginAt = DateTime.UtcNow,
                Orders = new List<Order>(), // Initialize navigation properties
                Portfolio = new List<UserPortfolio>(),
                Transactions = new List<Transaction>(),
                Notifications = new List<Notification>(),
                AuditLogs = new List<AuditLog>(),
                Achievements = new List<Achievement>()
            };

            await _userRepository.AddAsync(user);

            await _emailService.SendEmailAsync(user.Email, "Verify Your Email", $"Please verify your account by clicking this link: [link-to-verify-email?token={user.VerificationToken}]");
            _logger.LogInformation($"User {username} registered. Verification token: {user.VerificationToken}");

            // Check for achievements after registration
            await _achievementService.CheckAndGrantAchievementsAsync(user.Id);

            return user;
        }

        public async Task<User> LoginAsync(string username, string password)
        {
            var user = await _userRepository.GetByUsernameAsync(username);
            if (user == null || !BCrypt.Net.BCrypt.Verify(password, user.PasswordHash)) throw new Exception("Invalid credentials.");
            if (!user.IsEmailVerified) throw new Exception("Email not verified.");
            if (!user.IsActive) throw new Exception("User account is inactive.");

            user.LastLoginAt = DateTime.UtcNow;
            await _userRepository.UpdateAsync(user);

            _logger.LogInformation($"User {username} logged in.");

            return user;
        }

        public async Task SetRefreshTokenAsync(int userId, string refreshToken)
        {
            var user = await _userRepository.GetByIdAsync(userId);
            if (user == null) throw new Exception("User not found.");

            // For now, we'll store refresh token directly in User model. In a real app,
            // you might want a separate RefreshToken entity with expiration and more security.
            user.RefreshToken = refreshToken; // Assuming RefreshToken property in User model
            user.RefreshTokenExpires = DateTime.UtcNow.AddDays(7);
            await _userRepository.UpdateAsync(user);
        }

        public async Task VerifyEmailAsync(string token)
        {
            var user = (await _userRepository.GetAllAsync()).FirstOrDefault(u => u.VerificationToken == token);
            if (user == null || user.VerificationTokenExpires < DateTime.UtcNow) throw new Exception("Invalid or expired verification token.");

            user.IsEmailVerified = true;
            user.VerificationToken = null;
            user.VerificationTokenExpires = null;
            await _userRepository.UpdateAsync(user);

            _logger.LogInformation($"Email for user {user.Username} verified.");
        }

        public async Task GeneratePasswordResetTokenAsync(string email)
        {
            var user = await _userRepository.GetByEmailAsync(email);
            if (user == null) throw new Exception("User not found."); // Don't reveal if user exists for security

            user.ResetToken = GenerateResetToken();
            user.ResetTokenExpires = DateTime.UtcNow.AddHours(1);
            await _userRepository.UpdateAsync(user);

            await _emailService.SendEmailAsync(user.Email, "Password Reset", $"Please reset your password by clicking this link: [link-to-reset-password?token={user.ResetToken}]");
            _logger.LogInformation($"Password reset token generated for {email}. Token: {user.ResetToken}");
        }

        public async Task ResetPasswordAsync(string token, string newPassword)
        {
            var user = (await _userRepository.GetAllAsync()).FirstOrDefault(u => u.ResetToken == token);
            if (user == null || user.ResetTokenExpires < DateTime.UtcNow) throw new Exception("Invalid or expired reset token.");

            user.PasswordHash = BCrypt.Net.BCrypt.HashPassword(newPassword);
            user.ResetToken = null;
            user.ResetTokenExpires = null;
            await _userRepository.UpdateAsync(user);

            _logger.LogInformation($"Password for user {user.Username} reset successfully.");
        }

        public async Task<User?> GetByIdAsync(int userId)
        {
            return await _userRepository.GetByIdAsync(userId);
        }

        public async Task<IEnumerable<User>> GetAllUsersAsync(int pageNumber, int pageSize)
        {
            return await _userRepository.GetAllAsync(); // TODO: Implement pagination in GetAllAsync if needed
        }

        public async Task UpdateUserAsync(int userId, UpdateUserRequest request)
        {
            var user = await _userRepository.GetByIdAsync(userId);
            if (user == null) throw new Exception("User not found.");

            if (request.Username != null) user.Username = request.Username;
            if (request.Email != null) user.Email = request.Email;
            if (request.Balance.HasValue) user.Balance = request.Balance.Value;
            if (request.Level.HasValue) user.Level = request.Level.Value;
            if (request.IsActive.HasValue) user.IsActive = request.IsActive.Value;
            if (request.KycStatus != null) user.KycStatus = request.KycStatus;
            
            await _userRepository.UpdateAsync(user);
            _logger.LogInformation($"User {userId} updated.");
        }

        private string GenerateVerificationToken()
        {
            return Convert.ToBase64String(Guid.NewGuid().ToByteArray()).Replace("+", "-").Replace("/", "_").Replace("=", "");
        }

        private string GenerateResetToken()
        {
            return Convert.ToBase64String(Guid.NewGuid().ToByteArray()).Replace("+", "-").Replace("/", "_").Replace("=", "");
        }
    }
}
