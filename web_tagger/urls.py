# -*- coding: utf-8 -*-

"""
web_tagger URL Configuration
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from apps.registro.urls import registro_urls
from apps.usuarios.urls import usuarios_urls
from apps.documentos.urls import documentos_urls


urlpatterns = [
    url(r'^', include(registro_urls,namespace='registro_app')),
    url(r'^', include(usuarios_urls,namespace='usuarios_app')),
    url(r'^', include(documentos_urls,namespace='usuarios_app')),
    url(r'^jet/', include('jet.urls', namespace='jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    url(r'^admin/', admin.site.urls),
]
