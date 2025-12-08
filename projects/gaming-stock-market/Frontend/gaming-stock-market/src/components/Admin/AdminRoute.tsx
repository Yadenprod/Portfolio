import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useSelector } from 'react-redux';
import type { RootState } from 'store'; // Updated path

interface AdminRouteProps {
  children?: React.ReactNode;
}

const AdminRoute: React.FC<AdminRouteProps> = ({ children }) => {
  const isAuthenticated = useSelector((state: RootState) => state.auth.isAuthenticated);
  // const userRole = useSelector((state: RootState) => state.auth.user?.role); // This assumes a 'user' object with a 'role' property
  // For now, we'll just check if the user is authenticated. 
  // In a real application, you'd decode the JWT or fetch user details to check the role.

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // if (userRole !== 'Admin') {
  //   return <Navigate to="/dashboard" replace />;
  // }

  return children ? <>{children}</> : <Outlet />;
};

export default AdminRoute;
