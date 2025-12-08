using System.ComponentModel.DataAnnotations;
using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.DTOs
{
    // Auth DTOs
    public class RegisterRequest
    {
        [Required]
        [StringLength(50, MinimumLength = 3)]
        public string Username { get; set; } = string.Empty;

        [Required]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;

        [Required]
        [MinLength(6)]
        public string Password { get; set; } = string.Empty;
    }

    public class LoginRequest
    {
        [Required]
        public string Username { get; set; } = string.Empty;

        [Required]
        public string Password { get; set; } = string.Empty;
    }

    public class AuthResponse
    {
        public string Token { get; set; } = string.Empty;
        public DateTime Expiration { get; set; }
        public string RefreshToken { get; set; } = string.Empty;
    }

    public class RefreshTokenRequest
    {
        [Required]
        public string RefreshToken { get; set; } = string.Empty;
    }

    public class VerifyEmailRequest
    {
        [Required]
        public string Token { get; set; } = string.Empty;
    }

    public class ForgotPasswordRequest
    {
        [Required]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;
    }

    public class ResetPasswordRequest
    {
        [Required]
        public string Token { get; set; } = string.Empty;

        [Required]
        [MinLength(6)]
        public string NewPassword { get; set; } = string.Empty;
    }

    // Trading DTOs
    public class PlaceOrderRequest
    {
        public int? PlayerId { get; set; }
        public int? TeamId { get; set; }

        [Required]
        public OrderType Type { get; set; }

        [Required]
        [Range(1, 1000)]
        public int Shares { get; set; }

        [Required]
        [Range(0.01, 10000.00)]
        public decimal Price { get; set; }
    }

    public class OrderResponse
    {
        public int OrderId { get; set; }
        public OrderStatus Status { get; set; }
        public int FilledShares { get; set; }
    }

    public class OrderBookResponse
    {
        public int? PlayerId { get; set; }
        public int? TeamId { get; set; }
        public List<OrderDto> BuyOrders { get; set; } = new List<OrderDto>();
        public List<OrderDto> SellOrders { get; set; } = new List<OrderDto>();
    }

    public class PortfolioResponse
    {
        public int UserId { get; set; }
        public decimal Balance { get; set; }
        public List<UserPortfolio> Holdings { get; set; } = new List<UserPortfolio>();
        public decimal TotalValue { get; set; }
    }

    // Player/Team DTOs
    public class PlayerResponse
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Game { get; set; } = string.Empty;
        public string? Team { get; set; }
        public decimal CurrentPrice { get; set; }
        public decimal? Rating { get; set; }
        public int PopularityScore { get; set; }
    }

    public class TeamResponse
    {
        public int Id { get; set; }
        public string Name { get; set; } = string.Empty;
        public string Game { get; set; } = string.Empty;
        public decimal CurrentPrice { get; set; }
        public int? Ranking { get; set; }
    }

    // Payment DTOs
    public class DepositRequest
    {
        [Required]
        [Range(1.0, 100000.0)]
        public decimal Amount { get; set; }

        [Required]
        public string Currency { get; set; } = "USD";

        [Required]
        public string PaymentMethodId { get; set; } = string.Empty; // Stripe PaymentMethodId
    }

    public class WithdrawalRequest
    {
        [Required]
        [Range(1.0, 100000.0)]
        public decimal Amount { get; set; }

        [Required]
        public string Currency { get; set; } = "USD";

        [Required]
        public string WithdrawalMethodDetails { get; set; } = string.Empty; // e.g., bank account details, crypto wallet address
    }

    public class PaymentResponse
    {
        public int TransactionId { get; set; }
        public string Status { get; set; } = string.Empty;
        public decimal Amount { get; set; }
        public string Currency { get; set; } = string.Empty;
    }

    // Notification DTOs
    public class NotificationResponse
    {
        public int Id { get; set; }
        public string Type { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public bool IsRead { get; set; }
        public DateTime CreatedAt { get; set; }
    }

    // Analytics DTOs
    public class DailyMetric
    {
        public DateTime Date { get; set; }
        public decimal Value { get; set; }
    }

    public class AnalyticsResponse
    {
        public int TotalUsers { get; set; }
        public int ActiveUsers { get; set; }
        public decimal TotalTradingVolume { get; set; }
        public List<DailyMetric> DailyTradingVolume { get; set; } = new List<DailyMetric>();
        public List<DailyMetric> DailyNewUsers { get; set; } = new List<DailyMetric>();
    }

    // Admin DTOs
    public class UpdateUserRequest
    {
        public string? Username { get; set; }
        public string? Email { get; set; }
        public decimal? Balance { get; set; }
        public int? Level { get; set; }
        public bool? IsActive { get; set; }
        public string? KycStatus { get; set; }
    }

    public class CreatePlayerRequest
    {
        [Required]
        public string Name { get; set; } = string.Empty;
        [Required]
        public string Game { get; set; } = string.Empty;
        public string? Team { get; set; }
        [Required]
        public decimal BasePrice { get; set; }
    }

    public class UpdatePlayerRequest : CreatePlayerRequest
    {
        [Required]
        public int Id { get; set; }
        public bool? IsActive { get; set; }
    }

    public class CreateTeamRequest
    {
        [Required]
        public string Name { get; set; } = string.Empty;
        [Required]
        public string Game { get; set; } = string.Empty;
        [Required]
        public decimal BasePrice { get; set; }
    }

    public class UpdateTeamRequest : CreateTeamRequest
    {
        [Required]
        public int Id { get; set; }
        public bool? IsActive { get; set; }
    }
}
