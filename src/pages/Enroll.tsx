// Página de cadastro de biometria facial

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserPlus, ArrowLeft, CheckCircle } from 'lucide-react';
import { useAuthContext } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { api, APIError } from '../lib/api';
import { ImageUpload } from '../components/ImageUpload';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { toast } from 'sonner';
import { mockAPI, USE_MOCK_API } from '../lib/mockAPI';

export function Enroll() {
  const { user, isAuthenticated } = useAuthContext();
  const { theme } = useTheme();
  const [username, setUsername] = useState('');
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [enrolled, setEnrolled] = useState(false);
  const [allowManualUsername, setAllowManualUsername] = useState(false);
  const navigate = useNavigate();

  // Se usuário está logado, usar seu username automaticamente
  useEffect(() => {
    if (isAuthenticated && user) {
      setUsername(user.username);
      setAllowManualUsername(false);
    } else {
      setAllowManualUsername(true);
    }
  }, [isAuthenticated, user]);

  const handleImageSelect = (file: File) => {
    setSelectedImage(file);
  };

  const handleSubmit = async () => {
    if (!username.trim()) {
      toast.error('Por favor, informe o nome de usuário');
      return;
    }

    if (!selectedImage) {
      toast.error('Por favor, selecione uma imagem');
      return;
    }

    setLoading(true);

    try {
      let response;
      
      if (USE_MOCK_API) {
        console.log('🔧 Usando API simulada para cadastro de biometria');
        // Converter arquivo para base64 para mock
        const reader = new FileReader();
        reader.onload = async (e) => {
          const base64 = e.target?.result as string;
          const imageData = base64.split(',')[1]; // Remove data:image prefix
          
          response = await mockAPI.enroll(username, imageData);
          toast.success(response.message || 'Biometria cadastrada com sucesso!');
          setEnrolled(true);
          setLoading(false);
        };
        reader.readAsDataURL(selectedImage);
        return;
      } else {
        // Usar API real com upload de arquivo
        response = await api.enrollImageUpload(username, selectedImage);
      }
      
      toast.success(response.message || 'Biometria cadastrada com sucesso via upload!');
      setEnrolled(true);
    } catch (error) {
      console.error('Erro no cadastro:', error);
      
      if (USE_MOCK_API) {
        toast.error(error instanceof Error ? error.message : 'Erro no cadastro de biometria');
      } else if (error instanceof APIError) {
        if (error.status === 409) {
          toast.error('Este usuário já possui biometria cadastrada.');
        } else if (error.status === 404) {
          toast.error('Usuário não encontrado no sistema.');
        } else if (error.status === 400) {
          toast.error('Não foi possível detectar um rosto na imagem ou formato inválido.');
        } else {
          toast.error(error.message);
        }
      } else {
        toast.error('Erro ao conectar com o servidor. Verifique se o backend está rodando.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setUsername('');
    setSelectedImage(null);
    setEnrolled(false);
  };

  const handleGoToLogin = () => {
    navigate('/login');
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4" style={{
      background: theme === 'light' 
        ? 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%)'
        : 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #262626 100%)'
    }}>
      <div className="w-full max-w-2xl">
        <div className="mb-6">
          <Button
            variant="ghost"
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/login')}
            className="mb-4"
            style={{
              color: theme === 'light' ? '#15803d' : '#86efac'
            }}
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            {isAuthenticated ? 'Voltar ao Dashboard' : 'Voltar para Login'}
          </Button>
          
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 rounded-full mb-4" style={{
              background: theme === 'light' 
                ? 'linear-gradient(135deg, #16a34a, #15803d)'
                : 'linear-gradient(135deg, #3b82f6, #1d4ed8)'
            }}>
              <UserPlus className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl mb-2 font-bold" style={{
              color: theme === 'light' ? '#0f172a' : '#f1f5f9'
            }}>
              Cadastro de Biometria
            </h1>
            <p style={{
              color: theme === 'light' ? '#64748b' : '#94a3b8'
            }}>
              {isAuthenticated 
                ? `Registrando biometria para: ${user?.username}` 
                : 'Registre sua biometria facial para acessar o sistema'
              }
            </p>
          </div>
        </div>

        <Card className="p-8" style={{
          background: theme === 'light' 
            ? 'rgba(255, 255, 255, 0.9)'
            : 'rgba(38, 38, 38, 0.9)',
          backdropFilter: 'blur(20px)',
          WebkitBackdropFilter: 'blur(20px)',
          borderColor: theme === 'light' ? '#e2e8f0' : '#404040'
        }}>
          {!enrolled ? (
            <div className="space-y-6">
              {allowManualUsername ? (
                <div className="space-y-2">
                  <Label htmlFor="username">Nome de Usuário</Label>
                  <Input
                    id="username"
                    type="text"
                    placeholder="Digite seu nome de usuário"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    disabled={loading}
                    autoFocus
                  />
                  <p className="text-xs text-muted-foreground">
                    Use um dos usuários do sistema: ana.luiza, diretor.silva ou ministro.ambiente
                  </p>
                </div>
              ) : (
                <div className="space-y-2">
                  <Label>Usuário Logado</Label>
                  <div className="bg-muted p-3 rounded-lg">
                    <p className="font-medium">{username}</p>
                    <p className="text-xs text-muted-foreground">
                      Cadastrando biometria para o usuário atual
                    </p>
                  </div>
                </div>
              )}

              <div className="space-y-4">
                <div className="text-center p-4 rounded-lg border" style={{
                  background: theme === 'light' ? '#f0fdf4' : '#064e3b',
                  borderColor: theme === 'light' ? '#86efac' : '#047857'
                }}>
                  <h3 className="font-semibold mb-2" style={{
                    color: theme === 'light' ? '#15803d' : '#86efac'
                  }}>
                    📸 Cadastro de Biometria
                  </h3>
                  <p className="text-sm" style={{
                    color: theme === 'light' ? '#166534' : '#6ee7b7'
                  }}>
                    Selecione uma imagem sua (PNG/JPEG) para cadastrar sua biometria facial.
                  </p>
                  <p className="text-xs mt-1" style={{
                    color: theme === 'light' ? '#15803d' : '#86efac'
                  }}>
                    💡 Use imagens com fundo branco para melhor precisão
                  </p>
                </div>

                <ImageUpload
                  onImageSelect={handleImageSelect}
                  disabled={loading}
                  label="Selecionar Imagem Biométrica"
                  showPreview={true}
                />
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={handleSubmit}
                  disabled={!username || !selectedImage || loading}
                  className="flex-1 text-white shadow-md"
                  style={{
                    background: theme === 'light' 
                      ? 'linear-gradient(135deg, #16a34a, #15803d)'
                      : 'linear-gradient(135deg, #3b82f6, #1d4ed8)',
                    opacity: (!username || !selectedImage || loading) ? 0.5 : 1
                  }}
                >
                  {loading ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                      Processando...
                    </>
                  ) : (
                    <>
                      <UserPlus className="w-4 h-4 mr-2" />
                      Cadastrar Biometria
                    </>
                  )}
                </Button>
                
                {selectedImage && (
                  <Button
                    onClick={handleReset}
                    variant="outline"
                    disabled={loading}
                  >
                    Selecionar Nova Imagem
                  </Button>
                )}
              </div>

              <div className="border rounded-lg p-4" style={{
                background: theme === 'light' ? '#fef3c7' : '#422006',
                borderColor: theme === 'light' ? '#fbbf24' : '#78350f'
              }}>
                <p className="text-sm" style={{
                  color: theme === 'light' ? '#92400e' : '#fbbf24'
                }}>
                  <strong>Dica:</strong> Certifique-se de estar em um ambiente bem iluminado e olhe diretamente para a câmera.
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center space-y-6">
              <div className="inline-flex items-center justify-center w-20 h-20 rounded-full" style={{
                background: theme === 'light' ? '#dcfce7' : '#064e3b'
              }}>
                <CheckCircle className="w-10 h-10" style={{
                  color: theme === 'light' ? '#16a34a' : '#86efac'
                }} />
              </div>
              
              <div>
                <h3 className="mb-2 text-xl font-bold" style={{
                  color: theme === 'light' ? '#15803d' : '#86efac'
                }}>
                  Biometria Cadastrada!
                </h3>
                <p style={{
                  color: theme === 'light' ? '#64748b' : '#94a3b8'
                }}>
                  Sua biometria facial foi registrada com sucesso.
                </p>
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={() => navigate(isAuthenticated ? '/dashboard' : '/login')}
                  className="flex-1 text-white shadow-md"
                  style={{
                    background: theme === 'light' 
                      ? 'linear-gradient(135deg, #16a34a, #15803d)'
                      : 'linear-gradient(135deg, #3b82f6, #1d4ed8)'
                  }}
                >
                  {isAuthenticated ? 'Voltar ao Dashboard' : 'Fazer Login'}
                </Button>
                {!isAuthenticated && (
                  <Button
                    onClick={handleReset}
                    variant="outline"
                  >
                    Cadastrar Outro
                  </Button>
                )}
              </div>
            </div>
          )}
        </Card>
      </div>
    </div>
  );
}
