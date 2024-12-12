import socket

def start_client(host='127.0.0.1', port=65432):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to the server at {host}:{port}")

    while True:
        command = input("Enter command (upload, download, exit): ").strip().lower()
        client_socket.send(command.encode())

        if command == 'upload':
            filename = input("Enter the full path of the file to upload: ").strip()
            client_socket.send(filename.encode())  # send file name to the server
            try:
                with open(filename, 'rb') as f:  
                    while chunk := f.read(1024):
                        client_socket.send(chunk)  
                client_socket.send(b'DONE')  
                print(client_socket.recv(1024).decode())  # receive server acknowledgment
            except FileNotFoundError:
                print("File not found. Please provide a valid file path.")

        elif command == 'download':
            filename = input("Enter the name of the file to download: ").strip()
            client_socket.send(filename.encode())  # send file name to the server
            with open(f'downloaded_{filename}', 'wb') as f: 
                while True:
                    data = client_socket.recv(1024)
                    if data == b'DONE':  
                        break
                    elif data == b'ERROR: File not found.':
                        print("File not found on the server.")
                        break
                    f.write(data)  
                if data != b'ERROR: File not found.':
                    print(f"File {filename} downloaded successfully.")

        elif command == 'exit':
            print("Disconnecting from the server.")
            break

        else:
            print("Invalid command.")

    client_socket.close()

if __name__ == "__main__":
    start_client()
