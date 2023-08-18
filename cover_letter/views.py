import json

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from cover_letter.schemas.subscriber import Subscriber
from cover_letter.services.chat_service import CoverLetterAssistant
from cover_letter.services.subscriber_service import SubscriberService


def index(request):
    return render(request, 'cover_letter/home.html')


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
                subscriber_service = SubscriberService()
                subscriber = Subscriber(whatsapp_name=profile_name, whatsapp_number=from_id)
                subscriber_service.create(subscriber)
                cover_letter_assistant = CoverLetterAssistant(from_id, text)
                cover_letter_assistant.handle_chat()
            else:
                pass
        else:
            pass

        return HttpResponse('success', status=200)
