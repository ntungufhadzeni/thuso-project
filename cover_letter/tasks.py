import os
import time

import openai
import pdfkit
import requests
from celery import shared_task
from django.conf import settings

from cover_letter.repositories.answer_repository import AnswerRepository
from cover_letter.services.subscriber_service import SubscriberService

openai.api_key = settings.OPENAI_API_KEY


@shared_task(name='generate prompt')
def generate_prompt(from_id: str):
    answers_repo = AnswerRepository()
    answers = answers_repo.get_by_id(from_id)[0]
    prompt = f"""Write a cover letter for me. Here is my details:
        Full Name: {answers.full_name}, Address: {answers.address}, Phone: {answers.phone_number},
        Email address: {answers.email}, Job Details: {answers.job_title}, Company Name:{answers.company_name},
        Company Address: {answers.company_address}, Salutation: {answers.hiring_manager}, Introduction: {answers.introduction},
        Skills and Qualifications: {answers.skills_and_qualifications}, Achievements and Accomplishments: {answers.achievements},
        Motivation: {answers.motivation}, Closing: {answers.closing}. Return answer as html_letters."""

    generate_html.delay(prompt=prompt, to=from_id)  # send cover letter via whatsapp
    answers_repo.delete(from_id)
    return 'success'


@shared_task(name='generate html')
def generate_html(prompt, to):
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

    # create html_letters
    html_file_path = os.path.join(settings.BASE_DIR, 'cover_letter', 'html_letters', f'{to}.html')
    os.makedirs(os.path.join(settings.BASE_DIR, 'cover_letter', 'html_letters'), exist_ok=True)
    with open(html_file_path, 'w') as f:
        f.write(html)
        f.close()
    generate_pdf.delay(to=to)
    return "HTML created"


@shared_task(name='generate pdf')
def generate_pdf(to):
    filename = f'{to}.pdf'
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }

    # Saving the File
    file_path = os.path.join(settings.MEDIA_ROOT, 'cover_letters')
    os.makedirs(file_path, exist_ok=True)
    pdf_save_path = os.path.join(file_path, filename)

    # Save the PDF
    try:
        html_file_path = os.path.join(settings.BASE_DIR, 'cover_letter', 'html_letters', f'{to}.html')
        config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        success = pdfkit.from_file(html_file_path, pdf_save_path, configuration=config, options=options, verbose=True)
        time.sleep(30)
    except OSError:
        return "wkhtmltopdf not present in PATH"

    if success:
        link = 'https://' + settings.HOST + '/media/' + 'cover_letters/{}'.format(filename)
        send_whatsapp_doc.delay(to=to, link=link)
        return 'pdf generated'
    else:
        return 'pdf not generated'


@shared_task(name='send WhatsApp document')
def send_whatsapp_doc(to, link):
    headers = {"Authorization": settings.TOKEN}
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "document",
        "document": {
            "link": link,
        }
    }
    res = requests.post(settings.GRAPHQL_URL, headers=headers, json=payload)
    return res.json()


@shared_task(name='send advert to cover letter subscribers')
def send_ad_to_cover_letter_sub(link: str):
    subscriber_service = SubscriberService()
    subscribers = subscriber_service.get_all()
    for subscriber in subscribers:
        send_whatsapp_doc(subscriber.whatsapp_number, link)
