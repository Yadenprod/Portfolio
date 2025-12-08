using Microsoft.AspNetCore.Mvc;
using GamingStockMarket.API.DTOs;
using GamingStockMarket.API.Extensions;
using GamingStockMarket.API.Repositories;
using GamingStockMarket.API.Services.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System;

namespace GamingStockMarket.API.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    [Authorize]
    public class NotificationController : ControllerBase
    {
        private readonly INotificationRepository _notificationRepository;
        private readonly ILogger<NotificationController> _logger;

        public NotificationController(INotificationRepository notificationRepository, ILogger<NotificationController> logger)
        {
            _notificationRepository = notificationRepository;
            _logger = logger;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<NotificationResponse>>> GetUserNotifications([FromQuery] bool? isRead = null)
        {
            try
            {
                var userId = User.GetUserId();
                var notifications = await _notificationRepository.GetUserNotificationsAsync(userId, isRead ?? false);
                var notificationResponses = notifications.Select(n => new NotificationResponse
                {
                    Id = n.Id,
                    Type = n.Type,
                    Message = n.Message,
                    IsRead = n.IsRead,
                    CreatedAt = n.CreatedAt
                });
                return Ok(notificationResponses);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting notifications for user {UserId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpGet("unread-count")]
        public async Task<ActionResult<int>> GetUnreadNotificationsCount()
        {
            try
            {
                var userId = User.GetUserId();
                // var count = await _notificationRepository.GetUnreadNotificationsCountAsync(userId); // Метод удален из интерфейса
                var count = (await _notificationRepository.GetUserNotificationsAsync(userId, unreadOnly: true)).Count();
                return Ok(count);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error getting unread notifications count for user {UserId}", User.GetUserId());
                return StatusCode(500, new { message = "Internal server error." });
            }
        }

        [HttpPut("{id}/mark-read")]
        public async Task<ActionResult> MarkNotificationAsRead(int id)
        {
            try
            {
                var userId = User.GetUserId();
                var notification = await _notificationRepository.GetByIdAsync(id);
                if (notification == null || notification.UserId != userId) return NotFound(new { message = "Notification not found or unauthorized." });

                notification.IsRead = true;
                await _notificationRepository.UpdateAsync(notification);
                _logger.LogInformation("Notification {NotificationId} marked as read by user {UserId}", id, userId);
                return Ok(new { message = "Notification marked as read." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error marking notification {NotificationId} as read for user {UserId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }

        [HttpDelete("{id}")]
        public async Task<ActionResult> DeleteNotification(int id)
        {
            try
            {
                var userId = User.GetUserId();
                var notification = await _notificationRepository.GetByIdAsync(id);
                if (notification == null || notification.UserId != userId) return NotFound(new { message = "Notification not found or unauthorized." });

                await _notificationRepository.DeleteAsync(notification);
                _logger.LogInformation("Notification {NotificationId} deleted by user {UserId}", id, userId);
                return Ok(new { message = "Notification deleted." });
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error deleting notification {NotificationId} for user {UserId}", id, User.GetUserId());
                return BadRequest(new { message = ex.Message });
            }
        }
    }
}
