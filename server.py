import cv2, imutils, socket
import time
import base64

# Define constants
BUFF_SIZE = 65536
host_ip = "192.168.1.142"  # This should be your public IP
port = 9999

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)

# Bind the socket to the address
socket_address = (host_ip, port)
server_socket.bind(socket_address)

# Print listening address
print("Listening at:", socket_address)

# Open the video file for capturing frames
video = cv2.VideoCapture("video_test.mp4")  # Replace "video_test.mp4" with 0 for webcam

# Variables for FPS calculation
fps, st, frames_to_count, cnt = (0, 0, 20, 0)

while True:
    # Wait for a message from the client
    msg, client_address = server_socket.recvfrom(BUFF_SIZE)
    print("GOT connection from", client_address)

    # Define the width of the frame
    WIDHT = 400

    # Loop through the video frames
    while video.isOpened():
        # Read a frame from the video
        _, frame = video.read()

        # Resize the frame
        frame = imutils.resize(frame, width=WIDHT)

        # Encode the frame as JPEG
        encoded, buffer = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])

        # Encode the buffer as base64
        message = base64.b64encode(buffer)

        # Send the encoded frame to the client
        server_socket.sendto(message, client_address)

        # Display the frame with FPS information
        frame = cv2.putText(frame, "FPS: " + str(fps), (10, 40), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
        cv2.imshow("TRANSMITTING VIDEO", frame)

        # Check for quit command
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            server_socket.close()
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
