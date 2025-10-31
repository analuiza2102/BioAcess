// Página de relatórios de auditoria (apenas clearance 3)

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ArrowLeft, 
  Download, 
  Search, 
  Filter,
  CheckCircle,
  XCircle,
  Calendar
} from 'lucide-react';
import { useAuthContext } from '../contexts/AuthContext';
import { api, APIError } from '../lib/api';
import { Button } from '../components/ui/button';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table';
import { Badge } from '../components/ui/badge';
import { toast } from 'sonner';
import type { AuditLog, AuditParams } from '../types';

export function Reports() {
  const { user, token, logout } = useAuthContext();
  const navigate = useNavigate();
  const [logs, setLogs] = useState<AuditLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [total, setTotal] = useState(0);
  
  const [filters, setFilters] = useState<AuditParams>({
    page: 1,
    limit: 10,
    start_date: '',
    end_date: '',
    action: '',
    success: undefined
  });

  useEffect(() => {
    loadLogs();
  }, [filters.page]);

  const loadLogs = async () => {
    if (!token) {
      setLoading(false);
      return;
    }

    setLoading(true);

    try {
      const response = await api.fetchAudit(filters, token);
      setLogs(response.logs);
      setTotal(response.total);
    } catch (error) {
      console.error('Erro ao carregar logs:', error);
      
      if (error instanceof APIError) {
        if (error.status === 403) {
          toast.error('Acesso negado! Apenas usuários com clearance 3 podem acessar relatórios.');
          // Usa setTimeout para evitar navegação durante renderização
          setTimeout(() => navigate('/dashboard'), 100);
        } else if (error.status === 401) {
          toast.error('Sessão expirada. Faça login novamente.');
          logout();
          // Usa setTimeout para evitar navegação durante renderização
          setTimeout(() => navigate('/login'), 100);
        } else {
          toast.error(error.message);
        }
      } else {
        toast.error('Erro ao conectar com o servidor.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    setFilters(prev => ({ ...prev, page: 1 }));
    loadLogs();
  };

  const handleExportCSV = () => {
    if (logs.length === 0) {
      toast.warning('Não há dados para exportar');
      return;
    }

    const headers = ['ID', 'Usuário', 'Ação', 'Nível', 'Sucesso', 'IP', 'Data/Hora'];
    const rows = logs.map(log => [
      log.id,
      log.user,
      log.action,
      log.level_requested,
      log.success ? 'Sim' : 'Não',
      log.origin_ip || 'N/A',
      new Date(log.ts).toLocaleString('pt-BR')
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    
    link.setAttribute('href', url);
    link.setAttribute('download', `audit_logs_${new Date().getTime()}.csv`);
    link.style.visibility = 'hidden';
    
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    toast.success('Relatório exportado com sucesso!');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const totalPages = Math.ceil(total / (filters.limit || 10));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-950 border-b shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <Button
            variant="ghost"
            onClick={() => navigate('/dashboard')}
            className="mb-2"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Voltar ao Dashboard
          </Button>
          
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl mb-1">Relatórios de Auditoria</h1>
              <p className="text-sm text-muted-foreground">
                Visualize e exporte logs de acesso ao sistema
              </p>
            </div>
            
            <Button onClick={handleExportCSV} disabled={logs.length === 0}>
              <Download className="w-4 h-4 mr-2" />
              Exportar CSV
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {/* Filters */}
        <Card className="p-6 mb-6">
          <div className="flex items-center gap-2 mb-4">
            <Filter className="w-5 h-5 text-muted-foreground" />
            <h3>Filtros</h3>
          </div>

          <div className="grid md:grid-cols-4 gap-4">
            <div className="space-y-2">
              <Label htmlFor="start-date">Data Inicial</Label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
                <Input
                  id="start-date"
                  type="date"
                  value={filters.start_date}
                  onChange={(e) => setFilters(prev => ({ ...prev, start_date: e.target.value }))}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="end-date">Data Final</Label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
                <Input
                  id="end-date"
                  type="date"
                  value={filters.end_date}
                  onChange={(e) => setFilters(prev => ({ ...prev, end_date: e.target.value }))}
                  className="pl-10"
                />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="action">Ação</Label>
              <Input
                id="action"
                type="text"
                placeholder="Ex: verify, enroll"
                value={filters.action}
                onChange={(e) => setFilters(prev => ({ ...prev, action: e.target.value }))}
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="success">Status</Label>
              <Select
                value={filters.success === undefined ? 'all' : filters.success.toString()}
                onValueChange={(value: string) => setFilters(prev => ({
                  ...prev,
                  success: value === 'all' ? undefined : value === 'true'
                }))}
              >
                <SelectTrigger id="success">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Todos</SelectItem>
                  <SelectItem value="true">Sucesso</SelectItem>
                  <SelectItem value="false">Falha</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="flex gap-2 mt-4">
            <Button onClick={handleSearch} disabled={loading}>
              <Search className="w-4 h-4 mr-2" />
              Buscar
            </Button>
            <Button
              variant="outline"
              onClick={() => {
                setFilters({
                  page: 1,
                  limit: 10,
                  start_date: '',
                  end_date: '',
                  action: '',
                  success: undefined
                });
                loadLogs();
              }}
            >
              Limpar Filtros
            </Button>
          </div>
        </Card>

        {/* Table */}
        <Card className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <div className="text-center space-y-4">
                <div className="w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto" />
                <p className="text-muted-foreground">Carregando logs...</p>
              </div>
            </div>
          ) : logs.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-muted-foreground">Nenhum log encontrado</p>
            </div>
          ) : (
            <>
              <div className="mb-4 text-sm text-muted-foreground">
                Total de {total} registros • Página {filters.page} de {totalPages}
              </div>

              <div className="border rounded-lg overflow-hidden">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Usuário</TableHead>
                      <TableHead>Ação</TableHead>
                      <TableHead>Nível</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>IP</TableHead>
                      <TableHead>Data/Hora</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {logs.map((log) => (
                      <TableRow key={log.id}>
                        <TableCell className="font-mono text-sm">
                          #{log.id}
                        </TableCell>
                        <TableCell>{log.user}</TableCell>
                        <TableCell>
                          <Badge variant="outline">{log.action}</Badge>
                        </TableCell>
                        <TableCell>N{log.level_requested}</TableCell>
                        <TableCell>
                          {log.success ? (
                            <div className="flex items-center gap-2 text-green-600 dark:text-green-400">
                              <CheckCircle className="w-4 h-4" />
                              <span className="text-sm">Sucesso</span>
                            </div>
                          ) : (
                            <div className="flex items-center gap-2 text-red-600 dark:text-red-400">
                              <XCircle className="w-4 h-4" />
                              <span className="text-sm">Falha</span>
                            </div>
                          )}
                        </TableCell>
                        <TableCell className="font-mono text-sm">
                          {log.origin_ip || 'N/A'}
                        </TableCell>
                        <TableCell className="text-sm">
                          {formatDate(log.ts)}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between mt-4">
                  <Button
                    variant="outline"
                    onClick={() => setFilters(prev => ({ ...prev, page: Math.max(1, (prev.page || 1) - 1) }))}
                    disabled={filters.page === 1 || loading}
                  >
                    Anterior
                  </Button>
                  
                  <span className="text-sm text-muted-foreground">
                    Página {filters.page} de {totalPages}
                  </span>
                  
                  <Button
                    variant="outline"
                    onClick={() => setFilters(prev => ({ ...prev, page: Math.min(totalPages, (prev.page || 1) + 1) }))}
                    disabled={(filters.page || 1) >= totalPages || loading}
                  >
                    Próxima
                  </Button>
                </div>
              )}
            </>
          )}
        </Card>
      </main>
    </div>
  );
}
