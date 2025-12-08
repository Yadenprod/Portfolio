import React, { useState } from 'react';
import Input from 'components/Input'; // Updated path
import Button from 'components/Button'; // Updated path

const SettingsPage: React.FC = () => {
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [email, setEmail] = useState('user@example.com'); // Placeholder
  const [username, setUsername] = useState('currentuser'); // Placeholder

  const handlePasswordChange = (e: React.FormEvent) => {
    e.preventDefault();
    if (newPassword !== confirmNewPassword) {
      alert("New passwords do not match!");
      return;
    }
    // TODO: Implement password change API call
    console.log("Changing password...");
    alert("Password change functionality is not yet implemented.");
  };

  const handleProfileUpdate = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement profile update API call
    console.log("Updating profile...");
    alert("Profile update functionality is not yet implemented.");
  };

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold text-white mb-6">Settings</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Profile Settings */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4">Profile Information</h2>
          <form onSubmit={handleProfileUpdate}>
            <Input
              label="Username"
              id="username"
              type="text"
              value={username}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setUsername(e.target.value)}
              className="bg-gray-700 border-gray-600 text-white"
            />
            <Input
              label="Email"
              id="email"
              type="email"
              value={email}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setEmail(e.target.value)}
              className="bg-gray-700 border-gray-600 text-white"
            />
            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">Update Profile</Button>
          </form>
        </div>

        {/* Change Password */}
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 className="text-xl font-semibold text-white mb-4">Change Password</h2>
          <form onSubmit={handlePasswordChange}>
            <Input
              label="Current Password"
              id="currentPassword"
              type="password"
              value={currentPassword}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setCurrentPassword(e.target.value)}
              required
              className="bg-gray-700 border-gray-600 text-white"
            />
            <Input
              label="New Password"
              id="newPassword"
              type="password"
              value={newPassword}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setNewPassword(e.target.value)}
              required
              className="bg-gray-700 border-gray-600 text-white"
            />
            <Input
              label="Confirm New Password"
              id="confirmNewPassword"
              type="password"
              value={confirmNewPassword}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setConfirmNewPassword(e.target.value)}
              required
              className="bg-gray-700 border-gray-600 text-white"
            />
            <Button type="submit" className="w-full bg-blue-600 hover:bg-blue-700">Change Password</Button>
          </form>
        </div>
      </div>

      {/* TODO: Add other settings like 2FA, Notification preferences, etc. */}
    </div>
  );
};

export default SettingsPage;
