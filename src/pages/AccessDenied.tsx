// Página de acesso negado

import { useNavigate } from 'react-router-dom';
import { ShieldAlert, ArrowLeft, Home } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { useAuthContext } from '../contexts/AuthContext';

export function AccessDenied() {
  const navigate = useNavigate();
  const { user } = useAuthContext();

  return (
    <div className="min-h-screen bg-gradient-to-br from-red-50 to-orange-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <Card className="max-w-md w-full p-8 text-center">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-red-100 dark:bg-red-900/30 rounded-full mb-6">
          <ShieldAlert className="w-10 h-10 text-red-600 dark:text-red-400" />
        </div>

        <h1 className="text-2xl mb-2">Acesso Negado</h1>
        
        <p className="text-muted-foreground mb-6">
          Você não possui clearance suficiente para acessar esta página.
        </p>

        {user && (
          <div className="bg-muted/50 rounded-lg p-4 mb-6 text-sm">
            <p className="text-muted-foreground mb-1">
              Seu nível de clearance atual:
            </p>
            <p className="font-medium">
              Nível {user.clearance} - {user.role}
            </p>
          </div>
        )}

        <div className="space-y-2">
          <Button
            onClick={() => navigate('/dashboard')}
            className="w-full"
          >
            <Home className="w-4 h-4 mr-2" />
            Ir para Dashboard
          </Button>
          
          <Button
            onClick={() => navigate(-1)}
            variant="outline"
            className="w-full"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar
          </Button>
        </div>
      </Card>
    </div>
  );
}
