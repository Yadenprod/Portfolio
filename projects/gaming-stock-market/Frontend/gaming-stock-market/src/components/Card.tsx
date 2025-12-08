import React from 'react';
import { Link } from 'react-router-dom';
import type { PlayerResponse, TeamResponse } from 'types/api';

interface CardProps {
  item: PlayerResponse | TeamResponse;
  type: 'player' | 'team';
}

const Card: React.FC<CardProps> = ({ item, type }) => {
  const isPlayer = type === 'player';
  const title = isPlayer ? (item as PlayerResponse).name : (item as TeamResponse).name;
  const currentPrice = item.currentPrice.toFixed(2);

  return (
    <div className="bg-gray-800 rounded-lg shadow-lg overflow-hidden flex flex-col">
      <div className="p-4 flex-grow">
        <h3 className="text-xl font-bold mb-2 text-white">{title}</h3>
        <p className="text-gray-400 text-sm">Game: {item.game}</p>
        {isPlayer && (item as PlayerResponse).team && <p className="text-gray-400 text-sm">Team: {(item as PlayerResponse).team}</p>}
        <p className="text-lg font-semibold mt-2 text-green-400">Price: ${currentPrice}</p>
        {isPlayer && (item as PlayerResponse).rating && <p className="text-gray-400 text-sm">Rating: {(item as PlayerResponse).rating?.toFixed(2)}</p>}
        {isPlayer && <p className="text-gray-400 text-sm">Popularity: {(item as PlayerResponse).popularityScore}</p>}
        {!isPlayer && (item as TeamResponse).ranking && <p className="text-gray-400 text-sm">Ranking: {(item as TeamResponse).ranking}</p>}
      </div>
      <div className="p-4 bg-gray-700">
        <Link 
          to={isPlayer ? `/players/${item.id}` : `/teams/${item.id}`}
          className="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          View Details
        </Link>
      </div>
    </div>
  );
};

export default Card;
