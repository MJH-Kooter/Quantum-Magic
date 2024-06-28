""" MOVE TO README
git clone https://github.com/QuTech-Delft/quantuminspire
cd quantuminspire
pip install .
pip install .[projectq,qiskit]
"""
from getpass import getpass
from coreapi.auth import BasicAuthentication
from quantuminspire.api import QuantumInspireAPI
from quantuminspire.qiskit import QI
import importlib
import time

#ADD LOGIN FUNCTION TO MAIN MENU
#Make user apply Credentials for the Quantum Inspire Account
#print('To calculate the results you'll need to login to Quantum Inspire in Delft.\n
#'Please enter your linked email address')
#email = input()

def CallCurrentLvl(level):
    global L
    module_i = f"Levels.lvl{level}"
    module = importlib.import_module(module_i)
    L = module

#print('Now enter your password')
#password = getpass()

circuit = list()
circuit_length = 0

## Prepares a gate for the qasm format based on the input
def prep_gate(gate, qbits, data):
    if (gate == "Rx" or gate == "Ry" or gate == "Rz" or gate == "wait"):
        prepped = f"{gate} q[{qbits}] , {data}"
    elif (gate == "CZ" or gate == "CNOT" or gate == "SWAP"):
        prepped = f"{gate} q[{qbits}],q[{int(data)+1}]"
    elif ("ignore" in gate):
        return "ignore"
    else:
        prepped = f"{gate} q[{qbits}]"
    return prepped

## Add a gate to the quantum circuit by placing it in the list
# Params: str gate, int/str/pair qbits, str data, int pos
def add_gate(gate, qbits, data):
    global circuit_length
    gate = prep_gate(gate, qbits, data)
    if gate != "ignore":
        circuit.append(gate)
        circuit_length += 1

## Prepares a circuit to be sent to the Quantum Inspire QC
def send_circuit(level):
    res = f""
    for gate in circuit:
        print (gate)
        res += f"{gate} \n"
    final = f"version 1.0\nqubits 5\nprep_z q[0:4]\n"
    if level == 4:
        final += "X q[0]\n"
    final += res
    if level != 0:
        final += L.getMeasure()
    else:
        final += "measure_x q[0]"
    return final

## Connect to the Quantum Inspire API and process the circuit
def run_Delft(level):
    #Connect to QI API, If no project has been initialized yet, uncomment the 3rd line to create one
    server_url = r'https://api.quantum-inspire.com'
    authentication = BasicAuthentication('MJHK26@gmail.com','DummyPass')#email,password)
    #QI.set_authentication(authentication, project_name='my-project-name')
    qi = QuantumInspireAPI(server_url, authentication, 'Qit STAR')

    #Create the qasm code for the Quantum Computer/Simulator
    qasm = send_circuit(level)

    #Select the backend and make the run.
    #The result contains lots of text and URL's, but we're interested in the result of the run.
    # This  can be found in the 'histogram', ordered as: [OrderedDict({'1': 1.0})]
    backend_type = qi.get_backend_type_by_name('Starmon-5')
    result = qi.execute_qasm(qasm, backend_type=backend_type, number_of_shots=2048)

    if result.get('histogram', {}):
        return (result['histogram'][0])
    else:
        return "error"

## Front end sends the lines created for the level
# Add all the objects on those line to the circuit
# Then send the signal to Quantum Backend to process the circuit 
def run(level, lines):
    runtime = 0
    CallCurrentLvl(level)
    for line in lines:
        for obj in line.circuit:
            if obj.gate != "":
                add_gate(obj.gate, line.line_id, obj.data)
            if obj.gate == "wait":
                runtime += (float(obj.data)/50)
    result = run_Delft(level)
    print(result)
    
    if level == 3:
        L.storescore(result)
        result = run_Delft(level)
        print(result)
    circuit.clear()
    L.calculatescore(result,runtime)

    ## When the backend is offline, this code simulates a run
    # so that the frontend can still be tested
    # To do so uncomment this block and comment everything from "for line in lines:"
    '''
    time.sleep(2)
    L.current_score = 10000 '''
