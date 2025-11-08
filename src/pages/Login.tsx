import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, User, Lock, Upload, Camera, Eye, EyeOff, Sun, Moon } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import './Login.css';
import { useAuthContext } from '../contexts/AuthContext';
import { api, APIError } from '../lib/api';
import { CameraLogin } from '../components/CameraLogin';
import { ImageUpload } from '../components/ImageUpload';

import { toast } from 'sonner';
import { mockAPI, USE_MOCK_API } from '../lib/mockAPI';

export function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loginMode, setLoginMode] = useState<'traditional' | 'upload' | 'camera'>('traditional');
  const [showImageUpload, setShowImageUpload] = useState(false);
  const [showCameraLogin, setShowCameraLogin] = useState(false);
  const [selectedImage, setSelectedImage] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const { login } = useAuthContext();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleTraditionalLogin = async () => {
    if (!username.trim() || !password.trim()) {
      toast.error('Por favor, preencha usuário e senha');
      return;
    }

    setLoading(true);
    try {
      if (USE_MOCK_API) {
        const data = await mockAPI.login(username, password);
        login(data.token, {
          username: data.username!,
          role: data.role as 'public' | 'director' | 'minister',
          clearance: data.clearance as 1 | 2 | 3
        });
      } else {
        const data = await api.login(username, password);
        const token = data.access_token || data.token || '';
        login(token, {
          username: data.username || username,
          role: data.role as 'public' | 'director' | 'minister',
          clearance: data.clearance as 1 | 2 | 3
        });
      }

      toast.success('Login realizado com sucesso!');
      setTimeout(() => navigate('/dashboard'), 100);
    } catch (error: any) {
      toast.error(error.message || 'Erro ao fazer login');
    } finally {
      setLoading(false);
    }
  };

  const handleStartImageUpload = async () => {
    if (!username.trim()) {
      toast.error('Por favor, informe seu nome de usuário');
      return;
    }
    setShowImageUpload(true);
  };

  const handleStartCameraLogin = async () => {
    if (!username.trim()) {
      toast.error('Por favor, informe seu nome de usuário');
      return;
    }
    setShowCameraLogin(true);
  };

  const handleImageSelect = (file: File) => {
    setSelectedImage(file);
  };

  const handleBiometricVerification = async () => {
    if (!selectedImage || !username.trim()) {
      toast.error('Por favor, selecione uma imagem e informe o nome de usuário');
      return;
    }

    setLoading(true);
    try {
      const response = USE_MOCK_API 
        ? await mockAPI.login(username, 'password')
        : await api.verifyImageUpload(username, selectedImage);

      const token = ('access_token' in response ? response.access_token : response.token) || '';
      login(token, {
        username: response.username || username,
        role: response.role as 'public' | 'director' | 'minister',
        clearance: response.clearance as 1 | 2 | 3
      });

      toast.success('Autenticação bem-sucedida!');
      setTimeout(() => navigate('/dashboard'), 100);
    } catch (error: any) {
      toast.error('Falha na verificação biométrica');
    } finally {
      setLoading(false);
      setSelectedImage(null);
    }
  };

  const handleCameraCapture = async (imageData: string) => {
    console.log('📷 handleCameraCapture chamado com imagem de tamanho:', imageData.length);
    setLoading(true);
    try {
      let response;
      if (USE_MOCK_API) {
        response = await mockAPI.login(username, 'password');
      } else {
        // Converter base64 para File
        const byteCharacters = atob(imageData);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const cameraFile = new File([byteArray], 'camera_capture.jpg', { type: 'image/jpeg' });
        
        response = await api.loginByCamera(username, cameraFile);
      }

      console.log('✅ Resposta da API recebida:', {
        token: ('access_token' in response ? response.access_token : response.token) || 'null',
        role: response.role,
        clearance: response.clearance,
        username: response.username
      });

      const token = ('access_token' in response ? response.access_token : response.token) || '';
      login(token, {
        username: response.username || username,
        role: response.role as 'public' | 'director' | 'minister',
        clearance: response.clearance as 1 | 2 | 3
      });

      toast.success('Login por reconhecimento facial realizado com sucesso!');
      console.log('🔄 Navegando para dashboard em 100ms...');
      setTimeout(() => {
        console.log('🎯 Executando navigate("/dashboard")');
        navigate('/dashboard');
      }, 100);
    } catch (error: any) {
      toast.error('Falha no reconhecimento facial. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };
  return (
    <div className="login-page">
      <div className="bioaccess-container">
        <div className="bioaccess-card" style={{ position: 'relative' }}>
          {/* Botão de alternância de tema */}
          <button
            onClick={toggleTheme}
            className="theme-toggle-button"
          >
            {theme === 'light' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
          </button>
        <div className="text-center mb-8">
          <div className="bioaccess-logo">
            <ShieldCheck className="w-10 h-10 text-white" />
          </div>
          <h1 className="bioaccess-title">BioAccess</h1>
          <p className="bioaccess-subtitle">
            Sistema de Autenticação Biométrica Facial
          </p>
        </div>
          {showCameraLogin ? (
            <div className="space-y-4 md:space-y-6 w-full">
              <div className="text-center px-4">
                <h2 className="text-lg md:text-xl font-semibold mb-2 text-gray-800 dark:text-white">Login por Reconhecimento Facial</h2>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Usuário: <span className="font-medium text-gray-800 dark:text-white">{username}</span>
                </p>
              </div>
              <CameraLogin
                onCapture={handleCameraCapture}
                onCancel={() => setShowCameraLogin(false)}
                loading={loading}
              />
            </div>
          ) : showImageUpload ? (
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold text-white">Verificação Biométrica por Upload</h2>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    Usuário: <span className="font-medium text-gray-800 dark:text-white">{username}</span>
                  </p>
                </div>
                <button
                  onClick={() => setShowImageUpload(false)}
                  disabled={loading}
                  className="px-4 py-2 text-sm bg-transparent border border-gray-600 text-gray-300 rounded-lg hover:bg-gray-700"
                >
                  Voltar
                </button>
              </div>
              <div className="space-y-4">
                <ImageUpload
                  onImageSelect={handleImageSelect}
                  disabled={loading}
                  label="Selecionar Imagem para Verificação"
                  showPreview={true}
                />
                {selectedImage && (
                  <button
                    onClick={handleBiometricVerification}
                    className="bioaccess-button"
                    disabled={loading}
                  >
                    {loading ? 'Verificando...' : 'Verificar Biometria'}
                  </button>
                )}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {/* Tabs de navegação */}
              <div className="bioaccess-tabs">
                <button
                  onClick={() => setLoginMode('traditional')}
                  className={`bioaccess-tab ${loginMode === 'traditional' ? 'active' : ''}`}
                >
                  <Lock style={{width: '20px', height: '20px'}} />
                  <span>Tradicional</span>
                </button>
                <button
                  onClick={() => setLoginMode('upload')}
                  className={`bioaccess-tab ${loginMode === 'upload' ? 'active' : ''}`}
                >
                  <Upload style={{width: '20px', height: '20px'}} />
                  <span>Upload</span>
                </button>
                <button
                  onClick={() => setLoginMode('camera')}
                  className={`bioaccess-tab ${loginMode === 'camera' ? 'active' : ''}`}
                >
                  <Camera style={{width: '20px', height: '20px'}} />
                  <span>Câmera</span>
                </button>
              </div>

              {/* Ícone central baseado no modo */}
              <div className="text-center" style={{padding: '24px 0'}}>
                <div className="bioaccess-center-icon">
                  <Lock style={{width: '24px', height: '24px'}} />
                </div>
                <h3 className="text-xl font-semibold mb-2">Login com Usuário e Senha</h3>
                <p className="text-sm">Digite suas credenciais para acessar o sistema</p>
              </div>

              <div className="space-y-4">
                <div className="space-y-2">
                  <label htmlFor="username" className="bioaccess-label">Nome de Usuário</label>
                  <div className="bioaccess-input-wrapper">
                    <User style={{width: '16px', height: '16px'}} className="bioaccess-input-icon" />
                    <input
                      id="username"
                      type="text"
                      placeholder="Digite seu nome de usuário"
                      value={username}
                      onChange={(e) => setUsername(e.target.value)}
                      className="bioaccess-input"
                    />
                  </div>
                </div>

                {loginMode === 'traditional' && (
                  <div className="space-y-2">
                    <label htmlFor="password" className="bioaccess-label">Senha</label>
                    <div className="bioaccess-input-wrapper">
                      <Lock style={{width: '16px', height: '16px'}} className="bioaccess-input-icon" />
                      <input
                        id="password"
                        type={showPassword ? 'text' : 'password'}
                        placeholder="Digite sua senha"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleTraditionalLogin()}
                        className="bioaccess-input"
                        style={{paddingRight: '2.5rem'}}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="bioaccess-input-icon-right"
                      >
                        {showPassword ? <EyeOff style={{width: '16px', height: '16px'}} /> : <Eye style={{width: '16px', height: '16px'}} />}
                      </button>
                    </div>
                  </div>
                )}
              </div>

              {loginMode === 'traditional' ? (
                <button
                  onClick={handleTraditionalLogin}
                  className="bioaccess-button"
                  disabled={loading}
                >
                  {loading ? 'Entrando...' : 'Entrar'}
                </button>
              ) : loginMode === 'upload' ? (
                <button
                  onClick={handleStartImageUpload}
                  className="bioaccess-button"
                  disabled={loading}
                >
                  📁 Fazer Upload de Imagem
                </button>
              ) : (
                <button
                  onClick={handleStartCameraLogin}
                  className="bioaccess-button"
                  disabled={loading}
                >
                  📷 Iniciar Câmera
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

