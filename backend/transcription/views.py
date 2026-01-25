from django.shortcuts import redirect, render#, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from urllib.parse import urlencode
from django.views.generic import TemplateView
import os
from django.conf import settings
from .tasks import transcribe_audio_task
from celery.result import AsyncResult
from django.http import JsonResponse
#from autos.models import Make,Auto



class SuccessView(TemplateView):
    template_name = 'transcription/success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filename'] = self.request.GET.get('filename')
        context['filesize'] = self.request.GET.get('filesize')
        context['language'] = self.request.GET.get('language')
        context['transcription'] = self.request.GET.get('transcription')
        return context

class TranscriptionView(LoginRequiredMixin, View):
    def get(self, request):
        test_text = "This is a test."
        context = {'test_text': test_text}
        return render(request, 'transcription/transcription_list.html', context)
    
    def post(self, request):
        audio_file = request.FILES.get('audio_file')
        language = request.POST.get('language')
        num_speakers = request.POST.get('num_speakers', 1)

        if audio_file:

             # Save file temporarily
            upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', audio_file.name)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)

            # ACTUALLY SAVE THE FILE
            with open(upload_path, 'wb+') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # Send task to Celery (non-blocking)
            task = transcribe_audio_task.delay(upload_path, language, num_speakers)

            # Redirect to processing page with task ID
            return redirect(f"{reverse_lazy('transcription:processing', kwargs={'task_id': task.id})}?language={language}")
        
        return render(request, 'transcription/upload.html', {'error': 'No file uploaded'})
    

class ProcessingView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        language = request.GET.get('language', 'english')  # Get from URL
        context = {'task_id': task_id, 'language': language}
        return render(request, 'transcription/processing.html', context)
    
class TaskStatusView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = AsyncResult(task_id)
        
        if task.state == 'PENDING':
            response = {'state': task.state, 'status': 'Processing...'}
        elif task.state == 'SUCCESS':
            response = {
                'state': task.state,
                'result': task.result
            }
        elif task.state == 'FAILURE':
            response = {'state': task.state, 'status': str(task.info)}
        else:
            response = {'state': task.state}
        
        return JsonResponse(response)