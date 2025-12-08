using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Notification
    {
        [Key]
        public int Id { get; set; }

        public int UserId { get; set; }
        [ForeignKey("UserId")]
        public User? User { get; set; }

        [Required]
        [StringLength(50)]
        public required string Type { get; set; } // e.g., "PRICE_ALERT", "TRADE_CONFIRMATION", "SYSTEM_MESSAGE"

        [Required]
        [StringLength(500)]
        public required string Message { get; set; }

        public bool IsRead { get; set; } = false;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public string? RelatedEntityId { get; set; } // e.g., OrderId, TradeId
    }
}
