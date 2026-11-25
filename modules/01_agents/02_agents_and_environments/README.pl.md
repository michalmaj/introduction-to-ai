[English](README.md) | **Polski**

# Lekcja 1.2 — Agent i środowisko

**Core** · Wymagania: 1.1 Czym jest AI.

## Cele lekcji

Po tej lekcji:

- opiszesz agenta przez jego percepcje, akcje i miarę jakości;
- odróżnisz funkcję agenta od programu agenta;
- opiszesz zadanie agenta w schemacie PEAS;
- sklasyfikujesz środowisko według sześciu własności;
- zaimplementujesz agenta reaktywnego i zobaczysz w eksperymencie, gdzie kończą się jego możliwości.

## Problem

Robot w magazynie ma zebrać paczki. Nie widzi całej hali. W każdym kroku wie tylko, czy na jego polu leży paczka i w których z czterech kierunków droga jest wolna. Jak taki robot ma działać? I jak ocenić, czy działa dobrze?

Ta lekcja wprowadza słownik do opisu takich sytuacji, czyli agenta i jego środowisko, oraz pierwszy, najprostszy rodzaj agenta.

## Agent, percepcja, akcja

- **Percepcja** to to, co agent odbiera z otoczenia w danej chwili. **Sekwencja percepcji** to wszystko, co odebrał od początku.
- **Akcja** to to, co agent robi. Działając, zmienia środowisko.
- **Funkcja agenta** to abstrakcyjny opis zachowania: każdej sekwencji percepcji przypisuje akcję.
- **Program agenta** to konkretny kod, który tę funkcję realizuje na rzeczywistej maszynie.

W naszym świecie, zwanym dalej **światem paczek** (`introai.agents`):

| Element | Opis |
|---|---|
| Percepcja | `Percept(parcel_here, free)`: czy na polu robota leży paczka oraz wolne kierunki w kolejności N, E, S, W |
| Akcje | `N`, `E`, `S`, `W` (jedź), `PICK` (podnieś paczkę), `WAIT` (czekaj) |
| Ruch w przeszkodę | robot uderza w nią i zostaje na miejscu |
| Koniec epizodu | wszystkie paczki zebrane albo wyczerpany limit kroków |

## Miara jakości i racjonalność

**Miara jakości** ocenia, jak dobrze agent wykonał zadanie. W świecie paczek:

- każda akcja kosztuje **1 punkt**;
- każda zebrana paczka daje **10 punktów**.

Koszt akcji sprawia, że liczy się nie tylko to, *czy* robot zbierze paczki, ale też *jak szybko*.

Ważna zasada: miarę jakości definiujemy przez **stan środowiska**, czyli to, co chcemy osiągnąć, a nie przez to, jak naszym zdaniem agent powinien się zachowywać. Gdybyśmy nagradzali „dużo jeżdżenia”, dostalibyśmy robota, który jeździ w kółko i niczego nie zbiera.

Jak w lekcji 1.1, **agent racjonalny** wybiera akcję, która według jego wiedzy maksymalizuje oczekiwaną miarę jakości. To, czy agent jest racjonalny, zależy od czterech rzeczy:

- od miary jakości;
- od wiedzy, którą ma na starcie;
- od dostępnych akcji;
- od dotychczasowej sekwencji percepcji.

## PEAS

Zadanie agenta wygodnie opisać czterema składnikami, w skrócie **PEAS**:

| | Robot w świecie paczek |
|---|---|
| **P**erformance (miara jakości) | +10 za paczkę, −1 za każdą akcję |
| **E**nvironment (środowisko) | hala z regałami, paczki leżące na podłodze |
| **A**ctuators (aktuatory) | koła (ruch w czterech kierunkach) i chwytak (`PICK`) |
| **S**ensors (sensory) | czujnik paczki na własnym polu, czujniki przeszkód w czterech kierunkach |

## Własności środowisk

| Własność | Pytanie | Możliwe odpowiedzi |
|---|---|---|
| obserwowalność | Czy percepcja pokazuje cały stan istotny dla decyzji? | w pełni (`fully`) albo częściowo (`partially`) |
| liczba agentów | Czy w środowisku działają inni agenci? | jeden (`single`) albo wielu (`multi`) |
| determinizm | Czy stan i akcja jednoznacznie wyznaczają następny stan? | deterministyczne (`deterministic`) albo stochastyczne (`stochastic`) |
| epizodyczność | Czy decyzje są niezależnymi epizodami, czy obecna akcja wpływa na przyszłe sytuacje? | epizodyczne (`episodic`) albo sekwencyjne (`sequential`) |
| zmienność | Czy środowisko może się zmienić, gdy agent się namyśla? | statyczne (`static`) albo dynamiczne (`dynamic`) |
| ciągłość | Czy stany, czas i akcje mają skończenie wiele dyskretnych wartości? | dyskretne (`discrete`) albo ciągłe (`continuous`) |

Przykłady spoza magazynu:

- Szachy bez zegara są w pełni obserwowalne, deterministyczne i dyskretne, ale mają dwóch agentów.
- Prowadzenie samochodu jest częściowo obserwowalne, stochastyczne, dynamiczne i ciągłe.
- Rozpoznawanie, czy na zdjęciu jest kot, jest epizodyczne, bo każde zdjęcie to osobna decyzja.

## Dwa warianty magazynu

To dwa opisy potrzebne do części A zadania.

**Wariant 1** to świat paczek z tej lekcji:

- robot pracuje w hali sam;
- czuje tylko, czy na jego polu leży paczka, i które z czterech sąsiednich pól są wolne;
- każda akcja ma zawsze ten sam skutek: ruch na wolne pole zawsze się udaje, ruch w przeszkodę zawsze kończy się uderzeniem;
- nic poza robotem się nie zmienia;
- hala to siatka pól, a robot działa w krokach.

**Wariant 2** to ta sama hala, ale:

- robot dostaje w każdym kroku obraz z kamery pod sufitem, który pokazuje całą halę, wszystkie paczki i przeszkody;
- w hali jeżdżą jednocześnie inne roboty, które też zbierają paczki;
- koła się ślizgają: w 10% przypadków ruch się nie udaje i robot zostaje na miejscu;
- inne roboty poruszają się również wtedy, gdy nasz robot decyduje, co zrobić;
- hala nadal jest siatką pól, a robot nadal działa w krokach.

## Agent reaktywny

Najprostszy rodzaj agenta to **agent reaktywny** (*simple reflex agent*). Decyduje wyłącznie na podstawie bieżącej percepcji, według reguł „warunek → akcja”. Niczego nie pamięta.

Reguły naszego agenta, sprawdzane po kolei:

1. Jeśli na polu leży paczka, wykonaj `PICK`.
2. W przeciwnym razie jedź w pierwszym wolnym kierunku w kolejności N, E, S, W.
3. Jeśli żaden kierunek nie jest wolny, wykonaj `WAIT`.

## Prześledź ręcznie

Mapa `data/maps/parcels.txt` zawiera trzy paczki `P`:

```text
#######
#R.P#P#
#.#...#
#..P#D#
#######
```

Pierwsze kroki agenta reaktywnego:

<!-- generated:episode-table agent=reflex map=parcels steps=8 lang=pl -->
| Krok | Pole robota | Percepcja: paczka; wolne kierunki | Akcja | Punkty po kroku |
|---|---|---|---|---|
| 1 | (1, 1) | nie; E, S | E | -1 |
| 2 | (1, 2) | nie; E, W | E | -2 |
| 3 | (1, 3) | tak; S, W | PICK | 7 |
| 4 | (1, 3) | nie; S, W | S | 6 |
| 5 | (2, 3) | nie; N, E, S | N | 5 |
| 6 | (1, 3) | nie; S, W | S | 4 |
| 7 | (2, 3) | nie; N, E, S | N | 3 |
| 8 | (1, 3) | nie; S, W | S | 2 |

Po 8 krokach: zebrane paczki 1, wynik 2.
<!-- /generated -->

Od kroku 4 robot jeździ tam i z powrotem między `(1, 3)` a `(2, 3)`. Na `(1, 3)` reguła 2 wybiera S, bo N i E są zablokowane. Na `(2, 3)` ta sama reguła wybiera N, bo N jest wolne i ma pierwszeństwo. Agent nie pamięta, że przed chwilą tam był, więc ta pętla nigdy się nie skończy, choć dwie paczki wciąż czekają.

## Częste błędy

1. **Ignorowanie paczki.** Agent stoi na paczce, ale jedzie dalej, bo sprawdza kierunki przed paczką.
2. **Zła kolejność kierunków.** Reguła 2 wymaga kolejności N, E, S, W. Inna kolejność to inny agent.
3. **Wjazd w ścianę.** Agent ignoruje listę wolnych kierunków i jedzie tam, gdzie stoi przeszkoda.
4. **Brak reguły na zamknięcie.** Gdy nie ma dokąd jechać, agent mimo to próbuje ruchu zamiast czekać.

Testy lekcji wykrywają każdy z tych błędów.

## Zadanie

### Część A: własności środowisk

Uzupełnij w `task.py` słowniki `VARIANT_1` i `VARIANT_2`. Dla każdej z sześciu własności wybierz jedną z dwóch wartości podanych w komentarzu. Jeśli coś się nie zgadza, testy podają tylko liczbę błędnych odpowiedzi, a nie które to są. Inaczej przy dwóch możliwościach zdradzałyby wynik.

### Część B: agent reaktywny

Zaimplementuj `reflex_agent(percept)` według trzech reguł z sekcji „Agent reaktywny”. Funkcja zwraca jedną z akcji `N`, `E`, `S`, `W`, `PICK`, `WAIT`.

### Jak sprawdzić

```bash
uv run pytest modules/01_agents/02_agents_and_environments
```

### Kryteria akceptacji

- Wszystkie testy lekcji przechodzą.
- Potrafisz odpowiedzieć na pytania kontrolne.

## Czego testy nie sprawdzają

- **Czy reguły są dobre.** Testy sprawdzają tylko, czy agent wykonuje podane reguły, a eksperyment pokazuje, że te reguły są słabe.
- **Uzasadnienia odpowiedzi z części A.** Testy porównują wartości, ale nie Twoje rozumowanie.
- **Stylu i czytelności kodu.**

## Eksperymenty

Otwórz [experiments.pl.ipynb](experiments.pl.ipynb) i porównaj trzech agentów:

- losowego;
- reaktywnego (Twojego);
- wzorcowego agenta z pamięcią, który zapamiętuje, gdzie już był.

Przed uruchomieniem zapisz, który agent według Ciebie wypadnie najlepiej, a który najgorzej, najpierw na mapie `parcels`, a potem na większej mapie z alejkami.

## Pytania kontrolne

1. Dlaczego agent reaktywny utknął, choć do zebrania zostały dwie paczki? Czego mu brakuje?
2. Dlaczego miarę jakości lepiej definiować przez stan środowiska (zebrane paczki) niż przez zachowanie agenta (na przykład „robot dużo jeździ”)?
3. Która własność wariantu 2 najbardziej utrudnia projektowanie agenta i dlaczego?
4. Czy agent losowy jest racjonalny w świecie paczek?

## Jeśli utkniesz

<details>
<summary>Podpowiedź 1: kolejność reguł</summary>

Reguły sprawdzasz od góry: najpierw paczka, potem ruch, na końcu czekanie. W kodzie to po prostu trzy kolejne warunki `if` z `return`.

</details>

<details>
<summary>Podpowiedź 2: pierwszy wolny kierunek</summary>

`percept.free` jest już uporządkowane w kolejności N, E, S, W. Pierwszy wolny kierunek to po prostu pierwszy element tej krotki, jeśli nie jest pusta.

</details>

## Co zapamiętać

- Agenta opisujemy przez percepcje, akcje i miarę jakości. Zadanie opisujemy w schemacie PEAS.
- Miarę jakości definiujemy przez stan środowiska, a nie przez pożądane zachowanie agenta.
- Środowiska klasyfikujemy według sześciu własności. Od nich zależy, jakiego agenta potrzebujemy.
- Agent reaktywny jest prosty i szybki, ale niczego nie pamięta. W częściowo obserwowalnym świecie łatwo wpada w pętle.

## Co dalej

- Po własnej próbie porównaj się z [rozwiązaniem i odpowiedziami](../../../solutions/01_agents/02_agents_and_environments/).
- Następna lekcja, [1.3 Typy agentów i sformułowanie problemu](../03_problem_formulation/README.pl.md), pokazuje agentów, którzy pamiętają i planują.

## Bibliografia

- S. Russell, P. Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed., Pearson, 2020, rozdz. 2.
