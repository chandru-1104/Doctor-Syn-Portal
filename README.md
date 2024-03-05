**The DocSyn Portal integrates web development technologies with server-side scripting to create a comprehensive platform for patient-doctor interaction.
The use of WebSocket technology ensures real-time communication, while the appointment scheduling system and email notifications enhance the overall functionality of the portal.
The portal's responsive design makes it accessible to users on different devices, providing a seamless and engaging experience.**

**1.Login Page:** 
The portal includes a secure login page designed using HTML, CSS, and Bootstrap.
Users can enter their credentials, and a client-side script validates the input.
Successful login redirects the user to the Messenger tab.

**2.Messenger Tab:**
The Messenger tab allows patients to communicate with doctors in real-time.
WebSocket technology is employed for efficient and instant messaging.
A WebSocket client is implemented in JavaScript, providing a seamless chat experience.
The server-side Python script manages WebSocket connections and handles incoming messages.

**3.Appointment Tab:**

The Appointment tab enables patients to schedule appointments with doctors.
A user-friendly form, styled with Bootstrap, collects patient details such as name, age, gender, phone, email, and the reason for the appointment.
Validations ensure the correctness of user input.
Upon submission, the details are stored locally and can be downloaded as a text file.
The system maintains an available list of IP addresses (doctors) and allocates them to patients.

**4.Server-Side Script:**

Python's socket and http.server modules are utilized for the server-side implementation.
The server manages HTTP requests and WebSocket connections.
A periodic check ensures the availability of doctors' IP addresses, freeing up inactive ones.
Email notifications are sent to patients confirming their scheduled appointments.

**5.Email Notifications:**

The server-side script includes functionality to send email notifications to patients.
A Gmail account is used for sending emails, and the server-side script triggers email notifications for the patients in the dataset.
Notifications include appointment details and instructions for the patient.

**6.Dataset:**

Patient data is stored in a dataset.txt file, and the system processes the entries for email notifications.
The dataset includes patient names, emails, and other relevant information.

**7.Responsive Design:**

The portal is designed to be responsive, ensuring a consistent and user-friendly experience across various devices and screen sizes.
Bootstrap's grid system and responsive utilities are utilized for achieving responsiveness.
