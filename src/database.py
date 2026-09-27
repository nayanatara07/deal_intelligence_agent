"""SQLite database models for deal metadata."""
import os
import sqlite3
import json
from datetime import datetime
from typing import Optional
from contextlib import contextmanager

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "deals.db")


def init_db():
    """Initialize the database with all tables."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS deals (
                id TEXT PRIMARY KEY,
                company TEXT NOT NULL,
                industry TEXT NOT NULL,
                value REAL NOT NULL,
                stage TEXT NOT NULL,
                created_at TEXT NOT NULL,
                metadata TEXT
            );

            CREATE TABLE IF NOT EXISTS calls (
                id TEXT PRIMARY KEY,
                deal_id TEXT NOT NULL,
                call_number INTEGER NOT NULL,
                call_date TEXT NOT NULL,
                transcript TEXT NOT NULL,
                summary TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            );

            CREATE TABLE IF NOT EXISTS objections (
                id TEXT PRIMARY KEY,
                call_id TEXT NOT NULL,
                deal_id TEXT NOT NULL,
                text TEXT NOT NULL,
                raised_by TEXT,
                resolved BOOLEAN DEFAULT 0,
                tactic_used TEXT,
                FOREIGN KEY (call_id) REFERENCES calls(id),
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            );

            CREATE TABLE IF NOT EXISTS competitors (
                id TEXT PRIMARY KEY,
                call_id TEXT NOT NULL,
                deal_id TEXT NOT NULL,
                name TEXT NOT NULL,
                context TEXT,
                outcome TEXT,
                FOREIGN KEY (call_id) REFERENCES calls(id),
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            );

            CREATE TABLE IF NOT EXISTS pricing (
                id TEXT PRIMARY KEY,
                call_id TEXT NOT NULL,
                deal_id TEXT NOT NULL,
                amount REAL,
                discount REAL,
                approved BOOLEAN,
                notes TEXT,
                FOREIGN KEY (call_id) REFERENCES calls(id),
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            );

            CREATE TABLE IF NOT EXISTS tactics (
                id TEXT PRIMARY KEY,
                call_id TEXT NOT NULL,
                deal_id TEXT NOT NULL,
                description TEXT NOT NULL,
                outcome TEXT,
                effectiveness_score INTEGER,
                FOREIGN KEY (call_id) REFERENCES calls(id),
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            );

            CREATE TABLE IF NOT EXISTS stakeholders (
                id TEXT PRIMARY KEY,
                deal_id TEXT NOT NULL,
                name TEXT NOT NULL,
                role TEXT,
                sentiment TEXT,
                concerns TEXT,
                FOREIGN KEY (deal_id) REFERENCES deals(id)
            );
        """)


@contextmanager
def get_connection():
    """Get a database connection with row factory."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def insert_deal(deal_id, company, industry, value, stage, metadata=None):
    """Insert a new deal (or replace if exists)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO deals (id, company, industry, value, stage, created_at, metadata) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (deal_id, company, industry, value, stage, datetime.now().isoformat(), json.dumps(metadata) if metadata else None)
        )


def insert_call(call_id, deal_id, call_number, call_date, transcript, summary=None):
    """Insert a new call (or replace if exists)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO calls (id, deal_id, call_number, call_date, transcript, summary) VALUES (?, ?, ?, ?, ?, ?)",
            (call_id, deal_id, call_number, call_date, transcript, summary)
        )


def insert_objection(objection_id, call_id, deal_id, text, raised_by=None, resolved=0, tactic_used=None):
    """Insert an objection (or replace if exists)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO objections (id, call_id, deal_id, text, raised_by, resolved, tactic_used) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (objection_id, call_id, deal_id, text, raised_by, resolved, tactic_used)
        )


def insert_competitor(competitor_id, call_id, deal_id, name, context=None, outcome=None):
    """Insert a competitor mention (or replace if exists)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO competitors (id, call_id, deal_id, name, context, outcome) VALUES (?, ?, ?, ?, ?, ?)",
            (competitor_id, call_id, deal_id, name, context, outcome)
        )


def insert_pricing(pricing_id, call_id, deal_id, amount, discount=None, approved=None, notes=None):
    """Insert a pricing discussion (or replace if exists)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO pricing (id, call_id, deal_id, amount, discount, approved, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pricing_id, call_id, deal_id, amount, discount, approved, notes)
        )


def insert_tactic(tactic_id, call_id, deal_id, description, outcome=None, effectiveness_score=None):
    """Insert a tactic (or replace if exists)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO tactics (id, call_id, deal_id, description, outcome, effectiveness_score) VALUES (?, ?, ?, ?, ?, ?)",
            (tactic_id, call_id, deal_id, description, outcome, effectiveness_score)
        )


def insert_stakeholder(stakeholder_id, deal_id, name, role=None, sentiment=None, concerns=None):
    """Insert a stakeholder (or replace if exists)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO stakeholders (id, deal_id, name, role, sentiment, concerns) VALUES (?, ?, ?, ?, ?, ?)",
            (stakeholder_id, deal_id, name, role, sentiment, concerns)
        )


def get_deal(deal_id):
    """Get a deal by ID."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM deals WHERE id = ?", (deal_id,)).fetchone()
        return dict(row) if row else None


def get_all_deals():
    """Get all deals."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM deals ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


def get_calls_for_deal(deal_id):
    """Get all calls for a deal, ordered by call number."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM calls WHERE deal_id = ? ORDER BY call_number", (deal_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_objections_for_deal(deal_id):
    """Get all objections for a deal."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM objections WHERE deal_id = ? ORDER BY id", (deal_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_competitors_for_deal(deal_id):
    """Get all competitor mentions for a deal."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM competitors WHERE deal_id = ? ORDER BY id", (deal_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_pricing_for_deal(deal_id):
    """Get all pricing discussions for a deal."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM pricing WHERE deal_id = ? ORDER BY id", (deal_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_tactics_for_deal(deal_id):
    """Get all tactics for a deal."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tactics WHERE deal_id = ? ORDER BY id", (deal_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def get_stakeholders_for_deal(deal_id):
    """Get all stakeholders for a deal."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM stakeholders WHERE deal_id = ? ORDER BY id", (deal_id,)
        ).fetchall()
        return [dict(r) for r in rows]


def delete_deal_data(deal_id):
    """Delete all extracted data for a deal (for re-processing)."""
    with get_connection() as conn:
        conn.execute("DELETE FROM objections WHERE deal_id = ?", (deal_id,))
        conn.execute("DELETE FROM competitors WHERE deal_id = ?", (deal_id,))
        conn.execute("DELETE FROM pricing WHERE deal_id = ?", (deal_id,))
        conn.execute("DELETE FROM tactics WHERE deal_id = ?", (deal_id,))
        conn.execute("DELETE FROM stakeholders WHERE deal_id = ?", (deal_id,))
