from bs4 import BeautifulSoup

from .resume import ResumeSmall, ResumeLarge
from .vacancy import VacancySmall


def get_soup(method):
    """
        Обертка для методов парсера, чтобы каждый раз не прописывать создание супа
    :param method: метод декорирования
    """
    def _wrapper(cls, html: str):
        soup = BeautifulSoup(html, features="lxml")
        return method(cls, soup)
    return _wrapper


class HHHtmlParser:
    """
        Парсер необходимых данных из самого HTML
    """

    @classmethod
    @get_soup
    def get_resume_large(cls, soup: BeautifulSoup) -> ResumeLarge:
        resume_tag = soup.select_one(".resume-applicant")
        return ResumeLarge(resume_tag)


    @classmethod
    @get_soup
    def get_vacancies_small(cls, soup: BeautifulSoup) -> tuple[VacancySmall, ...]:
        # vacancy_tables = soup.select(".vacancy-search-item__card")
        vacancy_tables = soup.select('[data-sentry-element="Element"]')
        return tuple(VacancySmall(vacancy_table) for vacancy_table in vacancy_tables)


    @classmethod
    @get_soup
    def get_resumes_small(cls, soup: BeautifulSoup) -> tuple[ResumeSmall, ...]:
        resume_tables = soup.select(".applicant-resumes-card-wrapper")
        return tuple(ResumeSmall(resume_table) for resume_table in resume_tables)

    @classmethod
    @get_soup
    def get_xsrf_token(cls, soup: BeautifulSoup ) -> str:
        return soup.select_one("input[name='_xsrf']").get('value')

    @classmethod
    @get_soup
    def get_vk_login_button(cls, soup: BeautifulSoup ):
        return soup.select_one("a.bloko-social-icon_vk")
