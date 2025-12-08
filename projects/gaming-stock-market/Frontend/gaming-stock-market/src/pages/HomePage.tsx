import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[calc(100vh-160px)]">
      <h1 className="text-5xl font-extrabold text-white mb-6">Welcome to Gaming Stock Market</h1>
      <p className="text-xl text-gray-300 mb-8 text-center max-w-2xl">
        Trade shares of your favorite esports players and teams, analyze market trends,
        and build your ultimate gaming portfolio.
      </p>
      <div className="space-x-4">
        <a href="/register" className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg text-lg transition-colors duration-200">
          Get Started
        </a>
        <a href="/players" className="bg-gray-700 hover:bg-gray-600 text-white font-bold py-3 px-6 rounded-lg text-lg transition-colors duration-200">
          Browse Players
        </a>
      </div>
    </div>
  );
};

export default HomePage;
