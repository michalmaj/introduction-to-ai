[English](answers.md) | **Polski**

# Lekcja 1.4 — odpowiedzi

Zajrzyj tutaj dopiero po własnej próbie. Pytania znajdziesz w [lekcji](../../../modules/01_agents/04_history_of_ai/README.pl.md).

## 1. Dlaczego perceptron czekał kilkadziesiąt lat

Jednowarstwowy perceptron ma poważne ograniczenia: nie rozwiąże nawet problemu XOR. Minsky i Papert pokazali to w 1969 roku i zainteresowanie sieciami spadło. Sieci wielowarstwowe nie mają tego ograniczenia, ale brakowało skutecznego sposobu ich trenowania. Taki sposób, propagację wsteczną, spopularyzowano dopiero w 1986 roku. Pełne możliwości ujawniły się jeszcze później, około 2012 roku, gdy pojawiły się ogromne zbiory danych i wystarczająca moc obliczeniowa, w tym karty graficzne.

Dobra odpowiedź zawiera:

- ograniczenie jednowarstwowego perceptronu (XOR, rok 1969);
- propagację wsteczną jako sposób trenowania sieci wielowarstwowych;
- rolę danych i mocy obliczeniowej w przełomie po 2012 roku.

## 2. Źródło wiedzy: system ekspertowy a model językowy

Wiedzę systemu ekspertowego zapisywali ręcznie ludzie (inżynierowie wiedzy i eksperci) jako jawne reguły. Każdą regułę da się przeczytać i sprawdzić. Duży model językowy uzyskuje wiedzę w trakcie uczenia na ogromnych zbiorach tekstu, a przechowuje ją w milionach albo miliardach parametrów, których nie da się przeczytać jak reguł. Pierwsze podejście jest przejrzyste, ale wymaga żmudnej ręcznej pracy i jest kruche. Drugie skaluje się bez ręcznego zapisywania wiedzy, ale jest trudniejsze do wyjaśnienia i weryfikacji.

Dobra odpowiedź zawiera:

- ręcznie zapisane reguły w systemie ekspertowym;
- wiedzę wyuczoną z danych i ukrytą w parametrach modelu językowego;
- konsekwencje: przejrzystość kontra skalowalność.

## 3. Przyczyny „zim AI”

Obie zimy zaczęły się od rozczarowania. Zapowiedzi wyprzedzały możliwości. Metody działające na małych przykładach nie skalowały się (eksplozja przestrzeni stanów), a systemy ekspertowe okazały się drogie w utrzymaniu i kruche. Gdy wyniki nie spełniły oczekiwań, malało finansowanie i zainteresowanie. Podobne ryzyko istnieje i dziś: gdy oczekiwania wobec AI rosną szybciej niż jej rzeczywiste możliwości i niezawodność, rozczarowanie może znów ograniczyć inwestycje. Różnicą jest to, że dzisiejsze systemy są już szeroko używane w praktyce.

Dobra odpowiedź zawiera:

- rozdźwięk między zapowiedziami a możliwościami;
- przynajmniej jedną techniczną przyczynę: brak skalowania albo kruchość;
- uzasadnioną opinię o dzisiejszym ryzyku.

## 4. System łączący obie tradycje

AlphaGo (2016). Sieci neuronowe, czyli tradycja ucząca się, oceniały pozycje i podpowiadały obiecujące ruchy, czego dla gry go nie dało się dobrze opisać ręcznymi regułami. Przeszukiwanie drzewa gry, czyli tradycja symboliczna, planowało kolejne posunięcia, korzystając z tych ocen. Każda część robi to, w czym jest dobra: sieć daje „intuicję”, a przeszukiwanie systematycznie sprawdza konsekwencje.

Dobra odpowiedź zawiera:

- konkretny system z osi czasu;
- rolę części uczącej się i części symbolicznej;
- uzasadnienie, dlaczego połączenie działa lepiej niż każda część osobno.
