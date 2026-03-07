# 🏛️ Arquitetura e Design Patterns

Documentação técnica sobre a arquitetura e padrões de design implementados no projeto Loto.

## 📐 Padrões de Design Implementados

### 1. MVC (Model-View-Controller)

**Definição**: Separação da aplicação em três componentes interconectados.

**Implementação no Loto**:
```
Models     → app/models/          (Estrutura de dados e lógica de domínio)
Views      → app/templates/       (Templates HTML para apresentação)
Controllers→ app/routes/          (Blueprints Flask - lógica de requisições)
```

**Benefícios**:
- ✅ Separação clara de responsabilidades
- ✅ Fácil manutenção e testes
- ✅ Escalabilidade
- ✅ Reutilização de código

---

### 2. Factory Pattern

**Definição**: Cria instâncias sem especificar as classes exactas.

**Implementação**:
```python
# app/__init__.py
def create_app():
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configuração
    app.config['SECRET_KEY'] = 'seu_secret_key_aqui'
    
    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(stats_bp)
    
    return app
```

**Vantagens**:
- ✅ Centraliza criação da aplicação
- ✅ Facilita testes
- ✅ Permite múltiplas instâncias
- ✅ Configuração flexível

**Uso**:
```python
# run.py
app = create_app()
app.run(debug=True)
```

---

### 3. Blueprint Pattern (Modularização)

**Definição**: Organiza rotas em módulos reutilizáveis.

**Implementação**:
```python
# app/routes/main.py
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# app/routes/estadisticas.py
stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/estatisticas')
def estatisticas():
    return render_template('estatisticas.html')
```

**Benefícios**:
- ✅ Código organizado por funcionalidade
- ✅ Fácil adicionar novas rotas
- ✅ Evita conflitos de nomes
- ✅ Escalável para aplicações maiores

---

### 4. Service Layer Pattern

**Definição**: Isola lógica de negócio em serviços reutilizáveis.

**Implementação**:
```
app/utils/
  ├── csv_handler.py       (Serviço de persistência)
  ├── validators.py        (Serviço de validação)
  └── stats_calculator.py  (Serviço de cálculos)
```

**Exemplo - csv_handler.py**:
```python
class CSVHandler:
    """Responsável apenas por I/O de dados"""
    
    def carregar_dados(self):
        # Lógica de leitura
        
    def salvar_dados(self, data):
        # Lógica de escrita
```

**Benefícios**:
- ✅ Lógica reutilizável
- ✅ Testável independentemente
- ✅ Sem dependências Flask
- ✅ Fácil de mockar em testes

---

### 5. Separation of Concerns

**Definição**: Cada módulo tem apenas uma responsabilidade.

**Implementação**:

| Arquivo | Responsabilidade |
|---------|-----------------|
| `csv_handler.py` | Ler/escrever CSV |
| `validators.py` | Validar entrada |
| `stats_calculator.py` | Calcular estatísticas |
| `routes/main.py` | Processar requisições HTTP |
| `routes/estadisticas.py` | Servir página de análises |
| `templates/` | Renderizar HTML |

**Exemplo de fluxo**:
```
Requisição HTTP
    ↓
routes/main.py (Processa requisição)
    ↓
validators.py (Valida dados)
    ↓
csv_handler.py (Salva dados)
    ↓
Resposta HTTP
```

---

## 🗂️ Estrutura de Diretórios

```
Loto/
├── run.py                    # Entry point
├── requirements.txt          # Dependências
├── README.md                 # Documentação principal
├── ARCHITECTURE.md           # Este arquivo
├── .gitignore               # Configuração Git
│
└── app/                     # Pacote principal
    ├── __init__.py          # Factory application
    │
    ├── models/              # Modelos de dados
    │   └── __init__.py
    │
    ├── routes/              # Controllers (Blueprints)
    │   ├── __init__.py
    │   ├── main.py          # Rotas principais
    │   └── estadisticas.py  # Rotas de análises
    │
    ├── utils/               # Services (Lógica de negócio)
    │   ├── __init__.py
    │   ├── csv_handler.py   # I/O de dados
    │   ├── validators.py    # Validações
    │   └── stats_calculator.py  # Cálculos
    │
    ├── static/              # Arquivos estáticos
    │   └── (CSS, JS, imagens)
    │
    └── templates/           # Views (HTML)
        ├── index.html
        ├── novo.html
        └── estatisticas.html
```

---

## 🔄 Fluxo de uma Requisição

### Exemplo: Salvar novo sorteio

```
1. Cliente (Navegador)
   └─→ POST /api/salvar {id, data, numeros}
   
2. routes/main.py (@main_bp.route('/api/salvar'))
   └─→ Extrai dados do request JSON
   
3. validators.py (SorteioValidator.validar_numeros())
   └─→ Valida se números estão corretos
   
4. csv_handler.py (CSVHandler.salvar_dados())
   └─→ Escreve no arquivo CSV
   
5. routes/main.py
   └─→ Retorna JSON response com sucesso
   
6. Cliente
   └─→ Recebe resposta e redireciona para home
```

---

## 🧪 Como Testar

Cada camada pode ser testada independentemente:

### Tester CSVHandler
```python
from app.utils.csv_handler import CSVHandler

handler = CSVHandler('dados_teste.csv')
dados = handler.carregar_dados()
assert len(dados) > 0
```

### Testar Validador
```python
from app.utils.validators import SorteioValidator

valido, msg = SorteioValidator.validar_numeros([1, 2, 3, ..., 15])
assert valido == True
```

### Testar Rotas
```python
from app import create_app

app = create_app()
client = app.test_client()

response = client.get('/')
assert response.status_code == 200
```

---

## 📝 Boas Práticas Implementadas

### 1. Single Responsibility Principle (SRP)
Cada classe tem apenas uma razão para mudar:
- `CSVHandler` muda se formato de arquivo mudar
- `SorteioValidator` muda se regras de validação mudarem
- `StatsCalculator` muda se fórmulas estatísticas mudarem

### 2. Open/Closed Principle (OCP)
Aberto para extensão, fechado para modificação:
```python
# Fácil adicionar novo validador
class NovoValidador(SorteioValidator):
    @staticmethod
    def validar_novo_campo():
        pass
```

### 3. Dependency Inversion
Depende de abstrações, não de implementações concretas:
```python
# Ao invés de:
csv = CSVHandler()  # Concreto

# Melhor (poderia ser):
class DataStore(ABC):  # Abstrato
    @abstractmethod
    def carregar(self): pass
```

### 4. Type Hints
Melhor documentação e erros mais cedo:
```python
def validar_numeros(numeros: List[str]) -> Tuple[bool, str]:
    # Type hints melhoram IDE autocomplete e detecção de erros
    pass
```

---

## 🚀 Escalabilidade Futura

Esta arquitetura facilita:

### 1. Adicionar Banco de Dados
```python
# app/models/sorteio.py
class Sorteio(db.Model):
    id = db.Column(db.String, primary_key=True)
    data = db.Column(db.Date)
    numeros = db.Column(db.String)  # JSON ou array
```

Depois apenas trocar `csv_handler.py` por um `db_handler.py`.

### 2. Adicionar API REST
```python
# app/routes/api.py
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/sorteios', methods=['GET'])
def listar_sorteios():
    return jsonify(dados)
```

### 3. Adicionar Autenticação
```python
# app/utils/auth.py
class AuthService:
    @staticmethod
    def verificar_token(token):
        pass
```

### 4. Adicionar Cache
```python
# Em csv_handler.py
from functools import lru_cache

@lru_cache(maxsize=128)
def carregar_dados(self):
    pass
```

---

## 📊 Diagrama de Dependências

```
┌─ routes/main.py
│  ├─ utils/validators.py
│  ├─ utils/csv_handler.py
│  └─ templates/
│
├─ routes/estadisticas.py
│  ├─ utils/csv_handler.py
│  ├─ utils/stats_calculator.py
│  └─ templates/
│
app/__init__.py
└─ routes/main.py
└─ routes/estadisticas.py
```

No há dependências circulares! ✅

---

## 🔐 Segurança

Aplicadas as seguintes medidas:

1. **Input Validation**: Todos os inputs são validados
2. **Type Safety**: Type hints ajudam a prevenir bugs
3. **Separation**: Lógica separada de apresentação
4. **Error Handling**: Tratamento de exceções em todas as camadas

---

## 📚 Referências

- [Python Design Patterns](https://refactoring.guru/design-patterns/python)
- [Flask Best Practices](https://flask.palletsprojects.com/patterns/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/)

---

**Versão 1.0** - 2026  
**Última atualização**: Março 2026
