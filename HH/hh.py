import requests

from HH.vacancy import VacancySmall
from HH.html_parsers import HHHtmlParser


class HHParser:
    login_url = "/account/login"
    resumes_page = "/applicant/resumes"

    def __init__(self, host):
        self._host = host
        self._session = requests.session()
        self._set_session_param()

    def _set_session_param(self):
        self._session.verify = False
        self._session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        }

    def login(self, login: str, password: str):
        """
            Авторизация на сайте
        :param login: Логин/почта
        :param password: Пароль
        """
        response = self._session.get(self._host + self.login_url)
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

    def get_resumes_small(self) -> tuple["ResumeSmall", ...]:
        """
            Получить краткие резюме
        """
        response = self._session.get(self._host + self.resumes_page)
        response.raise_for_status()
        return HHHtmlParser.get_resumes_small(response.text)

    def get_resume_large(self, resume_id):
        # TODO: Описать получение полного резюме
        pass

    def get_vacancies(self, query: str, only_in_title=False, from_IT_compony=False) -> tuple[VacancySmall, ...]:
        """
            Получаем все вакансии по запросу.
            Функция генератор, отдает вакансии по одной странице
        :param only_in_title: Поиск только в названии вакансий
        :param from_IT_compony: Поиск только от акредитованных IT компаний
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
            if from_IT_compony:
                url += "&label=accredited_it"

            response = self._session.get(self._host + f"/search/vacancy?page={page}"
                                                      f"")
            response.raise_for_status()
            vacancies = HHHtmlParser.get_vacancies_small(response.text)

            if not vacancies: break

            yield vacancies

            page += 1

    @property
    def host(self):
        return self._host






