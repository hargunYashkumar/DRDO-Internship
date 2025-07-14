from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.quantum_info import Statevector
from qiskit.visualization import (
    plot_histogram,
    plot_bloch_multivector,
    plot_state_city
)
import matplotlib.pyplot as plt


def grover_oracle(qc, target):
    """Oracle to flip the sign of the target state"""
    n = len(target)
    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # Multi-controlled X (acts as Z here)
    qc.h(n-1)
    for i, bit in enumerate(target):
        if bit == '0':
            qc.x(i)


def diffuser(qc, n):
    """Inversion about the mean (diffuser)"""
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))


def grover_algorithm(n, target_bin):
    """Grover circuit for n-qubit with one marked state"""
    qc = QuantumCircuit(n, n)

    # Step 1: Initialize superposition
    qc.h(range(n))

    # Step 2: Apply Oracle
    grover_oracle(qc, target_bin)
    qc.barrier()

    # Step 3: Apply Diffuser
    diffuser(qc, n)
    qc.barrier()

    # Step 4: Measure
    qc.measure(range(n), range(n))
    return qc


# Parameters
n = 7
target_state = '1101101'

# Build Grover circuit
grover_circuit = grover_algorithm(n, target_state)

# Show circuit diagram (draw as image)
grover_circuit.draw(output='mpl')
plt.title("Grover's Algorithm Circuit")
plt.show()

# Simulate using Statevector for pre-measurement insights
init_sv = Statevector.from_label('0'*n)
final_sv = init_sv.evolve(grover_circuit.remove_final_measurements(inplace=False))

# Plot: Full Bloch Multivector (all qubits together)
plot_bloch_multivector(final_sv)
plt.title("Bloch Multivector: Full State")
plt.show()

# Plot: Bloch sphere for individual qubits
for i in range(n):
    plot_bloch_multivector(final_sv.ptrace(i))
    plt.title(f"Bloch Sphere for Qubit {i}")
    plt.show()

# Plot: State vector city (real/imag amplitudes)
plot_state_city(final_sv, title="Statevector after Grover Iteration")
plt.show()

# Plot: Output histogram (simulated measurement results)
counts = final_sv.sample_counts(1000)
plot_histogram(counts)
plt.title("Measurement Outcomes (Target = '101')")
plt.show()
