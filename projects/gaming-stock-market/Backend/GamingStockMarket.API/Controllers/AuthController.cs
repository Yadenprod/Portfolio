using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using System.Threading.Tasks;
using GamingStockMarket.API.Services.Interfaces; // Updated using
using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AuthController : ControllerBase
    {
        private readonly IUserService _userService;
        private readonly IJwtService _jwtService;
        private readonly ILogger<AuthController> _logger;

        public AuthController(IUserService userService, IJwtService jwtService, ILogger<AuthController> logger)
        {
            _userService = userService;
            _jwtService = jwtService;
            _logger = logger;
        }

        [HttpPost("register")]
        public async Task<ActionResult<AuthResponse>> Register([FromBody] RegisterRequest request)
        {
            try
            {
                var user = await _userService.RegisterAsync(request.Username, request.Email, request.Password);
                var token = _jwtService.GenerateJwtToken(user);
                var refreshToken = _jwtService.GenerateRefreshToken();
                await _userService.SetRefreshTokenAsync(user.Id, refreshToken);

                _logger.LogInformation($"User {user.Username} registered successfully.");

                return Ok(new AuthResponse { Token = token, Expiration = DateTime.UtcNow.AddHours(24), RefreshToken = refreshToken });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Registration failed.");
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("login")]
        public async Task<ActionResult<AuthResponse>> Login([FromBody] LoginRequest request)
        {
            try
            {
                var user = await _userService.LoginAsync(request.Username, request.Password);
                var token = _jwtService.GenerateJwtToken(user);
                var refreshToken = _jwtService.GenerateRefreshToken();
                await _userService.SetRefreshTokenAsync(user.Id, refreshToken);

                _logger.LogInformation($"User {user.Username} logged in successfully.");

                return Ok(new AuthResponse { Token = token, Expiration = DateTime.UtcNow.AddHours(24), RefreshToken = refreshToken });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Login failed.");
                return Unauthorized(new { message = ex.Message });
            }
        }

        [HttpPost("refresh-token")]
        public async Task<ActionResult<AuthResponse>> RefreshToken([FromBody] RefreshTokenRequest request)
        {
            try
            {
                var (user, newToken, newRefreshToken) = await _jwtService.RefreshTokenAsync(request.RefreshToken);

                _logger.LogInformation($"Token refreshed for user {user.Username}.");

                return Ok(new AuthResponse { Token = newToken, Expiration = DateTime.UtcNow.AddHours(24), RefreshToken = newRefreshToken });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Refresh token failed.");
                return Unauthorized(new { message = ex.Message });
            }
        }

        [HttpPost("verify-email")]
        public async Task<ActionResult> VerifyEmail([FromBody] VerifyEmailRequest request)
        {
            try
            {
                await _userService.VerifyEmailAsync(request.Token);
                _logger.LogInformation("Email verified successfully.");
                return Ok(new { message = "Email verified successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Email verification failed.");
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("forgot-password")]
        public async Task<ActionResult> ForgotPassword([FromBody] ForgotPasswordRequest request)
        {
            try
            {
                await _userService.GeneratePasswordResetTokenAsync(request.Email);
                _logger.LogInformation($"Password reset token sent to {request.Email}.");
                return Ok(new { message = "Password reset link sent to your email." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Forgot password failed.");
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpPost("reset-password")]
        public async Task<ActionResult> ResetPassword([FromBody] ResetPasswordRequest request)
        {
            try
            {
                await _userService.ResetPasswordAsync(request.Token, request.NewPassword);
                _logger.LogInformation("Password reset successfully.");
                return Ok(new { message = "Password reset successfully." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Password reset failed.");
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}
