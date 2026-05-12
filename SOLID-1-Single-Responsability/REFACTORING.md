# Refatoração SOLID - Single Responsibility Principle

## 📋 Resumo das Mudanças

O código foi refatorado para seguir o **Single Responsibility Principle (SRP)**, onde cada classe tem uma única razão para mudar.

---

## 🏗️ Arquitetura Anterior (Violando SRP)

**Problema:** Uma única classe/função tinha múltiplas responsabilidades:

```
ConnectionCategoriaDataBase.connectar()
├── Conectar ao banco dados
├── Executar queries SQL
├── Validar dados
├── Renderizar HTML
└── Gerenciar transações
```

```
views.produtos()
├── Conectar ao banco dados
├── Executar queries SQL
├── Validar dados
├── Renderizar HTML
└── Gerenciar transações
```

---

## ✅ Arquitetura Nova (Seguindo SRP)

Cada arquivo tem uma responsabilidade única:

### 1️⃣ **repositories.py** - Camada de Data Access
- **Responsabilidade única:** Acessar e manipular dados do banco
- **Classes:**
  - `DatabaseRepository`: Gerencia conexão com BD
  - `CategoriaRepository`: CRUD de Categorias
  - `ProdutoRepository`: CRUD de Produtos

```python
class CategoriaRepository(DatabaseRepository):
    def listar(self)
    def obter_por_id(id)
    def incluir(descricao)
    def alterar(id, descricao)
    def excluir(id)
```

### 2️⃣ **services.py** - Camada de Lógica de Negócio
- **Responsabilidade única:** Implementar regras de negócio
- **Classes:**
  - `CategoriaService`: Lógica de Categoria
  - `ProdutoService`: Lógica de Produto

```python
class CategoriaService:
    def criar_categoria(descricao):
        # Valida descrição
        # Chama repository.incluir()
    
    def deletar_categoria(id):
        # Valida existência
        # Chama repository.excluir()
```

**Benefícios:**
- ✅ Validações de negócio centralizadas
- ✅ Fácil de testar
- ✅ Reutilizável em outras views/APIs

### 3️⃣ **forms.py** - Camada de Formulários
- **Responsabilidade única:** Definir estrutura de formulários Django
- **Classes:**
  - `CategoriaForm`: Formulário de Categoria
  - `ProdutoForm`: Formulário de Produto

```python
class CategoriaForm(forms.Form):
    id = forms.IntegerField(...)
    descricao = forms.CharField(...)
```

### 4️⃣ **views.py** - Camada de Apresentação
- **Responsabilidade única:** Receber requisições HTTP e retornar respostas
- **Funções:**
  - `categorias()`: Gerencia rotas de Categoria
  - `produtos()`: Gerencia rotas de Produto
  - `home()`: Página inicial

```python
def categorias(request, acao=None, id=None):
    service = CategoriaService()
    
    if acao is None:
        registros = service.listar_categorias()
        return render(request, 'categorias_listar.html', ...)
```

### 5️⃣ **connection.py** - Compatibilidade
- Mantido apenas para compatibilidade com código existente
- Delega chamadas para `views.categorias()`

---

## 🔄 Fluxo de Dados

```
HTTP Request
    ↓
views.py (Recebe requisição)
    ↓
services.py (Aplica lógica de negócio)
    ↓
repositories.py (Acessa banco de dados)
    ↓
SQLite Database
    ↓
repositories.py (Retorna dados)
    ↓
services.py (Processa dados)
    ↓
views.py (Renderiza HTML)
    ↓
HTTP Response
```

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|--------|-------|--------|
| **Responsabilidades por função** | 5+ | 1 |
| **Connection ao BD** | Dentro da view | Repository |
| **Validações** | Na view | Service |
| **Queries SQL** | Na view | Repository |
| **Renderização** | Na view | View |
| **Testabilidade** | Difícil | Fácil |
| **Reusabilidade** | Baixa | Alta |

---

## 🧪 Exemplos de Uso

### Criar Categoria (Antes)
```python
sql = f"INSERT INTO Categoria(descricao) VALUES('{descricao}')"
conexao.cursor().execute(sql)
conexao.commit()
```

### Criar Categoria (Depois)
```python
service = CategoriaService()
service.criar_categoria(descricao="Eletrônicos")
```

---

## 🎯 Benefícios da Refatoração

1. ✅ **Manutenibilidade:** Mudanças em um lugar não afetam outras
2. ✅ **Testabilidade:** Fácil escrever testes unitários
3. ✅ **Reutilização:** Services podem ser usados em APIs, CLIs, etc.
4. ✅ **Clareza:** Cada arquivo tem um propósito claro
5. ✅ **Escalabilidade:** Fácil adicionar novas funcionalidades

---

## 📝 Próximos Passos (Sugestões)

- [ ] Adicionar testes unitários para `repositories.py`
- [ ] Adicionar testes para `services.py`
- [ ] Implementar SQL parameterizado (contra SQL injection)
- [ ] Adicionar logging
- [ ] Considerar usar ORM (Django Models/SQLAlchemy)

---

## 📚 Referências SOLID

**S**ingle Responsibility Principle - Uma classe, uma responsabilidade
**O**pen/Closed Principle - Aberto para extensão, fechado para modificação
**L**iskov Substitution Principle - Subclasses devem ser substituíveis
**I**nterface Segregation Principle - Interfaces específicas ao cliente
**D**ependency Inversion Principle - Depender de abstrações, não de implementações
