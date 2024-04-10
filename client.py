import cv2, socket
import numpy as np
import time
import base64

# Define constants
BUFF_SIZE = 65536
host_ip = "192.168.1.142"  # This should be your public IP
port = 9999

# Create a UDP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

# Send a "Hello" message to the server
message = b"Hello"
client_socket.sendto(message, (host_ip, port))

# Variables for FPS calculation
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:
    # Receive packets from the server
    packet, _ = client_socket.recvfrom(BUFF_SIZE)

    # Decode base64 data and convert it to an image frame
    data = base64.b64decode(packet, " /")
    npdata = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1)

    # Display the received frame with FPS information
    frame = cv2.putText(frame, "FPS: " + str(fps), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
    cv2.imshow("RECEIVING VIDEO", frame)

    # Check for quit command
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        client_socket.close()
        break

    # Update FPS count
    if cnt == frames_to_count:
        try:
            fps = round(frames_to_count / (time.time() - st))
            st = time.time()
            cnt = 0
        except Exception as error_message:
            print("Error:", error_message)
            pass
    cnt += 1
