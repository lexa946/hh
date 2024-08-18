from typing import Union

import requests

from .resume import ResumeSmall, ResumeLarge
from .vacancy import VacancySmall, VacancyLarge
from .html_parsers import HHHtmlParser


class HHParser:
    login_url = "/account/login"
    resumes_page = "/applicant/resumes"

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
        response = self._session.get(self._host + self.resumes_page + "/" +resume_id)
        response.raise_for_status()
        return HHHtmlParser.get_resume_large(response.text)


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
                  f"&items_on_page=20" \
                  f"&hhtmFrom=vacancy_search_filter" \
                  f"&text={query}"
            if only_in_title:
                url += "&search_field=name"
            if from_IT_company:
                url += "&label=accredited_it"

            response = self._session.get(self._host + f"/search/vacancy?page={page}"
                                                      f"")
            response.raise_for_status()
            vacancies = HHHtmlParser.get_vacancies_small(response.text)

            if not vacancies: break

            yield vacancies

            page += 1

    def send_response_to_vacancy(self, vacancy: Union[VacancySmall, VacancyLarge],
                                 resume: Union[ResumeSmall, ResumeLarge]) -> None:
        """
            Отправка отклика на вакансию
        :param vacancy: вакансия на которую отправится отклик
        :param resume: резюме, которое будет приложено
        """
        response = self._session.get(self._host + vacancy.link_response)
        response.raise_for_status()
        xsrf_token = HHHtmlParser.get_xsrf_token(response.text)
        response = self._session.post(self._host + vacancy.link_response, data={
            "_xsrf": xsrf_token,
            "vacancy_id": vacancy.id,
            "resume_hash": resume.id,
            "mark_applicant_visible_in_vacancy_country": False,

        })
        response.raise_for_status()

    @property
    def host(self):
        return self._host
