from app.repositories import CategoriaRepository, ProdutoRepository


class CategoriaService:
    """Responsável APENAS pela lógica de negócio de Categorias"""
    
    def __init__(self):
        self.repository = CategoriaRepository()
    
    def listar_categorias(self):
        """Retorna lista de categorias"""
        return self.repository.listar()
    
    def obter_categoria(self, id: int):
        """Obtém uma categoria pelo ID"""
        categoria = self.repository.obter_por_id(id)
        if not categoria:
            raise ValueError(f"Categoria com ID {id} não encontrada")
        return categoria
    
    def criar_categoria(self, descricao: str):
        """Cria uma nova categoria com validações"""
        if not descricao or len(descricao.strip()) == 0:
            raise ValueError("Descrição não pode estar vazia")
        
        self.repository.incluir(descricao)
    
    def atualizar_categoria(self, id: int, descricao: str):
        """Atualiza uma categoria com validações"""
        categoria = self.repository.obter_por_id(id)
        if not categoria:
            raise ValueError(f"Categoria com ID {id} não encontrada")
        
        if not descricao or len(descricao.strip()) == 0:
            raise ValueError("Descrição não pode estar vazia")
        
        self.repository.alterar(id, descricao)
    
    def deletar_categoria(self, id: int):
        """Deleta uma categoria com validações"""
        categoria = self.repository.obter_por_id(id)
        if not categoria:
            raise ValueError(f"Categoria com ID {id} não encontrada")
        
        self.repository.excluir(id)


class ProdutoService:
    """Responsável APENAS pela lógica de negócio de Produtos"""
    
    def __init__(self):
        self.repository = ProdutoRepository()
        self.categoria_service = CategoriaService()
    
    def listar_produtos(self):
        """Retorna lista de produtos"""
        return self.repository.listar()
    
    def obter_produto(self, id: int):
        """Obtém um produto pelo ID"""
        produto = self.repository.obter_por_id(id)
        if not produto:
            raise ValueError(f"Produto com ID {id} não encontrado")
        return produto
    
    def criar_produto(self, descricao: str, preco_unitario: float, 
                     quantidade_estoque: int, categoria_id: int):
        """Cria um novo produto com validações"""
        # Valida descrição
        if not descricao or len(descricao.strip()) == 0:
            raise ValueError("Descrição não pode estar vazia")
        
        # Valida preço
        if preco_unitario < 0:
            raise ValueError("Preço não pode ser negativo")
        
        # Valida quantidade
        if quantidade_estoque < 0:
            raise ValueError("Quantidade não pode ser negativa")
        
        # Valida se categoria existe
        self.categoria_service.obter_categoria(categoria_id)
        
        self.repository.incluir(descricao, preco_unitario, quantidade_estoque, categoria_id)
    
    def atualizar_produto(self, id: int, descricao: str, preco_unitario: float,
                         quantidade_estoque: int, categoria_id: int):
        """Atualiza um produto com validações"""
        # Valida se produto existe
        produto = self.repository.obter_por_id(id)
        if not produto:
            raise ValueError(f"Produto com ID {id} não encontrado")
        
        # Valida descrição
        if not descricao or len(descricao.strip()) == 0:
            raise ValueError("Descrição não pode estar vazia")
        
        # Valida preço
        if preco_unitario < 0:
            raise ValueError("Preço não pode ser negativo")
        
        # Valida quantidade
        if quantidade_estoque < 0:
            raise ValueError("Quantidade não pode ser negativa")
        
        # Valida se categoria existe
        self.categoria_service.obter_categoria(categoria_id)
        
        self.repository.alterar(id, descricao, preco_unitario, quantidade_estoque, categoria_id)
    
    def deletar_produto(self, id: int):
        """Deleta um produto com validações"""
        produto = self.repository.obter_por_id(id)
        if not produto:
            raise ValueError(f"Produto com ID {id} não encontrado")
        
        self.repository.excluir(id)
