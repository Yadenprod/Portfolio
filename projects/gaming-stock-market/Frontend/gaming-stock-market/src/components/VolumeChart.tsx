import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

interface VolumeChartProps {
  data: { date: string; volume: number }[];
  title: string;
}

const VolumeChart: React.FC<VolumeChartProps> = ({ data, title }) => {
  const chartData = {
    labels: data.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Volume',
        data: data.map(item => item.volume),
        backgroundColor: 'rgba(153, 102, 255, 0.5)',
        borderColor: 'rgb(153, 102, 255)',
        borderWidth: 1,
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

  return <Bar data={chartData} options={options} />;
};

export default VolumeChart;
