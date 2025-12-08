'use client';

import React from 'react';
import Link from 'next/link';
import { FaFutbol, FaBroadcastTower } from 'react-icons/fa';
import Profile from './Profile';

const Sidebar = () => {
  return (
    <aside className="w-64 bg-gray-800 p-4 flex flex-col justify-between">
      <div>
        <div className="text-white text-2xl font-bold mb-8">Gemini Bet</div>
        <nav>
          <ul>
            <li>
              <Link href="/" className="flex items-center p-3 text-white rounded-lg hover:bg-gray-700 transition-colors">
                <FaFutbol className="mr-3" />
                <span>Sports</span>
              </Link>
            </li>
            <li>
              <Link href="/live" className="flex items-center p-3 text-white rounded-lg hover:bg-gray-700 transition-colors">
                <FaBroadcastTower className="mr-3" />
                <span>Live</span>
              </Link>
            </li>
          </ul>
        </nav>
      </div>
      <Profile />
    </aside>
  );
};

export default Sidebar;