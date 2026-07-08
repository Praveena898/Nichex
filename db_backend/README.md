# Digital Bodyguard — Database Setup (SQLite)

This is your working starter database. It's already been created and tested —
you just need to run it on your own machine now and understand what each file does.

## Files in this folder

```
db_backend/
  app/
    __init__.py
    database.py    # connects to SQLite, creates the .db file
    models.py       # your 5 tables, defined as Python classes
    crud.py          # functions to add/read data (Create, Read, Update, Delete)
  init_db.py          # RUN THIS FIRST — creates tables + sample data
  test_db.py           # RUN THIS SECOND — proves reading data back works
  requirements.txt
```

## Step-by-step

### Step 1 — Install dependencies
```bash
cd db_backend
pip install -r requirements.txt
```

### Step 2 — Create your database
```bash
python init_db.py
```
This creates a file called `digital_bodyguard.db` in this folder. That file
**is** your entire database — one file, nothing else to install or configure.

You should see:
```
Tables created in digital_bodyguard.db
Sample user created: id=1, email=praveena@example.com
Done. Open digital_bodyguard.db in DB Browser for SQLite to see it.
```

### Step 3 — See it visually
1. Download **DB Browser for SQLite** (free): https://sqlitebrowser.org/
2. Open `digital_bodyguard.db` in it
3. Click "Browse Data" and pick a table (e.g. `users`, `contacts`) from the dropdown
4. You'll see the sample row that `init_db.py` inserted — proof it worked

### Step 4 — Confirm reading works too
```bash
python test_db.py
```
This reads the sample data back out using the functions in `crud.py` and prints it.

## What each file actually does

- **`app/models.py`** — your schema. 5 tables: `users`, `contacts`, `calls`,
  `notifications`, `settings`. If you ever need to add a new field (e.g. a
  `location` column on calls), this is the only file you touch, then re-run
  `init_db.py`.
- **`app/crud.py`** — every action anyone will ever need to do to your database
  is one function here (`create_user`, `add_contact`, `save_call_result`, etc.).
  Nobody else on your team should write raw database code — they just call
  these functions.
- **`init_db.py`** — one-time setup script. Safe to re-run; it won't duplicate
  the sample user if it already exists.

## Where this connects to the rest of the project

- **Your friend doing validation/model work**: once their model produces a
  verdict, the *only* thing they need from you is calling
  `crud.save_call_result(db, user_id, verdict, confidence)` — that's the one
  function that writes a real ML result into your `calls` table. You don't
  need to understand their model, and they don't need to understand your
  database.
- **Whoever builds the API endpoints (FastAPI routes)**: they'll import from
  `app.crud` and `app.database.get_db` — your work here is already
  API-ready, nothing needs to change.
- **Frontend**: doesn't touch this at all directly — it only ever talks to
  the API layer, which talks to `crud.py`, which talks to the database.

## Next steps after this

Once this is working and you're comfortable with it, the natural next step
is wrapping these `crud.py` functions in actual FastAPI routes (e.g.
`POST /contacts` calls `crud.add_contact(...)`) so the frontend can reach
them over HTTP. Ask for that when you're ready — it reuses everything you
just built, you won't redo any of this.
