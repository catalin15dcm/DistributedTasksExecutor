import sqlite3

DB_FILE = "jobs.db"

def init_db():
    """Initializes the database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            job_id TEXT PRIMARY KEY,
            task TEXT NOT NULL,
            finished BOOLEAN DEFAULT 0,
            answer TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            worker_name TEXT PRIMARY KEY,
            last_seen INTEGER
        )
    """)

    conn.commit()
    conn.close()

def add_job(job_id, task):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO jobs (job_id, task) VALUES (?, ?)", (job_id, task))
    conn.commit()
    conn.close()

def update_job(job_id, answer):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE jobs SET finished = 1, answer = ? WHERE job_id = ?", (answer, job_id))
    conn.commit()
    conn.close()

def get_job(job_id):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT job_id, finished, answer FROM jobs WHERE job_id = ?", (job_id,))
    job = cursor.fetchone()
    conn.close()
    return job
