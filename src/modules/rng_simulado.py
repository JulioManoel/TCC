# qrng_simulado.py
import time

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator as Aer


def gerar_matriz_qrng(tamanho=400):
    """Gera uma matriz tamanho x tamanho de inteiros de 8 bits via QRNG otimizado (simulador)."""
    total_numeros = tamanho * tamanho
    num_bits = 8

    qc = QuantumCircuit(num_bits, num_bits)
    for qubit in range(num_bits):
        qc.h(qubit)
        qc.measure(qubit, qubit)

    simulator = Aer()
    compiled = transpile(qc, simulator)

    print("Executando circuito no simulador...")

    start = time.time()
    result = simulator.run(compiled, shots=total_numeros).result()
    counts = result.get_counts()

    todos_bitstrings = []
    for bitstring, freq in counts.items():
        todos_bitstrings.extend([bitstring] * freq)

    np.random.shuffle(todos_bitstrings)

    valores = np.array([int(b, 2) for b in todos_bitstrings], dtype=np.uint8)
    matriz = valores.reshape((tamanho, tamanho))

    end = time.time()
    print(f"Matriz gerada em {end - start:.2f} segundos.")

    return matriz


