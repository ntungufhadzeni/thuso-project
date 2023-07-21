import openai
import requests
from django.conf import settings

from .crud import AnswerRepository
from .tasks import generate_cover_letter

openai.api_key = settings.OPENAI_API_KEY


class CoverLetterAssistant:
    questions = [
        'What is your full name as you would like it to appear in the letter?',
        'What is the best phone number to reach you at?',
        'What is your current address?',
        'What is your preferred email address for correspondence?',
        'What is the specific job title or position you are applying for?',
        'What is the name of the company or organization you are applying to?',
        'What is the address of the company or organization you are applying to?',
        'Do you have the name of the hiring manager or the person who will be reviewing applications? If yes, please provide the name.',
        'Please provide a brief introduction about yourself, including your educational background, current employment status, and any relevant achievements or experiences.',
        'What are your skills, qualifications, and relevant work experience that are applicable to the job you are applying for?',
        'Can you mention any notable achievements or accomplishments that demonstrate your abilities and suitability for the position? This could include awards, certifications, successful projects, or significant contributions in previous roles.',
        'Why are you interested in the job and the company? Please provide your motivations and reasons for applying.',
        'Do you have any specific closing statements or information you would like to include in the letter? For example, your availability for an interview or references.'
    ]

    def __init__(self, phone_id: str, profile_name: str, whatsapp_id: str, from_id: str, text: str):
        self.phone_id = phone_id
        self.profile_name = profile_name
        self.whatsapp_id = whatsapp_id
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
        requests.post(settings.GRAPHLY_URL, headers=headers, json=payload)

    def __handle_chat(self):
        if self.__answers.full_name:
            if self.__answers.phone_number:
                if self.__answers.address:
                    if self.__answers.email:
                        if self.__answers.job_title:
                            if self.__answers.company_name:
                                if self.__answers.company_address:
                                    if self.__answers.hiring_manager:
                                        if self.__answers.introduction:
                                            if self.__answers.skills_and_qualifications:
                                                if self.__answers.achievements:
                                                    if self.__answers.motivation:
                                                        if self.__answers.closing:
                                                            self.__answers = \
                                                                self.__answers_repo.get_by_id(self.from_id)[0]
                                                            generate_cover_letter(self.__answers, self.from_id)
                                                            self.__send_whatsapp_message(
                                                                "😀 Great we have everything we need to create your "
                                                                "Cover Letter. We will send it to you when we are "
                                                                "done . . . . ")
                                                        else:
                                                            data = {'closing': self.text}
                                                            self.__answers_repo.update(self.from_id, data)
                                                            self.__answers = \
                                                                self.__answers_repo.get_by_id(self.from_id)[0]
                                                            generate_cover_letter.delay(self.__answers, self.from_id)
                                                            self.__send_whatsapp_message(
                                                                "😀 Great we have everything we need to create your "
                                                                "Cover Letter. We will send it to you when we are "
                                                                "done . . . . ")
                                                    else:
                                                        data = {'motivation': self.text}
                                                        self.__answers_repo.update(self.from_id, data)
                                                        self.__send_whatsapp_message(CoverLetterAssistant.questions[12])
                                                else:
                                                    data = {'achievements': self.text}
                                                    self.__answers_repo.update(self.from_id, data)
                                                    self.__send_whatsapp_message(CoverLetterAssistant.questions[11])
                                            else:
                                                data = {'skills_and_qualifications': self.text}
                                                self.__answers_repo.update(self.from_id, data)
                                                self.__send_whatsapp_message(CoverLetterAssistant.questions[10])
                                        else:
                                            data = {'introduction': self.text}
                                            self.__answers_repo.update(self.from_id, data)
                                            self.__send_whatsapp_message(CoverLetterAssistant.questions[9])
                                    else:
                                        data = {'hiring_manager': self.text}
                                        self.__answers_repo.update(self.from_id, data)
                                        self.__send_whatsapp_message(CoverLetterAssistant.questions[8])
                                else:
                                    data = {'company_address': self.text}
                                    self.__answers_repo.update(self.from_id, data)
                                    self.__send_whatsapp_message(CoverLetterAssistant.questions[7])
                            else:
                                data = {'company_name': self.text}
                                self.__answers_repo.update(self.from_id, data)
                                self.__send_whatsapp_message(CoverLetterAssistant.questions[6])
                        else:
                            data = {'job_title': self.text}
                            self.__answers_repo.update(self.from_id, data)
                            self.__send_whatsapp_message(CoverLetterAssistant.questions[5])
                    else:
                        data = {'email': self.text}
                        self.__answers_repo.update(self.from_id, data)
                        self.__send_whatsapp_message(CoverLetterAssistant.questions[4])
                else:
                    data = {'address': self.text}
                    self.__answers_repo.update(self.from_id, data)
                    self.__send_whatsapp_message(CoverLetterAssistant.questions[3])
            else:
                data = {'phone_number': self.text}
                self.__answers_repo.update(self.from_id, data)
                self.__send_whatsapp_message(CoverLetterAssistant.questions[2])
        else:
            data = {'full_name': self.text}
            self.__answers_repo.update(self.from_id, data)
            self.__send_whatsapp_message(CoverLetterAssistant.questions[1])

    def send_response(self):
        answers = self.__answers_repo.get_by_id(self.from_id)
        if len(answers) == 0 or self.text.lower() == 'reset':
            message = 'Welcome to the AI Cover Letter creator 😀. I am going to help you write a cover letter that ' \
                      'will help you land your dream job. If you make a mistake during the process, reply with ' \
                      '"reset" to start over.'
            self.__send_whatsapp_message(message)
            self.__send_whatsapp_message('To get started, answer this question: \n')
            self.__send_whatsapp_message(CoverLetterAssistant.questions[0])
            self.__answers = self.__answers_repo.create(self.from_id)[0]
        else:
            self.__answers = answers[0]
            self.__handle_chat()



