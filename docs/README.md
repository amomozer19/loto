# 🎰 Aplicação Loto

Uma aplicação web moderna para gerenciar sorteios de números usando Flask e Bootstrap com arquitetura MVC profissional.

## ✨ Características

- 🔐 **Autenticação Segura** - Email + Token com persistência em CSV
- 🎨 Interface moderna com Bootstrap 5
- 🏛️ Arquitetura MVC escalável e profissional
- 🎲 Geração automática de números aleatórios (1-25)
- ✅ Validação robusta em tempo real
- 📊 Histórico de sorteios com tabela interativa
- 📈 Estatísticas detalhadas por dia da semana
- 💾 Armazenamento em arquivo CSV
- 📱 Design responsivo (funciona em desktop e mobile)
- ⚡ Performance otimizada

## 📁 Estrutura do Projeto (Design Patterns)

```
Loto/
├── run.py                          # Entry point da aplicação
├── requirements.txt                # Dependências do projeto
├── README.md                       # Este arquivo
├── .gitignore                      # Configuração git
├── dados_loto.csv                  # Arquivo de dados CSV
│
└── app/                            # Pacote principal
    ├── __init__.py                 # Factory do Flask
    │
    ├── models/                     # Modelos de dados
    │   └── __init__.py
    │
    ├── routes/                     # Blueprints de rotas (Controllers)
    │   ├── __init__.py
    │   ├── main.py                 # Rotas principais
    │   └── estadisticas.py         # Rotas de estatísticas
    │
    ├── utils/                      # Serviços e utilidades
    │   ├── __init__.py
    │   ├── csv_handler.py          # Manipulação de dados CSV
    │   ├── validators.py           # Validadores de entrada
    │   └── stats_calculator.py     # Calculadora de estatísticas
    │
    ├── static/                     # Arquivos estáticos
    │   └── (Bootstrap via CDN)
    │
    └── templates/                  # Templates HTML (Views)
        ├── index.html              # Página inicial
        ├── novo.html               # Novo sorteio
        └── estatisticas.html       # Estatísticas
```

## 🎯 Design Patterns Implementados

### **1. MVC (Model-View-Controller)**
- **Models** (`app/models/`): Estrutura de dados
- **Views** (`app/templates/`): Templates HTML Jinja2
- **Controllers** (`app/routes/`): Blueprints Flask

### **2. Blueprints Flask**
Organização modular com blueprints separados:
- `main_bp`: Funcionalidades principais
- `stats_bp`: Estatísticas

### **3. Separation of Concerns**
Cada módulo tem responsabilidade única:
- **csv_handler.py**: I/O de dados
- **validators.py**: Validação de entrada
- **stats_calculator.py**: Cálculos e análises
- **routes**: Apenas lógica HTTP

### **4. Factory Pattern**
`app/__init__.py` usa factory para criar a aplicação Flask:
```python
def create_app():
    app = Flask(__name__)
    # Registrar blueprints
    return app
```

### **5. Service Layer**
Lógica de negócio isolada em serviços:
- Reutilizável em diferentes contextos
- Sem dependências com Flask

## � Autenticação e Segurança

### Sistema de Autenticação Completo
A aplicação agora possui uma camada robusta de segurança:

**Características**:
- ✅ Email + Token seguro (criptográfico)
- ✅ Persistência em CSV (`dados_usuarios.csv`)
- ✅ Tokens com expiração automática (24h)
- ✅ Sessões HttpOnly + CSRF protection
- ✅ Rotas protegidas com decorator `@requer_autenticacao`

**Fluxo**:
```
1. Usuário: /auth/login → Insere email
2. Sistema: Gera token seguro → Salva em auth_tokens.log
3. Usuário: /auth/verificar → Insere código recebido
4. Sistema: Verifica token → Cria sessão → Acesso liberado
5. Resultado: Acesso às rotas protegidas (/, /novo, /estatisticas)
```

**APIs RESTful**:
- `POST /auth/api/solicitar-token` - Solicitar token
- `POST /auth/api/verificar-token` - Autenticar com token
- `GET /auth/api/status` - Verificar autenticação
- `POST /auth/api/logout` - Fazer logout

**Classes principais**:
- `AuthHandler`: Gerencia autenticação
- `UserManager`: Persistência em CSV
- `EmailService`: Envio de tokens (log em dev)
- `@requer_autenticacao`: Proteção de rotas

**Documentação**: Ver [AUTH_IMPLEMENTATION.md](AUTH_IMPLEMENTATION.md) e [QUICK_START_AUTH.md](QUICK_START_AUTH.md)

## �📚 Módulos Detalhados

### `app/utils/csv_handler.py`
Gerencia I/O de dados CSV:
```python
handler = CSVHandler()
dados = handler.carregar_dados()          # Carrega arquivo
handler.salvar_dados(id, data, numeros)   # Salva novo registro
proximo_id = handler.obter_proximo_id()   # Calcula próximo ID
```

### `app/utils/validators.py`
Valida dados de entrada:
```python
validator = SorteioValidator()
SorteioValidator.validar_numeros([números])  # Valida lista
SorteioValidator.validar_id(id)              # Valida ID
SorteioValidator.validar_data(data)          # Valida data
```

### `app/utils/stats_calculator.py`
Calcula estatísticas:
```python
calc = StatsCalculator()
stats_dia = calc.calcular_estatisticas_por_dia(dados)
stats_globais = calc.calcular_estatisticas_globais(dados)
```

### `app/routes/main.py`
Rotas principais:
- `GET /` - Página inicial
- `GET /novo` - Formulário
- `GET /api/gerar_numeros` - Gera números
- `POST /api/validar` - Valida dados
- `POST /api/salvar` - Salva sorteio

### `app/routes/estadisticas.py`
Rotas de análises:
- `GET /estatisticas` - Página com análises

## 🚀 Como Executar

### 1. Instalar dependências
```powershell
cd "c:\Users\SAMSUNG\OneDrive\Meus Documentos\Python Projects\Loto"
pip install -r requirements.txt
```

### 2. Executar a aplicação
```powershell
python run.py
```

### 3. Acessar no navegador
```
http://localhost:5000
```

## 📖 Funcionalidades

### Página Inicial
- Últimos 20 sorteios em tabela
- Estatísticas rápidas
- Botão para novo sorteio
- Link para estatísticas detalhadas

### Novo Sorteio
- ID gerado automaticamente
- Seleção de data
- 15 campos para números (1-25)
- Botão gerar aleatoriamente
- Validação antes de salvar

### Estatísticas
- Análise por dia da semana
- Números top 10
- Números nunca sorteados
- Média, mediana, desvio padrão
- Média ponderada
- Heatmap de probabilidades
- Estatísticas globais

## 🔌 Como Adicionar Nova Rota

1. Criar arquivo em `app/routes/nova_funcao.py`:
```python
from flask import Blueprint

nova_bp = Blueprint('nova', __name__)

@nova_bp.route('/nova-pagina')
def nova_pagina():
    return render_template('nova_pagina.html')
```

2. Atualizar `app/routes/__init__.py`:
```python
from app.routes.nova_funcao import nova_bp
__all__ = ['main_bp', 'stats_bp', 'nova_bp']
```

3. Registrar em `app/__init__.py`:
```python
app.register_blueprint(nova_bp)
```

## 🔧 Como Adicionar Novo Serviço

1. Criar arquivo em `app/utils/novo_servico.py`:
```python
class NovoServico:
    @staticmethod
    def metodo_importante():
        return "resultado"
```

2. Usar em rotas:
```python
from app.utils.novo_servico import NovoServico
resultado = NovoServico.metodo_importante()
```

## 📊 Estatísticas Disponíveis

Para cada dia da semana:
- Total de sorteios
- Números sorteados
- Números nunca sorteados
- Média
- Mediana
- Desvio padrão
- Mínimo/Máximo
- Média ponderada
- Top 10 números mais frequentes
- Probabilidade de cada número (1-25)
- Heatmap visual de probabilidades

Globais:
- Total de sorteios
- Primeiro e último sorteio
- Números mais/menos frequentes
- Total de números únicos

## 🐛 Troubleshooting

### Porta 5000 em uso
Edite `run.py`:
```python
app.run(debug=True, port=5001)
```

### Erro de importação
Certifique-se de estar no diretório raiz do Loto e que `PYTHONPATH` está correto.

### Arquivo CSV corrompido
Delete `dados_loto.csv` e execute novamente.

## 📝 Notas

- Dados em CSV com separador `;`
- Próximo ID calculado automaticamente
- Bootstrap via CDN (sem dependências de CSS local)
- Sem banco de dados (apenas CSV)
- Estrutura escalável para adicionar banco de dados no futuro

## 📦 Dependências

- Flask 2.3.3
- Werkzeug 2.3.7

## 🎓 Conceitos Implementados

- ✅ MVC Pattern
- ✅ Blueprints (módulos)
- ✅ Factory Pattern
- ✅ Service Layer
- ✅ Separation of Concerns
- ✅ Validação em camadas
- ✅ Type hints
- ✅ Documentação inline

## 🚀 Próximos Passos (Sugestões)

1. Adicionar banco de dados (SQLAlchemy)
2. Testes unitários e integração
3. Autenticação de usuários
4. API REST com documentação Swagger
5. Dashboard com gráficos interativos
6. Exportação de relatórios em PDF

---

**Versão 2.0** - 2026  
**Arquitetura**: MVC com Blueprints  
**Pattern**: Factory + Service Layer  
**Status**: Production Ready
