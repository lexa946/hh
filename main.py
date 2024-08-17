from HH import HHParser

from creds import HH_LOGIN, HH_PASSWORD

host = "https://hh.ru"

hh_parser = HHParser(host)

hh_parser.login(HH_LOGIN, HH_PASSWORD)

for vacancies in hh_parser.get_vacancies("Python Developer", only_in_title=True, from_IT_compony=True):
    for vacancy in vacancies:
        print(vacancy)
    print()
# my_resumes = hh_parser.get_resumes_small()
print()

