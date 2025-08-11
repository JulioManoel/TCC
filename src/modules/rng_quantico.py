import time
import numpy as np
from qiskit_ibm_runtime import QiskitRuntimeService, Sampler
from qiskit import QuantumCircuit
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from collections import Counter

token = "L_8r3A6RlPdjorP_bo05Ne-HrP9H0gRL9tFGc0gaL7bH"
instance = "crn:v1:bluemix:public:quantum-computing:us-east:a/3355d3654c8e42ec9f98a727b463cf27:b8bc1faa-cf1a-42ff-859c-51c4d32fc1c3::"

def gerar_matriz_qrng_real(tamanho=16, job_id=None):
    total_numeros = tamanho * tamanho
    num_bits = 8

    service = QiskitRuntimeService(channel='ibm_quantum_platform', instance=instance, token=token)
    backend = service.least_busy(simulator=False, operational=True)
    print(f"Usando backend real: {backend.name}")

    if job_id:
        # Usar resultado de job já executado
        print(f"Buscando resultado do job {job_id}...")
        job = service.job(job_id)
        job_result = job.result()
        pub_result = job_result[0]
        counts = pub_result.data.meas.get_counts()

        todos_bits = []
        for bitstring, freq in counts.items():
            todos_bits.extend([bitstring.zfill(num_bits)] * freq)

    else:
        # Executar o circuito
        qc = QuantumCircuit(num_bits)
        qc.h(range(num_bits))
        qc.measure_all()

        pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
        optimized_circuit = pm.run(qc)

        sampler = Sampler(mode=backend)
        sampler.options.default_shots = total_numeros

        print("Executando no Sampler...")
        start = time.time()

        job = sampler.run([optimized_circuit])
        result = job.result()[0]

        todos_bits = [format(b, f'0{num_bits}b') for b in result.data.meas]


        end = time.time()
        print(f"Matriz gerada em {end - start:.2f} segundos.")

    np.random.shuffle(todos_bits)
    valores = np.array([int(b[::-1], 2) for b in todos_bits], dtype=np.uint8)
    matriz = valores.reshape((tamanho, tamanho))

    return matriz

# Exemplo de uso:
# matriz = gerar_matriz_qrng_real(tamanho=16)  # executa na IBM
# matriz = gerar_matriz_qrng_real(tamanho=16, job_id='d2ceu425v10c73c02epg')  # usa job já rodado
# print(matriz)
