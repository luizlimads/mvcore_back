from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import InstituicaoFinanceira, ContaFinanceira, CategoriaFinanceira, Lancamento, TipoLancamentoChoices, TipoCategoriaChoices
from .serializers import InstituicaoFinanceiraSerializer, ContaFinanceiraSerializer, CategoriaFinanceiraSerializer, LancamentoSerializer, LancamentoDetailSerializer
from .filters import LancamentoFilter

from collections import defaultdict
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncDay

class InstituicaoFinanceiraList(generics.ListCreateAPIView):
    serializer_class = InstituicaoFinanceiraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InstituicaoFinanceira.objects.filter(tenant=self.request.user.tenant)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class InstituicaoFinanceiraDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InstituicaoFinanceiraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InstituicaoFinanceira.objects.filter(tenant=self.request.user.tenant)

class ContaFinanceiraList(generics.ListCreateAPIView):
    serializer_class = ContaFinanceiraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ContaFinanceira.objects.filter(tenant=self.request.user.tenant)
        instituicao = self.request.query_params.get('id_instituicao_financeira')
        
        return queryset.filter(id_instituicao_financeira=instituicao) if instituicao else queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class ContaFinanceiraDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ContaFinanceiraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ContaFinanceira.objects.filter(tenant=self.request.user.tenant)

class CategoriaFinanceiraList(generics.ListCreateAPIView):
    serializer_class = CategoriaFinanceiraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = CategoriaFinanceira.objects.filter(tenant=self.request.user.tenant)
        categoria_pai = self.request.query_params.get('categoria_pai')
        
        return queryset.filter(categoria_pai=categoria_pai) if categoria_pai else queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context

class CategoriaFinanceiraDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoriaFinanceiraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CategoriaFinanceira.objects.filter(tenant=self.request.user.tenant)

class LancamentoList(generics.ListCreateAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = LancamentoFilter

    def get_queryset(self):
        return Lancamento.objects.filter(tenant=self.request.user.tenant)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['tenant'] = self.request.user.tenant
        return context
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LancamentoDetailSerializer
        return LancamentoSerializer

class LancamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LancamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lancamento.objects.filter(tenant=self.request.user.tenant)

class ContaFinanceiraResumo(APIView):
    permission_classes = [IsAuthenticated]

    def _get_datas_periodo(self, query_params):
        data_fim_param = query_params.get('data_fim')
        n_meses = int(query_params.get('n_meses', 18))

        if data_fim_param:
            data_ref = datetime.strptime(data_fim_param[:7], '%Y-%m').date()
            data_fim = data_ref + relativedelta(months=1, days=-1)
        else:
            data_fim = date.today()

        data_inicio = (data_fim.replace(day=1) - relativedelta(months=n_meses - 1))
        
        meses = []
        curr = data_inicio
        while curr <= data_fim.replace(day=1):
            meses.append(curr.strftime('%Y-%m'))
            curr += relativedelta(months=1)
            
        return data_inicio, data_fim, meses

    def get(self, request):
        try:
            data_inicio, data_fim, meses_periodo = self._get_datas_periodo(request.query_params)
        except ValueError:
            return Response({"error": "Parâmetros inválidos."}, status=400)

        tenant = request.user.tenant

        lancamentos = Lancamento.objects.filter(
            tenant=tenant,
            data_competencia__range=[data_inicio, data_fim] # Range é mais limpo que gte/lte
        ).annotate(
            mes=TruncMonth('data_competencia')
        ).values('conta', 'mes', 'tipo').annotate(total=Sum('valor')).order_by('mes')

        dados_map = defaultdict(lambda: defaultdict(dict))
        
        for l in lancamentos:
            if not l['mes']: continue
            mes_str = l['mes'].strftime('%Y-%m')
            dados_map[l['conta']][mes_str][l['tipo']] = l['total'] or 0

        contas = ContaFinanceira.objects.filter(tenant=tenant)
        
        def montar_movimentacoes(conta_id, tipo_lancamento):
            """Gera a lista de meses preenchida para um tipo específico"""
            return [
                {
                    "competencia": mes,
                    "valor": dados_map[conta_id][mes].get(tipo_lancamento, 0)
                }
                for mes in meses_periodo
            ]

        resumo_entradas = []
        resumo_saidas = []

        for conta in contas:
            base_info = {"conta_id": conta.id, "nome": conta.descricao}
            
            resumo_entradas.append({
                **base_info,
                "movimentacoes": montar_movimentacoes(conta.id, TipoLancamentoChoices.CREDITO)
            })
            
            resumo_saidas.append({
                **base_info,
                "movimentacoes": montar_movimentacoes(conta.id, TipoLancamentoChoices.DEBITO)
            })

        return Response({
            "meta": {
                "periodo_inicio": data_inicio.strftime('%Y-%m'),
                "periodo_fim": data_fim.strftime('%Y-%m')
            },
            "entradas": resumo_entradas,
            "saidas": resumo_saidas
        })

class LancamentoResumoDiarioPeriodo(APIView):
    permission_classes = [IsAuthenticated]

    def _get_periodo_dias(self, query_params):
        data_inicio_param = query_params.get('periodo_inicio')
        data_fim_param = query_params.get('periodo_fim')

        if data_fim_param:
            data_fim = datetime.strptime(data_fim_param, '%Y-%m-%d').date()
        else:
            data_fim = date.today()

        if data_inicio_param:
            data_inicio = datetime.strptime(data_inicio_param, '%Y-%m-%d').date()
        else:
            data_inicio = data_fim.replace(day=1)

        dias = []
        curr = data_inicio
        while curr <= data_fim:
            dias.append(curr.strftime('%Y-%m-%d'))
            curr += timedelta(days=1)
            
        return data_inicio, data_fim, dias

    def get(self, request):
        try:
            data_inicio, data_fim, lista_dias = self._get_periodo_dias(request.query_params)
        except ValueError:
            return Response({"error": "Parâmetros de data inválidos. Use YYYY-MM-DD."}, status=400)

        tenant = request.user.tenant

        lancamentos = Lancamento.objects.filter(
            tenant=tenant,
            data_competencia__date__range=[data_inicio, data_fim]
        ).annotate(
            dia=TruncDay('data_competencia')
        ).values(
            'dia', 
            'tipo',            
            'categoria__tipo'
        ).annotate(
            total=Sum('valor')
        ).order_by('dia')

        dados_map = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        for l in lancamentos:
            if not l['dia']: continue
            
            dia_str = l['dia'].strftime('%Y-%m-%d')
            
            tipo_lanc = l['tipo']
            tipo_cat = l['categoria__tipo']
            total = l['total'] or 0
            
            if tipo_lanc and tipo_cat:
                dados_map[dia_str][tipo_lanc][tipo_cat] += float(total)

        resultado_data = []

        def processar_valores(dia, tipo_lancamento_db):
            dados_dia_tipo = dados_map[dia][tipo_lancamento_db]

            val_entrada = dados_dia_tipo.get(TipoCategoriaChoices.ENTRADAS.value, 0)
            val_saida = dados_dia_tipo.get(TipoCategoriaChoices.SAIDAS.value, 0)
            
            return {
                "entradas": val_entrada,
                "saidas": val_saida,
                "total": val_entrada - val_saida
            }

        for dia in lista_dias:
            resultado_data.append({
                "data_competencia": dia,
                "lancamentos": {
                    "credito": processar_valores(dia, TipoLancamentoChoices.CREDITO.value),
                    "debito": processar_valores(dia, TipoLancamentoChoices.DEBITO.value)
                }
            })

        return Response({
            "meta": {
                "periodo_inicio": data_inicio.strftime('%Y-%m-%d'),
                "periodo_fim": data_fim.strftime('%Y-%m-%d')
            },
            "data": resultado_data
        })