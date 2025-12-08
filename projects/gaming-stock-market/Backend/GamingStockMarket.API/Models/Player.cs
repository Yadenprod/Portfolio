using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Player
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public required string Name { get; set; }

        [Required]
        [StringLength(50)]
        public required string Game { get; set; }

        [StringLength(100)]
        public string? Team { get; set; }

        [Column(TypeName = "decimal(18, 2)")]
        public decimal BasePrice { get; set; }

        [Column(TypeName = "decimal(18, 2)")]
        public decimal CurrentPrice { get; set; }

        public int TotalShares { get; set; } = 1000; // Default total shares

        public int AvailableShares { get; set; } = 1000; // Default available shares

        [Column(TypeName = "decimal(3, 2)")]
        public decimal? Rating { get; set; } // Player performance rating (e.g., HLTV rating for CS:GO)

        public int PopularityScore { get; set; } = 0; // Based on social media, mentions, etc.

        public DateTime LastUpdated { get; set; } = DateTime.UtcNow;

        public bool IsActive { get; set; } = true;

        // Navigation properties
        public required ICollection<Order> Orders { get; set; }
        public required ICollection<Trade> Trades { get; set; }
        public required ICollection<UserPortfolio> PortfolioHoldings { get; set; }
        public required ICollection<Match> Matches { get; set; }
        public required ICollection<PriceHistory> PriceHistory { get; set; }
    }
}
