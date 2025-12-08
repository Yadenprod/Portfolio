using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class PriceHistory
    {
        [Key]
        public int Id { get; set; }

        public int? PlayerId { get; set; }
        [ForeignKey("PlayerId")]
        public Player? Player { get; set; }

        public int? TeamId { get; set; }
        [ForeignKey("TeamId")]
        public Team? Team { get; set; }

        [Required]
        [Column(TypeName = "decimal(18, 2)")]
        public decimal Price { get; set; }

        public int Volume { get; set; } = 0; // Volume of shares traded at this price

        public DateTime RecordedAt { get; set; } = DateTime.UtcNow;
    }
}
