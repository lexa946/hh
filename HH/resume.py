import re
from collections import namedtuple
from typing import List, Tuple

from bs4 import Tag

WorkExperience = namedtuple('WorkExperience', ('year', 'month'))


class CompanyExperience:
    def __init__(self, name=None, work_experience=None, position=None, experience_description=None):
        self.name = name
        self.work_experience = work_experience
        self.position = position
        self.experience_description = experience_description


    def __repr__(self):
        return f"<CompanyExperience {self.name}>"

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
        Полное отображение резюме.
    """

    def __init__(self, tag: Tag):
        self._tag = tag
        self.id = self._tag.select_one("a[data-qa='resume-block-photo-edit']")['href'][37:75]
        self.name = self._tag.select_one(".resume-block__title-text-wrapper").text
        self.img_link = self._tag.select_one(".resume-media__image")['src']
        self.specialization_category = tuple(
            tag.text for tag in self._tag.select("[data-qa='resume-block-position-specialization']"))

        self.employment = self._tag.select_one("[data-qa='resume-block-position'] p:nth-child(2)").text[11:]
        self.work_graphic = self._tag.select_one("[data-qa='resume-block-position'] p:nth-child(3)").text[15:]
        self.travel_time = self._tag.select_one("[data-qa='resume-block-position'] p:nth-child(4)").text[36:]
        self.business_trip = self._tag.select_one("[data-qa='resume-block-position'] p:nth-child(5)").text

        self.search_status = self._tag.select_one("[data-qa='job-search-status']").text

        self.phone = self._tag.select_one("[data-qa='resume-contacts-phone'] a")['href'][4:]
        self.email = self._tag.select_one("[data-qa='resume-contact-email'] a").text

        self.total_work_experience = self._get_work_experience(
            self._tag.select_one("[data-qa='resume-block-experience'] h2"))
        self.work_companies = self._get_work_companies()
        self.description = self._tag.select_one("[data-qa='resume-block-skills-content']").text

        # TODO: Надо дописать сбор полной статистики по резюме. Портфолио, Электронные сетификаты, Образование, Рекомендации.
        #  и проверить как будет работать, если резюме вообще пустое.



    def _get_work_experience(self, tag_from: Tag) -> WorkExperience:
        """
            Возвращает абочий стаж из тега
        """
        year, month = re.findall(r"\d+", tag_from.text)
        return WorkExperience(year, month)

    def _get_work_companies(self) -> tuple[CompanyExperience, ...]:
        """
        :return: Возвращает список компаний, где работал сотрудник
        """
        companies = []
        for company_tag in self._tag.select("[data-qa='resume-block-experience'] .resume-block-item-gap")[1:]:
            company = CompanyExperience()
            company.name = company_tag.select_one(".bloko-text_strong").text
            company.position = company_tag.select_one("[data-qa='resume-block-experience-position']").text
            company.experience_description = company_tag.select_one(
                "[data-qa='resume-block-experience-description']").text

            experience_tag = company_tag.select_one("[data-sentry-element='Column'] .bloko-text_tertiary")
            company.work_experience = self._get_work_experience(experience_tag)
            companies.append(company)
        return tuple(companies)
