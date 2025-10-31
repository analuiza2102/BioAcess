"""Rotas de acesso a dados por nível de clearance"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import User
from ..security import require_level
from ..services.audit import log_action

router = APIRouter(prefix="/data", tags=["dados"])


@router.get("/level/{level}")
async def get_level_data(
    request: Request,
    level: int,
    user: User = Depends(require_level(1)),  # mínimo nível 1 para estar autenticado
    db: Session = Depends(get_db)
):
    """
    Retorna dados de um nível específico de clearance.
    
    O usuário deve ter clearance >= level solicitado.
    
    Args:
        level: Nível solicitado (1, 2 ou 3)
    
    Returns:
        - level: int
        - data: dict com título, conteúdo e itens
        - message: str
    """
    if level < 1 or level > 3:
        raise HTTPException(status_code=400, detail="Nível inválido")
    
    # Verifica se usuário tem clearance suficiente
    if user.clearance < level:
        log_action(
            db, user.username, f"access_level_{level}", False,
            level_requested=level,
            origin_ip=request.client.host if request.client else None
        )
        raise HTTPException(status_code=403, detail="Clearance insuficiente")
    
    # Dados sobre agrotóxicos proibidos por nível de clearance
    # Em produção, estes viriam de diferentes tabelas/schemas do banco
    data_by_level = {
        1: {
            "title": "Nível 1 - Dados Públicos sobre Agrotóxicos",
            "content": "Informações gerais e estatísticas sobre agrotóxicos proibidos no Brasil.",
            "summary": {
                "total_propriedades_monitoradas": 15420,
                "agrotoxicos_proibidos_detectados": 47,
                "percentual_conformidade": "95.2%",
                "regioes_afetadas": ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
            },
            "items": [
                "📊 Total de propriedades monitoradas: 15.420",
                "⚠️ Agrotóxicos proibidos detectados: 47 substâncias",
                "✅ Percentual de conformidade: 95.2%",
                "🏛️ Total de multas aplicadas: 892 (R$ 45.2 milhões)",
                "🌍 Regiões com detecções: Norte, Nordeste, Centro-Oeste, Sudeste, Sul",
                "💧 Lençóis freáticos contaminados: 12 regiões",
                "🏞️ Rios com resíduos detectados: 28 bacias hidrográficas",
                "🌊 Áreas marinhas afetadas: 5 zonas costeiras"
            ],
            "agrotoxicos_principais": [
                "Paraquat (proibido desde 2020) - Neurotoxicidade extrema",
                "Carbofurano (alta toxicidade) - Mortalidade de abelhas e aves",
                "Metamidofós (neurotóxico) - Contaminação de lençóis freáticos",
                "Endosulfan (persistente) - Bioacumulação em peixes"
            ]
        },
        2: {
            "title": "Nível 2 - Relatórios Regionais Detalhados",
            "content": "Dados específicos de propriedades infratoras e análises regionais para diretores de divisões.",
            "propriedades_infratoras": [
                {
                    "codigo": "BR-GO-001547",
                    "nome": "Fazenda São Miguel",
                    "municipio": "Rio Verde - GO",
                    "area_hectares": 2850,
                    "agrotoxicos": ["Paraquat - 15.2 mg/L", "Status: Em tramitação"],
                    "multa": "R$ 850.000",
                    "prazo": "2024-12-30"
                },
                {
                    "codigo": "BR-MT-002341", 
                    "nome": "Agropecuária Cerrado Verde",
                    "municipio": "Sorriso - MT",
                    "area_hectares": 4200,
                    "agrotoxicos": ["Carbofurano - 8.7 mg/L", "Status: Recurso interposto"],
                    "multa": "R$ 1.200.000",
                    "prazo": "2025-01-15"
                }
            ],
            "items": [
                "🏭 Propriedades infratoras identificadas: 67 casos ativos",
                "🧪 Análises laboratoriais realizadas: 1.247 amostras",
                "⚖️ Processos administrativos em andamento: 89",
                "💰 Valor total de multas aplicadas: R$ 28.4 milhões",
                "🔍 Centro-Oeste: 67 infrações (maior incidência)",
                "🌿 Substâncias mais frequentes: Paraquat, 2,4-D, Glifosato irregulares",
                "💧 Impacto hídrico: Moderado a Alto em 15 bacias",
                "📈 Recomendação: Intensificar fiscalização em Rio Verde-GO"
            ],
            "regioes_criticas": [
                "Rio Verde-GO: 23 propriedades infratoras",
                "Sorriso-MT: 18 casos de Carbofurano",
                "Barreiras-BA: 15 detecções de Paraquat",
                "Sinop-MT: 12 casos de contaminação hídrica"
            ]
        },
        3: {
            "title": "Nível 3 - Informações Estratégicas Confidenciais",
            "content": "Dados sigilosos sobre operações especiais, inteligência ambiental e estratégias governamentais.",
            "operacoes_ativas": [
                {
                    "nome": "Operação Águas Limpas",
                    "codigo": "OAL-2024-07",
                    "status": "EM EXECUÇÃO",
                    "coordenador": "Dr. Roberto Mendes (PF)",
                    "prazo": "2024-11-30",
                    "resultados": "18 mandados cumpridos, 7 prisões, R$ 15.8M em multas"
                }
            ],
            "items": [
                "🕵️ Operação Águas Limpas: 18/23 mandados cumpridos",
                "🚔 Prisões efetuadas: 7 pessoas (tráfico de agrotóxicos)",
                "📦 Produtos apreendidos: 12 toneladas de agrotóxicos proibidos",
                "💰 Multas aplicadas na operação: R$ 15.8 milhões",
                "🏭 Distribuidora Agrícola SP Ltda: INVESTIGAÇÃO CRÍTICA",
                "🛣️ Rota de contrabando: Paraguai → MS/MT/GO/SP (500 ton/ano)",
                "🎯 Projeto Sentinela: Monitoramento por satélite (RESERVADO)",
                "🌍 Meta nacional 2025: Redução de 30% no uso de agrotóxicos proibidos",
                "💵 Investimento em tecnologia limpa: R$ 2.1 bilhões aprovados",
                "🤝 Parcerias internacionais: FAO, UNEP, Banco Mundial"
            ],
            "inteligencia": {
                "fornecedores_irregulares": "7 empresas sob investigação da PF",
                "rotas_contrabando": "Fronteira paraguaia - volume: 500 ton/ano",
                "prejuizo_estimado": "R$ 80 milhões/ano",
                "custo_remediacao": "R$ 890 milhões (estimativa 5 anos)"
            },
            "classificacao": "RESTRITO - ACESSO MINISTRO EXCLUSIVO"
        }
    }
    
    # Registra acesso bem-sucedido no log
    log_action(
        db, user.username, f"access_level_{level}", True,
        level_requested=level,
        origin_ip=request.client.host if request.client else None
    )
    
    return {
        "level": level,
        "data": data_by_level[level],
        "message": "Acesso concedido"
    }
