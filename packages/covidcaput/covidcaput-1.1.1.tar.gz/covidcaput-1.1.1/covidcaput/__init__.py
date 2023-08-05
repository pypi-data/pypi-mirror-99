from covidcaput.covid_caput import TeamMember, support_generator


__version__ = '1.1.0'

team = [
    TeamMember(name="Paweł",
               support_message='Ich wünsche Ihnen eine baldige Genesung für Sie und die ganze Familie.'),

    TeamMember(name="Maks",
               support_message='Człowiek musi czasem chorować. Chociażby po to, żeby poczytać. '
                               'Zostaw to czytanie i wracaj do nas.'),

    TeamMember(name="Iza",
               support_message='Mam nadzieję, że całą rodziną czujecie się trochę lepiej.\n'
                               'Wracajcie szybko do zdrowia!\n'
                               'Daily bez Twojego "Dzień dobry" nie są już takie same, więc mam nadzieję, '
                               'że szybko się zobaczymy na Teamsach.\n'
                               'Pamiętaj, że zawsze możesz na nas liczyć.'),

    TeamMember(name="Tomek",
               support_message="Trzymaj się mocno i dużo wypoczywaj. Odpoczywanie to takie coś co się robi "
                               "jak się leży i nic nie robi. Dużo zdrowia dla Ciebie i całej rodziny!"),

    TeamMember(name="Natalia",
               support_message='Zasady obowiązująca na kwarantannie:\n'
                               '1) Każda pizza ma pomidory więc jest zdrowym, pełnowartościowym posiłkiem dla'
                               ' Twojego dziecka.\n'
                               '2) Nie istnieje coś takiego jak "za dużo" bajek.'),

    TeamMember(name="Kuba",
               support_message='Michał, bez Twojej dawki optymizmu nawet memy Maksa bawią jakoś mniej.\n'
                               'Kurujcie się kieleckimi metodami i wracaj jak najszybciej!')
]

anti_covid_generator = support_generator(team)

receiver = TeamMember('Michał', support_message="Jest koszernie.", is_sick=True)
while receiver.is_sick:
    print(next(anti_covid_generator), end="\n\n")


