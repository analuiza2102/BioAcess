import '@testing-library/jest-dom';

// Mock para getUserMedia (necessário para testes de câmera)
Object.defineProperty(window, 'navigator', {
  value: {
    ...window.navigator,
    mediaDevices: {
      getUserMedia: async () => ({
        getTracks: () => [],
      }),
    },
  },
  writable: true,
});

// Mock para sessionStorage
const sessionStorageMock = (() => {
  let store: Record<string, string> = {};

  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    },
  };
})();

Object.defineProperty(window, 'sessionStorage', {
  value: sessionStorageMock,
});
