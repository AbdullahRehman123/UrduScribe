from django.shortcuts import redirect, render#, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from urllib.parse import urlencode
from django.views.generic import TemplateView
import os
from django.conf import settings
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

        if audio_file:

             # Save file temporarily
            upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads', audio_file.name)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)

            # Call your transcription function
            from app.transcribe import transcribe  # Your existing function
            transcription_text = transcribe(upload_path, language)

            params = urlencode({
                'filename': audio_file.name,
                'filesize': audio_file.size,
                'language': language,
                'transcription': transcription_text
            })

            #return render(request, 'transcription/success.html')
            return redirect(f"{reverse_lazy('transcription:success')}?{params}")
        
        return render(request, 'transcription/upload.html', {'error': 'No file uploaded'})