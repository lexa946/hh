from bs4 import Tag


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
