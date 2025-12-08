
'use client';

import React from 'react';
import { useTelegram } from '@/hooks/useTelegram';
import { FaUserCircle } from 'react-icons/fa';

const Profile = () => {
  const { user } = useTelegram();

  const userName = user ? `${user.first_name} ${user.last_name || ''}`.trim() : 'Guest';

  return (
    <div className="p-2 text-white rounded-lg bg-gray-700">
        <div className="flex items-center">
            <FaUserCircle className="mr-3 text-2xl" />
            <span className="font-semibold">{userName}</span>
        </div>
    </div>
  );
};

export default Profile;
