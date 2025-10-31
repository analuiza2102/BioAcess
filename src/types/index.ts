// Tipos e interfaces do sistema BioAccess

export interface User {
  username: string;
  role: 'public' | 'director' | 'minister';
  clearance: 1 | 2 | 3;
}

export interface AuthResponse {
  token?: string;
  access_token?: string;
  token_type?: string;
  role: string;
  clearance: number;
  username?: string;
  message?: string;
}

export interface CreateUserResponse {
  success: boolean;
  message: string;
  user_id: number;
  username: string;
  role: string;
  clearance: number;
}

export interface EnrollResponse {
  success: boolean;
  message: string;
  user_id?: number;
}

export interface AuditLog {
  id: number;
  user: string;
  action: string;
  level_requested: number;
  success: boolean;
  origin_ip: string | null;
  ts: string;
}

export interface AuditParams {
  page?: number;
  limit?: number;
  start_date?: string;
  end_date?: string;
  action?: string;
  success?: boolean;
}

export interface LevelDataResponse {
  level: number;
  data: any;
  message: string;
}

export interface LivenessImages {
  image_a: string;
  image_b: string;
}

export type ClearanceLevel = 1 | 2 | 3;

export const ROLE_LABELS: Record<string, string> = {
  public: 'Acesso Público',
  director: 'Diretor de Divisão',
  minister: 'Ministro do Meio Ambiente'
};

export const LEVEL_LABELS: Record<number, string> = {
  1: 'Nível 1 - Dados Públicos sobre Agrotóxicos',
  2: 'Nível 2 - Relatórios Regionais Detalhados',
  3: 'Nível 3 - Informações Estratégicas Confidenciais'
};
