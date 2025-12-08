using Microsoft.AspNetCore.SignalR;
using System.Threading.Tasks;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.DTOs;

namespace GamingStockMarket.API.Hubs
{
    public class NotificationHub : Hub
    {
        // Method to send a notification to a specific user
        public async Task SendUserNotification(int userId, NotificationResponse notification)
        {
            // You would map userId to ConnectionId(s) here. For simplicity, we'll use a group per user.
            await Clients.User(userId.ToString()).SendAsync("ReceiveUserNotification", notification);
        }

        // Method to send a general broadcast notification
        public async Task SendBroadcastNotification(NotificationResponse notification)
        {
            await Clients.All.SendAsync("ReceiveBroadcastNotification", notification);
        }

        // Example: Client joins a user-specific group
        public override async Task OnConnectedAsync()
        {
            // In a real application, you'd get the UserId from claims after authentication
            // For now, let's assume Context.User.Identity.Name contains the UserId.
            if (Context.User?.Identity?.IsAuthenticated == true)
            {
                var userId = Context.User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
                if (userId != null)
                {
                    await Groups.AddToGroupAsync(Context.ConnectionId, userId);
                    _ = Clients.Caller.SendAsync("ConnectionStatus", "Connected and joined user group.");
                }
            }
            await base.OnConnectedAsync();
        }

        public override async Task OnDisconnectedAsync(Exception? exception)
        {
            if (Context.User?.Identity?.IsAuthenticated == true)
            {
                var userId = Context.User.FindFirst(System.Security.Claims.ClaimTypes.NameIdentifier)?.Value;
                if (userId != null)
                {
                    await Groups.RemoveFromGroupAsync(Context.ConnectionId, userId);
                    _ = Clients.Caller.SendAsync("ConnectionStatus", "Disconnected from user group.");
                }
            }
            await base.OnDisconnectedAsync(exception);
        }
    }
}
