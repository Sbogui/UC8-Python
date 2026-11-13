# A16: assinaturas de apoio; traga sua implementação anterior.
from pathlib import Path
import csv
import os
import tempfile

CABECALHO = ["id", "nome", "quantidade", "preco_centavos", "subtotal_centavos", "forma", "total_pedido_reais"]


def exportar_csv(caminho, comprovante):
    if comprovante is None:
        raise ValueError("Finalize o pedido antes de exportar o relatório.")
    if len(comprovante["itens"]) == 0:
        raise ValueError("O comprovante não tem itens para exportar.")

    total = comprovante["total_centavos"]
    total_texto = f"{total // 100},{total % 100:02d}"  

    caminho = Path(caminho)
    temporario = None
    try:
        identificador, temporario = tempfile.mkstemp(dir=caminho.parent, suffix=".tmp")
        with os.fdopen(identificador, "w", encoding="utf-8-sig", newline="") as arquivo:
            escritor = csv.writer(arquivo, delimiter=";")
            escritor.writerow(CABECALHO)
            for codigo, nome, quantidade, subtotal in comprovante["itens"]:
                preco = subtotal // quantidade
                escritor.writerow([codigo, nome, quantidade, preco, subtotal, comprovante["forma"], total_texto])
        os.replace(temporario, caminho)
    except OSError:
        if temporario is not None and os.path.exists(temporario):
            os.remove(temporario)
        raise ValueError("Não foi possível exportar. O relatório anterior foi mantido.")