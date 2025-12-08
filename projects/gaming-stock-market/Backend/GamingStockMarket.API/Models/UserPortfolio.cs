using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class UserPortfolio
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
        public int Shares { get; set; }

        [Required]
        [Column(TypeName = "decimal(18, 2)")]
        public decimal AveragePrice { get; set; } // Average purchase price

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    }
}
