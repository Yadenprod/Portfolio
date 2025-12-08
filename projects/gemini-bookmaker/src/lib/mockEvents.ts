
export type Outcome = {
  name: string;
  price: number;
};

export type Market = {
  key: string;
  outcomes: Outcome[];
};

export type Event = {
  id: string;
  sport: string;
  homeTeam: string;
  awayTeam: string;
  startTime: Date;
  markets: Market[];
};

export const mockEvents: Event[] = [
  {
    id: "1",
    sport: "Football",
    homeTeam: "Manchester United",
    awayTeam: "Manchester City",
    startTime: new Date(Date.now() + 1000 * 60 * 60 * 2), // 2 hours from now
    markets: [
      {
        key: "h2h",
        outcomes: [
          { name: "Manchester United", price: 3.5 },
          { name: "Draw", price: 3.4 },
          { name: "Manchester City", price: 2.1 },
        ],
      },
    ],
  },
  {
    id: "2",
    sport: "Football",
    homeTeam: "Liverpool",
    awayTeam: "Chelsea",
    startTime: new Date(Date.now() + 1000 * 60 * 60 * 4), // 4 hours from now
    markets: [
      {
        key: "h2h",
        outcomes: [
          { name: "Liverpool", price: 2.2 },
          { name: "Draw", price: 3.6 },
          { name: "Chelsea", price: 3.1 },
        ],
      },
    ],
  },
  {
    id: "3",
    sport: "Football",
    homeTeam: "Arsenal",
    awayTeam: "Tottenham Hotspur",
    startTime: new Date(Date.now() + 1000 * 60 * 60 * 24), // 1 day from now
    markets: [
      {
        key: "h2h",
        outcomes: [
          { name: "Arsenal", price: 2.5 },
          { name: "Draw", price: 3.5 },
          { name: "Tottenham Hotspur", price: 2.8 },
        ],
      },
    ],
  },
    {
    id: "4",
    sport: "Basketball",
    homeTeam: "Los Angeles Lakers",
    awayTeam: "Golden State Warriors",
    startTime: new Date(Date.now() + 1000 * 60 * 60 * 3), // 3 hours from now
    markets: [
      {
        key: "h2h",
        outcomes: [
          { name: "Los Angeles Lakers", price: 1.9 },
          { name: "Golden State Warriors", price: 1.9 },
        ],
      },
    ],
  },
];
