from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'transcription'

urlpatterns = [
    path('', views.TranscriptionView.as_view(), name='all'),
    #path('success', TemplateView.as_view(template_name='transcription/success.html'), name='success'),
    path('success/', views.SuccessView.as_view(), name='success'),
    #path('make', views.MakeView.as_view(), name='make_list'),
    #path('auto/create/', views.AutoCreate.as_view(), name='auto_create'),
    #path('auto/<int:pk>/update', views.AutoUpdate.as_view(), name='auto_update'),
    #path('auto/<int:pk>/delete', views.AutoDelete.as_view(), name='auto_delete'),
    #path('make/create/', views.MakeCreate.as_view(), name='make_create'),
    #path('make/<int:pk>/update', views.MakeUpdate.as_view(), name='make_update'),
    #path('make/<int:pk>/delete', views.MakeDelete.as_view(), name='make_delete'),
]