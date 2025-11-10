import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ShieldCheck, 
  LogOut, 
  Users,
  UserPlus,
  Trash2,
  Shield,
  Sun,
  Moon,
  AlertCircle,
  Key,
  Copy
} from 'lucide-react';
import { useAuthContext } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { api } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Badge } from '../components/ui/badge';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { toast } from 'sonner';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '../components/ui/dialog';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';

interface User {
  username: string;
  role: string;
  clearance: number;
  created_at: string | null;
}

export function AdminPanel() {
  const { user, token, logout } = useAuthContext();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [resetDialogOpen, setResetDialogOpen] = useState(false);
  const [selectedUser, setSelectedUser] = useState<string>('');
  const [newPassword, setNewPassword] = useState('');
  
  // Formulário de novo usuário
  const [newUser, setNewUser] = useState({
    username: '',
    password: '',
    role: 'public',
    clearance: 1
  });

  // Verificar se é ana.luiza
  useEffect(() => {
    if (user?.username !== 'ana.luiza') {
      toast.error('Acesso negado! Apenas o administrador pode acessar esta página.');
      navigate('/dashboard');
    }
  }, [user, navigate]);

  // Carregar lista de usuários
  const loadUsers = async () => {
    if (!token) return;
    
    setLoading(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'https://bioacess-production.up.railway.app'}/auth/users`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        throw new Error('Erro ao carregar usuários');
      }
      
      const data = await response.json();
      setUsers(data.users || []);
    } catch (error) {
      console.error('Erro ao carregar usuários:', error);
      toast.error('Erro ao carregar lista de usuários');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUsers();
  }, [token]);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!token) return;
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'https://bioacess-production.up.railway.app'}/auth/register`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(newUser)
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao cadastrar usuário');
      }
      
      toast.success('Usuário cadastrado com sucesso!');
      setDialogOpen(false);
      setNewUser({ username: '', password: '', role: 'public', clearance: 1 });
      loadUsers();
    } catch (error: any) {
      console.error('Erro ao cadastrar usuário:', error);
      toast.error(error.message || 'Erro ao cadastrar usuário');
    }
  };

  const handleDeleteUser = async (username: string) => {
    if (!token) return;
    
    if (!confirm(`Tem certeza que deseja deletar o usuário "${username}"?`)) {
      return;
    }
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'https://bioacess-production.up.railway.app'}/auth/users/${username}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao deletar usuário');
      }
      
      toast.success(`Usuário "${username}" deletado com sucesso!`);
      loadUsers();
    } catch (error: any) {
      console.error('Erro ao deletar usuário:', error);
      toast.error(error.message || 'Erro ao deletar usuário');
    }
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!token || !selectedUser) return;
    
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL || 'https://bioacess-production.up.railway.app'}/auth/users/${selectedUser}/reset-password`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ new_password: newPassword })
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Erro ao resetar senha');
      }
      
      toast.success(`Senha do usuário "${selectedUser}" resetada com sucesso!`);
      setResetDialogOpen(false);
      setSelectedUser('');
      setNewPassword('');
    } catch (error: any) {
      console.error('Erro ao resetar senha:', error);
      toast.error(error.message || 'Erro ao resetar senha');
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Copiado para a área de transferência!');
  };

  const getRoleBadgeColor = (clearance: number) => {
    switch (clearance) {
      case 1:
        return 'bg-blue-500';
      case 2:
        return 'bg-purple-500';
      case 3:
        return 'bg-amber-500';
      default:
        return 'bg-gray-500';
    }
  };

  const getRoleLabel = (role: string) => {
    const labels: Record<string, string> = {
      'public': 'Público',
      'director': 'Diretor',
      'minister': 'Ministro'
    };
    return labels[role] || role;
  };

  return (
    <div className="min-h-screen" style={{
      background: theme === 'light' 
        ? 'linear-gradient(135deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%)'
        : 'linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 50%, #262626 100%)'
    }}>
      {/* Header */}
      <header className="border-b shadow-lg" style={{
        background: theme === 'light' ? 'rgba(255, 255, 255, 0.8)' : 'rgba(26, 26, 26, 0.8)',
        borderColor: theme === 'light' ? 'rgba(255, 255, 255, 0.3)' : 'rgba(64, 64, 64, 0.3)',
        backdropFilter: 'blur(20px)'
      }}>
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-11 h-11 rounded-xl flex items-center justify-center shadow-lg" style={{
              background: 'linear-gradient(135deg, #dc2626, #991b1b)'
            }}>
              <Shield className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold" style={{ color: theme === 'light' ? '#dc2626' : '#ef4444' }}>
                Painel Administrativo
              </h1>
              <p className="text-xs" style={{ color: theme === 'light' ? '#64748b' : '#94a3b8' }}>
                Gerenciamento de Usuários
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/dashboard')}
              className="cursor-pointer"
            >
              Voltar ao Dashboard
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={toggleTheme}
              className="p-2 cursor-pointer"
            >
              {theme === 'light' ? <Moon className="w-4 h-4" /> : <Sun className="w-4 h-4" />}
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={() => {
                logout();
                navigate('/login');
              }}
              className="cursor-pointer"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Sair
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Warning */}
        <Card className="p-4 mb-6 border-2" style={{
          background: theme === 'light' ? '#fef2f2' : 'rgba(127, 29, 29, 0.3)',
          borderColor: theme === 'light' ? '#fecaca' : 'rgba(220, 38, 38, 0.5)'
        }}>
          <div className="flex items-center gap-3">
            <AlertCircle className="w-5 h-5" style={{ color: theme === 'light' ? '#dc2626' : '#fca5a5' }} />
            <p className="text-sm font-medium" style={{ color: theme === 'light' ? '#991b1b' : '#fca5a5' }}>
              Área restrita! Apenas o administrador (ana.luiza) tem acesso a esta página.
            </p>
          </div>
        </Card>

        {/* Actions */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold" style={{ color: theme === 'light' ? '#1e293b' : '#f1f5f9' }}>
              Usuários do Sistema
            </h2>
            <p className="text-sm" style={{ color: theme === 'light' ? '#64748b' : '#94a3b8' }}>
              Total: {users.length} usuários
            </p>
          </div>

          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-green-600 hover:bg-green-700 cursor-pointer">
                <UserPlus className="w-4 h-4 mr-2" />
                Novo Usuário
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Cadastrar Novo Usuário</DialogTitle>
                <DialogDescription>
                  Preencha os dados do novo usuário abaixo
                </DialogDescription>
              </DialogHeader>
              <form onSubmit={handleCreateUser} className="space-y-4">
                <div>
                  <Label htmlFor="username">Nome de Usuário</Label>
                  <Input
                    id="username"
                    value={newUser.username}
                    onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="password">Senha</Label>
                  <Input
                    id="password"
                    type="password"
                    value={newUser.password}
                    onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <Label htmlFor="role">Função</Label>
                  <Select value={newUser.role} onValueChange={(value: string) => setNewUser({ ...newUser, role: value })}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="public">Público</SelectItem>
                      <SelectItem value="director">Diretor</SelectItem>
                      <SelectItem value="minister">Ministro</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <Label htmlFor="clearance">Nível de Acesso</Label>
                  <Select 
                    value={newUser.clearance.toString()} 
                    onValueChange={(value: string) => setNewUser({ ...newUser, clearance: parseInt(value) })}
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1">Nível 1 - Público</SelectItem>
                      <SelectItem value="2">Nível 2 - Diretoria</SelectItem>
                      <SelectItem value="3">Nível 3 - Ministério</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <Button type="submit" className="w-full cursor-pointer">
                  Cadastrar Usuário
                </Button>
              </form>
            </DialogContent>
          </Dialog>
        </div>

        {/* Users List */}
        {loading ? (
          <Card className="p-8 text-center">
            <p style={{ color: theme === 'light' ? '#64748b' : '#94a3b8' }}>
              Carregando usuários...
            </p>
          </Card>
        ) : (
          <div className="grid gap-4">
            {users.map((u) => (
              <Card key={u.username} className="p-6 border-2" style={{
                background: theme === 'light' ? 'rgba(255, 255, 255, 0.5)' : 'rgba(26, 26, 26, 0.5)',
                backdropFilter: 'blur(16px)'
              }}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl flex items-center justify-center text-white" style={{
                      background: u.clearance === 3 ? 'linear-gradient(135deg, #f59e0b, #d97706)' :
                                 u.clearance === 2 ? 'linear-gradient(135deg, #8b5cf6, #7c3aed)' :
                                 'linear-gradient(135deg, #3b82f6, #2563eb)'
                    }}>
                      <Users className="w-6 h-6" />
                    </div>
                    <div>
                      <h3 className="font-bold text-lg" style={{ color: theme === 'light' ? '#1e293b' : '#f1f5f9' }}>
                        {u.username}
                      </h3>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge className={`${getRoleBadgeColor(u.clearance)} text-xs`}>
                          {getRoleLabel(u.role)}
                        </Badge>
                        <span className="text-xs" style={{ color: theme === 'light' ? '#64748b' : '#94a3b8' }}>
                          Nível {u.clearance}
                        </span>
                      </div>
                    </div>
                  </div>

                  {u.username !== 'ana.luiza' && (
                    <div className="flex gap-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setSelectedUser(u.username);
                          setNewPassword('');
                          setResetDialogOpen(true);
                        }}
                        className="cursor-pointer"
                      >
                        <Key className="w-4 h-4 mr-2" />
                        Resetar Senha
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDeleteUser(u.username)}
                        className="cursor-pointer"
                      >
                        <Trash2 className="w-4 h-4 mr-2" />
                        Deletar
                      </Button>
                    </div>
                  )}
                </div>
              </Card>
            ))}
          </div>
        )}
      </main>

      {/* Reset Password Dialog */}
      <Dialog open={resetDialogOpen} onOpenChange={setResetDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Resetar Senha - {selectedUser}</DialogTitle>
            <DialogDescription>
              Digite uma nova senha para o usuário. Certifique-se de copiar e guardar a senha antes de fechar.
            </DialogDescription>
          </DialogHeader>
          <form onSubmit={handleResetPassword}>
            <div className="space-y-4 py-4">
              <div className="space-y-2">
                <Label htmlFor="newPassword">Nova Senha</Label>
                <div className="flex gap-2">
                  <Input
                    id="newPassword"
                    type="text"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="Digite a nova senha"
                    required
                    minLength={6}
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="icon"
                    onClick={() => copyToClipboard(newPassword)}
                    disabled={!newPassword}
                    title="Copiar senha"
                    className="cursor-pointer"
                  >
                    <Copy className="w-4 h-4" />
                  </Button>
                </div>
                <p className="text-xs text-muted-foreground">
                  Mínimo de 6 caracteres
                </p>
              </div>
            </div>
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => {
                  setResetDialogOpen(false);
                  setNewPassword('');
                  setSelectedUser('');
                }}
                className="cursor-pointer"
              >
                Cancelar
              </Button>
              <Button type="submit" className="cursor-pointer">
                Resetar Senha
              </Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
