# Test task PY - internships Skygate W18

https://docs.google.com/document/d/11liwY2o6ZTWITK4zY1uWSwqszecyZbLCOJf1SZ1PN4g/edit

At the moment, the solution is far from complete. However, the models are defined and you can fiddle with the database using the `admin/` panel (which provides basic CRUD functionality).

Another view available now is at `shelves/` url: it displays all the shelves in the storehouse and all the loads in them. It is also possible to add new shelves using a link at the top of the shelves' list (there is a limit of 10 on the number of shelves, however).

The algorithm sorting the shelves in the database depending on the order and types of transports is implemented in `sort_shelves.py` file. The last line (`transfer_all()` function) also fills the transports with loads from shelves and accordingly shifts the shelves, so the final result will not reflect the original order of shelves.

The project is still in development phase, therefore the `settings.py` file has not been updated etc., but I have rebased the `master` branch onto my `working` branch in order to make it clear that there is anything at all that works in the repository.

After having cloned the repo (and installed Django), running the `./scripts/setup.sh` script in bash console:
* starts a server at port 8000 (in the background),
* creates a database and loads a fixture - a sample, randomly generated set of data,
* creates a superuser *admin* with a *pass* password.

In order to flush the database and reload the fixture, run `bash ./scripts/flush_and_fill.sh`. Running `python ./scripts/fill_database.py` will populate the **empty** database with a brand new random set of objects: shelves, loads on them, and (empty) transports. (This takes a bit longer than loading a fixture, though.)

----

I used: (see also `requirements.txt`)

python3.5
Django2.0
