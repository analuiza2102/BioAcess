// Componente para proteger rotas por autenticação e clearance

import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuthContext } from '../contexts/AuthContext';
import type { ClearanceLevel } from '../types';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredLevel?: ClearanceLevel;
}

export function ProtectedRoute({ children, requiredLevel }: ProtectedRouteProps) {
  const { isAuthenticated, hasAccess, loading } = useAuthContext();
  const navigate = useNavigate();
  const location = useLocation();
  const [shouldRender, setShouldRender] = useState(false);

  useEffect(() => {
    // Aguarda o carregamento do estado de autenticação
    if (loading) {
      setShouldRender(false);
      return;
    }

    // Verifica autenticação
    if (!isAuthenticated) {
      setShouldRender(false);
      // Adiciona pequeno delay para evitar navegação durante renderização
      const timer = setTimeout(() => {
        navigate('/login', { replace: true });
      }, 0);
      return () => clearTimeout(timer);
    }

    // Verifica clearance
    if (requiredLevel && !hasAccess(requiredLevel)) {
      setShouldRender(false);
      const timer = setTimeout(() => {
        navigate('/access-denied', { replace: true });
      }, 0);
      return () => clearTimeout(timer);
    }

    // Se passou por todas as verificações, permite renderização
    setShouldRender(true);
  }, [loading, isAuthenticated, requiredLevel, hasAccess, navigate, location]);

  // Estado de carregamento
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-muted-foreground">Carregando...</p>
        </div>
      </div>
    );
  }

  // Estado de redirecionamento
  if (!shouldRender) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-muted-foreground">Redirecionando...</p>
        </div>
      </div>
    );
  }

  return <>{children}</>;
}
