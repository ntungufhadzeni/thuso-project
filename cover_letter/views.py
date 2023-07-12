from .chat_gpt import JobSeekerAssistant
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return HttpResponse("Home")


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'GET':
        verify_token = 'b6046276-0ab2-4c8a-98cf-94c62be80ed8'
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
                phone_number_id = data['entry'][0]['changes'][0]['value']['metadata']['phone_number_id']
                whatsapp_id = data['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
                from_id = data['entry'][0]['changes'][0]['value']['messages'][0]['from']
                text = data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']

                chat = JobSeekerAssistant(profile_name, phone_number_id, whatsapp_id, from_id, text)
                chat.ask_agent()
                chat.send_whatsapp_message()
            else:
                pass
        else:
            pass

        return HttpResponse('success', status=200)
