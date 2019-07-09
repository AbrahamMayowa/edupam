from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from ckeditor_uploader import views



urlpatterns = [
    path('forum/', include('forum.urls')),
    path('user/', include('user.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('academic/', include('coursematerial.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('content/', include('cms.urls')),
    path('ckeditor/upload', views.upload, name='ckeditor_upload'),
    path('ckeditor/browser/', views.browse, name='ckeditor_browse'),
    path('vote/', include('voting.urls')),
    path('search/', include('haystack.urls'), name='haystack_search'),
    path('follow/', include('follow.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

