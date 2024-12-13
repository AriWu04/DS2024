from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def send_file(filepath):
    if rank == 0:  # Client process
        filename = filepath.split("/")[-1]  # Extract file name
        comm.send(filename, dest=1)  # Send file name to server
        print(f"Sending file: {filename}")
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(1024):  # Read file in chunks
                    comm.send(chunk, dest=1)  # Send each chunk to server
                    print(f"Sent chunk of size {len(chunk)} bytes.")
            comm.send(b'DONE', dest=1)  # Signal end of file transfer
            print("File transfer complete.")
        except FileNotFoundError:
            print(f"File {filepath} not found.")

if __name__ == "__main__":
    file_to_send = input("Enter the full path of the file to upload: ").strip()
    send_file(file_to_send)
