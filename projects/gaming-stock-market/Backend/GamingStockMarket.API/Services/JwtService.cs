using Microsoft.Extensions.Configuration;
using Microsoft.IdentityModel.Tokens;
using System;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;
using System.Threading.Tasks;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using GamingStockMarket.API.Services.Interfaces; // Added for IJwtService
using System.Linq;

namespace GamingStockMarket.API.Services
{
    public class JwtService : IJwtService
    {
        private readonly IConfiguration _configuration;
        private readonly IUserRepository _userRepository;
        private readonly ILogger<JwtService> _logger;

        public JwtService(IConfiguration configuration, IUserRepository userRepository, ILogger<JwtService> logger)
        {
            _configuration = configuration;
            _userRepository = userRepository;
            _logger = logger;
        }

        public string GenerateJwtToken(User user)
        {
            var jwtSettings = _configuration.GetSection("JwtSettings");
            var secretKey = jwtSettings["SecretKey"];
            var issuer = jwtSettings["Issuer"];
            var audience = jwtSettings["Audience"];
            var expirationHours = double.Parse(jwtSettings["ExpirationHours"] ?? "24");

            var claims = new List<Claim>
            {
                new Claim(ClaimTypes.NameIdentifier, user.Id.ToString()),
                new Claim(ClaimTypes.Name, user.Username),
                new Claim(ClaimTypes.Email, user.Email),
                new Claim(ClaimTypes.Role, user.Level == 4 ? "Admin" : "User") // Simple role based on level
            };

            var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(secretKey));
            var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);
            var expires = DateTime.UtcNow.AddHours(expirationHours);

            var token = new JwtSecurityToken(
                issuer: issuer,
                audience: audience,
                claims: claims,
                expires: expires,
                signingCredentials: creds
            );

            return new JwtSecurityTokenHandler().WriteToken(token);
        }

        public string GenerateRefreshToken()
        {
            var randomNumber = new byte[32];
            using (var rng = System.Security.Cryptography.RandomNumberGenerator.Create())
            {
                rng.GetBytes(randomNumber);
                return Convert.ToBase64String(randomNumber);
            }
        }

        public async Task<(User user, string newToken, string newRefreshToken)> RefreshTokenAsync(string refreshToken)
        {
            var user = (await _userRepository.GetAllAsync()).FirstOrDefault(u => u.RefreshToken == refreshToken);
            if (user == null || user.RefreshTokenExpires < DateTime.UtcNow) throw new Exception("Invalid or expired refresh token.");

            var newToken = GenerateJwtToken(user);
            var newRefreshToken = GenerateRefreshToken();
            user.RefreshToken = newRefreshToken;
            user.RefreshTokenExpires = DateTime.UtcNow.AddDays(7);
            await _userRepository.UpdateAsync(user); // Update user's refresh token

            _logger.LogInformation($"Refresh token used for user {user.Username}. Generated new tokens.");

            return (user, newToken, newRefreshToken);
        }
    }
}
