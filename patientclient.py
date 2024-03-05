import socket

def run_patient(patient_name):
    # DNS server configuration
    dns_server_host = "127.0.0.1"
    dns_server_port = 53

    # Create a UDP socket for the patient (client)
    patient_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connect to the DNS server
        patient_socket.connect((dns_server_host, dns_server_port))
        print(f"{patient_name} connected to DNS server at {dns_server_host}:{dns_server_port}")

        # Send a request to the DNS server
        request_message = f"Requesting Doctor's IP address for {patient_name}".encode()
        patient_socket.send(request_message)

        # Receive and print the response from the server
        response = patient_socket.recv(1024)
        print(f"{patient_name} - Response from server: {response.decode()}")

    finally:
        # Close the patient socket
        patient_socket.close()

# Parse patient names from dataset.txt
with open("dataset.txt", "r") as file:
    patient_lines = file.readlines()

# Run patients concurrently
for patient_line in patient_lines:
    parts = patient_line.strip().split(", ")
    patient_data = {key: value for part in parts for key, value in [part.split(": ")]}
    run_patient(patient_data["Name"])
