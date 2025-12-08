using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Transaction
    {
        [Key]
        public int Id { get; set; }

        public int UserId { get; set; }
        [ForeignKey("UserId")]
        public User? User { get; set; }

        [Required]
        public TransactionType Type { get; set; } // DEPOSIT, WITHDRAWAL, COMMISSION, BONUS

        [Required]
        [Column(TypeName = "decimal(18, 2)")]
        public decimal Amount { get; set; }

        [Required]
        [StringLength(20)]
        public required string Status { get; set; } = "PENDING"; // PENDING, COMPLETED, FAILED, CANCELLED

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime? CompletedAt { get; set; }

        [StringLength(500)]
        public string? Notes { get; set; }

        [StringLength(255)]
        public string? ExternalTransactionId { get; set; } // For Stripe/PayPal etc.
    }

    public enum TransactionType
    {
        Deposit,
        Withdrawal,
        Commission,
        Bonus,
        TradeBuy,
        TradeSell
    }
}
