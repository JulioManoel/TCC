import os
import sys

import cv2


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.rng_simulado import gerar_matriz_qrng


def salvar_matrizes_qrng(qtd=200, tamanho=400):

    for i in range(100, qtd + 1):
        matriz = gerar_matriz_qrng(tamanho)
        
        caminho_img = f"src/matrices/simuladas/matriz_qrng_{i:03d}.png"

        cv2.imwrite(str(caminho_img), matriz)

        print(f"Salvo {caminho_img}")

if __name__ == "__main__":
    salvar_matrizes_qrng()
