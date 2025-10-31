import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useAuth } from '../src/hooks/useAuth';

describe('useAuth Hook', () => {
  beforeEach(() => {
    sessionStorage.clear();
  });

  afterEach(() => {
    sessionStorage.clear();
  });

  it('deve iniciar sem usuário autenticado', () => {
    const { result } = renderHook(() => useAuth());

    expect(result.current.user).toBeNull();
    expect(result.current.token).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
  });

  it('deve fazer login e armazenar dados', () => {
    const { result } = renderHook(() => useAuth());

    act(() => {
      result.current.login('test-token', {
        username: 'alice',
        role: 'public',
        clearance: 1
      });
    });

    expect(result.current.user?.username).toBe('alice');
    expect(result.current.token).toBe('test-token');
    expect(result.current.isAuthenticated).toBe(true);
    
    // Verifica sessionStorage
    expect(sessionStorage.getItem('bioaccess_token')).toBe('test-token');
    expect(sessionStorage.getItem('bioaccess_user')).toContain('alice');
  });

  it('deve fazer logout e limpar dados', () => {
    const { result } = renderHook(() => useAuth());

    act(() => {
      result.current.login('test-token', {
        username: 'alice',
        role: 'public',
        clearance: 1
      });
    });

    expect(result.current.isAuthenticated).toBe(true);

    act(() => {
      result.current.logout();
    });

    expect(result.current.user).toBeNull();
    expect(result.current.token).toBeNull();
    expect(result.current.isAuthenticated).toBe(false);
    expect(sessionStorage.getItem('bioaccess_token')).toBeNull();
  });

  it('deve verificar hasAccess corretamente', () => {
    const { result } = renderHook(() => useAuth());

    act(() => {
      result.current.login('test-token', {
        username: 'bruno',
        role: 'director',
        clearance: 2
      });
    });

    expect(result.current.hasAccess(1)).toBe(true);
    expect(result.current.hasAccess(2)).toBe(true);
    expect(result.current.hasAccess(3)).toBe(false);
  });

  it('deve carregar dados do sessionStorage ao montar', () => {
    const userData = {
      username: 'ministro',
      role: 'minister',
      clearance: 3
    };

    sessionStorage.setItem('bioaccess_token', 'stored-token');
    sessionStorage.setItem('bioaccess_user', JSON.stringify(userData));

    const { result } = renderHook(() => useAuth());

    // Aguarda carregamento
    expect(result.current.loading).toBe(true);
    
    // Após carregamento
    setTimeout(() => {
      expect(result.current.loading).toBe(false);
      expect(result.current.user?.username).toBe('ministro');
      expect(result.current.token).toBe('stored-token');
    }, 0);
  });
});
