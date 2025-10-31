// Página de cadastro de biometria facial

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserPlus, ArrowLeft, CheckCircle } from 'lucide-react';
import { useAuthContext } from '../contexts/AuthContext';
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
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="mb-6">
          <Button
            variant="ghost"
            onClick={() => navigate(isAuthenticated ? '/dashboard' : '/login')}
            className="mb-4"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            {isAuthenticated ? 'Voltar ao Dashboard' : 'Voltar para Login'}
          </Button>
          
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-green-600 rounded-full mb-4">
              <UserPlus className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-3xl mb-2">Cadastro de Biometria</h1>
            <p className="text-muted-foreground">
              {isAuthenticated 
                ? `Registrando biometria para: ${user?.username}` 
                : 'Registre sua biometria facial para acessar o sistema'
              }
            </p>
          </div>
        </div>

        <Card className="p-8">
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
                <div className="text-center p-4 bg-green-50 rounded-lg border border-green-200">
                  <h3 className="font-semibold text-green-800 mb-2">
                    📸 Cadastro de Biometria
                  </h3>
                  <p className="text-sm text-green-700">
                    Selecione uma imagem sua (PNG/JPEG) para cadastrar sua biometria facial.
                  </p>
                  <p className="text-xs text-green-600 mt-1">
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
                  className="flex-1"
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

              <div className="bg-amber-50 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
                <p className="text-sm text-amber-900 dark:text-amber-100">
                  <strong>Dica:</strong> Certifique-se de estar em um ambiente bem iluminado e olhe diretamente para a câmera.
                </p>
              </div>
            </div>
          ) : (
            <div className="text-center space-y-6">
              <div className="inline-flex items-center justify-center w-20 h-20 bg-green-100 dark:bg-green-900/30 rounded-full">
                <CheckCircle className="w-10 h-10 text-green-600 dark:text-green-400" />
              </div>
              
              <div>
                <h3 className="mb-2">Biometria Cadastrada!</h3>
                <p className="text-muted-foreground">
                  Sua biometria facial foi registrada com sucesso.
                </p>
              </div>

              <div className="flex gap-2">
                <Button
                  onClick={() => navigate(isAuthenticated ? '/dashboard' : '/login')}
                  className="flex-1"
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
