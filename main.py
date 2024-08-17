from hh import HHParser

host = "https://nn.hh.ru"

hh_parser = HHParser(host)

hh_parser.login("pozhara98@mail.ru", "89108787515z")

my_resumes = hh_parser.get_resumes_small()
print()

