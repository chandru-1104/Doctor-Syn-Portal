import http.server
import socketserver
import socket
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

IP_ADDRESS = '127.0.0.1'
HTTP_PORT_NUMBER = 9090
DNS_PORT_NUMBER = 53

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Content-type', 'text/html')
        super().end_headers()

    def do_GET(self):
        if self.path == '/favicon.ico':
            self.send_response(200)
            self.end_headers()
        else:
            # Serve the specific HTML file for all paths
            self.path = '/lastmain.html'
            try:
                super().do_GET()
            except ConnectionAbortedError:
                pass

# All available IP addresses
available_ip_addresses = [
    "192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4",
    "192.168.1.5", "192.168.1.6", "192.168.1.7", "192.168.1.8",
    "192.168.1.9", "192.168.1.10", "192.168.1.11", "192.168.1.12",
    "192.168.1.13", "192.168.1.14"
]

# Maintain a dictionary to keep track of allocated IP addresses and their last activity time
allocated_addresses = {ip: {"status": False, "last_activity": 0} for ip in available_ip_addresses}

# Function to allocate an available IP address to a patient
def allocate_ip_address():
    current_time = time.time()
    
    for ip, info in allocated_addresses.items():
        if not info["status"] or (current_time - info["last_activity"]) > 300:  # If the doctor (IP) is available or not active for 5 minutes
            allocated_addresses[ip]["status"] = True  # Mark the doctor as busy
            allocated_addresses[ip]["last_activity"] = current_time
            return ip
    return None  # No available doctor

# Function to send email to the patient
def send_email(patient_name, patient_email, schedule_time, doctor_name, room_number, floor_number):
    sender_email = "sparklit28@gmail.com"  # Replace with your email
    sender_password = "ebad affx nfgv nund"  # Replace with your email password
    
    receiver_emails = [patient_email]

    subject = "ABC HOSPITAL Appointment Confirmation"
    message = f"Hello {patient_name},\n\nYour appointment has been scheduled at {schedule_time}.\n\nDoctor: {doctor_name}\nRoom: {room_number}\nFloor: {floor_number}\n\nPlease arrive on time. Thank you!"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(receiver_emails)
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    smtp_server.starttls()
    smtp_server.login(sender_email, sender_password)
    smtp_server.sendmail(sender_email, receiver_emails, msg.as_string())
    smtp_server.quit()

# Function to send emails to the first 5 patients in the dataset
def send_emails_to_first_5():
    with open("dataset.txt", "r") as file:
        for _ in range(5):
            line = file.readline()
            if not line:
                break  # End of file reached

            patient_data = {}
            parts = line.strip().split(", ")
            for part in parts:
                key, value = part.split(": ")
                patient_data[key] = value

            if "Name" in patient_data and "Email" in patient_data:
                # Send email to the patient
                schedule_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 3600))  # Schedule appointment 1 hour from now
                send_email(patient_data["Name"], patient_data["Email"], schedule_time, "Dr. John Doe", "Room 101", "3rd Floor")
                print(f"Email sent to {patient_data['Name']} at {patient_data['Email']}")
            else:
                print("Patient data is incomplete. Please check the dataset.")

# Function to periodically check and free up inactive IP addresses
def periodic_check():
    while True:
        current_time = time.time()
        for ip, info in allocated_addresses.items():
            if info["status"] and (current_time - info["last_activity"]) > 300:  # If IP address is busy and inactive for 5 minutes
                allocated_addresses[ip]["status"] = False  # Mark the doctor as available
        time.sleep(60)  # Check every minute

# Start the periodic check thread
check_thread = threading.Thread(target=periodic_check)
check_thread.daemon = True
check_thread.start()

# Start the thread to send emails to the first 5 patients
email_thread = threading.Thread(target=send_emails_to_first_5)
email_thread.start()

# HTTP server configuration
http_server = socketserver.TCPServer((IP_ADDRESS, HTTP_PORT_NUMBER), MyRequestHandler)

# DNS server configuration
dns_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
dns_socket.bind((IP_ADDRESS, DNS_PORT_NUMBER))

print(f'HTTP server is running at http://{IP_ADDRESS}:{HTTP_PORT_NUMBER}')
print("DNS server listening on {}:{}".format(IP_ADDRESS, DNS_PORT_NUMBER))

# HTTP server thread
http_thread = threading.Thread(target=http_server.serve_forever)
http_thread.daemon = True
http_thread.start()

while True:
    # Receive data from the patient (client)
    data, patient_address = dns_socket.recvfrom(1024)
    print("Received request from {}:{}".format(patient_address[0], patient_address[1]))

    # Allocate an IP address (doctor) to the patient
    allocated_ip = allocate_ip_address()

    if allocated_ip:
        # Parse patient data from dataset.txt
        with open("dataset.txt", "r") as file:
            for line in file:
                patient_data = {}
                parts = line.strip().split(", ")
                for part in parts:
                    key, value = part.split(": ")
                    patient_data[key] = value

                # Send email to the patient
                schedule_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + 3600))  # Schedule appointment 1 hour from now

                if "Name" in patient_data and "Email" in patient_data:
                    send_email(patient_data["Name"], patient_data["Email"], schedule_time, "Dr. John Doe", "Room 101", "3rd Floor")
                    response = f"Allocated IP address (Doctor): {allocated_ip}\nAppointment scheduled at: {schedule_time}"
                else:
                    response = "Patient data is incomplete. Please check the dataset."
                
                # Send the response back to the patient
                dns_socket.sendto(response.encode(), patient_address)
                break  # Stop after processing the first line in the dataset
    else:
        response = "No available doctor at the moment. Please try again later."
        dns_socket.sendto(response.encode(), patient_address)
