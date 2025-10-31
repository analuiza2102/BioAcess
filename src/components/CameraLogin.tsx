// Componente para captura de imagem via câmera para login biométrico

import { useState, useRef, useCallback, useEffect } from 'react';
import { Camera, RefreshCw, Check, X, AlertTriangle } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { toast } from 'sonner';

interface CameraLoginProps {
  onCapture: (imageData: string) => void;
  onCancel: () => void;
  loading?: boolean;
}

export function CameraLogin({ onCapture, onCancel, loading = false }: CameraLoginProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState<string>('');

  // Inicializar câmera
  const startCamera = useCallback(async () => {
    try {
      setError('');
      setIsReady(false);
      
      // Verificar se getUserMedia está disponível
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        throw new Error('Câmera não suportada neste navegador');
      }

      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 640, min: 320 },
          height: { ideal: 480, min: 240 },
          facingMode: 'user'
        },
        audio: false
      });

      if (videoRef.current) {
        const video = videoRef.current;
        video.srcObject = mediaStream;
        setStream(mediaStream);
        
        // Configurar eventos
        video.onloadedmetadata = () => {
          console.log('📊 Camera metadata loaded:', {
            videoWidth: video.videoWidth,
            videoHeight: video.videoHeight,
            readyState: video.readyState,
            srcObject: !!video.srcObject
          });
          
          // Tentar reproduzir o vídeo
          const playPromise = video.play();
          
          if (playPromise !== undefined) {
            playPromise.then(() => {
              console.log('✅ Camera started successfully');
              setIsReady(true);
            }).catch(playError => {
              console.error('❌ Error playing video:', playError);
              // Tentar novamente sem som
              video.muted = true;
              video.play().then(() => {
                console.log('✅ Camera started successfully (muted)');
                setIsReady(true);
              }).catch(() => {
                setError('Erro ao iniciar visualização da câmera');
              });
            });
          } else {
            // Para navegadores mais antigos
            console.log('✅ Camera started (legacy mode)');
            setIsReady(true);
          }
        };
        
        video.onerror = (e) => {
          console.error('❌ Video element error:', e);
          setError('Erro no elemento de vídeo');
        };
        
        // Fallback timeout
        setTimeout(() => {
          if (mediaStream && mediaStream.active && !isReady) {
            console.log('⏱️ Timeout fallback: forcing camera activation');
            setIsReady(true);
            video.play().catch(console.error);
          }
        }, 3000);
      }
    } catch (err: any) {
      console.error('Erro ao acessar câmera:', err);
      
      if (err.name === 'NotAllowedError') {
        setError('Permissão de câmera negada. Por favor, permita o acesso à câmera.');
      } else if (err.name === 'NotFoundError') {
        setError('Nenhuma câmera encontrada no dispositivo.');
      } else if (err.name === 'NotReadableError') {
        setError('Câmera está sendo usada por outro aplicativo.');
      } else {
        setError(`Erro ao acessar câmera: ${err.message || 'Erro desconhecido'}`);
      }
      toast.error('Erro ao acessar câmera. Verifique as permissões.');
    }
  }, [isReady]);

  // Parar câmera
  const stopCamera = useCallback(() => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setIsReady(false);
    }
  }, [stream]);

  // Capturar foto
  const capturePhoto = useCallback(() => {
    if (!videoRef.current || !canvasRef.current || !isReady) {
      toast.error('Câmera não está pronta');
      return;
    }

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (!context) {
      toast.error('Erro no canvas');
      return;
    }

    // Configurar dimensões
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Desenhar frame atual
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Converter para base64
    const imageData = canvas.toDataURL('image/jpeg', 0.8);
    const base64Data = imageData.split(',')[1];

    onCapture(base64Data);
  }, [isReady, onCapture]);

  // Inicializar e limpar câmera
  useEffect(() => {
    console.log('🎥 CameraLogin component mounted, starting camera...');
    startCamera();
    
    return () => {
      console.log('🧹 Cleaning up camera stream...');
      if (stream) {
        stream.getTracks().forEach(track => {
          track.stop();
          console.log('🛑 Stopped track:', track.kind);
        });
      }
    };
  }, []); // Array vazio para executar apenas uma vez

  return (
    <div className="w-full max-w-2xl mx-auto p-2 md:p-4">
      <Card className="p-4 md:p-6 bg-gradient-to-br from-blue-50/80 to-indigo-50/80 dark:from-blue-900/30 dark:to-indigo-900/30 border border-blue-200/50 dark:border-blue-700/50 backdrop-blur-sm">
        <div className="text-center mb-4 md:mb-6">
          <div className="inline-flex items-center justify-center w-12 h-12 md:w-16 md:h-16 bg-blue-600 rounded-full mb-3 md:mb-4">
            <Camera className="w-6 h-6 md:w-8 md:h-8 text-white" />
          </div>
          <h3 className="text-lg md:text-xl font-semibold text-gray-800 dark:text-white mb-2">
            📷 Login por Reconhecimento Facial
          </h3>
          <p className="text-gray-600 dark:text-gray-300 text-sm md:text-base leading-relaxed px-2">
            Posicione seu rosto no centro da câmera e clique em "Capturar"
          </p>
        </div>

      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-red-700 dark:text-red-300">
              <AlertTriangle className="w-4 h-4" />
              <span className="text-sm">{error}</span>
            </div>
            <Button
              onClick={() => {
                setError('');
                startCamera();
              }}
              size="sm"
              variant="outline"
              className="ml-2 border-red-300 text-red-700 hover:bg-red-50 dark:border-red-600 dark:text-red-400"
            >
              <RefreshCw className="w-3 h-3 mr-1" />
              Tentar Novamente
            </Button>
          </div>
        </div>
      )}

        <div className="relative mb-4 md:mb-6 mx-auto w-full max-w-md">
          <div className="relative overflow-hidden rounded-lg md:rounded-xl bg-gray-900 shadow-xl md:shadow-2xl border border-blue-300/50 md:border-2 md:border-blue-300/30">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              controls={false}
              className="w-full h-auto block"
              style={{ 
                aspectRatio: '4/3',
                minHeight: '250px',
                maxHeight: '400px',
                objectFit: 'cover'
              }}
            />
            <canvas
              ref={canvasRef}
              className="hidden"
            />
            
            {!isReady && !error && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-900/70 backdrop-blur-sm">
                <div className="text-white text-center">
                  <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-2" />
                  <p className="text-sm">Inicializando câmera...</p>
                </div>
              </div>
            )}

            {isReady && (
              <div className="absolute inset-0 pointer-events-none">
                {/* Bordas de enquadramento */}
                <div className="absolute inset-2">
                  <div className="w-full h-full border-2 border-green-400/80 rounded-lg"></div>
                  {/* Cantos de enquadramento */}
                  <div className="absolute top-0 left-0 w-6 h-6 border-t-4 border-l-4 border-green-400"></div>
                  <div className="absolute top-0 right-0 w-6 h-6 border-t-4 border-r-4 border-green-400"></div>
                  <div className="absolute bottom-0 left-0 w-6 h-6 border-b-4 border-l-4 border-green-400"></div>
                  <div className="absolute bottom-0 right-0 w-6 h-6 border-b-4 border-r-4 border-green-400"></div>
                </div>
                
                {/* Indicador de status */}
                <div className="absolute top-3 right-3 bg-green-500 text-white px-2 py-1 rounded-md text-xs font-medium shadow-lg flex items-center gap-1">
                  <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                  PRONTO
                </div>
                
                {/* Linha de referência central */}
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="w-px h-8 bg-green-400/60"></div>
                </div>
                <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                  <div className="w-8 h-px bg-green-400/60"></div>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-col gap-2 md:gap-3">
          <Button
            onClick={capturePhoto}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 md:py-3 text-sm md:text-base font-medium"
            disabled={!isReady || loading}
          >
            {loading ? (
              <>
                <RefreshCw className="w-4 h-4 md:w-5 md:h-5 mr-2 animate-spin" />
                Verificando...
              </>
            ) : (
              <>
                <Check className="w-4 h-4 md:w-5 md:h-5 mr-2" />
                Capturar e Verificar
              </>
            )}
          </Button>
          
          <div className="flex gap-2 md:gap-3">
            <Button
              onClick={onCancel}
              variant="outline"
              className="flex-1 border-gray-300 text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:text-gray-300 py-2 text-sm md:text-base"
              disabled={loading}
            >
              <X className="w-3 h-3 md:w-4 md:h-4 mr-1 md:mr-2" />
              Cancelar
            </Button>
            
            <Button
              onClick={() => {
                stopCamera();
                startCamera();
              }}
              variant="outline"
              className="flex-1 border-blue-300 text-blue-700 hover:bg-blue-50 dark:border-blue-600 dark:text-blue-300 py-2 text-sm md:text-base"
              disabled={loading}
            >
              <RefreshCw className="w-3 h-3 md:w-4 md:h-4 mr-1 md:mr-2" />
              Reiniciar
            </Button>
          </div>
        </div>

        <div className="mt-4 text-center">
          <p className="text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
            🔒 Sua imagem será comparada com a biometria cadastrada de forma segura
          </p>
        </div>
      </Card>
    </div>
  );
}