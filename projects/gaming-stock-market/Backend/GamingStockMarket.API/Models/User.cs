using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class User
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(50, MinimumLength = 3)]
        public required string Username { get; set; }

        [Required]
        [EmailAddress]
        [StringLength(100)]
        public required string Email { get; set; }

        [Required]
        [StringLength(255)]
        public required string PasswordHash { get; set; }

        [Column(TypeName = "decimal(18, 2)")]
        public decimal Balance { get; set; } = 0.00m;

        public int Level { get; set; } = 1;

        public int TotalTrades { get; set; } = 0;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime? LastLoginAt { get; set; }

        public bool IsActive { get; set; } = true;

        // KYC & Verification
        public bool IsEmailVerified { get; set; } = false;
        public string? VerificationToken { get; set; }
        public DateTime? VerificationTokenExpires { get; set; }
        public string? ResetToken { get; set; }
        public DateTime? ResetTokenExpires { get; set; }
        public string? RefreshToken { get; set; }
        public DateTime? RefreshTokenExpires { get; set; }
        public bool IsKycVerified { get; set; } = false;
        public string? KycStatus { get; set; } // PENDING, APPROVED, REJECTED
        public string? StripeCustomerId { get; set; } // For Stripe integration

        // Navigation properties
        public required ICollection<Order> Orders { get; set; }
        public required ICollection<UserPortfolio> Portfolio { get; set; }
        public required ICollection<Transaction> Transactions { get; set; }
        public required ICollection<Notification> Notifications { get; set; }
        public required ICollection<AuditLog> AuditLogs { get; set; }
        public required ICollection<Achievement> Achievements { get; set; }
    }
}
