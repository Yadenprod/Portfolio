using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Order
    {
        [Key]
        public int Id { get; set; }

        public int UserId { get; set; }
        [ForeignKey("UserId")]
        public User? User { get; set; }

        public int? PlayerId { get; set; }
        [ForeignKey("PlayerId")]
        public Player? Player { get; set; }

        public int? TeamId { get; set; }
        [ForeignKey("TeamId")]
        public Team? Team { get; set; }

        [Required]
        public OrderType Type { get; set; } // BUY or SELL

        [Required]
        [Range(1, 1000)] // Example limits
        public int Shares { get; set; }

        [Required]
        [Column(TypeName = "decimal(18, 2)")]
        [Range(0.01, 10000.00)] // Example limits
        public decimal Price { get; set; }

        public OrderStatus Status { get; set; } = OrderStatus.Pending; // PENDING, FILLED, PARTIALLY_FILLED, CANCELLED

        public int FilledShares { get; set; } = 0;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;

        [NotMapped]
        public int RemainingShares => Shares - FilledShares;

        // Navigation properties
        public required ICollection<Trade> BuyTrades { get; set; }
        public required ICollection<Trade> SellTrades { get; set; }
    }

    public enum OrderType
    {
        Buy,
        Sell
    }

    public enum OrderStatus
    {
        Pending,
        Filled,
        PartiallyFilled,
        Cancelled
    }
}
