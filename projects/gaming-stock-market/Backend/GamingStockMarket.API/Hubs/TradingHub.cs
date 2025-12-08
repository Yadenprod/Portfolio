using Microsoft.AspNetCore.SignalR;
using System.Threading.Tasks;
using GamingStockMarket.API.DTOs;

namespace GamingStockMarket.API.Hubs
{
    public class TradingHub : Hub
    {
        // Methods that clients can call on the server
        public async Task JoinMarket(string marketName)
        {
            await Groups.AddToGroupAsync(Context.ConnectionId, marketName);
            await Clients.Group(marketName).SendAsync("ReceiveMessage", $"{Context.ConnectionId} has joined the {marketName} market.");
        }

        public async Task LeaveMarket(string marketName)
        {
            await Groups.RemoveFromGroupAsync(Context.ConnectionId, marketName);
            await Clients.Group(marketName).SendAsync("ReceiveMessage", $"{Context.ConnectionId} has left the {marketName} market.");
        }

        // Example: Server-side method to broadcast a new trade (called by TradingService)
        public async Task SendTradeUpdate(TradeUpdateDto tradeUpdate)
        {
            await Clients.All.SendAsync("ReceiveTradeUpdate", tradeUpdate);
        }

        // Example: Server-side method to broadcast an order book update
        public async Task SendOrderBookUpdate(OrderBookResponseDto orderBookUpdate)
        {
            await Clients.All.SendAsync("ReceiveOrderBookUpdate", orderBookUpdate);
        }

        // Example: Server-side method to broadcast a price update for a specific asset
        public async Task SendPriceUpdate(PriceUpdateDto priceUpdate)
        {
            // You might want to send to a specific group for a player/team
            await Clients.All.SendAsync("ReceivePriceUpdate", priceUpdate);
        }
    }
}
