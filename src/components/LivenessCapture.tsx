// Componente para captura de liveness (duas fotos com movimento)

import { useState } from 'react';
import { Camera, CheckCircle2, Circle } from 'lucide-react';
import { Card } from './ui/card';
import { Button } from './ui/button';
import { CameraCapture } from './CameraCapture';
import type { LivenessImages } from '../types';

interface LivenessCaptureProps {
  onComplete: (images: LivenessImages) => void;
  disabled?: boolean;
}

export function LivenessCapture({ onComplete, disabled }: LivenessCaptureProps) {
  const [imageA, setImageA] = useState<string>('');
  const [imageB, setImageB] = useState<string>('');
  const [currentStep, setCurrentStep] = useState<1 | 2>(1);

  const handleCaptureA = (base64: string) => {
    setImageA(base64);
    setCurrentStep(2);
  };

  const handleCaptureB = (base64: string) => {
    setImageB(base64);
  };

  const handleSubmit = () => {
    if (imageA && imageB) {
      onComplete({ image_a: imageA, image_b: imageB });
    }
  };

  const handleReset = () => {
    setImageA('');
    setImageB('');
    setCurrentStep(1);
  };

  const isComplete = imageA && imageB;

  return (
    <div className="space-y-6">
      {/* Indicador de progresso */}
      <div className="flex items-center justify-center gap-4">
        <div className="flex items-center gap-2">
          {currentStep === 1 ? (
            <Circle className="w-5 h-5 text-primary fill-primary" />
          ) : (
            <CheckCircle2 className="w-5 h-5 text-green-500" />
          )}
          <span className={currentStep === 1 ? 'font-medium' : 'text-muted-foreground'}>
            Foto 1: Olhar reto
          </span>
        </div>
        
        <div className="w-12 h-0.5 bg-border" />
        
        <div className="flex items-center gap-2">
          {currentStep === 1 ? (
            <Circle className="w-5 h-5 text-muted-foreground" />
          ) : isComplete ? (
            <CheckCircle2 className="w-5 h-5 text-green-500" />
          ) : (
            <Circle className="w-5 h-5 text-primary fill-primary" />
          )}
          <span className={currentStep === 2 ? 'font-medium' : 'text-muted-foreground'}>
            Foto 2: Piscar ou virar
          </span>
        </div>
      </div>

      {/* Instruções */}
      <Card className="p-4 bg-blue-50 dark:bg-blue-950/20 border-blue-200 dark:border-blue-800">
        <div className="flex gap-3">
          <Camera className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="text-sm text-blue-900 dark:text-blue-100">
              {currentStep === 1 ? (
                <>
                  <strong>Primeira captura:</strong> Olhe diretamente para a câmera com expressão neutra.
                </>
              ) : !isComplete ? (
                <>
                  <strong>Segunda captura:</strong> Pisque os olhos ou vire levemente a cabeça para comprovar que você é uma pessoa real.
                </>
              ) : (
                <>
                  <strong>Capturas concluídas!</strong> Clique em "Verificar Identidade" para prosseguir.
                </>
              )}
            </p>
          </div>
        </div>
      </Card>

      {/* Área de captura */}
      {currentStep === 1 && !imageA && (
        <CameraCapture
          onCapture={handleCaptureA}
          disabled={disabled}
          label="Capturar Primeira Foto"
        />
      )}

      {currentStep === 2 && !imageB && (
        <CameraCapture
          onCapture={handleCaptureB}
          disabled={disabled}
          label="Capturar Segunda Foto"
        />
      )}

      {/* Preview e ações */}
      {isComplete && (
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-muted-foreground mb-2">Foto 1</p>
              <div className="relative bg-muted rounded-lg overflow-hidden aspect-video">
                <img
                  src={`data:image/jpeg;base64,${imageA}`}
                  alt="Captura 1"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
            <div>
              <p className="text-sm text-muted-foreground mb-2">Foto 2</p>
              <div className="relative bg-muted rounded-lg overflow-hidden aspect-video">
                <img
                  src={`data:image/jpeg;base64,${imageB}`}
                  alt="Captura 2"
                  className="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>

          <div className="flex gap-2">
            <Button
              onClick={handleSubmit}
              disabled={disabled}
              className="flex-1"
            >
              <CheckCircle2 className="w-4 h-4 mr-2" />
              Verificar Identidade
            </Button>
            <Button
              onClick={handleReset}
              variant="outline"
              disabled={disabled}
            >
              Refazer
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
