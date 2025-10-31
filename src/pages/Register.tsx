// Página de registro de novos usuários

import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { UserPlus, User, Lock, Eye, EyeOff, Shield } from 'lucide-react';
import { api, APIError } from '../lib/api';
import type { CreateUserResponse } from '../types';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { toast } from 'sonner';

export function Register() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    role: 'public',
    clearance: 1
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleInputChange = (field: string, value: string | number) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const validateForm = () => {
    if (!formData.username.trim()) {
      toast.error('Username é obrigatório');
      return false;
    }

    if (formData.username.length < 3) {
      toast.error('Username deve ter pelo menos 3 caracteres');
      return false;
    }

    if (!formData.password) {
      toast.error('Senha é obrigatória');
      return false;
    }

    if (formData.password.length < 6) {
      toast.error('Senha deve ter pelo menos 6 caracteres');
      return false;
    }

    if (formData.password !== formData.confirmPassword) {
      toast.error('Senhas não coincidem');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const userData = {
        username: formData.username.trim(),
        password: formData.password,
        role: formData.role,
        clearance: formData.clearance
      };

      const response = await api.post<CreateUserResponse>('/auth/create-user', userData);

      toast.success('Usuário criado com sucesso!', {
        description: `Username: ${response.username} | Role: ${response.role} | Clearance: ${response.clearance}`
      });

      // Navegar para login com username preenchido
      navigate('/login', { 
        state: { 
          username: response.username,
          message: 'Usuário criado! Agora você pode fazer login.' 
        }
      });

    } catch (error) {
      console.error('Erro ao criar usuário:', error);
      
      if (error instanceof APIError) {
        if (error.status === 409) {
          toast.error('Username já existe', {
            description: 'Escolha um username diferente'
          });
        } else {
          toast.error('Erro ao criar usuário', {
            description: error.message
          });
        }
      } else {
        toast.error('Erro de conexão', {
          description: 'Verifique se o servidor está rodando'
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const roleDescriptions = {
    public: 'Funcionário padrão - Acesso a dados públicos',
    director: 'Diretor regional - Acesso a relatórios regionais',
    minister: 'Ministro - Acesso total ao sistema'
  };

  const clearanceDescriptions = {
    1: 'Nível 1 - Dados públicos e básicos',
    2: 'Nível 2 - Dados regionais e relatórios',
    3: 'Nível 3 - Dados confidenciais e estratégicos'
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <div className="p-6">
          {/* Header */}
          <div className="text-center mb-6">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-green-600 to-blue-600 rounded-full flex items-center justify-center mb-4">
              <UserPlus className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-gray-900">
              Criar Nova Conta
            </h1>
            <p className="text-gray-600 mt-2">
              Sistema de Monitoramento Ambiental
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Username */}
            <div>
              <Label htmlFor="username">Username</Label>
              <div className="relative">
                <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="username"
                  type="text"
                  value={formData.username}
                  onChange={(e) => handleInputChange('username', e.target.value)}
                  placeholder="Digite seu username"
                  className="pl-10"
                  disabled={loading}
                  autoComplete="username"
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <Label htmlFor="password">Senha</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={(e) => handleInputChange('password', e.target.value)}
                  placeholder="Digite sua senha"
                  className="pl-10 pr-10"
                  disabled={loading}
                  autoComplete="new-password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  disabled={loading}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <Label htmlFor="confirmPassword">Confirmar Senha</Label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  id="confirmPassword"
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={formData.confirmPassword}
                  onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                  placeholder="Confirme sua senha"
                  className="pl-10 pr-10"
                  disabled={loading}
                  autoComplete="new-password"
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3 top-3 text-gray-400 hover:text-gray-600"
                  disabled={loading}
                >
                  {showConfirmPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                </button>
              </div>
            </div>

            {/* Role Selection */}
            <div>
              <Label htmlFor="role">Função</Label>
              <Select
                value={formData.role}
                onValueChange={(value: string) => handleInputChange('role', value)}
                disabled={loading}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione a função" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="public">
                    <div className="flex items-center gap-2">
                      <User className="h-4 w-4" />
                      <span>Funcionário Público</span>
                    </div>
                  </SelectItem>
                  <SelectItem value="director">
                    <div className="flex items-center gap-2">
                      <Shield className="h-4 w-4" />
                      <span>Diretor Regional</span>
                    </div>
                  </SelectItem>
                  <SelectItem value="minister">
                    <div className="flex items-center gap-2">
                      <Shield className="h-4 w-4 text-red-600" />
                      <span>Ministro</span>
                    </div>
                  </SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-gray-500 mt-1">
                {roleDescriptions[formData.role as keyof typeof roleDescriptions]}
              </p>
            </div>

            {/* Clearance Level */}
            <div>
              <Label htmlFor="clearance">Nível de Acesso</Label>
              <Select
                value={formData.clearance.toString()}
                onValueChange={(value: string) => handleInputChange('clearance', parseInt(value))}
                disabled={loading}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Selecione o nível" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="1">Nível 1 - Público</SelectItem>
                  <SelectItem value="2">Nível 2 - Regional</SelectItem>
                  <SelectItem value="3">Nível 3 - Confidencial</SelectItem>
                </SelectContent>
              </Select>
              <p className="text-xs text-gray-500 mt-1">
                {clearanceDescriptions[formData.clearance as keyof typeof clearanceDescriptions]}
              </p>
            </div>

            {/* Submit Button */}
            <Button 
              type="submit" 
              className="w-full" 
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                  Criando...
                </>
              ) : (
                <>
                  <UserPlus className="w-4 h-4 mr-2" />
                  Criar Conta
                </>
              )}
            </Button>
          </form>

          {/* Footer */}
          <div className="mt-6 text-center text-sm">
            <p className="text-gray-600">
              Já tem uma conta?{' '}
              <Link 
                to="/login" 
                className="text-blue-600 hover:text-blue-700 font-medium"
              >
                Fazer Login
              </Link>
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
}