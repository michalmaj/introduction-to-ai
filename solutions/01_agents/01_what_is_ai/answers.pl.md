[English](answers.md) | **Polski**

# Lekcja 1.1 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Treść zadania znajdziesz w [lekcji](../../../modules/01_agents/01_what_is_ai/README.pl.md). Przy pytaniach (d) i (e) możliwe są inne dobrze uzasadnione odpowiedzi.

## Analiza systemów

### 1. Filtr antyspamowy

- **(a) Postrzega:** treść i nagłówki wiadomości, czyli nadawcę, słowa, linki i załączniki. Czasem też oznaczenia „to spam” dodawane przez użytkownika.
- **(b) Działania:** przenosi wiadomość do spamu albo zostawia ją w skrzynce odbiorczej.
- **(c) Miara jakości:** jak dużo spamu wyłapuje i jak rzadko myli zwykłą wiadomość ze spamem. Ten drugi błąd jest zwykle droższy, bo ważny list może przepaść.
- **(d) Uczenie czy reguły:** zwykle oba. Klasyfikator uczy się na oznaczonych wiadomościach, a do tego dochodzą reguły, na przykład listy zablokowanych nadawców.
- **(e) Ujęcie:** działać racjonalnie, czyli maksymalizować jakość klasyfikacji. Nikt nie oczekuje, że filtr będzie się zachowywał jak człowiek.

### 2. Program szachowy

- **(a) Postrzega:** całą pozycję na szachownicy i historię ruchów.
- **(b) Działania:** dozwolone ruchy.
- **(c) Miara jakości:** wynik partii (wygrana, remis, przegrana), a w dłuższej perspektywie ranking.
- **(d) Uczenie czy reguły:** klasyczne programy łączą przeszukiwanie drzewa gry z ręcznie zaprojektowaną funkcją oceny pozycji. Nowsze uczą się oceny, grając same ze sobą. Moduł 3 pokazuje przeszukiwanie.
- **(e) Ujęcie:** działać racjonalnie: wybrać ruch, który daje najlepszy oczekiwany wynik.

### 3. Nawigacja samochodowa

- **(a) Postrzega:** mapę drogową, pozycję z GPS i dane o ruchu.
- **(b) Działania:** proponuje trasę, wydaje polecenia „skręć w prawo” i wyznacza trasę od nowa.
- **(c) Miara jakości:** czas przejazdu lub długość trasy oraz trafność przewidywanego czasu przyjazdu.
- **(d) Uczenie czy reguły:** wyznaczanie trasy to przeszukiwanie grafu dróg (moduł 2), czyli podejście symboliczne. Przewidywanie korków często jest uczone z danych.
- **(e) Ujęcie:** działać racjonalnie.

### 4. Robot magazynowy

- **(a) Postrzega:** odczyty czujników, czyli przeszkody i paczki, a czasem też swoją pozycję.
- **(b) Działania:** jedzie, podnosi paczkę, czeka.
- **(c) Miara jakości:** liczba paczek zebranych w danym czasie, zużycie energii i brak kolizji.
- **(d) Uczenie czy reguły:** zależy od robota. Może działać według zapisanych reguł (lekcja 1.2), planować trasę (moduł 2) albo uczyć się nawigacji (moduł 8).
- **(e) Ujęcie:** działać racjonalnie: liczy się skuteczność, nie podobieństwo do człowieka.

### 5. Czatbot obsługi klienta

- **(a) Postrzega:** wiadomości klienta, a czasem też dane zamówienia.
- **(b) Działania:** odpowiada, zadaje pytania, przekazuje sprawę człowiekowi, a czasem wykonuje operacje, na przykład sprawdza status przesyłki.
- **(c) Miara jakości:** odsetek spraw rozwiązanych poprawnie, zadowolenie klienta, brak błędnych informacji oraz przekazanie sprawy człowiekowi wtedy, gdy trzeba.
- **(d) Uczenie czy reguły:** współczesne czatboty opierają się na modelach językowych uczonych na danych, a starsze na scenariuszach rozmowy pisanych ręcznie.
- **(e) Ujęcie:** zachowuje się *po ludzku*, bo rozmawia, ale oceniać go warto *racjonalnie*, czyli po tym, czy rozwiązał sprawę. To dobry przykład, że naturalna rozmowa i skuteczność to różne rzeczy (moduł 9).

Dobra analiza:

- odróżnia to, co system postrzega, od tego, co robi;
- podaje mierzalną miarę jakości, a nie ogólne „działa dobrze”;
- zauważa, że wiele systemów łączy reguły z uczeniem;
- uzasadnia wybór ujęcia AI.

## Pytania kontrolne

### 1. „Działać po ludzku” a „działać racjonalnie”

Działać po ludzku to zachowywać się tak, żeby nie dało się odróżnić systemu od człowieka. Działać racjonalnie to wybierać działania, które dają najlepszy wynik według miary jakości. Różnica ma znaczenie wtedy, gdy człowiek działa nieoptymalnie. Nawigacja „po ludzku” powtarzałaby typowe ludzkie błędy, na przykład wybór znanej, ale wolniejszej drogi. Nawigacja racjonalna wybierze szybszą. Podobnie czatbot może brzmieć naturalnie i mimo to podać nieprawdziwą informację.

Dobra odpowiedź zawiera:

- kryterium porównania z człowiekiem dla ujęcia ludzkiego;
- kryterium miary jakości dla ujęcia racjonalnego;
- przykład, w którym oba kryteria prowadzą do różnych zachowań.

### 2. Test Turinga a robot magazynowy

Test Turinga sprawdza, czy rozmowy z maszyną nie da się odróżnić od rozmowy z człowiekiem. Robot magazynowy nie rozmawia. Liczy się to, czy szybko i bezpiecznie zbiera paczki. Robot, który „zdałby” jakiś test podobieństwa do człowieka, mógłby jednocześnie zbierać paczki wolno i z kolizjami. Właściwą miarą jest miara jakości zadania.

Dobra odpowiedź zawiera:

- informację, że test mierzy nieodróżnialność od człowieka w rozmowie;
- uwagę, że robota oceniamy po wykonaniu zadania;
- przynajmniej jeden konkretny element miary jakości robota.

### 3. Termostat

Termostat jest agentem. Postrzega temperaturę (sensor) i włącza albo wyłącza ogrzewanie (aktuator). To bardzo prosty agent reaktywny: działa według reguły „za zimno, więc grzej”. W ramach swojej wąskiej miary jakości, czyli utrzymywania zadanej temperatury, jest racjonalny, bo przy tym, co postrzega, wybiera właściwą akcję. To pokazuje, że „agent” i „racjonalny” nie oznaczają „inteligentny jak człowiek”.

Dobra odpowiedź zawiera:

- wskazanie sensora i aktuatora termostatu;
- ocenę racjonalności względem konkretnej miary jakości;
- uwagę, że agent racjonalny nie musi być złożony.

### 4. Zalety i wady obu podejść

- **Podejście symboliczne.** Zaleta: przejrzystość i wyjaśnialność, bo widać regułę albo plan, który doprowadził do decyzji. Wada: kruchość wobec nieprzewidzianych sytuacji i żmudne ręczne zapisywanie wiedzy.
- **Podejście uczące się.** Zaleta: radzi sobie z percepcją i wzorcami, których nie umiemy opisać regułami, na przykład z rozpoznawaniem obrazów. Wada: potrzebuje dużo danych, a jego decyzje trudniej wyjaśnić.

Dobra odpowiedź zawiera:

- po jednej zalecie i jednej wadzie dla każdego podejścia;
- przynajmniej jeden konkretny przykład.
