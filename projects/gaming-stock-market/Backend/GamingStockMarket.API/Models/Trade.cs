using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Trade
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int BuyOrderId { get; set; }
        [ForeignKey("BuyOrderId")]
        public required Order BuyOrder { get; set; }

        [Required]
        public int SellOrderId { get; set; }
        [ForeignKey("SellOrderId")]
        public required Order SellOrder { get; set; }

        public int? PlayerId { get; set; }
        [ForeignKey("PlayerId")]
        public Player? Player { get; set; }

        public int? TeamId { get; set; }
        [ForeignKey("TeamId")]
        public Team? Team { get; set; }

        [Required]
        public int Shares { get; set; }

        [Required]
        [Column(TypeName = "decimal(18, 2)")]
        public decimal Price { get; set; }

        [Column(TypeName = "decimal(18, 2)")]
        public decimal Commission { get; set; } = 0.00m;

        [Column(TypeName = "decimal(18, 2)")]
        public decimal Tax { get; set; } = 0.00m; // For future tax implementation

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}
