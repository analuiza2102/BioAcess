// Dashboard principal com acesso aos níveis de dados

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ShieldCheck, 
  LogOut, 
  Lock, 
  Unlock,
  FileText,
  User,
  Shield,
  Crown,
  CheckCircle,
  XCircle,
  Sun,
  Moon
} from 'lucide-react';
import { useAuthContext } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { api, APIError } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { toast } from 'sonner';
import { ROLE_LABELS, LEVEL_LABELS } from '../types';

export function Dashboard() {
  const { user, token, logout, hasAccess } = useAuthContext();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [loadingLevel, setLoadingLevel] = useState<number | null>(null);
  const [levelData, setLevelData] = useState<Record<number, any>>({});
  const [hasBiometric, setHasBiometric] = useState<boolean | null>(null);
  const [loadingBiometric, setLoadingBiometric] = useState(false);

  const checkBiometricStatus = async () => {
    if (!user?.username) return;
    
    setLoadingBiometric(true);
    try {
      const status = await api.checkBiometricStatus(user.username);
      setHasBiometric(status.has_biometric);
    } catch (error) {
      console.error('Erro ao verificar status da biometria:', error);
      setHasBiometric(false);
    } finally {
      setLoadingBiometric(false);
    }
  };

  useEffect(() => {
    checkBiometricStatus();
  }, [user?.username]);

  const handleLogout = () => {
    logout();
    toast.info('Logout realizado com sucesso');
    setTimeout(() => navigate('/login'), 100);
  };

  const handleAccessLevel = async (level: number) => {
    if (!token) {
      toast.error('Token não encontrado. Faça login novamente.');
      return;
    }

    setLoadingLevel(level);

    try {
      const response = await api.fetchLevel(level, token);
      
      setLevelData(prev => ({
        ...prev,
        [level]: response.data
      }));
      
      toast.success(`Acesso ao ${LEVEL_LABELS[level]} concedido!`);
    } catch (error) {
      console.error('Erro ao acessar nível:', error);
      
      if (error instanceof APIError) {
        if (error.status === 403) {
          toast.error('Acesso negado! Sua clearance é insuficiente.');
        } else if (error.status === 401) {
          toast.error('Token inválido ou expirado. Faça login novamente.');
          logout();
          setTimeout(() => navigate('/login'), 100);
        } else {
          toast.error(error.message);
        }
      } else {
        toast.error('Erro ao conectar com o servidor.');
      }
    } finally {
      setLoadingLevel(null);
    }
  };

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'minister': return <Crown className="w-5 h-5" />;
      case 'director': return <Shield className="w-5 h-5" />;
      default: return <User className="w-5 h-5" />;
    }
  };

  const getRoleBadgeColor = (clearance: number) => {
    switch (clearance) {
      case 3: return 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300';
      case 2: return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300';
      default: return 'bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300';
    }
  };

  const levels = [
    {
      level: 1,
      title: 'Nível 1 - Público',
      description: 'Informações públicas e dados gerais',
      icon: Unlock,
      color: 'text-green-600 dark:text-green-400'
    },
    {
      level: 2,
      title: 'Nível 2 - Diretoria',
      description: 'Relatórios gerenciais e métricas',
      icon: Shield,
      color: 'text-blue-600 dark:text-blue-400'
    },
    {
      level: 3,
      title: 'Nível 3 - Ministério',
      description: 'Dados confidenciais e estratégicos',
      icon: Crown,
      color: 'text-purple-600 dark:text-purple-400'
    }
  ];

  // Safety check (ProtectedRoute should handle this, but just in case)
  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Carregando dados do usuário...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen" style={{
      background: theme === 'light' 
        ? 'linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%)'
        : 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #262626 100%)'
    }}>
      {/* Header */}
      <header className="border-b shadow-lg" style={{
        background: theme === 'light' ? 'rgba(255, 255, 255, 0.8)' : 'rgba(26, 26, 26, 0.8)',
        borderColor: theme === 'light' ? 'rgba(255, 255, 255, 0.3)' : 'rgba(64, 64, 64, 0.3)',
        backdropFilter: 'blur(20px)',
        WebkitBackdropFilter: 'blur(20px)'
      }}>
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl flex items-center justify-center shadow-lg" style={{
              background: theme === 'light' 
                ? 'linear-gradient(135deg, #16a34a, #15803d)' 
                : 'linear-gradient(135deg, #3b82f6, #1d4ed8)'
            }}>
              <ShieldCheck className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold leading-tight" style={{
                color: theme === 'light' ? '#059669' : '#10b981'
              }}>
                BioAccess
              </h1>
              <p className="text-xs font-medium" style={{
                color: theme === 'light' ? '#64748b' : '#94a3b8'
              }}>
                🔐 Sistema de Autenticação Biométrica Facial
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {user.username === 'ana.luiza' && (
              <Button
                variant="outline"
                size="sm"
                onClick={() => navigate('/admin')}
                className="bg-red-50 dark:bg-red-950 border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900 cursor-pointer"
              >
                <Shield className="w-4 h-4 mr-2" />
                Admin
              </Button>
            )}
            <Button
              variant="outline"
              size="sm"
              onClick={toggleTheme}
              className="p-2 cursor-pointer"
            >
              {theme === 'light' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleLogout}
              className="cursor-pointer"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Sair
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* User Info Card */}
        <Card className="p-6 mb-8 border-2 shadow-xl" style={{
          background: theme === 'light' ? 'rgba(255, 255, 255, 0.25)' : 'rgba(26, 26, 26, 0.25)',
          border: theme === 'light' ? '1px solid rgba(255, 255, 255, 0.3)' : '1px solid rgba(64, 64, 64, 0.3)',
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          borderRadius: '20px',
          boxShadow: theme === 'light' ? '0 8px 32px rgba(31, 38, 135, 0.37)' : '0 8px 32px rgba(0, 0, 0, 0.37)'
        }}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-6">
              <div className="w-20 h-20 rounded-2xl flex items-center justify-center text-white shadow-xl" style={{
                background: theme === 'light' 
                  ? 'linear-gradient(135deg, #16a34a, #15803d)' 
                  : 'linear-gradient(135deg, #3b82f6, #1d4ed8)'
              }}>
                {getRoleIcon(user.role)}
              </div>
              <div>
                <h2 className="text-2xl font-bold mb-2" style={{
                  color: theme === 'light' ? '#1e293b' : '#f1f5f9'
                }}>
                  Bem-vindo, {user.username}! 👋
                </h2>
                <div className="flex items-center gap-3">
                  <Badge className={`${getRoleBadgeColor(user.clearance)} text-sm px-3 py-1 shadow-md`}>
                    {ROLE_LABELS[user.role]}
                  </Badge>
                  <div className="flex items-center gap-2 rounded-full px-3 py-1" style={{
                    background: theme === 'light' 
                      ? 'rgba(22, 163, 74, 0.1)'
                      : 'rgba(59, 130, 246, 0.2)'
                  }}>
                    <div className="w-2 h-2 rounded-full animate-pulse" style={{
                      background: theme === 'light' ? '#16a34a' : '#3b82f6'
                    }}></div>
                    <span className="text-sm font-medium" style={{
                      color: theme === 'light' ? '#16a34a' : '#3b82f6'
                    }}>
                      Clearance Nível {user.clearance}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </Card>

        {/* Biometric Status Card */}
        <Card className="p-6 mb-8" style={{
          background: hasBiometric === true 
            ? (theme === 'light' ? 'rgba(255, 255, 255, 0.4)' : 'rgba(26, 26, 26, 0.25)')
            : (theme === 'light' ? 'rgba(255, 255, 255, 0.4)' : 'rgba(26, 26, 26, 0.25)'),
          border: hasBiometric === true
            ? (theme === 'light' ? '1px solid rgba(34, 197, 94, 0.3)' : '1px solid rgba(34, 197, 94, 0.3)')
            : (theme === 'light' ? '1px solid rgba(251, 146, 60, 0.3)' : '1px solid rgba(251, 146, 60, 0.3)'),
          backdropFilter: 'blur(16px)',
          WebkitBackdropFilter: 'blur(16px)',
          borderRadius: '20px',
          boxShadow: theme === 'light' ? '0 8px 32px rgba(31, 38, 135, 0.37)' : '0 8px 32px rgba(0, 0, 0, 0.37)'
        }}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className={`p-3 rounded-full ${
                hasBiometric === true
                  ? (theme === 'light' ? 'bg-green-100' : 'bg-green-800')
                  : (theme === 'light' ? 'bg-orange-100' : 'bg-orange-800')
              }`}>
                {loadingBiometric ? (
                  <div className="animate-spin w-6 h-6 border-2 border-gray-600 border-t-transparent rounded-full" />
                ) : hasBiometric === true ? (
                  <CheckCircle 
                    className="w-6 h-6"
                    style={{ color: theme === 'light' ? '#16a34a' : '#86efac' }}
                  />
                ) : (
                  <XCircle 
                    className="w-6 h-6"
                    style={{ color: theme === 'light' ? '#ea580c' : '#fdba74' }}
                  />
                )}
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-1" style={{
                  color: hasBiometric === true
                    ? (theme === 'light' ? '#166534' : '#86efac')
                    : (theme === 'light' ? '#ea580c' : '#fdba74')
                }}>
                  📸 {hasBiometric === true ? 'Biometria Cadastrada' : 'Cadastro de Biometria Facial'}
                </h3>
                <p className="text-sm" style={{
                  color: hasBiometric === true
                    ? (theme === 'light' ? '#15803d' : '#86efac')
                    : (theme === 'light' ? '#c2410c' : '#fdba74')
                }}>
                  {hasBiometric === true 
                    ? '✅ Sua biometria facial está ativa e pronta para uso'
                    : 'Cadastre uma imagem PNG/JPEG com fundo branco para acesso rápido e seguro'
                  }
                </p>
                <p className="text-xs mt-1" style={{
                  color: hasBiometric === true
                    ? (theme === 'light' ? '#059669' : '#6ee7b7')
                    : (theme === 'light' ? '#9a3412' : '#fed7aa')
                }}>
                  {hasBiometric === true 
                    ? '🔐 Você pode usar biometria na tela de login'
                    : '✨ Reconhecimento baseado em upload de imagem estática'
                  }
                </p>
              </div>
            </div>
            {hasBiometric !== true && (
              <Button
                onClick={() => {
                  navigate('/enroll');
                }}
                className="text-white shadow-lg cursor-pointer"
                size="lg"
                disabled={loadingBiometric}
                style={{
                  background: theme === 'light' 
                    ? 'linear-gradient(135deg, #16a34a 0%, #15803d 100%)'
                    : 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
                  border: 'none'
                }}
              >
                <User className="w-4 h-4 mr-2" />
                Cadastrar Biometria
              </Button>
            )}
            {hasBiometric === true && (
              <div className="flex flex-col gap-2">
                <Button
                  onClick={() => {
                    checkBiometricStatus();
                  }}
                  className="text-white shadow-md hover:opacity-90 cursor-pointer"
                  size="sm"
                  disabled={loadingBiometric}
                  style={{
                    background: theme === 'light' 
                      ? 'linear-gradient(135deg, #16a34a, #15803d)'
                      : 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                    border: theme === 'light' ? '1px solid #15803d' : '1px solid #1d4ed8'
                  }}
                >
                  🔄 Atualizar Status
                </Button>
                <Button
                  onClick={() => navigate('/enroll')}
                  className="text-white shadow-md cursor-pointer"
                  size="sm"
                  style={{
                    background: theme === 'light' 
                      ? 'linear-gradient(135deg, #16a34a, #15803d)'
                      : 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                    border: theme === 'light' ? '1px solid #15803d' : '1px solid #1d4ed8'
                  }}
                >
                  ↻ Recadastrar
                </Button>
              </div>
            )}
          </div>
        </Card>

        {/* Access Levels Grid */}
        <div className="mb-6">
          <h3 className="text-2xl font-bold mb-2" style={{
            color: theme === 'light' ? '#0f172a' : '#f1f5f9'
          }}>🔐 Níveis de Acesso Disponíveis</h3>
          <p style={{
            color: theme === 'light' ? '#475569' : '#94a3b8'
          }}>
            Você pode acessar dados de níveis iguais ou inferiores ao seu clearance. 
            Tentativas de acesso são registradas nos logs de auditoria.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          {levels.map((levelInfo) => {
            const hasLevelAccess = hasAccess(levelInfo.level);
            const isLoading = loadingLevel === levelInfo.level;
            const data = levelData[levelInfo.level];
            const Icon = levelInfo.icon;

            return (
              <Card
                key={levelInfo.level}
                className={`p-6 transition-all ${
                  hasLevelAccess 
                    ? 'hover:shadow-xl hover:scale-105 cursor-pointer' 
                    : 'opacity-60'
                }`}
                style={{
                  background: hasLevelAccess 
                    ? (theme === 'light' ? 'rgba(255, 255, 255, 0.25)' : 'rgba(26, 26, 26, 0.25)')
                    : (theme === 'light' ? 'rgba(255, 255, 255, 0.15)' : 'rgba(26, 26, 26, 0.15)'),
                  border: hasLevelAccess
                    ? (theme === 'light' ? '1px solid rgba(255, 255, 255, 0.3)' : '1px solid rgba(64, 64, 64, 0.3)')
                    : (theme === 'light' ? '1px solid rgba(255, 255, 255, 0.2)' : '1px solid rgba(64, 64, 64, 0.2)'),
                  backdropFilter: 'blur(16px)',
                  WebkitBackdropFilter: 'blur(16px)',
                  borderRadius: '20px',
                  boxShadow: theme === 'light' ? '0 8px 32px rgba(31, 38, 135, 0.37)' : '0 8px 32px rgba(0, 0, 0, 0.37)'
                }}
              >
                <div className="space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="p-4 rounded-xl shadow-md" style={{
                      background: hasLevelAccess 
                        ? (theme === 'light' ? 'rgba(255, 255, 255, 0.6)' : 'rgba(59, 130, 246, 0.15)')
                        : (theme === 'light' ? 'rgba(255, 255, 255, 0.3)' : 'rgba(64, 64, 64, 0.3)')
                    }}>
                      <Icon className={`w-7 h-7 ${
                        hasLevelAccess 
                          ? levelInfo.color 
                          : 'text-muted-foreground'
                      }`} />
                    </div>
                    <div className="flex items-center gap-1">
                      {hasLevelAccess ? (
                        <div className="flex items-center gap-1" style={{
                          color: theme === 'light' ? '#059669' : '#10b981'
                        }}>
                          <Unlock className="w-4 h-4" />
                          <span className="text-xs font-medium">Liberado</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1" style={{
                          color: theme === 'light' ? '#dc2626' : '#ef4444'
                        }}>
                          <Lock className="w-4 h-4" />
                          <span className="text-xs font-medium">Bloqueado</span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div>
                    <h4 className="font-bold mb-2 text-lg" style={{
                      color: theme === 'light' ? '#1e293b' : '#f1f5f9'
                    }}>{levelInfo.title}</h4>
                    <p className="text-sm leading-relaxed" style={{
                      color: theme === 'light' ? '#475569' : '#94a3b8'
                    }}>
                      {levelInfo.description}
                    </p>
                  </div>

                  {data && (
                    <div className="rounded-lg p-4" style={{
                      background: theme === 'light' 
                        ? 'rgba(255, 255, 255, 0.6)' 
                        : 'rgba(26, 26, 26, 0.5)',
                      border: theme === 'light' 
                        ? '1px solid rgba(34, 197, 94, 0.3)' 
                        : '1px solid rgba(34, 197, 94, 0.3)',
                      backdropFilter: 'blur(10px)',
                      WebkitBackdropFilter: 'blur(10px)'
                    }}>
                      <div className="flex items-center gap-2 mb-2">
                        <div className="w-2 h-2 rounded-full animate-pulse" style={{
                          background: theme === 'light' ? '#22c55e' : '#4ade80'
                        }}></div>
                        <span className="text-sm font-medium" style={{
                          color: theme === 'light' ? '#15803d' : '#86efac'
                        }}>Dados carregados</span>
                      </div>
                      <pre className="text-xs overflow-auto rounded p-2 border" style={{
                        background: theme === 'light' ? 'rgba(255, 255, 255, 0.5)' : 'rgba(0, 0, 0, 0.2)',
                        color: theme === 'light' ? '#374151' : '#d1d5db',
                        borderColor: theme === 'light' ? 'rgba(0, 0, 0, 0.1)' : 'rgba(255, 255, 255, 0.1)'
                      }}>
                        {JSON.stringify(data, null, 2)}
                      </pre>
                    </div>
                  )}

                  <Button
                    onClick={() => handleAccessLevel(levelInfo.level)}
                    disabled={!hasLevelAccess || isLoading}
                    className="w-full font-medium shadow-md hover:opacity-90 cursor-pointer"
                    size="lg"
                    style={{
                      background: hasLevelAccess 
                        ? (theme === 'light' 
                          ? 'linear-gradient(135deg, #16a34a, #15803d)'
                          : 'linear-gradient(135deg, #3b82f6, #1d4ed8)')
                        : (theme === 'light' ? '#f1f5f9' : '#374151'),
                      color: hasLevelAccess ? '#ffffff' : (theme === 'light' ? '#64748b' : '#9ca3af'),
                      border: hasLevelAccess 
                        ? (theme === 'light' ? '1px solid #15803d' : '1px solid #1d4ed8')
                        : (theme === 'light' ? '1px solid #e2e8f0' : '1px solid #4b5563'),
                      cursor: hasLevelAccess ? 'pointer' : 'not-allowed'
                    }}
                  >
                    {isLoading ? (
                      <>
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                        Carregando...
                      </>
                    ) : hasLevelAccess ? (
                      'Acessar Dados'
                    ) : (
                      'Acesso Bloqueado'
                    )}
                  </Button>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Info Footer */}
        <div className="grid md:grid-cols-2 gap-4 mt-8">
          <Card className="p-4 shadow-md" style={{
            background: theme === 'light' ? 'rgba(255, 255, 255, 0.6)' : 'rgba(26, 26, 26, 0.5)',
            border: theme === 'light' ? '1px solid rgba(59, 130, 246, 0.3)' : '1px solid rgba(59, 130, 246, 0.3)',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            borderRadius: '10px'
          }}>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full flex items-center justify-center" style={{
                background: theme === 'light' ? '#dbeafe' : 'rgba(29, 78, 216, 0.3)'
              }}>
                <ShieldCheck className="w-4 h-4" style={{
                  color: theme === 'light' ? '#2563eb' : '#93c5fd'
                }} />
              </div>
              <div>
                <h4 className="font-medium" style={{
                  color: theme === 'light' ? '#1e40af' : '#93c5fd'
                }}>Sistema de Segurança</h4>
                <p className="text-xs" style={{
                  color: theme === 'light' ? '#1d4ed8' : '#bfdbfe'
                }}>
                  Acesso baseado em clearance e logs de auditoria completos
                </p>
              </div>
            </div>
          </Card>

          <Card className="p-4 shadow-md" style={{
            background: theme === 'light' ? 'rgba(255, 255, 255, 0.6)' : 'rgba(26, 26, 26, 0.5)',
            border: theme === 'light' ? '1px solid rgba(34, 197, 94, 0.3)' : '1px solid rgba(34, 197, 94, 0.3)',
            backdropFilter: 'blur(10px)',
            WebkitBackdropFilter: 'blur(10px)',
            borderRadius: '10px'
          }}>
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full flex items-center justify-center" style={{
                background: theme === 'light' ? '#dcfce7' : 'rgba(21, 128, 61, 0.3)'
              }}>
                <User className="w-4 h-4" style={{
                  color: theme === 'light' ? '#16a34a' : '#86efac'
                }} />
              </div>
              <div>
                <h4 className="font-medium" style={{
                  color: theme === 'light' ? '#166534' : '#86efac'
                }}>Biometria Facial</h4>
                <p className="text-xs" style={{
                  color: theme === 'light' ? '#15803d' : '#bbf7d0'
                }}>
                  Upload de imagem PNG/JPEG para reconhecimento facial
                </p>
              </div>
            </div>
          </Card>
        </div>
      </main>
    </div>
  );
}
