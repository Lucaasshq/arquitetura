"""
Arquivo mantido apenas para compatibilidade. 
Use app.views.categorias() e app.services.CategoriaService() diretamente.
"""

from app.views import categorias


class ConnectionCategoriaDataBase:
    """
    Classe mantida apenas para compatibilidade com código existente.
    Delegar a chamada para a view de categorias.
    
    NOTA: Esta classe será descontinuada. Use app.views.categorias() diretamente.
    """

    @staticmethod
    def connectar(request, acao=None, id=None):
        """
        Método que delega para a view de categorias refatorada.
        
        Mantido apenas para compatibilidade com código existente.
        """
        return categorias(request, acao, id)