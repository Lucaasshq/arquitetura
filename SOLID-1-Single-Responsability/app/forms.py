import sqlite3
from django import forms


class CategoriaForm(forms.Form):
    """Responsável APENAS pela definição do formulário de Categoria"""
    id = forms.IntegerField(
        label='ID', 
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), 
        required=False
    )
    descricao = forms.CharField(
        label='Descrição', 
        max_length=30, 
        required=True
    )


class ProdutoForm(forms.Form):
    """Responsável APENAS pela definição do formulário de Produto"""
    id = forms.IntegerField(
        label='ID', 
        widget=forms.TextInput(attrs={'readonly': 'readonly'}), 
        required=False
    )
    descricao = forms.CharField(
        label='Descrição', 
        max_length=30, 
        required=True
    )
    preco_unitario = forms.DecimalField(
        label='Preço Unitário', 
        max_digits=10, 
        decimal_places=2, 
        required=True
    )
    quantidade_estoque = forms.IntegerField(
        label='Qtd. Estoque', 
        required=True
    )
    categoria_id = forms.ChoiceField(
        label='Categoria', 
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carrega as categorias disponíveis
        conexao = sqlite3.connect('db_solid.sqlite3')
        categorias = conexao.cursor().execute(
            'SELECT id, descricao FROM Categoria ORDER BY descricao'
        ).fetchall()
        conexao.close()
        self.fields['categoria_id'].choices = categorias
