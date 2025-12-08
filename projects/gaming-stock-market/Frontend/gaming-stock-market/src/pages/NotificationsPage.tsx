import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import type { AppDispatch, RootState } from 'store'; // Updated path
import { fetchNotificationsStart, fetchNotificationsSuccess, fetchNotificationsFailure, markNotificationAsRead, deleteNotification } from 'slices/notificationSlice'; // Updated path
import { notificationApi } from 'api/notificationApi'; // Updated path
import LoadingSpinner from 'components/LoadingSpinner'; // Updated path
import Button from 'components/Button'; // Updated path
import type { Notification } from 'slices/notificationSlice'; // Updated path

const NotificationsPage: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { notifications, loading, error } = useSelector((state: RootState) => state.notification);

  useEffect(() => {
    const getNotifications = async () => {
      dispatch(fetchNotificationsStart());
      try {
        const response = await notificationApi.getUserNotifications(); // Uncomment when notificationApi is ready
        dispatch(fetchNotificationsSuccess(response.data));
        // Dummy data for now:
        // dispatch(fetchNotificationsSuccess([
        //   { id: 1, type: "Trade", message: "Your buy order for PlayerX was filled.", isRead: false, createdAt: new Date().toISOString() },
        //   { id: 2, type: "System", message: "Welcome to Gaming Stock Market!", isRead: true, createdAt: new Date().toISOString() },
        //   { id: 3, type: "Achievement", message: "First Trade achievement unlocked!", isRead: false, createdAt: new Date().toISOString() },
        // ]));

      } catch (err: any) {
        dispatch(fetchNotificationsFailure(err.response?.data?.message || 'Failed to fetch notifications.'));
        // dispatch(fetchNotificationsFailure('Failed to fetch notifications (dummy error).'));
      }
    };
    getNotifications();
  }, [dispatch]);

  const handleMarkAsRead = (id: number) => {
    // TODO: Call API to mark as read
    console.log(`Marking notification ${id} as read`);
    dispatch(markNotificationAsRead(id));
  };

  const handleDelete = (id: number) => {
    // TODO: Call API to delete notification
    console.log(`Deleting notification ${id}`);
    dispatch(deleteNotification(id));
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <div className="text-red-500 text-center mt-8">Error: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">Notifications</h1>
      {notifications.length === 0 ? (
        <p className="text-gray-400 text-center">No notifications yet.</p>
      ) : (
        <div className="space-y-4">
          {notifications.map((notification: Notification) => (
            <div key={notification.id} className={`bg-gray-800 p-4 rounded-lg shadow-lg flex justify-between items-center ${notification.isRead ? 'opacity-75' : ''}`}>
              <div>
                <p className="text-lg font-semibold text-white">{notification.message}</p>
                <p className="text-sm text-gray-400">Type: {notification.type} - {new Date(notification.createdAt).toLocaleString()}</p>
              </div>
              <div className="flex space-x-2">
                {!notification.isRead && (
                  <Button size="sm" onClick={() => handleMarkAsRead(notification.id)}>Mark as Read</Button>
                )}
                <Button variant="danger" size="sm" onClick={() => handleDelete(notification.id)}>Delete</Button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default NotificationsPage;
