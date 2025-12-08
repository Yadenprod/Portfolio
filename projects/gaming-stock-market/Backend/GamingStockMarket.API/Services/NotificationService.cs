using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Hubs;
using GamingStockMarket.API.Models;
using GamingStockMarket.API.Repositories;
using GamingStockMarket.API.Services.Interfaces;
using Microsoft.AspNetCore.SignalR;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace GamingStockMarket.API.Services
{
    public class NotificationService : INotificationService
    {
        private readonly INotificationRepository _notificationRepository;
        private readonly IHubContext<NotificationHub> _hubContext;
        private readonly IEmailService _emailService;
        private readonly IUserRepository _userRepository;
        private readonly ILogger<NotificationService> _logger;

        public NotificationService(INotificationRepository notificationRepository,
                                   IHubContext<NotificationHub> hubContext,
                                   IEmailService emailService,
                                   IUserRepository userRepository,
                                   ILogger<NotificationService> logger)
        {
            _notificationRepository = notificationRepository;
            _hubContext = hubContext;
            _emailService = emailService;
            _userRepository = userRepository;
            _logger = logger;
        }

        public async Task SendUserNotificationAsync(int userId, NotificationResponse notificationDto)
        {
            // Save to database
            var notification = new Notification
            {
                UserId = userId,
                Message = notificationDto.Message,
                Type = notificationDto.Type,
                IsRead = false,
                CreatedAt = DateTime.UtcNow
            };
            await _notificationRepository.AddAsync(notification);
            
            // Send via SignalR
            await _hubContext.Clients.User(userId.ToString()).SendAsync("ReceiveUserNotification", notificationDto);
            _logger.LogInformation($"Notification sent to user {userId}: {notificationDto.Message}");

            // Optionally send email for critical notifications
            if (notificationDto.Type == "Critical") // Example condition
            {
                var user = await _userRepository.GetByIdAsync(userId);
                if (user != null && !string.IsNullOrEmpty(user.Email))
                {
                    await _emailService.SendEmailAsync(user.Email, "Critical Notification", notificationDto.Message);
                    _logger.LogInformation($"Critical notification email sent to user {userId}");
                }
            }
        }

        public async Task SendBroadcastNotificationAsync(NotificationResponse notificationDto)
        {
            // Save to database (optional for broadcasts, depends on requirements)
            var notification = new Notification
            {
                // No specific user ID for broadcast, or relate to an 'admin' user if needed
                Message = notificationDto.Message,
                Type = notificationDto.Type,
                IsRead = false,
                CreatedAt = DateTime.UtcNow
            };
            // await _notificationRepository.AddAsync(notification); // Uncomment if broadcast needs to be persisted for all

            // Send via SignalR to all clients
            await _hubContext.Clients.All.SendAsync("ReceiveBroadcastNotification", notificationDto);
            _logger.LogInformation($"Broadcast notification sent: {notificationDto.Message}");
        }

        public async Task<IEnumerable<NotificationResponse>> GetUserNotificationsAsync(int userId, bool unreadOnly = false)
        {
            var notifications = await _notificationRepository.GetUserNotificationsAsync(userId, unreadOnly);
            return notifications.Select(n => new NotificationResponse
            {
                Id = n.Id,
                Message = n.Message,
                Type = n.Type,
                IsRead = n.IsRead,
                CreatedAt = n.CreatedAt
            });
        }

        public async Task MarkNotificationAsReadAsync(int notificationId, int userId)
        {
            var notification = await _notificationRepository.GetByIdAsync(notificationId);
            if (notification == null || notification.UserId != userId) throw new Exception("Notification not found or unauthorized.");

            notification.IsRead = true;
            await _notificationRepository.UpdateAsync(notification);
            _logger.LogInformation($"Notification {notificationId} marked as read for user {userId}");
        }

        public async Task MarkAllUserNotificationsAsReadAsync(int userId)
        {
            var notifications = await _notificationRepository.GetUserNotificationsAsync(userId, unreadOnly: true);
            foreach (var notification in notifications)
            {
                notification.IsRead = true;
                await _notificationRepository.UpdateAsync(notification);
            }
            _logger.LogInformation($"All notifications marked as read for user {userId}");
        }

        public async Task DeleteNotificationAsync(int notificationId, int userId)
        {
            var notification = await _notificationRepository.GetByIdAsync(notificationId);
            if (notification == null || notification.UserId != userId) throw new Exception("Notification not found or unauthorized.");

            await _notificationRepository.DeleteAsync(notification);
            _logger.LogInformation($"Notification {notificationId} deleted for user {userId}");
        }
    }
}
