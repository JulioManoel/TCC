import time
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
    print("1 --> Upload de Imagem")
    print("2 --> Captura de Imagem")
    opcao = int(input("Selecione uma opção: "))

    if opcao == 1:
        imagem = upload_img()
    elif opcao == 2:
        imagem = captura_img()
    else:
        print("Opção inválida.")
        return

    if imagem is None:
        print("Nenhuma imagem carregada, abortando.")
        return

    print("Tamanho da imagem:", imagem.shape)

    tempo_start = time.time()

    imagem_processada = cortar_centro(imagem, 400)
    if imagem_processada is None:
        print("Erro ao cortar imagem, abortando.")
        return

    mostrar_imagem(imagem_processada, "Imagem de tamanho 400x400")

    hash_original = hash_imagem(imagem_processada)
    print("Hash da imagem original:", hash_original, "\n")

    matriz_qsimul = gerar_matriz_qrng()
    print("Matriz QRNG simulada gerada.\n")

    imagem_xor = aplicar_xor_com_qrng(imagem_processada, matriz_qsimul)

    imagem_caotica_simulada, chaos_seq = aplicar_lm(imagem_xor)

    mostrar_lado_a_lado(imagem_xor, imagem_caotica_simulada, "Após aplicar o XOR", "Após aplicar o mapa caótico")

    pacote = encrypt_config(chaos_seq, matriz_qsimul)

    tempo_end = time.time()
    print(f"Criptografia concluída em {tempo_end - tempo_start:.2f} segundos.")

    # Salvar pacote criptografado para usar na descriptografia
    import json
    with open("pacote_criptografado.json", "w") as f:
        json.dump(pacote, f)
    print("Pacote criptografado salvo em 'pacote_criptografado.json'.")

if __name__ == "__main__":
    main()
