import json
import time
import numpy as np
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.append('TCC/src/modules')


from modules.utils_image import mostrar_imagem, upload_img, captura_img, cortar_centro, hash_imagem, mostrar_lado_a_lado
from modules.rng_simulado import gerar_matriz_qrng
from modules.rng_quantico import gerar_matriz_qrng_real
from modules.crypt_image import aplicar_xor_com_qrng, aplicar_lm, desfazer_lm, recuperar_imagem
from modules.kyber import encrypt_config, decrypt_config, kyber512, MockKyber512

def main():
    try:
        with open("C:\GitHub\TCC\pacote_criptografado.json", "r") as f:
            pacote = json.load(f)
    except FileNotFoundError:
        print("Arquivo 'pacote_criptografado.json' não encontrado.")
        return

    tempo_start = time.time()

    resultado = decrypt_config(pacote)

    # Para ilustrar, vamos supor que você tenha salvo a imagem caótica também para recuperar
    # Como o pacote não contém a imagem caótica, peça para o usuário fornecer o arquivo ou adapte conforme seu fluxo.
    # Aqui vou assumir que o usuário tem a imagem caótica em arquivo numpy (exemplo):
    try:
        imagem_caotica_simulada = np.load("imagem_caotica.npy")
    except FileNotFoundError:
        print("Arquivo 'imagem_caotica.npy' não encontrado. Por favor, gere a imagem caótica durante a criptografia e salve.")
        return

    imagem_descriptografada = recuperar_imagem(imagem_caotica_simulada, resultado)
    mostrar_imagem(imagem_descriptografada, "Imagem descriptografada")

    # Calcular hash para validar integridade
    hash_descriptografada = hash_imagem(imagem_descriptografada)
    hash_original = None
    try:
        with open("hash_original.txt", "r") as f:
            hash_original = f.read().strip()
    except FileNotFoundError:
        print("Arquivo 'hash_original.txt' não encontrado. Não será possível validar integridade.")
    
    if hash_original:
        if hash_descriptografada == hash_original:
            print("A imagem foi descriptografada com sucesso!!!")
        else:
            print("A imagem foi corrompida ou alterada!!!")

    tempo_end = time.time()
    print(f"Descriptografia concluída em {tempo_end - tempo_start:.2f} segundos.")

if __name__ == "__main__":
    main()
