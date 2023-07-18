from .chat import CoverLetterAssistant
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings


def index(request):
    return HttpResponse("Home")


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        verify_token = settings.VERIFY_TOKEN
        mode = request.GET['hub.mode']
        token = request.GET['hub.verify_token']
        challenge = request.GET['hub.challenge']

        if mode == 'subscribe' and token == verify_token:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse('error', status=403)

    if request.method == 'POST':
        data = json.loads(request.body)

        if 'contacts' in data['entry'][0]['changes'][0]['value']:
            if data['object'] == 'whatsapp_business_account':
                profile_name = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
                from_id = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

                cover_letter_assistant = CoverLetterAssistant(profile_name, from_id, text)
                cover_letter_assistant.send_response()
            else:
                pass
        else:
            pass

        return HttpResponse('success', status=200)
