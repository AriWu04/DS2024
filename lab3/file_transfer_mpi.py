from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

def send_file(filepath):
    filename = os.path.basename(filepath)
    comm.send(filename, dest=1)  # Send file name to server
    print(f"[Client] Sending file: {filename}")
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(1024):  # Read file in chunks
                comm.send(chunk, dest=1)  # Send each chunk to server
                print(f"[Client] Sent chunk of size {len(chunk)} bytes.")
        comm.send(b'DONE', dest=1)  # Signal end of file transfer
        print("[Client] File transfer complete.")
    except FileNotFoundError:
        print(f"[Client] File {filepath} not found.")

def receive_file():
    print("[Server] Waiting for file...")
    filename = comm.recv(source=0)  # Receive file name from client
    print(f"[Server] Receiving file: {filename}")
    with open(filename, 'wb') as f:
        while True:
            chunk = comm.recv(source=0)  # Receive a file chunk from client
            if chunk == b'DONE':  # End-of-file signal
                print("[Server] File transfer complete.")
                break
            f.write(chunk)
            print(f"[Server] Received chunk of size {len(chunk)} bytes.")
    print(f"[Server] File {filename} saved successfully.")

if rank == 0:  # Client
    file_to_send = input("Enter the full path of the file to upload: ").strip()
    send_file(file_to_send)
elif rank == 1:  # Server
    receive_file()
