import os
import sqlite3
from datetime import datetime

DB_PATH = "cadastros.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # permite acessar colunas por nome
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cliente (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        cpf TEXT,
        email TEXT,
        telefone TEXT,
        status TEXT,
        comentario_interno TEXT,
        created_at TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS documento (
        id_documento INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER,
        tipo_documento TEXT,
        caminho_arquivo TEXT,
        uploaded_at TEXT,
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
    );
    """)

    conn.commit()
    conn.close()

def criar_cliente(nome, cpf, email, telefone):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO cliente (nome, cpf, email, telefone, status, comentario_interno, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        nome,
        cpf,
        email,
        telefone,
        "PENDENTE",        # status inicial
        None,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def salvar_documento(id_cliente, tipo_documento, caminho_arquivo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO documento (id_cliente, tipo_documento, caminho_arquivo, uploaded_at)
        VALUES (?, ?, ?, ?)
    """, (
        id_cliente,
        tipo_documento,
        caminho_arquivo,
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def listar_clientes_pendentes():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_cliente, nome, cpf, email, telefone, status, created_at
        FROM cliente
        WHERE status = 'PENDENTE'
        ORDER BY created_at ASC;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_cliente(id_cliente):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_cliente, nome, cpf, email, telefone, status, comentario_interno, created_at
        FROM cliente
        WHERE id_cliente = ?;
    """, (id_cliente,))
    row = cur.fetchone()
    conn.close()
    return row

def listar_documentos_cliente(id_cliente):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT id_documento, tipo_documento, caminho_arquivo, uploaded_at
        FROM documento
        WHERE id_cliente = ?;
    """, (id_cliente,))
    rows = cur.fetchall()
    conn.close()
    return rows

def atualizar_status_cliente(id_cliente, novo_status, comentario_interno):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE cliente
        SET status = ?, comentario_interno = ?
        WHERE id_cliente = ?;
    """, (
        novo_status,
        comentario_interno,
        id_cliente
    ))
    conn.commit()
    conn.close()