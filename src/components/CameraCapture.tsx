// Componente para captura de foto via webcam

import { useRef, useState, useEffect } from 'react';
import { Camera, RotateCw } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface CameraCaptureProps {
  onCapture: (imageBase64: string) => void;
  disabled?: boolean;
  label?: string;
}

export function CameraCapture({ onCapture, disabled, label = 'Capturar Foto' }: CameraCaptureProps) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    return () => {
      // Limpa stream ao desmontar
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, [stream]);

  const startCamera = async () => {
    try {
      setError('');
      
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
        console.log('📺 Configurando vídeo - elemento:', video);
        console.log('📺 Dimensões do vídeo antes:', video.videoWidth, 'x', video.videoHeight);
        
        video.srcObject = mediaStream;
        console.log('🔗 Stream atribuído ao vídeo');
        
        // Configurar eventos
        video.onloadedmetadata = () => {
          console.log('📊 Metadata carregada - dimensões:', video.videoWidth, 'x', video.videoHeight);
          console.log('📊 Estado do vídeo:', {
            paused: video.paused,
            muted: video.muted,
            readyState: video.readyState,
            srcObject: !!video.srcObject
          });
          
          video.play().then(() => {
            console.log('✅ Vídeo reproduzindo com sucesso');
            setStream(mediaStream);
            setIsCameraActive(true);
          }).catch(playError => {
            console.error('❌ Erro ao reproduzir vídeo:', playError);
            setError('Erro ao iniciar visualização da câmera');
          });
        };
        
        video.onerror = (e) => {
          console.error('❌ Erro no elemento de vídeo:', e);
        };
        
        // Tentar reproduzir imediatamente também
        video.play().catch(e => {
          console.log('⚠️ Play imediato falhou (normal), aguardando metadata:', e.message);
        });
        
        // Fallback: marcar como ativo após timeout
        setTimeout(() => {
          if (mediaStream && mediaStream.active && !isCameraActive) {
            console.log('⏱️ Timeout: Forçando ativação da câmera');
            console.log('📊 Estado final do vídeo:', {
              paused: video.paused,
              videoWidth: video.videoWidth,
              videoHeight: video.videoHeight,
              readyState: video.readyState
            });
            setStream(mediaStream);
            setIsCameraActive(true);
            video.play().catch(console.error);
          }
        }, 3000);
      } else {
        console.error('❌ videoRef.current é null!');
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
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setIsCameraActive(false);
    }
  };

  const capture = () => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    if (!context) return;

    // Define dimensões do canvas
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Desenha frame atual do vídeo
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Converte para base64
    const imageBase64 = canvas.toDataURL('image/jpeg', 0.8);
    
    // Remove prefixo data:image/jpeg;base64,
    const base64Data = imageBase64.split(',')[1];
    
    onCapture(base64Data);
    stopCamera();
  };

  return (
    <Card className="p-6">
      <div className="space-y-4">
        <div className="relative bg-black rounded-lg overflow-hidden min-h-[300px]" style={{ aspectRatio: '4/3' }}>
          {/* Vídeo sempre presente, mas visível apenas quando ativo */}
          <video
            ref={videoRef}
            autoPlay
            playsInline
            muted
            className={`w-full h-full object-cover transition-opacity duration-300 ${
              isCameraActive ? 'opacity-100' : 'opacity-0'
            }`}
            style={{ transform: 'scaleX(-1)' }} // Espelhar para ser mais natural
          />
          
          {/* Overlay quando câmera não está ativa */}
          {!isCameraActive && (
            <div className="absolute inset-0 w-full h-full flex items-center justify-center bg-gray-100 dark:bg-gray-800">
              <div className="text-center space-y-2">
                <Camera className="w-16 h-16 mx-auto text-muted-foreground" />
                <p className="text-muted-foreground">
                  {error ? 'Erro na câmera' : 'Câmera desativada'}
                </p>
              </div>
            </div>
          )}
        </div>

        <canvas ref={canvasRef} className="hidden" />

        {error && (
          <div className="text-destructive text-sm p-3 bg-destructive/10 rounded">
            {error}
          </div>
        )}

        <div className="flex gap-2">
          {!isCameraActive ? (
            <Button
              onClick={startCamera}
              disabled={disabled}
              className="flex-1"
            >
              <Camera className="w-4 h-4 mr-2" />
              Ativar Câmera
            </Button>
          ) : (
            <>
              <Button
                onClick={capture}
                disabled={disabled}
                className="flex-1"
              >
                <Camera className="w-4 h-4 mr-2" />
                {label}
              </Button>
              <Button
                onClick={stopCamera}
                variant="outline"
                disabled={disabled}
              >
                <RotateCw className="w-4 h-4" />
              </Button>
            </>
          )}
        </div>
      </div>
    </Card>
  );
}
