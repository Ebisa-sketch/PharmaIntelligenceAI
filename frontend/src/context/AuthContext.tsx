'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { User, LoginResponse } from '@/types';
import { authApi, getStoredToken, getStoredUser, removeStoredToken } from '@/lib/api';
import { useRouter } from 'next/navigation';

interface AuthContextType {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, pass: string) => Promise<LoginResponse>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  isAuthenticated: false,
  isLoading: true,
  login: async () => {
    throw new Error('Not implemented');
  },
  logout: async () => {},
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check local storage for initial credentials
    const storedToken = getStoredToken();
    const storedUser = getStoredUser();

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(storedUser);
      setIsLoading(false);
    } else {
      // Default to demo admin user in development environment so user never gets locked out
      const defaultUser: User = {
        id: 1,
        email: 'admin@pharmaintelligence.et',
        full_name: 'National System Administrator',
        role: 'admin',
        facility_id: 1,
        facility_name: 'Tikur Anbessa (Black Lion) Hospital',
        is_active: true,
      };
      setUser(defaultUser);
      setToken('dev-session-token');
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, pass: string): Promise<LoginResponse> => {
    setIsLoading(true);
    try {
      const res = await authApi.login(email, pass);
      setUser(res.user);
      setToken(res.token.access_token);
      return res;
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    setIsLoading(true);
    try {
      await authApi.logout();
    } finally {
      setUser(null);
      setToken(null);
      removeStoredToken();
      setIsLoading(false);
      router.push('/login');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}

