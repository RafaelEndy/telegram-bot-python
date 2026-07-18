"""
Camada de persistencia do bot - gerencia as tarefas de cada usuario em um
banco SQLite. Cada usuario do Telegram (identificado pelo user_id) tem
sua propria lista de tarefas, isolada das demais.
"""

import sqlite3
from contextlib import contextmanager
from typing import Optional

DB_PATH = "tasks.db"


@contextmanager
def get_connection(db_path: str = DB_PATH):
    """Abre uma conexao com o banco, garantindo que ela sempre seja fechada."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db(db_path: str = DB_PATH) -> None:
    """Cria a tabela de tarefas caso ainda nao exista."""
    with get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                description TEXT NOT NULL,
                done        INTEGER NOT NULL DEFAULT 0,
                created_at  TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )


def add_task(user_id: int, description: str, db_path: str = DB_PATH) -> int:
    """Adiciona uma nova tarefa para o usuario. Retorna o id da tarefa criada."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (user_id, description) VALUES (?, ?)",
            (user_id, description),
        )
        return cursor.lastrowid


def list_tasks(user_id: int, include_done: bool = False, db_path: str = DB_PATH) -> list[sqlite3.Row]:
    """Lista as tarefas do usuario. Por padrao, so retorna as pendentes."""
    with get_connection(db_path) as conn:
        if include_done:
            query = "SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at"
        else:
            query = "SELECT * FROM tasks WHERE user_id = ? AND done = 0 ORDER BY created_at"
        return conn.execute(query, (user_id,)).fetchall()


def mark_done(user_id: int, task_id: int, db_path: str = DB_PATH) -> bool:
    """Marca uma tarefa como concluida. Retorna True se a tarefa existia."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "UPDATE tasks SET done = 1 WHERE id = ? AND user_id = ?",
            (task_id, user_id),
        )
        return cursor.rowcount > 0


def remove_task(user_id: int, task_id: int, db_path: str = DB_PATH) -> bool:
    """Remove uma tarefa definitivamente. Retorna True se a tarefa existia."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(
            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id),
        )
        return cursor.rowcount > 0


def get_task(user_id: int, task_id: int, db_path: str = DB_PATH) -> Optional[sqlite3.Row]:
    """Busca uma tarefa especifica do usuario, ou None se nao existir."""
    with get_connection(db_path) as conn:
        return conn.execute(
            "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
            (task_id, user_id),
        ).fetchone()
