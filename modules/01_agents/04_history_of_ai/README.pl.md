[English](README.md) | **Polski**

# Lekcja 1.4 — Krótka historia AI

**Opcjonalna** · Wymagania: 1.3 Typy agentów i sformułowanie problemu. To lekcja koncepcyjna, bez zadania programistycznego.

## Cele lekcji

Po tej lekcji:

- umieścisz najważniejsze wydarzenia historii AI na osi czasu;
- wyjaśnisz, czym były „zimy AI” i co do nich doprowadziło;
- opiszesz, jak przeplatały się tradycje symboliczna i ucząca się;
- spojrzysz z dystansem na dzisiejsze obietnice dotyczące AI.

## Dlaczego historia

Historia AI to kilka cykli wielkich oczekiwań i rozczarowań. Metody uznane za ślepy zaułek wracały po latach jako przełom. Kto zna te cykle, łatwiej oddziela trwałe idee od mody i rozsądniej ocenia, co obecne systemy naprawdę potrafią.

## Oś czasu

| Rok | Wydarzenie | Dlaczego ważne | W kursie |
|---|---|---|---|
| 1943 | McCulloch i Pitts opisują matematyczny model neuronu | pierwszy krok w stronę sieci neuronowych | moduł 7 |
| 1950 | Turing publikuje *Computing Machinery and Intelligence* | pytanie „czy maszyny mogą myśleć?” i test Turinga | lekcja 1.1 |
| 1956 | warsztaty w Dartmouth | narodziny AI jako dziedziny; nazwa „artificial intelligence” pojawia się we wniosku o te warsztaty | — |
| 1956–1959 | Logic Theorist i General Problem Solver (Newell, Simon, Shaw) | rozwiązywanie problemów jako przeszukiwanie | moduł 2 |
| 1958 | perceptron Rosenblatta | maszyna, która uczy się z przykładów | moduł 7 |
| 1966 | ELIZA (Weizenbaum) | proste reguły dają złudzenie rozmowy z człowiekiem | moduł 9 |
| 1969 | *Perceptrons* (Minsky, Papert) | pokazują ograniczenia jednowarstwowego perceptronu, na przykład problem XOR | lekcja 7.3 |
| 1973 | raport Lighthilla w Wielkiej Brytanii | krytyczna ocena dorobku AI i cięcia finansowania | — |
| lata 70. i 80. | systemy ekspertowe, na przykład MYCIN (diagnoza zakażeń) i XCON (konfiguracja komputerów) | wiedza ekspertów zapisana jako reguły; komercyjny boom w latach 80. | moduł 5 |
| 1986 | spopularyzowanie propagacji wstecznej (Rumelhart, Hinton, Williams) | da się trenować sieci wielowarstwowe | moduł 7 |
| lata 90. | rozwój metod probabilistycznych i uczenia maszynowego | rozumowanie przy niepewności, uczenie z danych | moduły 6 i 7 |
| 1997 | Deep Blue wygrywa mecz z Kasparowem | przeszukiwanie drzewa gry na ogromną skalę | moduł 3 |
| 2012 | AlexNet wygrywa konkurs ImageNet z dużą przewagą | początek ery głębokiego uczenia | moduł 7 |
| 2016 | AlphaGo wygrywa z Lee Sedolem | sieci neuronowe połączone z przeszukiwaniem | moduły 3 i 8 |
| 2017 | architektura Transformer (*Attention Is All You Need*) | podstawa dzisiejszych dużych modeli językowych | moduł 9 |
| 2022 | ChatGPT udostępniony publicznie | duże modele językowe trafiają do szerokiego użytku | moduł 9 |

## Fale optymizmu i „zimy AI”

Po Dartmouth panował wielki optymizm. Pierwsze programy dowodziły twierdzeń i rozwiązywały łamigłówki, a niektórzy badacze zapowiadali maszyny dorównujące ludziom w ciągu kilkudziesięciu lat. Metody działające na małych przykładach nie skalowały się jednak do prawdziwych problemów, bo przestrzeń stanów eksplodowała, jak w lekcji 1.3, a ludzkiej wiedzy nie umiano zapisać. Rozczarowanie, symbolizowane przez raport Lighthilla, przyniosło w latach 70. cięcia finansowania. To pierwsza **zima AI**.

W latach 80. nastąpił boom systemów ekspertowych. Okazały się jednak kosztowne w utrzymaniu, kruche poza wąską dziedziną i trudne do rozbudowy. Pod koniec lat 80. rynek się załamał i nadeszła druga zima.

## Dwie tradycje

- **Tradycja symboliczna** (przeszukiwanie, logika, reguły) dominowała od lat 50. do 80.
- **Tradycja ucząca się** (perceptron, sieci neuronowe) zaczęła się równie wcześnie. Po krytyce z 1969 roku zeszła w cień, wróciła w 1986 roku z propagacją wsteczną, a po 2012 roku, dzięki ogromnej ilości danych i mocy obliczeniowej, zdominowała wiele zastosowań.

Najciekawsze systemy często łączą obie tradycje. AlphaGo połączył sieci neuronowe z przeszukiwaniem drzewa gry, a Deep Blue z 1997 roku był niemal czystym przeszukiwaniem.

## Czego uczy historia

1. **Obietnice wyprzedzały możliwości.** Kolejne zimy zaczynały się od rozczarowania zbyt śmiałymi zapowiedziami.
2. **Idee wracają.** Sieci neuronowe czekały kilkadziesiąt lat, aż pojawią się dane, moc obliczeniowa i metody uczenia, które pozwoliły w pełni wykorzystać ich możliwości.
3. **Skala ma znaczenie.** Wiele przełomów, od Deep Blue po duże modele językowe, wynikało tyleż z nowych pomysłów, co z ogromnego wzrostu mocy obliczeniowej i ilości danych.
4. **Tradycje się uzupełniają.** Spór „symbole czy uczenie” rzadko kończy się zwycięstwem jednej strony.

## Jak sprawdzić

Ta lekcja nie ma testów automatycznych. Po własnej próbie porównaj odpowiedzi na pytania kontrolne z [odpowiedziami wzorcowymi](../../../solutions/01_agents/04_history_of_ai/answers.pl.md).

## Pytania kontrolne

1. Dlaczego idea perceptronu z 1958 roku przyniosła wielkie sukcesy dopiero po kilkudziesięciu latach?
2. Czym różni się źródło wiedzy systemu ekspertowego od źródła wiedzy dużego modelu językowego?
3. Co doprowadziło do „zim AI”? Czy podobne ryzyko istnieje dziś?
4. Wskaż na osi czasu przykład systemu, który łączy obie tradycje, i wyjaśnij, co każda z nich wnosi.

## Co zapamiętać

- AI jako dziedzina ma swój początek w 1956 roku (Dartmouth), ale jej idee sięgają lat 40. i 50.
- Historia AI to cykle optymizmu i rozczarowań, zwane zimami AI.
- Tradycje symboliczna i ucząca się przeplatały się i coraz częściej się łączą.
- Wiele przełomów zależało od danych i mocy obliczeniowej, nie tylko od nowych idei.

## Co dalej

- Moduł 2 zaczyna przeszukiwanie, czyli jedną z najstarszych technik AI. Listę lekcji znajdziesz w [mapie kursu](../../../COURSE_MAP.pl.md).

## Bibliografia

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, rozdz. 1.3 (historia AI).
- A. M. Turing, *Computing Machinery and Intelligence*, Mind 59 (236), 1950, s. 433–460.
