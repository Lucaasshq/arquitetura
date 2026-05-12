import sqlite3


class DatabaseRepository:
    """Responsável APENAS por conectar ao banco de dados"""
    
    def __init__(self, db_path: str = 'db_solid.sqlite3'):
        self.db_path = db_path
    
    def get_connection(self):
        """Retorna uma conexão ativa com o banco"""
        conexao = sqlite3.connect(self.db_path)
        conexao.execute("PRAGMA foreign_keys = ON;")
        return conexao


class CategoriaRepository(DatabaseRepository):
    """Responsável APENAS por operações de acesso aos dados de Categoria"""
    
    def listar(self):
        """Lista todas as categorias"""
        conexao = self.get_connection()
        sql = 'SELECT id, descricao FROM Categoria ORDER BY descricao'
        registros = conexao.cursor().execute(sql).fetchall()
        conexao.close()
        return registros
    
    def obter_por_id(self, id: int):
        """Obtém uma categoria específica pelo ID"""
        conexao = self.get_connection()
        sql = f'SELECT id, descricao FROM Categoria WHERE id={id}'
        registro = conexao.cursor().execute(sql).fetchone()
        conexao.close()
        return registro
    
    def incluir(self, descricao: str):
        """Insere uma nova categoria"""
        conexao = self.get_connection()
        sql = f"INSERT INTO Categoria(descricao) VALUES('{descricao}')"
        conexao.cursor().execute(sql)
        conexao.commit()
        conexao.close()
    
    def alterar(self, id: int, descricao: str):
        """Altera uma categoria existente"""
        conexao = self.get_connection()
        sql = f"UPDATE Categoria SET descricao = '{descricao}' WHERE id = {id}"
        conexao.cursor().execute(sql)
        conexao.commit()
        conexao.close()
    
    def excluir(self, id: int):
        """Deleta uma categoria"""
        conexao = self.get_connection()
        sql = f"DELETE FROM Categoria WHERE id = {id}"
        conexao.cursor().execute(sql)
        conexao.commit()
        conexao.close()


class ProdutoRepository(DatabaseRepository):
    """Responsável APENAS por operações de acesso aos dados de Produto"""
    
    def listar(self):
        """Lista todos os produtos com suas categorias"""
        conexao = self.get_connection()
        sql = '''
            SELECT  pro.id,
                    pro.descricao, 
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as categoria
                    
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            ORDER BY pro.descricao
        '''
        registros = conexao.cursor().execute(sql).fetchall()
        conexao.close()
        return registros
    
    def obter_por_id(self, id: int):
        """Obtém um produto específico pelo ID"""
        conexao = self.get_connection()
        sql = f'''
            SELECT  pro.id,
                    pro.descricao, 
                    pro.preco_unitario,
                    pro.quantidade_estoque,
                    pro.categoria_id,
                    cat.descricao as categoria
                    
            FROM Produto pro
            INNER JOIN Categoria cat ON cat.id = pro.categoria_id
            WHERE pro.id={id}    
        '''
        registro = conexao.cursor().execute(sql).fetchone()
        conexao.close()
        return registro
    
    def incluir(self, descricao: str, preco_unitario: float, 
                quantidade_estoque: int, categoria_id: int):
        """Insere um novo produto"""
        conexao = self.get_connection()
        sql = f'''
            INSERT INTO Produto (
                descricao, 
                preco_unitario, 
                quantidade_estoque, 
                categoria_id
            )
            VALUES(
                '{descricao}', 
                {preco_unitario}, 
                {quantidade_estoque}, 
                {categoria_id}
            )
        '''
        conexao.cursor().execute(sql)
        conexao.commit()
        conexao.close()
    
    def alterar(self, id: int, descricao: str, preco_unitario: float,
                quantidade_estoque: int, categoria_id: int):
        """Altera um produto existente"""
        conexao = self.get_connection()
        sql = f'''
            UPDATE Produto 
            SET descricao = '{descricao}', 
                preco_unitario = {preco_unitario}, 
                quantidade_estoque = {quantidade_estoque}, 
                categoria_id = {categoria_id} 
            WHERE id = {id}
        '''
        conexao.cursor().execute(sql)
        conexao.commit()
        conexao.close()
    
    def excluir(self, id: int):
        """Deleta um produto"""
        conexao = self.get_connection()
        sql = f"DELETE FROM Produto WHERE id = {id}"
        conexao.cursor().execute(sql)
        conexao.commit()
        conexao.close()
