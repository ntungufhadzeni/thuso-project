import os

import pdfkit
import requests
from celery import shared_task
from django.conf import settings
import openai

from cover_letter.crud import AnswerRepository

openai.api_key = settings.OPENAI_API_KEY


@shared_task()
def generate_cover_letter(answers, from_id):
    prompt = f"""Write a cover letter for me. Here is my details:
        Full Name: {answers.full_name}, Address: {answers.address}, Phone: {answers.phone_number},
        Email address: {answers.email}, Job Details: {answers.job_title}, Company Name:{answers.company_name},
        Company Address: {answers.company_address}, Salutation: {answers.hiring_manager}, Introduction: {answers.introduction},
        Skills and Qualifications: {answers.skills_and_qualifications}, Achievements and Accomplishments: {answers.achievements},
        Motivation: {answers.motivation}, Closing: {answers.closing}. Return cover letter body only as html."""

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

    cover_letter = response.choices[0].text
    generate_pdf.delay(cover_letter, from_id)  # send cover letter via whatsapp
    answers_repo = AnswerRepository()
    answers_repo.delete(from_id)


@shared_task()
def generate_pdf(cover_letter, from_id):
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
    pdfkit.from_string(cover_letter, pdf_save_path, configuration=config, options=options)

    link = 'https://www.' + settings.HOST + '/uploads' + '/{}'.format(filename)
    send_whatsapp_doc.delay(from_id, link)


@shared_task()
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
    requests.post(settings.GRAPHLY_URL, headers=headers, json=payload)
