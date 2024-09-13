from bs4 import Tag
import re

class VacancySmall:
    """
        Краткое отображение вакансии.
        https://nn.hh.ru/search/vacancy - тут примеры
    """
    def __init__(self, tag: Tag):
        self._tag = tag

        self.name = self._tag.select_one("h2").text
        self.link_more_info = self._tag.select_one("h2 a")['href']

        link_tag = self._tag.select_one("[data-qa='vacancy-serp__vacancy_response']")

        self.link_response = link_tag['href'] if link_tag else ""
        self.id = re.search(r"\d+", self.link_response)[0] if link_tag else ""

        experience_tag = self._tag.select_one("[data-qa='vacancy-serp__vacancy-work-experience']")
        self.experience = experience_tag.text if experience_tag else None

        remote_work_tag = self._tag.select_one("[data-qa='vacancy-label-remote-work-schedule']")
        self.can_remote = True if remote_work_tag else False

        # TODO: Какой-то тут не надежный селектор, надо подумать как сделать лучше
        cost_tag = self._tag.select_one(".compensation-text--kTJ0_rp54B2vNeZ3CTt2")
        self.cost = cost_tag.text if cost_tag else None

    def __repr__(self):
        return f"<VacancySmall {self.name}>"


class VacancyLarge:
    # TODO: описать полную вакансию
    pass
