from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.forms import CategoriaForm, ProdutoForm
from app.services import CategoriaService, ProdutoService


# Método responsável por listar, incluir, alterar e excluir as Categorias.
def categorias(request, acao=None, id=None):
    '''
    Método responsável por receber todas as rotas URL do cadastro de Categorias.
    
    De acordo com a "acao" e o "id" informados, esse método irá:
      - 'categorias/': Exibir a página de listagem
      - 'categorias/incluir/': Exibir a página de inclusão
      - 'categorias/alterar/<:id>/': Exibir a página de alteração
      - 'categorias/excluir/<:id>/': Exibir a página de exclusão
      - 'categorias/salvar/': insere, altera ou exclui um registro
    '''
    
    service = CategoriaService()

    try:
        # Listar registros
        if acao is None:
            registros = service.listar_categorias()
            return render(request, 'categorias_listar.html', context={'registros': registros})
        
        # Salvar registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            try:
                if acao_form == 'Inclusão':
                    service.criar_categoria(descricao=form_data['descricao'])

                elif acao_form == 'Exclusão':
                    service.deletar_categoria(int(form_data['id']))

                else:  # Alteração
                    service.atualizar_categoria(
                        id=int(form_data['id']),
                        descricao=form_data['descricao']
                    )

                return HttpResponseRedirect(reverse("categorias"))
            
            except ValueError as err:
                return render(request, 'home.html', context={'ERRO': str(err)})
        
        # Inserir registro
        elif acao == 'incluir':
            return render(request, 'categorias_editar.html',
                         context={'acao': 'Inclusão', 'form': CategoriaForm()})
        
        # Alterar ou excluir registro
        elif acao in ['alterar', 'excluir']:
            categoria = service.obter_categoria(id)
            categoria_dict = {'id': categoria[0], 'descricao': categoria[1]}

            acao_display = 'Alteração' if acao == 'alterar' else 'Exclusão'

            return render(request, 'categorias_editar.html',
                         context={'acao': acao_display, 'form': CategoriaForm(initial=categoria_dict)})
        
        # Ação inválida
        else:
            raise ValueError('Ação inválida')

    except Exception as err:
        return render(request, 'home.html', context={'ERRO': str(err)})
def produtos(request, acao=None, id=None):
    '''
    Método responsável por receber todas as rotas URL do cadastro de Produtos.
    
    De acordo com a "acao" e o "id" informados, esse método irá:
      - 'produtos/': Exibir a página de listagem
      - 'produtos/incluir/': Exibir a página de inclusão
      - 'produtos/alterar/<:id>/': Exibir a página de alteração
      - 'produtos/excluir/<:id>/': Exibir a página de exclusão
      - 'produtos/salvar/': insere, altera ou exclui um registro
    '''
    
    service = ProdutoService()

    try:
        # Listar registros
        if acao is None:
            registros = service.listar_produtos()
            return render(request, 'produtos_listar.html', context={'registros': registros})
        
        # Salvar registro
        elif acao == 'salvar':
            form_data = request.POST
            acao_form = form_data['acao']

            try:
                if acao_form == 'Inclusão':
                    service.criar_produto(
                        descricao=form_data['descricao'],
                        preco_unitario=float(form_data['preco_unitario']),
                        quantidade_estoque=int(form_data['quantidade_estoque']),
                        categoria_id=int(form_data['categoria_id'])
                    )

                elif acao_form == 'Exclusão':
                    service.deletar_produto(int(form_data['id']))

                else:  # Alteração
                    service.atualizar_produto(
                        id=int(form_data['id']),
                        descricao=form_data['descricao'],
                        preco_unitario=float(form_data['preco_unitario']),
                        quantidade_estoque=int(form_data['quantidade_estoque']),
                        categoria_id=int(form_data['categoria_id'])
                    )

                return HttpResponseRedirect(reverse("produtos"))
            
            except (ValueError, Exception) as err:
                return render(request, 'home.html', context={'ERRO': str(err)})
        
        # Inserir registro
        elif acao == 'incluir':
            return render(request, 'produtos_editar.html',
                         context={'acao': 'Inclusão', 'form': ProdutoForm()})
        
        # Alterar ou excluir registro
        elif acao in ['alterar', 'excluir']:
            registro = service.obter_produto(id)
            registro_dict = {
                'id': registro[0],
                'descricao': registro[1],
                'preco_unitario': registro[2],
                'quantidade_estoque': registro[3],
                'categoria_id': registro[4],
                'categoria': registro[5],
            }

            acao_display = 'Alteração' if acao == 'alterar' else 'Exclusão'

            return render(request, 'produtos_editar.html',
                         context={'acao': acao_display, 'form': ProdutoForm(initial=registro_dict)})
        
        # Ação inválida
        else:
            raise ValueError('Ação inválida')

    except Exception as err:
        return render(request, 'home.html', context={'ERRO': str(err)})


# Exibe a página inicial da aplicação
def home(request):
    '''Exibe a pagina inicial da aplicação'''
    # define a página HTML (template) que deverá será carregada
    template = 'home.html'
    return render(request, template)


