
from qiskit_ibm_runtime import QiskitRuntimeService

service = QiskitRuntimeService(
    channel='ibm_quantum_platform',
    instance='crn:v1:bluemix:public:quantum-computing:us-east:a/3355d3654c8e42ec9f98a727b463cf27:b8bc1faa-cf1a-42ff-859c-51c4d32fc1c3::',
    token='L_8r3A6RlPdjorP_bo05Ne-HrP9H0gRL9tFGc0gaL7bH'
)
job = service.job('d2ceu425v10c73c02epg')
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

print(counts)
