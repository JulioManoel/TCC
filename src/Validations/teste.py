
from qiskit_ibm_runtime import QiskitRuntimeService
import numpy as np
import cv2


tamanho = 400

service = QiskitRuntimeService(
    channel='ibm_quantum_platform',
    instance='',
    token=''
)
job = service.job('d2cenpgf4s4s73dfafa0')

# JA FORAM
#
# job = service.job('d2ceu425v10c73c02epg')

job_result = job.result()



# To get counts for a particular pub result, use
#
# pub_result = job_result[<idx>].data.<classical register>.get_counts()
# where <idx> is the index of the pub and <classical register> is the name of the classical register.
# You can use circuit.cregs to find the name of the classical registers.
# Para cada circuito submetido no job, você tem um pub_result
# Por exemplo, se você submeteu só 1 circuito, use índice 0
pub_result = job_result[0]

# O nome do registro clássico (classical register) depende do seu circuito.
# Se você criou o circuito com qc.measure_all(), o nome padrão costuma ser "meas"
counts = pub_result.data.meas.get_counts()

todos_bitstrings = []

for bitstring, freq in counts.items():
    todos_bitstrings.extend([bitstring] * freq)

np.random.shuffle(todos_bitstrings)
valores = np.array([int(b, 2) for b in todos_bitstrings], dtype=np.uint8)
matriz = valores.reshape((tamanho, tamanho))


print(counts)

        
caminho_img = f"src/matrices/real/matriz_qrng_{1}.png"

cv2.imwrite(str(caminho_img), matriz)

print(f"Salvo {caminho_img}")

