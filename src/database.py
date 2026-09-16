import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("data/helpdesk.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id TEXT UNIQUE NOT NULL,
            employee TEXT,
            description TEXT NOT NULL,
            category TEXT,
            priority TEXT,
            confidence REAL,
            faq_title TEXT,
            faq_solution TEXT,
            response TEXT,
            status TEXT DEFAULT 'Open',
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def create_ticket(
    employee,
    description,
    category,
    priority,
    confidence,
    faq_title,
    faq_solution,
    response
):
    conn = get_connection()

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    conn.execute(
        """
        INSERT INTO tickets (
            ticket_id,
            employee,
            description,
            category,
            priority,
            confidence,
            faq_title,
            faq_solution,
            response,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            f"HD-{timestamp}",
            employee,
            description,
            category,
            priority,
            confidence,
            faq_title,
            faq_solution,
            response,
            "Open",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    conn.commit()

    ticket_id = conn.execute(
        "SELECT ticket_id FROM tickets ORDER BY id DESC LIMIT 1"
    ).fetchone()[0]

    conn.close()

    return ticket_id


def get_all_tickets():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            ticket_id,
            employee,
            description,
            category,
            priority,
            confidence,
            status,
            created_at
        FROM tickets
        ORDER BY id DESC
        """
    ).fetchall()

    conn.close()

    return rows


def update_ticket_status(ticket_id, status):
    conn = get_connection()

    conn.execute(
        """
        UPDATE tickets
        SET status = ?
        WHERE ticket_id = ?
        """,
        (status, ticket_id),
    )

    conn.commit()
    conn.close()