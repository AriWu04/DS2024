from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def receive_file():
    if rank == 0:  # Server process
        print("Server started. Waiting for file chunks...")
        filename = comm.recv(source=MPI.ANY_SOURCE)  # Receive the file name
        print(f"Receiving file: {filename}")
        with open(filename, 'wb') as f:
            while True:
                chunk = comm.recv(source=MPI.ANY_SOURCE)  # Receive a file chunk
                if chunk == b'DONE':  # End-of-file signal
                    print("File transfer complete.")
                    break
                f.write(chunk)
                print(f"Received chunk of size {len(chunk)} bytes.")
        print(f"File {filename} saved successfully.")

if __name__ == "__main__":
    receive_file()
