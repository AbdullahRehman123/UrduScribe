from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'transcription'

urlpatterns = [
    path('', views.TranscriptionView.as_view(), name='all'),
    #path('success', TemplateView.as_view(template_name='transcription/success.html'), name='success'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('processing/<str:task_id>/', views.ProcessingView.as_view(), name='processing'),
    path('task-status/<str:task_id>/', views.TaskStatusView.as_view(), name='task_status'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('blog/', views.BlogView.as_view(), name='blog'),
]