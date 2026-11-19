# A19: assinaturas de apoio; traga sua implementação anterior.
from contextlib import closing
from pathlib import Path
import sqlite3
import sys


def criar_backup(origem, destino):
    origem = Path(origem)
    destino = Path(destino)
    if not origem.is_file():
        raise ValueError("Origem não encontrada: " + str(origem))  
    if destino.exists():
        raise ValueError("O destino já existe e não será sobrescrito: " + str(destino))
    if not destino.parent.is_dir():
        raise ValueError("A pasta do destino não existe: " + str(destino.parent))
    try:
        endereco = origem.resolve().as_uri() + "?mode=ro"
        with closing(sqlite3.connect(endereco, uri=True)) as con_origem:
            with closing(sqlite3.connect(destino)) as con_destino:
                con_origem.backup(con_destino)
        with closing(sqlite3.connect(destino)) as con_copia:
            resultado = con_copia.execute("PRAGMA integrity_check").fetchone()[0]
        if resultado != "ok":
            raise sqlite3.DatabaseError("a cópia não passou na verificação")
    except sqlite3.Error:
        if destino.exists():
            destino.unlink()
        raise ValueError("Não foi possível criar a cópia. A origem não foi alterada.")
    return destino


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python backup_sqlite.py origem-ficticia.db copia-nova.db")
    else:
        try:
            criar_backup(sys.argv[1], sys.argv[2])
            print("Cópia criada em:", sys.argv[2])
        except ValueError as erro:
            print("Erro:", erro)
