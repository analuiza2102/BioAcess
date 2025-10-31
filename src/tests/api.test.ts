import { describe, it, expect, vi, beforeEach } from 'vitest';
import { api, APIError } from '../src/lib/api';

// Mock global fetch
global.fetch = vi.fn();

describe('API Client', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('enroll', () => {
    it('deve cadastrar biometria com sucesso', async () => {
      const mockResponse = {
        success: true,
        message: 'Biometria cadastrada',
        user_id: 1
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await api.enroll('alice', 'base64image');
      
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/auth/enroll'),
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: expect.stringContaining('alice')
        })
      );
    });

    it('deve lançar APIError em caso de falha', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Usuário não encontrado' })
      });

      await expect(api.enroll('invalid', 'base64image'))
        .rejects
        .toThrow(APIError);
    });
  });

  describe('verify', () => {
    it('deve verificar biometria e retornar token', async () => {
      const mockResponse = {
        token: 'jwt-token-123',
        role: 'public',
        clearance: 1,
        username: 'alice'
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await api.verify('alice', 'img1', 'img2');
      
      expect(result).toEqual(mockResponse);
      expect(result.token).toBe('jwt-token-123');
    });

    it('deve lançar erro 401 para autenticação falha', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 401,
        json: async () => ({ detail: 'Autenticação falhou' })
      });

      await expect(api.verify('alice', 'img1', 'img2'))
        .rejects
        .toThrow(APIError);
    });
  });

  describe('fetchLevel', () => {
    it('deve buscar dados de nível com token válido', async () => {
      const mockResponse = {
        level: 1,
        data: { info: 'Dados públicos' },
        message: 'Acesso concedido'
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await api.fetchLevel(1, 'valid-token');
      
      expect(result).toEqual(mockResponse);
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/data/level/1'),
        expect.objectContaining({
          headers: expect.objectContaining({
            'Authorization': 'Bearer valid-token'
          })
        })
      );
    });

    it('deve lançar erro 403 para clearance insuficiente', async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 403,
        json: async () => ({ detail: 'Clearance insuficiente' })
      });

      await expect(api.fetchLevel(3, 'token'))
        .rejects
        .toThrow(APIError);
    });
  });

  describe('fetchAudit', () => {
    it('deve buscar logs de auditoria', async () => {
      const mockResponse = {
        logs: [
          {
            id: 1,
            user: 'alice',
            action: 'verify',
            level_requested: 1,
            success: true,
            origin_ip: '127.0.0.1',
            ts: '2025-10-27T10:00:00Z'
          }
        ],
        total: 1
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      });

      const result = await api.fetchAudit({ page: 1, limit: 10 }, 'token');
      
      expect(result.logs).toHaveLength(1);
      expect(result.total).toBe(1);
    });
  });
});
