using System.Threading.Tasks;
using System.Collections.Generic;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Models;

namespace GamingStockMarket.API.Services.Interfaces
{
    public interface INotificationService
    {
        Task SendUserNotificationAsync(int userId, NotificationResponse notification);
        Task SendBroadcastNotificationAsync(NotificationResponse notification);
        Task<IEnumerable<NotificationResponse>> GetUserNotificationsAsync(int userId, bool unreadOnly = false);
        Task MarkNotificationAsReadAsync(int notificationId, int userId);
        Task MarkAllUserNotificationsAsReadAsync(int userId);
        Task DeleteNotificationAsync(int notificationId, int userId);
    }
}
