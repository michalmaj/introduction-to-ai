[English](README.md) | **Polski**

# Lekcja 1.1 — Czym jest AI

**Core** · Wymagania: 0.1 Instalacja i praca z samouczkiem. To lekcja koncepcyjna, bez zadania programistycznego.

## Cele lekcji

Po tej lekcji:

- wyjaśnisz, dlaczego „sztuczna inteligencja” ma kilka definicji i czym się one różnią;
- opiszesz test Turinga i jego ograniczenia;
- wyjaśnisz, kim jest racjonalny agent i dlaczego ten kurs przyjmuje właśnie to ujęcie;
- odróżnisz AI wąską od ogólnej oraz podejście symboliczne od uczącego się;
- przeanalizujesz prawdziwy system: co postrzega, co robi i jak mierzymy jego sukces.

## Problem

Filtr antyspamowy, program szachowy, nawigacja samochodowa, robot w magazynie i czatbot obsługi klienta: wszystkie te systemy nazywamy „sztuczną inteligencją”. Co je łączy? Czy termostat też jest AI? Żeby odpowiadać na takie pytania, potrzebujemy wspólnego słownika. Ta lekcja go wprowadza.

## Cztery ujęcia AI

Definicje AI różnią się w dwóch sprawach. Po pierwsze, czy liczy się **myślenie**, czy **działanie**. Po drugie, czy wzorcem jest **człowiek**, czy **racjonalność**, czyli robienie tego, co najlepsze z punktu widzenia celu. Daje to cztery ujęcia (podział za Russellem i Norvigiem):

| | Wzorcem jest człowiek | Wzorcem jest racjonalność |
|---|---|---|
| **Myślenie** | modelowanie poznawcze: odtworzyć, jak myśli człowiek | „prawa myślenia”: poprawne wnioskowanie logiczne |
| **Działanie** | test Turinga: zachowywać się jak człowiek | racjonalny agent: działać najlepiej, jak się da |

- **Myśleć po ludzku.** Ten cel łączy AI z kognitywistyką. Żeby go osiągnąć, trzeba najpierw wiedzieć, jak działa ludzki umysł, a to wciąż w dużej mierze otwarte pytanie.
- **Działać po ludzku.** Alan Turing w 1950 roku zaproponował próbę, dziś zwaną **testem Turinga**. Sędzia prowadzi rozmowę tekstową z człowiekiem i z maszyną. Jeśli nie potrafi wiarygodnie wskazać, która jest która, maszyna zdaje test. Test mierzy jednak podobieństwo do człowieka, a nie skuteczność. Może nagradzać udawanie, na przykład celowe literówki, a krótka, gładka rozmowa nie dowodzi zrozumienia.
- **Myśleć racjonalnie.** To tradycja logiki: z prawdziwych przesłanek wyprowadzać prawdziwe wnioski. Ma dwa kłopoty. Nie każdą wiedzę da się zapisać w postaci logicznej, zwłaszcza wiedzę niepewną. Poza tym poprawne wnioskowanie samo z siebie nie mówi, co zrobić.
- **Działać racjonalnie.** Agent wybiera działania, które przy jego wiedzy dają najlepszy oczekiwany wynik. To ujęcie jest najogólniejsze, bo poprawne wnioskowanie jest tylko jednym ze sposobów, by dobrze działać. Jest też mierzalne i nie wymaga naśladowania człowieka.

Ten kurs przyjmuje czwarte ujęcie: **AI to projektowanie racjonalnych agentów.**

## Racjonalny agent

**Agent** to wszystko, co postrzega swoje otoczenie (przez sensory) i na nie oddziałuje (przez aktuatory). Robot w magazynie postrzega przeszkody i paczki, a działa, jeżdżąc i podnosząc paczki. Program szachowy „postrzega” pozycję na szachownicy, a działa, wykonując ruchy.

**Agent racjonalny** po każdej sekwencji percepcji wybiera akcję, która według jego wiedzy maksymalizuje oczekiwaną **miarę jakości**, czyli ustaloną z góry ocenę tego, jak dobrze agent działa.

Racjonalność to nie wszechwiedza. Liczy się najlepszy wybór przy wiedzy, którą agent ma w chwili decyzji, a nie to, jak sprawy potoczyły się potem. Jeśli robot wybrał najkrótszą znaną trasę, a w alejce niespodziewanie stanął wózek, robot nie przestaje być racjonalny. Szczegóły, czyli percepcja, akcje, miara jakości i rodzaje środowisk, omawia lekcja 1.2.

## AI wąska i ogólna

**AI wąska** dobrze rozwiązuje określone zadanie, na przykład gra w szachy, rozpoznaje mowę albo wyznacza trasę. Takie są niemal wszystkie działające dziś systemy.

**AI ogólna** umiałaby uczyć się i rozwiązywać bardzo szeroki zakres zadań, podobnie jak człowiek. To cel badań i przedmiot sporów: nie ma zgody ani co do definicji, ani co do tego, czy i kiedy taki system powstanie. Współczesne duże modele językowe radzą sobie z wieloma różnymi zadaniami, ale ich ograniczenia (lekcja 9.2) pokazują, jak daleko jest do pewności w tej sprawie.

## Dwie tradycje: symboliczna i ucząca się

- **Podejście symboliczne:** wiedza i procedury są zapisane jawnie, jako reguły, logika albo opis problemu do przeszukania. Tak działają moduły 2–5 tego kursu. Zaletą jest przejrzystość, bo da się wyjaśnić, dlaczego system zdecydował tak, a nie inaczej. Wadami są kruchość wobec sytuacji, których nikt nie przewidział, i żmudne ręczne zapisywanie wiedzy.
- **Podejście uczące się:** zachowanie jest wyuczone z danych, na przykład przez sieć neuronową. Tak działają moduły 7–9. Zaletą jest radzenie sobie z percepcją i nieostrymi wzorcami. Wadami są potrzeba dużej ilości danych i trudniejsze wyjaśnianie decyzji.

Wiele współczesnych systemów łączy obie tradycje. Na przykład AlphaGo (2016) łączył sieci neuronowe z przeszukiwaniem drzewa gry (Monte Carlo Tree Search).

## Częste błędne przekonania

1. **„AI to uczenie maszynowe.”** Uczenie maszynowe to tylko część AI. Przeszukiwanie, gry, logika czy planowanie to techniki AI, które niczego się nie uczą.
2. **„Racjonalny system nigdy się nie myli.”** Racjonalność oznacza najlepszy wybór przy dostępnej wiedzy, a nie nieomylność.
3. **„Zdanie testu Turinga dowodzi zrozumienia.”** Test sprawdza tylko, czy maszynę da się odróżnić od człowieka w rozmowie.
4. **„Im bardziej system przypomina człowieka, tym jest lepszy.”** Agenta oceniamy według miary jakości jego zadania, a nie według podobieństwa do ludzi.

## Zadanie: analiza systemów

Dla każdego z pięciu systemów odpowiedz na pytania (a)–(e). Pisz w zeszycie, w pliku tekstowym, gdziekolwiek: liczy się Twoje uzasadnienie.

Systemy:

1. Filtr antyspamowy w poczcie elektronicznej.
2. Program grający w szachy.
3. Aplikacja nawigacji samochodowej.
4. Robot magazynowy zbierający paczki.
5. Czatbot obsługi klienta w sklepie internetowym.

Pytania:

- (a) Co system postrzega (jakie ma wejście)?
- (b) Jakie działania może wykonać?
- (c) Jak zmierzyć, czy działa dobrze (miara jakości)?
- (d) Czy uczy się z danych, czy działa według zapisanych reguł, a może łączy oba?
- (e) Które z czterech ujęć AI najlepiej go opisuje i dlaczego?

Niektóre odpowiedzi są dyskusyjne, zwłaszcza (d) i (e). Porównując się z odpowiedziami wzorcowymi, sprawdzaj uzasadnienie, a nie dosłowne brzmienie.

## Jak sprawdzić

Ta lekcja nie ma testów automatycznych, bo odpowiedzi są opisowe. Po własnej próbie porównaj je z [odpowiedziami wzorcowymi](../../../solutions/01_agents/01_what_is_ai/answers.pl.md). Przy każdej odpowiedzi jest lista „dobra odpowiedź zawiera”, według której możesz ocenić swoją.

## Pytania kontrolne

1. Czym różni się podejście „działać po ludzku” od „działać racjonalnie”? Podaj przykład systemu, dla którego ta różnica ma znaczenie.
2. Dlaczego zdanie testu Turinga nie byłoby dobrą miarą skuteczności robota magazynowego?
3. Czy termostat jest agentem? Czy jest racjonalny?
4. Podaj jedną zaletę i jedną wadę podejścia symbolicznego oraz podejścia uczącego się.

## Co zapamiętać

- AI można definiować przez myślenie albo działanie, z człowiekiem albo racjonalnością jako wzorcem.
- Ten kurs patrzy na AI jak na projektowanie racjonalnych agentów: wybierać działania, które według wiedzy agenta dają najlepszy oczekiwany wynik.
- Racjonalność to nie wszechwiedza ani nieomylność.
- AI to więcej niż uczenie maszynowe. Tradycje symboliczna i ucząca się się uzupełniają.

## Co dalej

- Następna lekcja: [1.2 Agent i środowisko](../02_agents_and_environments/README.pl.md).

## Bibliografia

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, rozdz. 1.
- A. M. Turing, *Computing Machinery and Intelligence*, Mind 59 (236), 1950, s. 433–460.
