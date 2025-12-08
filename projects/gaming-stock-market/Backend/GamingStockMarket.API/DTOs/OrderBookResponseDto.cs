using System.Collections.Generic;

namespace GamingStockMarket.API.DTOs
{
    public class OrderBookResponseDto
    {
        public int PlayerId { get; set; }
        public string PlayerName { get; set; } = string.Empty;
        public List<OrderDto> BuyOrders { get; set; } = new List<OrderDto>();
        public List<OrderDto> SellOrders { get; set; } = new List<OrderDto>();
    }

    public class OrderDto
    {
        public int OrderId { get; set; }
        public int UserId { get; set; }
        public decimal Price { get; set; }
        public decimal Quantity { get; set; }
        public string Type { get; set; } = string.Empty; // "Buy" or "Sell"
        public DateTime CreatedAt { get; set; }
    }
}
