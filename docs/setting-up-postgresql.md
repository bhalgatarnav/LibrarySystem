# Setting Up PostgreSQL

These are my notes from setting up PostgreSQL on my Mac for the Database Design and Development final project. I am writing this as I go, so I have a record of what each command does and why I ran it.

## Installing PostgreSQL

I used Homebrew, which is a package manager for macOS, to install PostgreSQL.

```bash
brew install postgresql@16
```

This downloads and installs PostgreSQL version 16 along with the command line tools I need to interact with it.

## Starting the PostgreSQL Service

```bash
brew services start postgresql@16
```

PostgreSQL runs as a background service, meaning it needs to be running before I can connect to it. This command starts that service so it stays running in the background, even after I close my terminal.

I can check that it installed correctly with:

```bash
psql --version
```

`psql` is the command line tool used to interact with PostgreSQL. This command just confirms the version installed.

## Creating a Database

```bash
createdb library_db
```

A single PostgreSQL installation can hold many separate databases. This command creates a new, empty database named `library_db` for my library management system project. At this point, it has no tables yet.

## Running My Schema File

```bash
psql -d library_db -f library_schema.sql
```

This connects to the `library_db` database and runs every SQL command inside `library_schema.sql` in order, from top to bottom. The `-d` flag tells `psql` which database to connect to, and the `-f` flag tells it to run commands from a file instead of typing them one at a time.

### Understanding the Output

When I ran this, I saw a few `NOTICE` messages saying a table did not exist and was being skipped. This is expected. My schema file starts with `DROP TABLE IF EXISTS` for each table, which is a safety step that deletes old versions of a table before recreating it. Since this was my first time running the file, there was nothing to delete yet, so PostgreSQL just let me know and moved on.

After that, I saw a line for each `CREATE TABLE` statement and each `INSERT` statement, confirming they ran successfully. The number after `INSERT 0` tells me how many rows were added by that statement.

## Connecting to the Database Interactively

```bash
psql -d library_db
```

This opens an interactive session where I can type SQL commands directly and see results immediately, instead of running them from a file.

A few useful commands inside this session:

- `\dt` lists all the tables in the current database.
- `SELECT * FROM Member;` shows every row in the Member table.
- `\q` exits the session and returns to the regular terminal.