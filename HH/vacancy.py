from bs4 import Tag
from lxml import html


class VacancySmall:
    """
        Краткое отображение вакансии.
        https://nn.hh.ru/search/vacancy - тут примеры
    """
    def __init__(self, tag: Tag):
        self._tag = tag
        self._tree = html.fromstring(str(self._tag))
        self.name = self._tag.select_one("h2").text
        self.link = self._tag.select_one("h2 a")['href']

        experience_tag = self._tag.select_one("[data-qa='vacancy-serp__vacancy-work-experience']")
        self.experience = experience_tag.text if experience_tag else None

        remote_work_tag = self._tag.select_one("[data-qa='vacancy-label-remote-work-schedule']")
        self.can_remote = True if remote_work_tag else False

        # TODO: Какой-то тут не надежный селектор, надо подумать как сделать лучше
        cost_tag = self._tag.select_one(".compensation-text--kTJ0_rp54B2vNeZ3CTt2")
        self.cost = cost_tag.text if cost_tag else None

    def __repr__(self):
        return f"<VacancySmall {self.name}>"
