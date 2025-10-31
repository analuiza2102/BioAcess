// Componente para upload de imagem biométrica

import { useState, useRef } from 'react';
import { Upload, FileImage, X, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from './ui/button';
import { Card } from './ui/card';

interface ImageUploadProps {
  onImageSelect: (file: File) => void;
  disabled?: boolean;
  label?: string;
  acceptedFormats?: string[];
  maxSizeMB?: number;
  showPreview?: boolean;
}

export function ImageUpload({ 
  onImageSelect, 
  disabled = false, 
  label = 'Selecionar Imagem',
  acceptedFormats = ['image/jpeg', 'image/jpg', 'image/png'],
  maxSizeMB = 5,
  showPreview = true
}: ImageUploadProps) {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string>('');
  const [error, setError] = useState<string>('');

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validações
    if (!acceptedFormats.includes(file.type)) {
      setError(`Formato não suportado. Use: ${acceptedFormats.map(f => f.split('/')[1].toUpperCase()).join(', ')}`);
      return;
    }

    if (file.size > maxSizeMB * 1024 * 1024) {
      setError(`Arquivo muito grande. Máximo: ${maxSizeMB}MB`);
      return;
    }

    setError('');
    setSelectedFile(file);
    
    // Criar preview
    if (showPreview) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setPreviewUrl(e.target?.result as string);
      };
      reader.readAsDataURL(file);
    }

    onImageSelect(file);
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setPreviewUrl('');
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const triggerFileSelect = () => {
    fileInputRef.current?.click();
  };

  return (
    <div className="space-y-4">
      {/* Input oculto */}
      <input
        ref={fileInputRef}
        type="file"
        accept={acceptedFormats.join(',')}
        onChange={handleFileSelect}
        className="hidden"
        disabled={disabled}
      />

      {/* Área de upload */}
      {!selectedFile && (
        <Card className="border-2 border-dashed border-gray-300 hover:border-gray-400 transition-colors">
          <div 
            className="p-8 text-center cursor-pointer"
            onClick={triggerFileSelect}
          >
            <div className="flex flex-col items-center space-y-4">
              <div className="p-3 bg-blue-50 rounded-full">
                <Upload className="w-8 h-8 text-blue-500" />
              </div>
              
              <div className="space-y-2">
                <h3 className="font-medium text-gray-900">
                  Selecione uma imagem
                </h3>
                <p className="text-sm text-gray-500">
                  PNG, JPEG ou JPG até {maxSizeMB}MB
                </p>
                <p className="text-xs text-gray-400">
                  ⚡ Recomenda-se usar imagens com fundo branco para melhor precisão
                </p>
              </div>
              
              <Button type="button" disabled={disabled}>
                <FileImage className="w-4 h-4 mr-2" />
                {label}
              </Button>
            </div>
          </div>
        </Card>
      )}

      {/* Preview da imagem selecionada */}
      {selectedFile && showPreview && (
        <Card className="p-4">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              {previewUrl && (
                <img
                  src={previewUrl}
                  alt="Preview"
                  className="w-32 h-32 object-cover rounded-lg border"
                />
              )}
            </div>
            
            <div className="flex-1 min-w-0">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {selectedFile.name}
                  </p>
                  <p className="text-sm text-gray-500">
                    {selectedFile.type} • {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <div className="flex items-center mt-1">
                    <CheckCircle className="w-4 h-4 text-green-500 mr-1" />
                    <span className="text-sm text-green-600">Imagem selecionada</span>
                  </div>
                </div>
                
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={clearSelection}
                  disabled={disabled}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Informações sobre o arquivo sem preview */}
      {selectedFile && !showPreview && (
        <Card className="p-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <FileImage className="w-5 h-5 text-blue-500" />
              <div>
                <p className="text-sm font-medium text-gray-900 truncate">
                  {selectedFile.name}
                </p>
                <p className="text-xs text-gray-500">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={clearSelection}
              disabled={disabled}
            >
              <X className="w-4 h-4" />
            </Button>
          </div>
        </Card>
      )}

      {/* Mensagem de erro */}
      {error && (
        <div className="flex items-center space-x-2 p-3 bg-red-50 border border-red-200 rounded-md">
          <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Dicas de uso */}
      <div className="text-xs text-gray-500 space-y-1">
        <p><strong>💡 Dicas para melhor resultado:</strong></p>
        <ul className="list-disc list-inside space-y-1 ml-2">
          <li>Use imagem com fundo branco ou claro</li>
          <li>Rosto deve estar bem iluminado e centralizado</li>
          <li>Evite sombras ou reflexos</li>
          <li>Resolução mínima recomendada: 640x480px</li>
        </ul>
      </div>
    </div>
  );
}