DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'djoser',
    'corsheaders',
    'silk',
    'drf_spectacular',
]

CORE_APPS = [
    'core',
    'common.apps.CommonConfig',
    'financeiro.apps.FinanceiroConfig',
    'fornecedor.apps.FornecedorConfig',
    'funcionario.apps.FuncionarioConfig',
    'produto.apps.ProdutoConfig',
    'tenant.apps.TenantConfig',
    'usuario.apps.UsuarioConfig',
    'venda.apps.VendaConfig',
]

INTEGRADORES = [
    'integrador',

    'integrador.maestriabi.apps.MaestriaBIConfig',

    'integrador.ssotica.estoque.apps.SSOticaEstoqueConfig',
    'integrador.ssotica.financeiro.apps.SSOticaFinanceiroConfig',
    'integrador.ssotica.venda.apps.SSOticaVendaConfig',

    'integrador.sti3powerstock.estoque.apps.STi3PowerStockEstoqueConfig',
    'integrador.sti3powerstock.fornecedor.apps.STi3PowerStockFornecedorConfig',
    'integrador.sti3powerstock.loja.apps.STi3PowerStockLojaConfig',
    'integrador.sti3powerstock.produto.apps.STi3PowerStockProdutoConfig',
    'integrador.sti3powerstock.venda.apps.STi3PowerStockVendaConfig',

    'integrador.informezz.estoque.apps.InformezzEstoqueConfig',
    'integrador.informezz.loja.apps.InformezzLojaConfig',
    'integrador.informezz.produto.apps.InformezzProdutoConfig',
    'integrador.informezz.venda.apps.InformezzVendaConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CORE_APPS + INTEGRADORES
