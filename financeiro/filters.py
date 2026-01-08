from django_filters import rest_framework as filters
from .models import Lancamento

class LancamentoFilter(filters.FilterSet):
    # Cria um filtro para um intervalo na 'data_lancamento'
    data_lancamento_inicio = filters.DateFilter(field_name='data_lancamento', lookup_expr='gte')
    data_lancamento_fim = filters.DateFilter(field_name='data_lancamento', lookup_expr='lte')

    # Cria um filtro para um intervalo na 'data_competencia'
    data_competencia_inicio = filters.DateFilter(field_name='data_competencia', lookup_expr='gte')
    data_competencia_fim = filters.DateFilter(field_name='data_competencia', lookup_expr='lte')

    # Filtro de exemplo para o campo 'tipo' (busca exata)
    tipo = filters.CharFilter(field_name='tipo', lookup_expr='exact')

    # Filtro de exemplo para o campo 'descricao' (busca parcial, case-insensitive)
    descricao = filters.CharFilter(field_name='descricao', lookup_expr='icontains')

    class Meta:
        model = Lancamento
        # Lista de campos que podem ser filtrados diretamente com busca exata
        # (além dos que definimos customizados acima)
        fields = ['conta', 'categoria', 'fornecedor', 'venda']