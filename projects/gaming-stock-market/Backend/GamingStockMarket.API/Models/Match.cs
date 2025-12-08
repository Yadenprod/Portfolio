using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Match
    {
        [Key]
        public int Id { get; set; }

        public int? PlayerId { get; set; }
        [ForeignKey("PlayerId")]
        public Player? Player { get; set; }

        public int? TeamId { get; set; }
        [ForeignKey("TeamId")]
        public Team? Team { get; set; }

        [StringLength(100)]
        public string? Opponent { get; set; }

        [StringLength(10)]
        public string? Result { get; set; } // WIN/LOSS/DRAW

        [Column(TypeName = "decimal(3, 2)")]
        public decimal? PlayerRating { get; set; }

        public bool IsMVP { get; set; } = false;

        [StringLength(100)]
        public string? Tournament { get; set; }

        public int? TournamentTier { get; set; } // 1=Major, 2=Tier1, 3=Tier2

        public DateTime MatchDate { get; set; }

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    }
}
