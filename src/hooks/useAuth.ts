// Hook de autenticação para gerenciar estado do usuário

import { useState, useEffect, useCallback } from 'react';
import type { User } from '../types';

const TOKEN_KEY = 'bioaccess_token';
const USER_KEY = 'bioaccess_user';

export function useAuth() {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  // Carrega dados do sessionStorage ao montar
  useEffect(() => {
    const storedToken = sessionStorage.getItem(TOKEN_KEY);
    const storedUser = sessionStorage.getItem(USER_KEY);

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = useCallback((authToken: string, userData: User) => {
    sessionStorage.setItem(TOKEN_KEY, authToken);
    sessionStorage.setItem(USER_KEY, JSON.stringify(userData));
    setToken(authToken);
    setUser(userData);
  }, []);

  const logout = useCallback(() => {
    sessionStorage.removeItem(TOKEN_KEY);
    sessionStorage.removeItem(USER_KEY);
    setToken(null);
    setUser(null);
  }, []);

  const hasAccess = useCallback((requiredLevel: number): boolean => {
    if (!user) return false;
    return user.clearance >= requiredLevel;
  }, [user]);

  return {
    user,
    token,
    loading,
    isAuthenticated: !!token && !!user,
    login,
    logout,
    hasAccess
  };
}
