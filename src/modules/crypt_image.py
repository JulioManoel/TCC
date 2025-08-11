import numpy as np

# ======== Aplica XOR ========
def aplicar_xor_com_qrng(imagem_processada, matriz_qrng):
    if imagem_processada.shape[:2] != matriz_qrng.shape:
        raise ValueError("A imagem e a matriz QRNG devem ter o mesmo tamanho")
    if imagem_processada.ndim == 3 and imagem_processada.shape[2] == 3:
        xor_resultado = np.empty_like(imagem_processada, dtype=np.uint8)
        for canal in range(3):
            xor_resultado[:, :, canal] = np.bitwise_xor(imagem_processada[:, :, canal], matriz_qrng)
    else:
        xor_resultado = np.bitwise_xor(imagem_processada, matriz_qrng)
    return xor_resultado

# ======== Mapa Caótico ========
def logistic_map(size):
    r = 3.999
    x0 = 0.98892455322743
    x = x0
    seq = []
    for _ in range(size):
        x = r * x * (1 - x)
        seq.append(x)
    return np.array(seq)

def aplicar_lm(imagem):
    h, w = imagem.shape[:2]
    total = h * w
    chaos_seq = logistic_map(total)
    indices = np.argsort(chaos_seq)
    if imagem.ndim == 3:
        canais = []
        for c in range(imagem.shape[2]):
            canais.append(imagem[:, :, c].flatten()[indices].reshape(h, w))
        imagem_caotica = np.stack(canais, axis=2)
    else:
        imagem_caotica = imagem.flatten()[indices].reshape(h, w)
    return imagem_caotica, chaos_seq

# ======== Desfazer Mapa ========
def desfazer_lm(imagem_caotica, indices):
    h, w = imagem_caotica.shape[:2]
    reverse_indices = np.argsort(indices)
    if imagem_caotica.ndim == 3:
        canais = []
        for c in range(imagem_caotica.shape[2]):
            canais.append(imagem_caotica[:, :, c].flatten()[reverse_indices].reshape(h, w))
        return np.stack(canais, axis=2)
    else:
        return imagem_caotica.flatten()[reverse_indices].reshape(h, w)

def recuperar_imagem(imagem_codificada, resultado):
    chaos_seq = np.frombuffer(resultado["chaos_seq"], dtype=np.float64)
    indices = np.argsort(chaos_seq)
    matriz_qsimul = resultado["matriz_qsimul"]

    imagem_desarra = desfazer_lm(imagem_codificada, indices)
    if imagem_desarra.ndim == 3:
        imagem_recuperada = np.empty_like(imagem_desarra)
        for canal in range(3):
            imagem_recuperada[:, :, canal] = np.bitwise_xor(imagem_desarra[:, :, canal], matriz_qsimul)
    else:
        imagem_recuperada = np.bitwise_xor(imagem_desarra, matriz_qsimul)
    return imagem_recuperada
