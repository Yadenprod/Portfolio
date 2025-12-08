import api from 'api/api';
import type { NotificationResponse } from 'types/api';

export const notificationApi = {
  getUserNotifications: () => api.get<NotificationResponse[]>('/Notification'),
  markNotificationAsRead: (notificationId: number) => api.put(`/Notification/${notificationId}/read`),
  markAllNotificationsAsRead: () => api.put('/Notification/read-all'),
  deleteNotification: (notificationId: number) => api.delete(`/Notification/${notificationId}`),
};
