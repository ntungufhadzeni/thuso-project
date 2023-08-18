import os

import pdfkit
import requests
from celery import shared_task
from django.conf import settings
import openai

from cover_letter.repositories.answer_repository import AnswerRepository
from cover_letter.services.subscriber_service import SubscriberService

openai.api_key = settings.OPENAI_API_KEY


@shared_task
def generate_prompt(from_id: str):
    answers_repo = AnswerRepository()
    answers = answers_repo.get_by_id(from_id)[0]
    prompt = f"""Write a cover letter for me. Here is my details:
        Full Name: {answers.full_name}, Address: {answers.address}, Phone: {answers.phone_number},
        Email address: {answers.email}, Job Details: {answers.job_title}, Company Name:{answers.company_name},
        Company Address: {answers.company_address}, Salutation: {answers.hiring_manager}, Introduction: {answers.introduction},
        Skills and Qualifications: {answers.skills_and_qualifications}, Achievements and Accomplishments: {answers.achievements},
        Motivation: {answers.motivation}, Closing: {answers.closing}. Return cover letter body only as html."""

    generate_cover_letter.apply_async(kwargs={'prompt': prompt, 'from_id': from_id})  # send cover letter via whatsapp
    answers_repo.delete(from_id)


@shared_task
def generate_cover_letter(prompt, from_id):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    html = response.choices[0].text

    filename = f'{from_id}.pdf'

    options = {
        'encoding': 'UTF-8',
        'enable-local-file-access': None,  # To be able to access CSS
        'page-size': 'A4',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
    }

    config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

    # Saving the File
    file_path = settings.MEDIA_ROOT + '/cover_letters/'
    os.makedirs(file_path, exist_ok=True)
    pdf_save_path = os.path.join(file_path, filename)
    # Save the PDF
    pdfkit.from_string(html, pdf_save_path, configuration=config, options=options)

    link = 'https://' + settings.HOST + '/media/' + 'cover_letters/{}'.format(filename)
    send_whatsapp_doc.apply_async(kwargs={'from_id': from_id, 'link': link})


@shared_task
def send_whatsapp_doc(from_id, link):
    headers = {"Authorization": settings.TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": from_id,
        "type": "document",
        "document": {
            "link": link,
        }
    }
    requests.post(settings.GRAPHQL_URL, headers=headers, json=payload)


@shared_task
def send_ad_to_cover_letter_sub(link: str):
    subscriber_service = SubscriberService()
    subscribers = subscriber_service.get_all()
    for subscriber in subscribers:
        send_whatsapp_doc(subscriber.whatsapp_number, link)
