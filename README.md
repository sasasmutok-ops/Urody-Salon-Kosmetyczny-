## Instrukcja uruchomienia aktualnej wersji

1. Pobierz lub sklonuj repozytorium projektu.
2. Otwórz folder projektu w PyCharm.
3. Upewnij się, że jest zainstalowany Python 3.x.
4. Utwórz i aktywuj środowisko wirtualne:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
5. Zainstaluj wymagania:
   ```bash
   pip install -r requirements.txt
   ```
6. Uruchom aplikację:
   ```bash
   python main-window.py
   ```

### Opis działania aktualnej wersji

Aktualna wersja aplikacji Urody jest aplikacją desktopową stworzoną w Pythonie z wykorzystaniem Tkintera.

Po uruchomieniu programu użytkownik może korzystać z głównego interfejsu aplikacji i przechodzić do dostępnych funkcji.

#### Katalog usług
Plik `services.py` zawiera dane dotyczące dostępnych usług kosmetycznych, między innymi ich nazwy, ceny oraz przewidywany czas trwania.

#### Kalkulator ceny
Plik `calculator.py` odpowiada za wybór usług oraz obliczanie ich łącznej ceny. Użytkownik może wybrać kilka usług, a aplikacja oblicza sumę ich cen oraz czas trwania.

#### Planowanie wizyty
Moduły `appointment_planner.py` oraz `appointment_logic.py` odpowiadają za planowanie wizyty. Możliwe jest wybranie usługi, daty i godziny oraz sprawdzenie poprawności podanych danych.

Logika planowania uwzględnia między innymi poprawność daty i godziny oraz dostępność terminu.

#### Podsumowanie wizyty
Po wybraniu odpowiednich danych aplikacja może przedstawić podsumowanie planowanej wizyty wraz z wybranymi usługami i ich kosztami.

#### Testowanie
Plik `test_appointment.py` zawiera testy związane z logiką planowania wizyt.

### Aktualny stan projektu

Obecna wersja zawiera podstawową strukturę aplikacji oraz działające elementy MVP związane z katalogiem usług, kalkulacją ceny i planowaniem wizyty.

Projekt nie korzysta z zewnętrznej bazy danych ani serwera backendowego. Dane są obsługiwane lokalnie przez aplikację.







KARTA PROJEKTU
Urody – aplikacja desktopowa dla salonu kosmetycznego
1. Nazwa projektu
Urody – aplikacja desktopowa dla salonu kosmetycznego
2. Zespół i repozytorium
Nazwa zespołu: Urody Team Członkowie zespołu:
1	Oleksandr Smutok – GitHub: @sasasmutok-ops
1	Maksym Babenko – GitHub: @Mkreportuk20
1	Illia Podliesnov – GitHub: @prog123-ewer
Repozytorium GitHub: https://github.com/sasasmutok-ops/Urody-Salon-Kosmetyczny-
3. Branża
Branża beauty – salony kosmetyczne i usługi pielęgnacyjne.
4. Problem i użytkownicy
Problem:
Klienci salonów kosmetycznych często mają trudności z wyborem odpowiedniego zabiegu, poznaniem jego ceny oraz oszacowaniem czasu trwania wizyty. Małe salony potrzebują prostego sposobu prezentowania swoich usług i ułatwiania klientom planowania wizyt.
Rozwiązanie:
Urody to aplikacja desktopowa, która umożliwia przeglądanie oferty salonu kosmetycznego, obliczanie kosztów usług, planowanie wizyt oraz korzystanie z porad dotyczących pielęgnacji. Aplikacja będzie posiadać prosty i intuicyjny interfejs graficzny.
Główni użytkownicy:
1	Klienci salonów kosmetycznych.
1	Osoby zainteresowane pielęgnacją skóry i zabiegami kosmetycznymi.
1	Właściciele małych salonów kosmetycznych.
5. Główne funkcje
1	Katalog usług – prezentacja zabiegów kosmetycznych wraz z opisami, cenami i przewidywanym czasem trwania.
2	Kalkulator cen – automatyczne obliczanie łącznego kosztu wybranych usług.
3	Planer wizyty – wybór usług, daty i godziny oraz wyświetlanie podsumowania planowanej wizyty.
4	Poradnik pielęgnacyjny – prezentacja podstawowych wskazówek dotyczących pielęgnacji skóry i przygotowania do zabiegów kosmetycznych.
5	Informacje o salonie – wyświetlanie danych kontaktowych, adresu i godzin otwarcia.
6. Zakres MVP
Pierwsza wersja aplikacji będzie koncentrować się na najważniejszych funkcjach, które można zrealizować w ramach projektu studenckiego.
MVP będzie obejmować:
1	Graficzny katalog usług z przykładowymi cenami i czasem trwania zabiegów.
1	Wybór usług i kalkulator łącznej ceny.
1	Planer wizyty z możliwością wyboru daty i godziny.
1	Wyświetlanie podsumowania planowanej wizyty.
1	Informacje o salonie: adres, dane kontaktowe i godziny otwarcia.
1	Czytelny interfejs graficzny z przyciskami, formularzami i osobnymi widokami poszczególnych funkcji.
Urody • 1
Dane usług i cennik będą przechowywane lokalnie w plikach JSON lub bezpośrednio w kodzie programu. Aplikacja nie będzie wymagała bazy danych ani serwera backendowego.
7. Dodatkowe zadania
Jeżeli podstawowe funkcje zostaną ukończone przed terminem, projekt można rozszerzyć o następujące możliwości:
1	Zapisywanie podsumowania wizyty – zapisywanie informacji o wybranych usługach i ich cenach w pliku lokalnym.
1	Porównywarka pakietów – porównywanie cen pojedynczych zabiegów z przykładowymi pakietami promocyjnymi.
1	Kalkulator przychodów salonu – obliczanie szacunkowego przychodu na podstawie liczby klientów, dni pracy i średniej ceny usługi.
Dodatkowe zadania będą realizowane w Pythonie z wykorzystaniem Tkintera, bez bazy danych. Ich wykonanie będzie zależeć od dostępnego czasu i postępów zespołu.
8. Stos technologiczny
1	Python – główny język programowania odpowiedzialny za logikę aplikacji.
1	Tkinter – biblioteka do tworzenia graficznego interfejsu użytkownika (GUI).
1	JSON – przechowywanie przykładowych danych dotyczących usług, cen i czasu trwania zabiegów.
1	Git i GitHub – kontrola wersji oraz współpraca zespołowa.
1 PyCharm – środowisko programistyczne (IDE) wykorzystywane do pisania, uruchamiania i debugowania kodu.
1	AI(ChatGPT, Gemini, Cloude, Grok, Kimi, Gama) – narzędzie pomocnicze do szukania pomysłów, wyjaśniania błędów oraz wspierania pisania i sprawdzania kodu.
Aplikacja będzie programem desktopowym z interfejsem graficznym utworzonym w Tkinterze. Dane będą przechowywane lokalnie, bez wykorzystania bazy danych.
ChatGPT będzie wykorzystywany jako narzędzie wspierające proces tworzenia aplikacji. Sam program nie będzie wymagał połączenia z usługami sztucznej inteligencji ani płatnego API.
9. Podział ról w zespole
Oleksandr Smutok – koordynator projektu i Python developer: organizacja pracy, podział zadań, kontrola postępów i dokumentacja, a także implementacja katalogu usług, kalkulatora cen i głównej logiki aplikacji.
Illia Podliesnov – Python developer: implementacja planera wizyty i obsługa logiki związanej z planowaniem wizyt.
Maksym Babenko – UI/UX designer, Tkinter developer i tester: projektowanie interfejsu graficznego, rozmieszczenie elementów, poprawa wygody użytkowania, testowanie funkcji i poprawianie błędów.
Wszyscy członkowie zespołu będą uczestniczyć w testowaniu aplikacji, przeglądzie kodu i współpracy za pośrednictwem GitHuba. Podział zadań może być dostosowywany do postępów projektu.
10. Cel projektu
Celem projektu jest stworzenie prostej, estetycznej i funkcjonalnej aplikacji desktopowej dla branży beauty. Aplikacja ma ułatwiać użytkownikom zapoznanie się z ofertą salonu, wybór usług, obliczanie kosztów i planowanie wizyt.
Projekt będzie rozwijany etapami – najpierw zostanie zrealizowana podstawowa wersja MVP, a następnie, w zależności od dostępnego czasu i postępów zespołu, zostaną wykonane dodatkowe zadania.
Aplikacja zostanie stworzona w Pythonie z wykorzystaniem Tkintera. Do przechowywania danych będą używane pliki lokalne, dlatego tworzenie bazy danych i serwera backendowego nie będzie konieczne.

---

## Architektura aplikacji i lokalna lista wizyt

Projekt jest aplikacją desktopową w Pythonie/Tkinter. Nie korzysta z serwera; wszystkie zapisane wizyty są dostępne na komputerze, na którym uruchomiono program.

- `main-window.py` — okno aplikacji, menu, strony oraz ekran „Wszystkie wizyty”.
- `services.py` — katalog zabiegów, ceny i czas ich trwania.
- `calculator.py` — wybór zabiegów i obliczanie łącznej ceny.
- `modules/appointment_planner.py` — wybór usług i terminu wizyty; pola wyboru są płaskie i bez cienia.
- `modules/appointment_logic.py` — walidacja, wykrywanie zajętych terminów i zapis/odczyt.
- `appointments.json` — lokalne dane zapisanych wizyt; plik tworzy się przy pierwszym zapisie.
- `modules/assets/` — grafiki używane w interfejsie.
- `requirements.txt` — lista zewnętrznych zależności; obecnie nie są wymagane dodatkowe pakiety.

### Lista wizyt

Po zapisaniu terminu otwórz w menu „Wszystkie wizyty”. Ekran pokazuje zapisane wizyty posortowane od najnowszych, wraz z datą, godziną, usługami, czasem i ceną. Przycisk „Odśwież listę” wczytuje aktualne dane z `appointments.json`.

### Uruchomienie

W katalogu projektu utwórz i aktywuj środowisko, zainstaluj wymagania i uruchom aplikację:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main-window.py
```
