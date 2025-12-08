using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GamingStockMarket.API.Models
{
    public class Achievement
    {
        [Key]
        public int Id { get; set; }

        public int UserId { get; set; }
        [ForeignKey("UserId")]
        public User? User { get; set; }

        [Required]
        public required AchievementType Type { get; set; }

        [Required]
        [StringLength(100)]
        public required string Name { get; set; }

        [StringLength(500)]
        public string? Description { get; set; }

        public DateTime AchievedAt { get; set; } = DateTime.UtcNow;

        [Column(TypeName = "decimal(18, 2)")]
        public decimal? RewardAmount { get; set; } // e.g., bonus for achievement

        public string? RelatedData { get; set; } // JSON string for additional data
    }

    public enum AchievementType
    {
        FirstTrade,
        SuccessfulTrader, // X% profit
        ExpertTrader,     // Y% profit
        LegendTrader,     // 100% profit
        TopTraderOfMonth,
        ReferralBonus,
        DailyLoginStreak
    }
}
