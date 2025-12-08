using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Team
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public required string Name { get; set; }

        [Required]
        [StringLength(50)]
        public required string Game { get; set; }

        [Column(TypeName = "decimal(18, 2)")]
        public decimal BasePrice { get; set; }

        [Column(TypeName = "decimal(18, 2)")]
        public decimal CurrentPrice { get; set; }

        public int TotalShares { get; set; } = 1000;

        public int AvailableShares { get; set; } = 1000;

        public int? Ranking { get; set; } // Team ranking in the game

        public DateTime LastUpdated { get; set; } = DateTime.UtcNow;

        public bool IsActive { get; set; } = true;

        public ICollection<Player> Players { get; set; } = new List<Player>(); // Added for navigation

        // Navigation properties
        public required ICollection<Order> Orders { get; set; }
        public required ICollection<Trade> Trades { get; set; }
        public required ICollection<UserPortfolio> PortfolioHoldings { get; set; }
        public required ICollection<Match> Matches { get; set; }
        public required ICollection<PriceHistory> PriceHistory { get; set; }
    }
}
