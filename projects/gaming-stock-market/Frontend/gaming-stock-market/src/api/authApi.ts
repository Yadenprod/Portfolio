import api from 'api/api';
import type { LoginRequest, RegisterRequest, AuthResponse, RefreshTokenRequest, VerifyEmailRequest, ForgotPasswordRequest, ResetPasswordRequest } from 'types/api';

export const authApi = {
  register: (data: RegisterRequest) => api.post<AuthResponse>('/Auth/register', data),
  login: (data: LoginRequest) => api.post<AuthResponse>('/Auth/login', data),
  refreshToken: (data: RefreshTokenRequest) => api.post<AuthResponse>('/Auth/refresh-token', data),
  verifyEmail: (data: VerifyEmailRequest) => api.post('/Auth/verify-email', data),
  forgotPassword: (data: ForgotPasswordRequest) => api.post('/Auth/forgot-password', data),
  resetPassword: (data: ResetPasswordRequest) => api.post('/Auth/reset-password', data),
};
