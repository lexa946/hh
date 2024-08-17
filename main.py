from hh import HHParser

from creds import HH_LOGIN, HH_PASSWORD

host = "https://nn.hh.ru"

hh_parser = HHParser(host)

hh_parser.login(HH_LOGIN, HH_PASSWORD)

my_resumes = hh_parser.get_resumes_small()
print()

