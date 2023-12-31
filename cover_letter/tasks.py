import os

import openai
import pdfkit
import requests
from celery import shared_task
from django.conf import settings

from cover_letter.repositories.answer_redis_repository import AnswerRedisRepository
from cover_letter.repositories.subscriber_sql_repository import SubscriberSQLRepository
from cover_letter.services.subscriber_service import SubscriberService

openai.api_key = settings.OPENAI_API_KEY


@shared_task(name='generate_prompt')
def generate_prompt(sender_id: str):
    repo = AnswerRedisRepository()
    answers = repo.get_by_id(sender_id)[0]
    prompt = f"""Write a cover letter for me. Here is my details:
        Full Name: {answers.full_name}, Address: {answers.address}, Phone: {answers.phone_number},
        Email address: {answers.email}, Job Details: {answers.job_title}, Company Name:{answers.company_name},
        Company Address: {answers.company_address}, Salutation: {answers.hiring_manager}, 
        Introduction: {answers.introduction}, Skills and Qualifications: {answers.skills_and_qualifications}, 
        Achievements and Accomplishments: {answers.achievements}, Motivation: {answers.motivation}, 
        Closing: {answers.closing}. Return answer as html."""

    generate_pdf.delay(prompt=prompt, to=sender_id)  # send cover letter via whatsapp
    repo.delete(sender_id)
    return 'success'


@shared_task(name='generate_pdf')
def generate_pdf(prompt, to):
    response = openai.Completion.create(
        engine='__text-davinci-003',
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    html_content = response.choices[0].__text
    filename = f'{to}.pdf'

    # Saving the File
    file_path = os.path.join(settings.MEDIA_ROOT, 'cover_letters')
    os.makedirs(file_path, exist_ok=True)
    pdf_save_path = os.path.join(file_path, filename)

    try:
        os.remove(pdf_save_path)
        print(f"File '{pdf_save_path}' removed successfully.")
    except FileNotFoundError:
        print(f"File '{pdf_save_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Save the PDF
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
    }

    try:
        # config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
        pdfkit.from_string(html_content, pdf_save_path, verbose=True, options=options)
    except OSError:
        return "wkhtmltopdf not present in PATH"

    link = 'https://' + settings.HOST + '/media/' + 'cover_letters/{}'.format(filename)
    send_whatsapp_doc.apply_async(kwargs={"to": to, "link": link}, countdown=5 * 60)
    return 'pdf generated'


@shared_task(name='send_whatsapp_document')
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


@shared_task(name='send_advert_to_cover_letter_subscribers')
def send_ad_to_cover_letter_sub(link: str):
    subscriber_repository = SubscriberSQLRepository()
    subscriber_service = SubscriberService(subscriber_repository)

    subscribers = subscriber_service.get_all()
    for subscriber in subscribers:
        send_whatsapp_doc(subscriber.whatsapp_number, link)
