import socket
import os

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started at {host}:{port}. Waiting for a connection...")
    
    conn, addr = server_socket.accept()
    print(f"Connection established with {addr}")

    while True:
        try:
            command = conn.recv(1024).decode().lower()  
            if not command:
                print("Client disconnected.")
                break

            if command == 'upload':
                filename = conn.recv(1024).decode()
                filename = os.path.basename(filename)  
                print(f"Receiving file: {filename}")
                with open(filename, 'wb') as f:  
                    while True:
                        data = conn.recv(1024)
                        if data == b'DONE':  # end-of-file signal
                            print("End of file received.")
                            break
                        f.write(data)
                print(f"File {filename} uploaded successfully.")
                conn.send(f"File {filename} uploaded successfully.".encode())

            elif command == 'download':
                filename = conn.recv(1024).decode()
                filename = os.path.basename(filename)  
                try:
                    with open(filename, 'rb') as f:  
                        while chunk := f.read(1024):
                            conn.send(chunk)  # send file data in chunks
                    conn.send(b'DONE')  # signal for end of file
                    print(f"File {filename} sent successfully.")
                except FileNotFoundError:
                    conn.send(b'ERROR: File not found.')
                    print(f"File {filename} not found on server.")

            elif command == 'exit':
                print("Client requested to exit. Closing connection.")
                break

            else:
                print("Invalid command received.")
        except Exception as e:
            print(f"Error occurred: {e}")
            break

    conn.close()
    server_socket.close()
    print("Server shut down.")

if __name__ == "__main__":
    start_server()
