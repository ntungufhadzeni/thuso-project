import openai
import requests
from django.conf import settings

from cover_letter.repositories.answer_repository import AnswerRepository
from cover_letter.schemas.answer import Answer
from cover_letter.tasks import generate_cover_letter

from enum import Enum

openai.api_key = settings.OPENAI_API_KEY


class Question(Enum):
    FULL_NAME = 'What is your full name as you would like it to appear in the letter?'
    PHONE_NUMBER = 'What is the best phone number to reach you at?'
    ADDRESS = 'What is your current address?'
    EMAIL = 'What is your preferred email address for correspondence?'
    JOB_TITLE = 'What is the specific job title or position you are applying for?'
    COMPANY_NAME = 'What is the name of the company or organization you are applying to?'
    COMPANY_ADDRESS = 'What is the address of the company or organization you are applying to?'
    HIRING_MANAGER = 'Do you have the name of the hiring manager or the person who will be reviewing applications? If' \
                     ' yes, please provide the name.'
    INTRODUCTION = 'Please provide a brief introduction about yourself, including your educational background, ' \
                   'current employment status, and any relevant achievements or experiences.'
    SKILLS = 'What are your skills, qualifications, and relevant work experience that are applicable to the job you ' \
             'are applying for?'
    ACHIEVEMENTS = 'Can you mention any notable achievements or accomplishments that demonstrate your abilities and ' \
                   'suitability for the position? This could include awards, certifications, successful projects, ' \
                   'or significant contributions in previous roles.'
    MOTIVATION = 'Why are you interested in the job and the company? Please provide your motivations and reasons for ' \
                 'applying.'
    CLOSING = 'Do you have any specific closing statements or information you would like to include in the letter? ' \
              'For example, your availability for an interview or references.'


class CoverLetterAssistant:

    def __init__(self, from_id: str, text: str):
        self.from_id = from_id
        self.text = text
        self.__answers = None
        self.__answers_repo = AnswerRepository()

    def __send_whatsapp_message(self, response):
        headers = {"Authorization": settings.TOKEN}
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.from_id,
            "type": "text",
            "text": {"body": response}
        }
        return requests.post(settings.GRAPHQL_URL, headers=headers, json=payload)

    def __save_answer(self):
        if not self.__answers.full_name:
            self.__answers.full_name = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'full_name'}))
            self.__send_whatsapp_message(Question.PHONE_NUMBER.value)
        elif not self.__answers.phone_number:
            self.__answers.phone_number = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'phone_number'}))
            self.__send_whatsapp_message(Question.ADDRESS.value)
        elif not self.__answers.address:
            self.__answers.address = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'address'}))
            self.__send_whatsapp_message(Question.EMAIL.value)
        elif not self.__answers.email:
            self.__answers.email = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'email'}))
            self.__send_whatsapp_message(Question.JOB_TITLE.value)
        elif not self.__answers.job_title:
            self.__answers.job_title = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'job_title'}))
            self.__send_whatsapp_message(Question.COMPANY_NAME.value)
        elif not self.__answers.company_name:
            self.__answers.company_name = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'company_name'}))
            self.__send_whatsapp_message(Question.COMPANY_ADDRESS.value)
        elif not self.__answers.company_address:
            self.__answers.company_address = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'company_address'}))
            self.__send_whatsapp_message(Question.HIRING_MANAGER.value)
        elif not self.__answers.hiring_manager:
            self.__answers.hiring_manager = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'hiring_manager'}))
            self.__send_whatsapp_message(Question.INTRODUCTION.value)
        elif not self.__answers.introduction:
            self.__answers.introduction = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'introduction'}))
            self.__send_whatsapp_message(Question.SKILLS.value)
        elif not self.__answers.skills_and_qualifications:
            self.__answers.skills_and_qualifications = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'skills_and_qualifications'}))
            self.__send_whatsapp_message(Question.ACHIEVEMENTS.value)
        elif not self.__answers.achievements:
            self.__answers.achievements = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'achievements'}))
            self.__send_whatsapp_message(Question.MOTIVATION.value)
        elif not self.__answers.motivation:
            self.__answers.motivation = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'motivation'}))
            self.__send_whatsapp_message(Question.CLOSING.value)
        elif not self.__answers.closing:
            self.__answers.closing = self.text
            self.__answers_repo.update(self.from_id, self.__answers.dict(include={'closing'}))
            generate_cover_letter.delay(self.from_id)
            self.__send_whatsapp_message(
                "😀 Great we have everything we need to create your "
                "Cover Letter. We will send it to you when we are "
                "done . . . . ")
        else:
            generate_cover_letter.delay(self.from_id)
            self.__send_whatsapp_message(
                "😀 Great we have everything we need to create your "
                "Cover Letter. We will send it to you when we are "
                "done . . . . ")

    def handle_chat(self):
        answers = self.__answers_repo.get_by_id(self.from_id)
        if not len(answers) == 0 and self.text.lower() == 'reset':
            self.__answers_repo.delete(self.from_id)
            message = 'Welcome to the AI Cover Letter creator 😀. I am going to help you write a cover letter that ' \
                      'will help you land your dream job. If you make a mistake during the process, reply with ' \
                      '"reset" to start over.'
            self.__send_whatsapp_message(message)
            self.__send_whatsapp_message('To get started, answer this question: \n')
            self.__send_whatsapp_message(Question.FULL_NAME.value)
            self.__answers_repo.insert(Answer(whatsapp_number=self.from_id))
            return ''
        elif len(answers) == 0:
            message = 'Welcome to the AI Cover Letter creator 😀. I am going to help you write a cover letter that ' \
                      'will help you land your dream job. If you make a mistake during the process, reply with ' \
                      '"reset" to start over.'
            self.__send_whatsapp_message(message)
            self.__send_whatsapp_message('To get started, answer this question: \n')
            self.__send_whatsapp_message(Question.FULL_NAME.value)
            self.__answers_repo.insert(Answer(whatsapp_number=self.from_id))
            return ''
        
        else:
            self.__answers = answers[0]
            self.__save_answer()
            return ''
