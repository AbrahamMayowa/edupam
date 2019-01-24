from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('forum/', include('forum.urls')),
    path('user/', include('user.urls')),
    path('user/', include('django.contrib.auth.urls')),
    path('academic/', include('coursematerial.urls')),
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='user/home.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('content/', include('cms.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('vote/', include('voting.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)






