import time
from HH import HHParser
from creds import HH_LOGIN, HH_PASSWORD
from loguru import logger



import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)




logger.add("response.log")
host = "https://hh.ru"

hh_parser = HHParser(host)
hh_parser.login(HH_LOGIN, HH_PASSWORD)
my_resumes = hh_parser.get_resumes_small()
for resume in my_resumes:
    if "разработчик" in resume.name.lower():
        developer_resume = resume
        break

count = 10 # Тут ставь число кратное 10, если 5 , значит отправит 50 откликов




while True:
    for vacancies in hh_parser.get_vacancies_small("Разработчик Python", only_in_title=True, from_IT_company=True):
        for vacancy in vacancies:
            try:
                response = hh_parser.send_response_to_vacancy(vacancy, developer_resume, resume_only_one=False)
            except Exception as ex:
                print(ex)
                continue


            if response.get("error", ""):
                logger.error(f"Возникла ошибка {response} при отклике на вакансию {vacancy}. Ссылка на вакансию: {vacancy.link_more_info}.")
            else:
                logger.info(f"Отправил отклик на вакансию {vacancy}. Ссылка на вакансию: {vacancy.link_more_info}.")
            time.sleep(1)

        print(f"page {count}")
        if count > 0:
            count -= 1
        else:
            raise SystemExit
