# Zadanie testowe PY - staże Skygate W18

https://docs.google.com/document/d/11liwY2o6ZTWITK4zY1uWSwqszecyZbLCOJf1SZ1PN4g/edit

<!-- W nowoczesnym magazynie znajduje się 10 autonomicznych półek ustawionych w jednej linii do ładowni ciężarówek. Półki te potrafią same się przestawiać, dzięki czemu możliwy jest szybszy dostęp do zamówionych produktów.

Półki ustawiają się samoczynnie w nocy. Kiedy w trakcie ładunku towarów jest konieczna zmiana ustawień półek, półki mogą przesunąć się tylko do przodu, a półka znajdująca się na początku wędruje na koniec (jak w przypadku kolejki cyklicznej)

Na każdej półce znajduje się miejsce na 10 jednostek spośród jednego do trzech z 5 typów produktów. (Dla przykładu półka posiadająca 7 jednostek jabłek i 3 jednostki pomarańczy)
Do magazynu codziennie przyjeżdżają odbiorcy towaru w z góry zaplanowanej kolejności (10 transportów).

Każdy transport stara się zabrać 5 jednostek jednego typu produktu, po który przyjechał. Ciężarówka transportowa nie będzie nigdy żądać jednocześnie kilku typów produktów lub innej ilości niż 5 jednostek.

W przypadku kiedy w magazynie zabraknie danego typu towaru, transport odjedzie niepełny lub pusty.

W nocy półki powinny sortować się w taki sposób, aby czas załadunku wszystkich ciężarówek był w sumie jak najkrótszy.
Korzystając z django rest framework, flask, dowolnego innego frameworka lub czystego języka pythona napisz aplikację, która:
- umożliwi tworzenie, aktualizowanie i usuwanie typów towarów, półek i transportów
- pozwoli pobrać przez frontend listę półek wraz z ich zawartością oraz listę transportów
- przy pobraniu listy półek otrzymamy na miarę własnych możliwości optymalnie posortowane półki w taki sposób, aby obsłużyć wszystkie transporty z jak najmniejszą ilością przesunięć półek

W zadaniu należy wykorzystać relacyjną bazę danych, stworzyć odpowiednie modele oraz relacje.

Kod powinien posiadać testy jednostkowe i integracyjne tam, gdzie jest to potrzebne (z wykorzystaniem mocków jeśli jest to niezbędne)

Proszę się nie przejmować, jeżeli zaimplementowany algorytm nie będzie bardzo optymalny, dla nas ważniejsza jest umiejętność rozwiązywania problemów, nie chcielibyśmy aby poszukiwanie idealnego rozwiązania sprawiło, że projekt nie zostałoby ukończone :)
 -->

At the moment, the solution is far from complete. However, the models are defined and you can fiddle with the database using the `admin/` panel (which provides basic CRUD functionality).

The only other view available now is at `shelves/` url, and it displays all the shelves in the storehouse and all the loads in them.

The project is still in development phase, therefore the `settings.py` file has not been updated etc., but I have rebased the `master` branch onto my `working` branch in order to make it clear that there is anything at all that works in the repository.

After having cloned the repo (and installed Django), running the `./scripts/setup.sh` script:
* starts a server at port 8000 (in the background),
* creates a database and loads a fixture - a sample randomly generated set of data,
* creates a superuser *admin* with a *pass* password.

In order to flush the database and reload the fixture, run `bash ./scripts/flush_and_fill.sh`.
Running `python ./scripts/fill_database.py` will populate the **empty** database with a brand new random set of objects: shelves, loads on them, and (empty) transports.

Note: the `SECRET_KEY` is in a separate file, and has not been pushed to GitHub. For the time being the above instructions will not work, then!

----

I used: (see also `requirements.txt`)

python3.5
Django2.0
