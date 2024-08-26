import functools
import random
from typing import Union

import requests

from .resume import ResumeSmall, ResumeLarge
from .vacancy import VacancySmall, VacancyLarge
from .html_parsers import HHHtmlParser
PROXIES = [
    {
        'https': 'http://Io2Ar8:iN20YYFn5r@109.248.12.192:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@46.8.17.237:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@109.248.12.55:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@46.8.192.11:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@46.8.22.2:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@46.8.22.201:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@212.115.49.28:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@109.248.142.144:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@45.11.21.40:1050',
    },

    {
        'https': 'http://Io2Ar8:iN20YYFn5r@188.130.128.142:1050',
    },

]


def set_random_proxy(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if PROXIES:
            self._session.proxies.update(random.choice(PROXIES))
        return method(self, *args, **kwargs)

    return wrapper

class HHParser:
    login_url = "/account/login"
    resumes_page = "/applicant/resumes"
    vacancy_response = "/applicant/vacancy_response/popup"

    def __init__(self, host):
        self._host = host
        self._session = requests.session()
        self._set_session_param()

    def _set_session_param(self) -> None:
        """
            Установка базовых параметров для сессии requests
        """
        self._session.verify = False
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }
    @set_random_proxy
    def login(self, login: str, password: str) -> None:
        """
            Авторизация на сайте
        :param login: Логин/почта
        :param password: Пароль
        """
        response = self._session.get(self._host + self.login_url)
        response.raise_for_status()
        xsrf_token = HHHtmlParser.get_xsrf_token(response.text)
        response = self._session.post(self._host + self.login_url, data={
            "_xsrf": xsrf_token,
            "failUrl": "/account/login?backurl=%2F",
            "accountType": "APPLICANT",
            "remember": "yes",
            "username": login,
            "password": password,
            "isBot": False,
            "captchaText": None,
        })
        response.raise_for_status()

    def get_resumes_small(self) -> tuple[ResumeSmall, ...]:
        """
            Получить краткие резюме
        """
        response = self._session.get(self._host + self.resumes_page)
        response.raise_for_status()
        return HHHtmlParser.get_resumes_small(response.text)

    def get_resume_large(self, resume_id: str) -> ResumeLarge:
        """
            Получение полного резюме
        :param resume_id: ID резюме, у которого необходимо собрать инфу
        """
        response = self._session.get(self._host + self.resumes_page + "/" + resume_id)
        response.raise_for_status()
        return HHHtmlParser.get_resume_large(response.text)

    @set_random_proxy
    def get_vacancies_small(self, query: str, only_in_title=False, from_IT_company=False) -> tuple[VacancySmall, ...]:
        """
            Получаем все вакансии по запросу.
            Функция генератор, отдает вакансии по одной странице
        :param query: строка запроса
        :param only_in_title: Поиск только в названии вакансий
        :param from_IT_company: Поиск только от акредитованных IT компаний
        """
        query = query.replace(" ", "+")
        page = 0
        while True:
            # response = self._session.get(self._host + f"/vacancies/{query}?page={page}")
            url = f"/search/vacancy?page={page}" \
                  f"&order_by=relevance" \
                  f"&search_period=0" \
                  f"&items_on_page=10" \
                  f"&hhtmFrom=vacancy_search_filter" \
                  f"&text={query}"
            if only_in_title:
                url += "&search_field=name"
            if from_IT_company:
                url += "&label=accredited_it"

            response = self._session.get(self._host+url)
            response.raise_for_status()
            vacancies = HHHtmlParser.get_vacancies_small(response.text)

            if not vacancies: break

            yield vacancies

            page += 1

    @set_random_proxy
    def send_response_to_vacancy(self, vacancy: Union[VacancySmall, VacancyLarge],
                                 resume: Union[ResumeSmall, ResumeLarge], resume_only_one=False) -> dict:
        """
            Отправка отклика на вакансию
        :param vacancy: вакансия на которую отправится отклик
        :param resume: резюме, которое будет приложено
        """

        if resume_only_one:
            response = self._session.post(self._host + self.vacancy_response, json={
                "vacancy_id": vacancy.id,
                "resume_hash": resume.id,
                "mark_applicant_visible_in_vacancy_country": False,
                "ignore_postponed": True,
                "lux": True,
                "letterRequired": False,

            }, headers={"Accept": "application/json", })
            response.raise_for_status()
        else:
            response = self._session.get(self._host + vacancy.link_response)
            response.raise_for_status()
            xsrf_token = HHHtmlParser.get_xsrf_token(response.text)
            response = self._session.post(self._host+self.vacancy_response, data={
                "_xsrf": xsrf_token,
                "vacancy_id": vacancy.id,
                "resume_hash": resume.id,
                "mark_applicant_visible_in_vacancy_country": False,


            }, headers={"Accept": "application/json",})
            response.raise_for_status()


        return response.json()

    @property
    def host(self):
        return self._host
