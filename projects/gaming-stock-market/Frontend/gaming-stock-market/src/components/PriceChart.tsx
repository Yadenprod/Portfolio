import React from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface PriceChartProps {
  data: { date: string; price: number }[];
  title: string;
}

const PriceChart: React.FC<PriceChartProps> = ({ data, title }) => {
  const chartData = {
    labels: data.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Price',
        data: data.map(item => item.price),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.5)',
        tension: 0.1,
        fill: false,
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: title,
        color: '#ffffff',
      },
    },
    scales: {
      x: {
        ticks: { color: '#aaaaaa' },
        grid: { color: '#444444' },
      },
      y: {
        ticks: { color: '#aaaaaa' },
        grid: { color: '#444444' },
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default PriceChart;
