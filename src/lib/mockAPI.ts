// API simulada para resolver problemas de conexão com backend
// Esta é uma versão temporária que simula todas as respostas da API

export const mockAPI = {
  // Simular login tradicional
  async login(username: string, password: string) {
    console.log('🔑 Mock API: Login tradicional', { username, password });
    
    const users: Record<string, { password: string; role: string; clearance: number }> = {
      'ana.luiza': { password: 'senha123', role: 'public', clearance: 1 },
      'diretor.silva': { password: 'diretor2024', role: 'director', clearance: 2 },
      'ministro.ambiente': { password: 'ministro2024', role: 'minister', clearance: 3 }
    };
    
    const user = users[username];
    if (user && user.password === password) {
      return {
        token: `mock_token_${username}`,
        role: user.role,
        clearance: user.clearance,
        username: username
      };
    }
    
    throw new Error('Credenciais inválidas');
  },

  // Simular verificação de biometria
  async checkBiometric(username: string) {
    console.log('🔍 Mock API: Verificando biometria', { username });
    
    // Todos os usuários válidos têm biometria para demonstração
    const validUsers = ['ana.luiza', 'diretor.silva', 'ministro.ambiente'];
    const emailUsers = [
      'ana.luiza@meio-ambiente.gov.br', 
      'diretor.silva@meio-ambiente.gov.br', 
      'ministro.ambiente@gov.br'
    ];
    
    const isValid = validUsers.includes(username) || 
                   emailUsers.some(email => email.includes(username) || username.includes(email));
    
    if (isValid) {
      return {
        has_biometric: true,
        message: 'Biometria encontrada - Mock Demo'
      };
    }
    
    return {
      has_biometric: false,
      message: 'Biometria não encontrada. Cadastre primeiro.'
    };
  },

  // Simular verificação biométrica (novo formato compatível)
  async verifyBiometric(email: string, image: string) {
    console.log('🎭 Mock API: Verificação biométrica', { email, hasImage: !!image });
    
    // Aguardar um pouco para simular processamento
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const userMap: Record<string, { username: string; role: string; clearance: number; name: string }> = {
      'ana.luiza@meio-ambiente.gov.br': { username: 'ana.luiza', role: 'public', clearance: 1, name: 'Ana Luiza' },
      'diretor.silva@meio-ambiente.gov.br': { username: 'diretor.silva', role: 'director', clearance: 2, name: 'Diretor Silva' },
      'ministro.ambiente@gov.br': { username: 'ministro.ambiente', role: 'minister', clearance: 3, name: 'Ministro Ambiente' }
    };
    
    // Busca flexível por email ou username
    let user = userMap[email];
    if (!user) {
      for (const [userEmail, userData] of Object.entries(userMap)) {
        if (userEmail.includes(email) || email.includes(userData.username)) {
          user = userData;
          break;
        }
      }
    }
    
    if (!user) {
      throw new Error('Usuário não encontrado ou sem biometria cadastrada');
    }
    
    // Simular sempre sucesso para demo (alta similaridade)
    const similarity = 0.92 + Math.random() * 0.05; // Entre 0.92 e 0.97
    
    return {
      token: `biometric_${user.username}_${Date.now()}`,
      role: user.role,
      clearance: user.clearance,
      username: user.username
    };
  },

  // Simular cadastro de biometria
  async enroll(username: string, image: string) {
    console.log('📝 Mock API: Cadastro de biometria', { username, imageLength: image?.length });
    
    // Validação básica do nome de usuário
    if (!username || username.trim().length === 0) {
      throw new Error('Nome de usuário é obrigatório');
    }
    
    // Simular detecção de rosto
    if (!image || image.length < 100) {
      throw new Error('Não foi possível detectar um rosto na imagem. Tente novamente.');
    }
    
    // Aceitar qualquer usuário válido para cadastro
    console.log('✅ Mock API: Cadastro aprovado para usuário:', username);
    
    // Simular sucesso no cadastro
    return {
      success: true,
      message: `Biometria cadastrada com sucesso para ${username}!`,
      user_id: Math.floor(Math.random() * 1000)
    };
  }
};

// Função para alternar entre API real e mock
export const USE_MOCK_API = false; // FALSE para usar API real com DeepFace