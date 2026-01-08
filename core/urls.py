from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),    
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    re_path(r'^auth/', include('djoser.urls.jwt')),
    
    # MV CORE
    path('v1/financeiro/', include('financeiro.urls')),
    path('v1/fornecedor/', include('fornecedor.urls')),
    path('v1/funcionario/', include('funcionario.urls')),
    path('v1/integrador/', include('integrador.urls')),
    path('v1/produto/', include('produto.urls')),
    path('v1/tenant/', include('tenant.urls')),
    path('v1/usuario/', include('usuario.urls')),
    path('v1/venda/', include('venda.urls')),
]
