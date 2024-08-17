from typing import Tuple

import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse
from urllib.parse import parse_qs


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


    @property
    def host(self):
        return self._host




class HHHtmlParser:
    @classmethod
    def get_resumes_small(cls, html: str) -> tuple["ResumeSmall", ...]:
        soup = BeautifulSoup(html)
        resume_tables = soup.select(".applicant-resumes-card-wrapper")
        return tuple(ResumeSmall(resume_table) for resume_table in resume_tables)

    @classmethod
    def get_xsrf_token(cls, html: str) -> str:
        soup = BeautifulSoup(html)
        return soup.select_one("input[name='_xsrf']").get('value')

    @classmethod
    def get_vk_login_button(cls, html: str):
        soup = BeautifulSoup(html)
        return soup.select_one("a.bloko-social-icon_vk")


class ResumeSmall:
    """
        Краткое отображение резюме.
        https://nn.hh.ru/applicant/resumes - берется от сюда
    """
    def __init__(self, tag: Tag):
        self._tag = tag
        self.id = self._tag.select_one("h3 a")['href'][8:46]
        self.name = self._tag.select_one("h3").text
        self.description = self._tag.select_one(".applicant-resumes-action.applicant-resumes-action_second").text
        self.week_statistic = {
            "search": self._tag.select_one("[data-qa='search-shows'] span:nth-child(1)").text,
            "view": self._tag.select_one("[data-qa='count-new-views'] span:nth-child(1)").text,
            "invite": self._tag.select_one("[data-qa='new-invitations'] span:nth-child(1)").text,
        }

    def __repr__(self):
        return f"<ResumeSmall {self.id} | {self.name}>"


class ResumeLarge:
    """
        Полное резюме
    """
    # TODO: Описать полное резюме
    pass
