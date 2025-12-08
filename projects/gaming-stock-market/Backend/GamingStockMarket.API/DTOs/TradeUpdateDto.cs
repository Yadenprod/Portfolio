using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.DTOs
{
    public class TradeUpdateDto
    {
        public int TradeId { get; set; }
        public int PlayerId { get; set; }
        public string PlayerName { get; set; } = string.Empty;
        public decimal Price { get; set; }
        public decimal Quantity { get; set; }
        public DateTime TradeDate { get; set; }
        public TradeType Type { get; set; }
    }

    public enum TradeType
    {
        Buy,
        Sell
    }
}
