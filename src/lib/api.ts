// Cliente API para integração com backend FastAPI

/// <reference types="vite/client" />

import type {
  AuthResponse,
  EnrollResponse,
  AuditLog,
  AuditParams,
  LevelDataResponse
} from '../types';

import { mockAPI, USE_MOCK_API } from './mockAPI';

// URL da API com fallback para produção
const API_BASE = import.meta.env?.VITE_API_URL 
  || import.meta.env?.VITE_API_BASE 
  || (window.location.hostname.includes('vercel.app') ? 'https://bioacess.onrender.com' : 'http://localhost:8001');

console.log('🔍 Debug Environment Variables:', {
  VITE_API_URL: import.meta.env?.VITE_API_URL,
  VITE_API_BASE: import.meta.env?.VITE_API_BASE,
  hostname: window.location.hostname,
  API_BASE: API_BASE
});

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ 
      detail: 'Erro desconhecido' 
    }));
    throw new APIError(
      response.status,
      error.detail || error.message || 'Erro na requisição'
    );
  }
  return response.json();
}

export const api = {
  /**
   * Login tradicional
   */
  async login(username: string, password: string): Promise<AuthResponse> {
    if (USE_MOCK_API) {
      return mockAPI.login(username, password);
    }
    
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        password
      })
    });
    return handleResponse<AuthResponse>(response);
  },

  /**
   * Verificar se usuário tem biometria cadastrada
   */
  async checkBiometric(username: string): Promise<{ has_biometric: boolean; message: string }> {
    if (USE_MOCK_API) {
      return mockAPI.checkBiometric(username);
    }
    
    const response = await fetch(`${API_BASE}/auth/check-biometric`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username
      })
    });
    return handleResponse<{ has_biometric: boolean; message: string }>(response);
  },

  /**
   * Enrola biometria de um usuário
   */
  async enroll(name: string, email: string, imageBase64: string): Promise<EnrollResponse> {
    if (USE_MOCK_API) {
      return mockAPI.enroll(email, imageBase64);
    }
    
    const response = await fetch(`${API_BASE}/auth/enroll`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        email,
        image: imageBase64
      })
    });
    return handleResponse<EnrollResponse>(response);
  },

  /**
   * Verifica biometria (nova API compatível)
   */
  async verifyBiometric(email: string, image: string): Promise<AuthResponse> {
    if (USE_MOCK_API) {
      return mockAPI.verifyBiometric(email, image);
    }
    
    const response = await fetch(`${API_BASE}/auth/verify-biometric`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email,
        image
      })
    });
    return handleResponse<AuthResponse>(response);
  },

  /**
   * Verifica biometria com liveness detection (método legado)
   */
  async verify(
    username: string,
    imageA: string,
    imageB: string
  ): Promise<AuthResponse> {
    if (USE_MOCK_API) {
      // Converter para novo formato
      const email = username.includes('@') ? username : `${username}@meio-ambiente.gov.br`;
      return mockAPI.verifyBiometric(email, imageA);
    }
    
    const response = await fetch(`${API_BASE}/auth/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        image_b64_a: imageA,
        image_b64_b: imageB
      })
    });
    return handleResponse<AuthResponse>(response);
  },

  /**
   * Verifica se o usuário logado tem biometria cadastrada
   */
  async checkBiometricStatus(username: string): Promise<{ has_biometric: boolean; message: string }> {
    if (USE_MOCK_API) {
      // Mock sempre retorna false para demonstração
      return { has_biometric: false, message: "Biometria não cadastrada" };
    }
    
    const response = await fetch(`${API_BASE}/auth/check-biometric`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username
      })
    });
    return handleResponse<{ has_biometric: boolean; message: string }>(response);
  },

  /**
   * Login por reconhecimento facial usando câmera
   */
  async loginByCamera(username: string, cameraImage: File): Promise<AuthResponse> {
    if (USE_MOCK_API) {
      // Mock simula sucesso
      return mockAPI.login(username, 'password');
    }
    
    const formData = new FormData();
    formData.append('username', username);
    formData.append('camera_image', cameraImage, 'camera_capture.jpg');
    
    const response = await fetch(`${API_BASE}/auth/verify-camera`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<AuthResponse>(response);
  },

  /**
   * Busca dados de um nível específico (protegido por JWT)
   */
  async fetchLevel(level: number, token: string): Promise<LevelDataResponse> {
    const response = await fetch(`${API_BASE}/data/level/${level}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return handleResponse<LevelDataResponse>(response);
  },

  /**
   * Busca logs de auditoria (apenas clearance 3)
   */
  async fetchAudit(
    params: AuditParams,
    token: string
  ): Promise<{ logs: AuditLog[]; total: number }> {
    const searchParams = new URLSearchParams();
    
    if (params.page) searchParams.set('page', params.page.toString());
    if (params.limit) searchParams.set('limit', params.limit.toString());
    if (params.start_date) searchParams.set('start_date', params.start_date);
    if (params.end_date) searchParams.set('end_date', params.end_date);
    if (params.action) searchParams.set('action', params.action);
    if (params.success !== undefined) {
      searchParams.set('success', params.success.toString());
    }

    const response = await fetch(
      `${API_BASE}/reports/audit?${searchParams.toString()}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      }
    );
    return handleResponse<{ logs: AuditLog[]; total: number }>(response);
  },

  /**
   * Método POST genérico para requisições
   */
  async post<T = any>(endpoint: string, data: any): Promise<T> {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return handleResponse<T>(response);
  },

  /**
   * Cadastro de biometria via upload de arquivo de imagem
   */
  async enrollImageUpload(username: string, imageFile: File): Promise<EnrollResponse> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('image', imageFile);

    const response = await fetch(`${API_BASE}/auth/enroll-upload`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<EnrollResponse>(response);
  },

  /**
   * Verificação biométrica via upload de arquivo de imagem
   */
  async verifyImageUpload(username: string, imageFile: File): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('image', imageFile);

    const response = await fetch(`${API_BASE}/auth/verify-upload`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<AuthResponse>(response);
  },

  /**
   * Cadastro de biometria via base64 (método existente atualizado)
   */
  async enrollBiometric(username: string, imageBase64: string, imageFormat: string = 'jpeg'): Promise<EnrollResponse> {
    if (USE_MOCK_API) {
      return mockAPI.enroll(username, imageBase64);
    }
    
    const response = await fetch(`${API_BASE}/auth/enroll`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        image_b64: imageBase64,
        image_format: imageFormat
      })
    });
    return handleResponse<EnrollResponse>(response);
  },

  /**
   * Verificação biométrica via base64 (método existente atualizado)
   */
  async verifyBiometricImage(username: string, imageBase64: string, imageFormat: string = 'jpeg'): Promise<AuthResponse> {
    if (USE_MOCK_API) {
      return mockAPI.verifyBiometric(username, imageBase64);
    }
    
    const response = await fetch(`${API_BASE}/auth/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username,
        image_b64: imageBase64,
        image_format: imageFormat
      })
    });
    return handleResponse<AuthResponse>(response);
  }
};

export { APIError };
