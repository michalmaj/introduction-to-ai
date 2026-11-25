[English](answers.md) | **Polski**

# Lekcja 1.2 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadań znajdziesz w [lekcji](../../../modules/01_agents/02_agents_and_environments/README.pl.md).

## Część A

| Własność | Wariant 1 | Wariant 2 |
|---|---|---|
| obserwowalność | `partially`: robot czuje tylko swoje pole i czterech sąsiadów | `fully`: kamera pokazuje całą halę |
| liczba agentów | `single`: robot pracuje sam | `multi`: w hali jeżdżą inne roboty |
| determinizm | `deterministic`: każda akcja ma zawsze ten sam skutek | `stochastic`: koła się ślizgają, ruch może się nie udać |
| epizodyczność | `sequential`: zebrana paczka znika, a pozycja robota wpływa na dalsze kroki | `sequential`: tak samo |
| zmienność | `static`: poza robotem nic się nie zmienia | `dynamic`: inne roboty jeżdżą, gdy nasz decyduje |
| ciągłość | `discrete`: siatka pól, kroki, sześć akcji | `discrete`: tak samo |

## Pytania kontrolne

### 1. Dlaczego agent reaktywny utknął

Agent reaktywny decyduje wyłącznie na podstawie bieżącej percepcji i niczego nie pamięta. Na polach `(1, 3)` i `(2, 3)` dostaje za każdym razem tę samą percepcję, więc wybiera tę samą akcję. W efekcie jeździ tam i z powrotem. Świat jest tylko częściowo obserwowalny: percepcja nie mówi, gdzie leżą pozostałe paczki ani gdzie robot już był. Agentowi brakuje **stanu wewnętrznego**, na przykład pamięci odwiedzonych pól, albo choćby losowości, która przerwałaby pętlę.

Dobra odpowiedź zawiera:

- informację, że agent decyduje tylko na podstawie bieżącej percepcji i nie ma pamięci;
- obserwację, że w pętli percepcje się powtarzają, więc powtarzają się też akcje;
- wskazanie, czego brakuje: stanu wewnętrznego (lekcja 1.3) albo losowości.

### 2. Miara jakości przez stan środowiska

Miara jakości ma mierzyć to, na czym nam naprawdę zależy, czyli zebrane paczki i czas pracy. Nagradzanie zachowania („dużo jeździ”) da się „oszukać”: agent maksymalizujący taką miarę jeździłby w kółko i niczego nie zbierał. Poza tym projektant często nie wie z góry, jakie zachowanie jest najlepsze, więc nie powinien go narzucać w mierze jakości.

Dobra odpowiedź zawiera:

- uwagę, że miara jakości ma odzwierciedlać cel, a nie środek;
- przykład zachowania, które maksymalizuje źle dobraną miarę bez realizacji celu.

### 3. Co najbardziej utrudnia wariant 2

Najtrudniejsze jest połączenie **wielu agentów** i **dynamiki**. Inne roboty mogą zabrać paczkę, do której nasz jedzie, albo zablokować alejkę, a świat zmienia się, gdy nasz robot się namyśla. Plan ułożony na podstawie jednego obrazu z kamery szybko się dezaktualizuje, więc robot musi stale obserwować i zmieniać plany. Stochastyczność dokłada jeszcze jedno: nawet dobry ruch może się nie udać. Pełna obserwowalność to w wariancie 2 ułatwienie, nie trudność.

Dobra odpowiedź zawiera:

- wskazanie własności, która utrudnia zadanie, z konkretnym skutkiem dla agenta;
- uwagę, że pełna obserwowalność ułatwia zadanie.

Inne dobrze uzasadnione wybory, na przykład stochastyczność, też są w porządku.

### 4. Czy agent losowy jest racjonalny

Nie. Agent racjonalny wybiera akcję maksymalizującą oczekiwaną miarę jakości przy swojej wiedzy. Agent losowy ignoruje percepcję: na przykład wykonuje `PICK`, gdy wie, że na polu nie ma paczki, i traci punkt, choć przy tej samej wiedzy istnieje lepsza akcja. Eksperyment pokazuje, że na mapie `parcels` agent losowy wypadł lepiej od reaktywnego. Nie świadczy to o racjonalności agenta losowego, tylko o tym, że nasz agent reaktywny też nie jest racjonalny, bo wpada w pętlę. Losowość bywa jednak użyteczna w świecie częściowo obserwowalnym jako sposób na wyrwanie się z pętli.

Dobra odpowiedź zawiera:

- definicję racjonalności odniesioną do percepcji i miary jakości;
- przykład akcji agenta losowego, która przy jego wiedzy jest gorsza od dostępnej;
- komentarz do wyniku eksperymentu: lepszy wynik nie oznacza racjonalności.

## Eksperymenty

Wyniki implementacji wzorcowych. Agent losowy ma ziarno 0.

| Mapa (limit kroków) | Agent | Wynik | Paczki | Kroki |
|---|---|---|---|---|
| `parcels` (300) | losowy | −205 | 3 z 3 | 235 |
| `parcels` (300) | reaktywny | −290 | 1 z 3 | 300 |
| `parcels` (300) | z pamięcią | 11 | 3 z 3 | 19 |
| `aisles` z 4 paczkami (1000) | losowy | −990 | 1 z 4 | 1000 |
| `aisles` z 4 paczkami (1000) | reaktywny | −1000 | 0 z 4 | 1000 |
| `aisles` z 4 paczkami (1000) | z pamięcią | −288 | 4 z 4 | 328 |

- **Na mapie `parcels`** agent reaktywny utyka po pierwszej paczce. Losowy, choć marnuje mnóstwo kroków, przypadkiem zbiera wszystkie. Agent z pamięcią zbiera trzy paczki w 19 krokach, bo prowadzą go mało odwiedzane pola.
- **Na alejkach** agent losowy i reaktywny prawie niczego nie zbierają. Agent z pamięcią zbiera wszystkie cztery paczki, ale jego wynik jest wciąż ujemny: nie wie, gdzie leżą paczki, więc musi przeszukać dużą część hali. Gdyby znał całą mapę, mógłby planować (lekcja 1.3 i moduł 2).
