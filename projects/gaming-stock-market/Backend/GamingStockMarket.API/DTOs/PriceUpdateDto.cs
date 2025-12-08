using System;

namespace GamingStockMarket.API.DTOs
{
    public class PriceUpdateDto
    {
        public int AssetId { get; set; }
        public string AssetType { get; set; } = string.Empty; // "Player" or "Team"
        public decimal NewPrice { get; set; }
        public decimal PriceChange { get; set; }
        public DateTime Timestamp { get; set; }
    }
}
