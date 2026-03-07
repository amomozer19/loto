# Sistema de Registra de Apostas com Análise Inteligente

## 📋 Visão Geral

A nova funcionalidade **Registro de Apostas** permite que você registre as apostas que realizou, insira o resultado do sorteio e receba uma análise detalhada com recomendações inteligentes para futuras apostas.

## ✨ Funcionalidades Principais

### 1. **Registro de Apostas** (`/apostas`)
- Registre múltiplas apostas realizadas em um sorteio
- Cada aposta pode ter 7 a 15 números
- Inclua um nome/descrição para cada aposta
- Adicione raciocínio opcional explicando sua escolha
- Selecione os números que realmente saíram do sorteio

### 2. **Análise Automática** (`/apostas/analisar`)
O sistema verifica:
- ✅ Quantos números você acertou por aposta
- ✅ Padrões identificados (duplas, triplas, etc.)
- ✅ Se você "ganhou" (5+ acertos considerados como ganho)
- ✅ Score individual para cada aposta

### 3. **Agente Inteligente** (se não ganhou)
Quando você não atinge 5+ acertos, um agente analisa:

#### Padrões Não Identificados
- **Distribuição Par/Ímpar**: Identifica se há desequilíbrio
- **Números Sucessivos**: Detecta duplas ou triplas consecutivas
- **Frequências**: Analisa números mais comuns

#### Recomendações
- Variar entre números altos (13-25) e baixos (1-12)
- Considerar proporção par/ímpar
- Observar padrões de números consecutivos
- Analisar frequência de cada número

#### Números Recomendados
- Top 10 números com maior potencial
- Baseado em frequência histórica (2003-2026)
- Compatibilidade com números que saíram

### 4. **Integração com Página de Sorte**
Os números recomendados podem ser usados na página de Sorte, que oferece:
- 4 conjuntos de apostas automáticos
- Explicações para cada estratégia
- Níveis de confiança

## 📊 Como Usar

### Passo 1: Registrar Apostas
```
Navegue até o menu > Registrar Apostas
ou acesse direto: /apostas
```

**Completar:**
- ✓ Data da aposta
- ✓ Número do concurso
- ✓ Quantidade de apostas
- ✓ Para CADA aposta:
  - Nome/Descrição
  - Selecione 7-15 números
  - Raciocínio (opcional)
- ✓ Selecione os 15 números que saíram

### Passo 2: Enviar e Analisar
Clique em "Registrar e Analisar"

O sistema irá:
1. Validar os dados
2. Comparar apostas com resultado real
3. Calcular acertos
4. Gerar análise inteligente se necessário

### Passo 3: Ver Resultados
Você será redirecionado para a página de análise que mostra:

```
┌─────────────────────────────────────┐
│ Status Geral                         │
│ - Ganhou/Perdeu                      │
│ - Maior acerto                       │
│ - Melhor aposta                      │
│ - Score médio                        │
└─────────────────────────────────────┘
│ Números que Saíram                   │
│ [1] [2] [4] [5] [7] ...             │
└─────────────────────────────────────┘
│ Análise Detalhada por Aposta         │
│ Para CADA aposta:                   │
│ - Números apostados: [1][2][3]...   │
│ - Acertos: [1][2][4]                │
│ - Não acertados: [3][5]             │
│ - Estatísticas: 3/10 acertos        │
│ - Duplas/Triplas acertadas          │
└─────────────────────────────────────┘
```

### Passo 4: Análise Inteligente (se perdeu)
Se não ganhou (menos de 5 acertos):

```
╔═══════════════════════════════════════╗
║ ANÁLISE INTELIGENTE - POR QUE PERDEU? ║
╠═══════════════════════════════════════╣
║ ⚠️ Padrões Não Identificados:         ║
║  - Duplas Sucessivas: 35% freq.      ║
║  - Distribuição Par/Ímpar: 47%       ║
╠═══════════════════════════════════════╣
║ 💡 Recomendações:                    ║
║  ✓ Variar entre altos/baixos         ║
║  ✓ Considerar proporção par/ímpar    ║
║  ✓ Observar números consecutivos     ║
╠═══════════════════════════════════════╣
║ 📈 Números Recomendados:             ║
║  [23] (8.2% freq.)                   ║
║  [19] (7.9% freq.)                   ║
║  [15] (7.6% freq.)                   ║
║  ...com histórico de 1200+ sorteios  ║
╚═══════════════════════════════════════╝
```

## 🎯 Exemplos Práticos

### Exemplo 1: Ganhou
```
Apostas: 
- Aposta 1: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

Resultado: [1,2,4,5,7,8,10,11,13,14,15,16,17,18,19]

Acertos: 10/15 ✅ GANHOU!
Score: 85/100
```

### Exemplo 2: Perdeu (recebe recomendação)
```
Apostas:
- Aposta 1: [1,3,5,7,9,11,13,15,17,19,21,23,25] (7 números)

Resultado: [2,4,6,8,10,12,16,18,20,22,24,11,13,15,17]

Acertos: 4/13 (não ganhou)

Recomendação:
- Números faltando: Pares (2,4,6,8...)
- Distribuição: Muito desequilibrada
- Próximas apostas: incluir mais pares
- Top números: [2, 4, 6, 8, 10, 12, 16, 18, 20, 22]
```

## 📈 Integração com Sorte

Após registrar apostas, você pode:

1. Clicar em "Ver Recomendações da Sorte"
2. A página de Sorte mostrará 4 conjuntos recomendados
3. Cada conjunto segue uma estratégia diferente
4. Explicações baseadas no seu histórico

## 🔄 Fluxo Completo

```
┌─────────────────────┐
│ Página /apostas     │ Registra apostas
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│ POST /apostas/      │ Valida e analisa
│ analisar            │
└──────────┬──────────┘
           │
           ├─→ COM ACERTOS (5+) →─────────┐
           │                              ↓
           │                    ┌─────────────────────┐
           │                    │ Status: ✅ GANHOU!  │
           │                    │ Mostrar resultados  │
           │                    └─────────────────────┘
           │
           └─→ SEM ACERTOS (<5) ────┐
                                    ↓
                         ┌──────────────────────────────┐
                         │ Agente Inteligente          │
                         │ 1. Analisa padrões          │
                         │ 2. Gera recomendações       │
                         │ 3. Lista números top 10     │
                         │ 4. Calcula confiança        │
                         └──────────┬───────────────────┘
                                    ↓
                         ┌──────────────────────────────┐
                         │ /sorte usa recomendações    │
                         │ para gerar apostas           │
                         └──────────────────────────────┘
```

## 🛠️ Detalhes Técnicos

### Validação
- Data: Obrigatória, passada ou presente
- Concurso: Obrigatório, texto livre
- Apostas: 1-20 por sorteio
- Números por aposta: 7-15 (obrigatório)
- Resultado: Exatamente 15 números

### Algoritmo de Score
```
Score = (Acertos × 12) + (Duplas × 3) + (Triplas × 5)
Máximo: 100 (normalizado)
```

### Análise de Padrões
```
1. Duplas Sucessivas: +1 se números X,X+1 aparecem
2. Par/Ímpar: Conta proporção e compara com 50%
3. Números Altos/Baixos: 1-12 vs 13-25
4. Frequência: Baseada em 2000+ sorteios históricos
```

### Confiança da Recomendação
```
Muito Alta (80+): Muitos acertos passados + histórico largo
Alta (60-79):     Alguns acertos ou bom histórico
Média (40-59):    Pouco histórico mas consistente
Baixa (<40):      Primeiro registro ou histórico pequeno
```

## 📝 Campos do Form

| Campo | Tipo | Min | Max | Obrigatório | Descrição |
|-------|------|-----|-----|-------------|-----------|
| Data da Aposta | date | - | - | ✅ | Quando você apostou |
| Concurso | text | 1 | 20 | ✅ | ID do concurso |
| Quantidade | number | 1 | 20 | ✅ | Quantas apostas |
| Nome Aposta | text | - | - | ✅ | Ex: "Pares", "Sorte do Dia" |
| Números | checkbox | 7 | 15 | ✅ | Seleção múltipla (1-25) |
| Raciocínio | textarea | - | - | ❌ | Por que escolheu |
| Resultado | checkbox | 15 | 15 | ✅ | Números que saíram |

## 🔐 Segurança

- ✅ Autenticação obrigatória
- ✅ Dados salvos em sessão (não persistidos)
- ✅ Validação completa de entrada
- ✅ Sanitização de dados

## 📊 Dados Históricos

- Base de dados: **2000+ sorteios**
- Período: **2003-2026**
- Números: **1-25 (15 por sorteio)**
- Frequências calculadas em tempo real

## 🎓 Dicas

1. **Primeira Aposta**: O sistema aprende com seus registros
2. **Múltiplas Estratégias**: Use diferentes "nomes" para diferentes abordagens
3. **Raciocínio**: Deixar anotado ajuda a entender padrões depois
4. **Revisar**: Compare resultados anteriores com recomendações
5. **Combinar com Sorte**: Use tanto a página de Sorte quanto seu histórico

## 🚀 Próximas Melhorias

- [ ] Gráficos de acertos ao longo do tempo
- [ ] Comparação de estratégias
- [ ] Exportar relatórios em PDF
- [ ] Previsões machine learning
- [ ] Comunidade compartilhamento de estratégias

---

**Versão**: 1.0  
**Data**: Março 2026  
**Status**: ✅ Funcional
