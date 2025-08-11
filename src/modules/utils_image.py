# -*- coding: utf-8 -*-
"""
Módulo de utilidades para manipulação de imagens.

Contém funções para carregar, capturar, exibir, cortar e gerar hash de imagens.
Este módulo é agnóstico à lógica de criptografia.
"""

# Importações necessárias para este módulo
import cv2
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import time
import hashlib

# --- Funções de Exibição ---

def mostrar_imagem(imagem_input: np.ndarray, titulo: str) -> None:
    """
    Mostra uma única imagem usando Matplotlib.
    Converte de BGR (OpenCV) para RGB (Matplotlib).
    """
    if imagem_input is not None:
        # Converte a imagem do padrão BGR do OpenCV para o RGB do Matplotlib
        imagem_rgb = cv2.cvtColor(imagem_input, cv2.COLOR_BGR2RGB)
        plt.imshow(imagem_rgb)
        plt.title(titulo)
        plt.axis("off")
        plt.show()
    else:
        print("Erro: Tentativa de mostrar uma imagem que é nula (None).")

def mostrar_lado_a_lado(img1: np.ndarray, img2: np.ndarray, titulo1: str = "Imagem 1", titulo2: str = "Imagem 2") -> None:
    """Mostra duas imagens lado a lado para comparação."""
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Imagem 1
    axs[0].imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
    axs[0].set_title(titulo1)
    axs[0].axis('off')

    # Imagem 2
    axs[1].imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
    axs[1].set_title(titulo2)
    axs[1].axis('off')

    plt.tight_layout()
    plt.show()

# --- Funções de Entrada (Input) ---

def upload_img() -> np.ndarray | None:
    """
    Abre uma caixa de diálogo para o usuário selecionar um arquivo de imagem.

    Returns:
        np.ndarray: O objeto da imagem carregada (formato OpenCV BGR).
        None: Se o usuário cancelar a seleção.
    """
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do Tkinter
    path = filedialog.askopenfilename(
        title="Selecione a imagem",
        filetypes=[("Arquivos de imagem", "*.jpg *.jpeg *.png *.bmp")]
    )

    if path:
        imagem = cv2.imread(path)
        print(f"Imagem '{Path(path).name}' carregada com sucesso.")
        return imagem
    else:
        print("Nenhuma imagem selecionada.")
        return None

def captura_img() -> np.ndarray | None:
    """
    Captura uma imagem da webcam após um timer de 10 segundos.

    Returns:
        np.ndarray: O objeto da imagem capturada (formato OpenCV BGR).
        None: Se a captura for cancelada ou a webcam não for encontrada.
    """
    imagem_capturada = None  # Variável local para armazenar a imagem
    cap = cv2.VideoCapture(0) # 0 é geralmente a webcam padrão
    if not cap.isOpened():
        print("Erro: Webcam não detectada ou não pôde ser aberta.")
        return None

    print("Webcam aberta. A imagem será capturada em 10 segundos. Pressione 'ESC' para cancelar.")
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erro ao ler frame da webcam.")
            break

        # Adiciona um contador na tela
        tempo_restante = 10 - (time.time() - start_time)
        if tempo_restante < 0:
            tempo_restante = 0
        
        texto_display = f"Capturando em: {tempo_restante:.1f}s"
        cv2.putText(frame, texto_display, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Captura de Webcam - Pressione ESC para sair", frame)

        # Condição de captura
        if time.time() - start_time > 10:
            imagem_capturada = frame.copy() # Salva uma cópia do frame
            print("Imagem capturada com sucesso!")
            break

        # Condição de cancelamento
        if cv2.waitKey(1) & 0xFF == 27: # 27 é o código da tecla ESC
            print("Captura cancelada pelo usuário.")
            break

    # Libera a webcam e fecha todas as janelas do OpenCV
    cap.release()
    cv2.destroyAllWindows()

    return imagem_capturada

# --- Funções de Pré-Processamento e Utilitários ---

def cortar_centro(imagem: np.ndarray, tamanho: int) -> np.ndarray | None:
    """
    Recorta um quadrado central da imagem com o tamanho especificado.

    Returns:
        np.ndarray: A imagem cortada.
        None: Se a imagem for menor que o tamanho do corte.
    """
    if imagem is None:
        print("Erro: Nenhuma imagem fornecida para cortar.")
        return None

    h, w = imagem.shape[:2]
    if h < tamanho or w < tamanho:
        print(f"Erro: Imagem ({w}x{h}) muito pequena para cortar um quadrado de {tamanho}x{tamanho}.")
        return None

    centro_x, centro_y = w // 2, h // 2
    metade_tamanho = tamanho // 2
    
    # Calcula as coordenadas do corte
    y1 = centro_y - metade_tamanho
    y2 = centro_y + metade_tamanho
    x1 = centro_x - metade_tamanho
    x2 = centro_x + metade_tamanho

    return imagem[y1:y2, x1:x2]


def hash_imagem(imagem_array: np.ndarray, algoritmo: str = "sha256") -> str | None:
    """
    Gera uma hash criptográfica a partir dos bytes de uma imagem.

    Returns:
        str: A representação hexadecimal da hash.
        None: Se a imagem de entrada for nula.
    """
    if imagem_array is None:
        print("Erro: Nenhuma imagem fornecida para gerar hash.")
        return None

    # Converte o array numpy para uma sequência de bytes
    imagem_bytes = imagem_array.tobytes()

    # Cria o objeto hasher com base no algoritmo escolhido
    hasher = hashlib.new(algoritmo)
    hasher.update(imagem_bytes)

    # Retorna a hash em formato hexadecimal
    return hasher.hexdigest()

# Importação do Path para extrair o nome do arquivo de forma limpa.
from pathlib import Path