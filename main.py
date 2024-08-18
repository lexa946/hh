from HH import HHParser

from creds import HH_LOGIN, HH_PASSWORD

host = "https://hh.ru"

hh_parser = HHParser(host)

hh_parser.login(HH_LOGIN, HH_PASSWORD)

my_resumes = hh_parser.get_resumes_small()

developer_resume = my_resumes[0]
resume_large = hh_parser.get_resume_large(developer_resume.id)


for vacancies in hh_parser.get_vacancies_small("Python Developer", only_in_title=True, from_IT_company=True):
    for vacancy in vacancies:
        hh_parser.send_response_to_vacancy(vacancy, developer_resume)
    print()
print()

