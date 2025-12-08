import React, { useEffect, useState } from 'react';
import axios from 'axios';

interface Transaction {
  id: number;
  userId: number;
  username: string; // Assuming we can fetch username
  type: string;
  amount: number;
  status: string;
  createdAt: string;
  completedAt?: string;
  notes?: string;
}

const TransactionManagement: React.FC = () => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = async () => {
    try {
      setLoading(true);
      const response = await axios.get<Transaction[]>('http://localhost:5000/api/admin/transactions'); // Adjust API endpoint
      setTransactions(response.data);
    } catch (err) {
      setError('Failed to fetch transactions.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="text-center text-white">Loading transactions...</div>;
  if (error) return <div className="text-center text-red-500">Error: {error}</div>;

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <h1 className="text-3xl font-bold mb-6 text-indigo-400">Transaction Management</h1>
      <div className="overflow-x-auto">
        <table className="min-w-full bg-gray-800 rounded-lg shadow-md">
          <thead>
            <tr className="bg-gray-700">
              <th className="py-3 px-4 text-left">ID</th>
              <th className="py-3 px-4 text-left">User</th>
              <th className="py-3 px-4 text-left">Type</th>
              <th className="py-3 px-4 text-left">Amount</th>
              <th className="py-3 px-4 text-left">Status</th>
              <th className="py-3 px-4 text-left">Created At</th>
              <th className="py-3 px-4 text-left">Completed At</th>
              <th className="py-3 px-4 text-left">Notes</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction) => (
              <tr key={transaction.id} className="border-b border-gray-700 last:border-b-0">
                <td className="py-3 px-4">{transaction.id}</td>
                <td className="py-3 px-4">{transaction.username} (ID: {transaction.userId})</td>
                <td className="py-3 px-4">{transaction.type}</td>
                <td className="py-3 px-4">{transaction.amount.toFixed(2)}</td>
                <td className="py-3 px-4">
                  <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
                    transaction.status === 'COMPLETED' ? 'bg-green-500' :
                    transaction.status === 'PENDING' ? 'bg-yellow-500' :
                    'bg-red-500'
                  }`}>
                    {transaction.status}
                  </span>
                </td>
                <td className="py-3 px-4">{new Date(transaction.createdAt).toLocaleDateString()}</td>
                <td className="py-3 px-4">{transaction.completedAt ? new Date(transaction.completedAt).toLocaleDateString() : 'N/A'}</td>
                <td className="py-3 px-4">{transaction.notes || 'N/A'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TransactionManagement;
