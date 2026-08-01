import psycopg2


def connect():
    """Return a live connection to the library_db database."""
    return psycopg2.connect(
        dbname="library_db",
        host="localhost",
        # No password required for a local Homebrew PostgreSQL install.
        # If you ever move this to a real server, pull the password from an
        # environment variable (os.environ["DB_PASSWORD"]) instead of hardcoding it.
    )
