from django.urls import path, include

urlpatterns = [
    path('maestriabi/', include('integrador.maestriabi.urls')),
    path('ssotica/', include('integrador.ssotica.urls')),
    path('sti3powerstock/', include('integrador.sti3powerstock.urls')),
    path('informezz/', include('integrador.informezz.urls')),
]
