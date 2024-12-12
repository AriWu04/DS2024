import xmlrpc.client
import os

def start_client():
    server = xmlrpc.client.ServerProxy('http://127.0.0.1:65432')

    while True:
        command = input("Enter command (upload, download, exit): ").strip().lower()

        if command == 'upload':
            filepath = input("Enter the full path of the file to upload: ").strip()
            try:
                with open(filepath, 'rb') as f:
                    file_data = f.read()
                filename = os.path.basename(filepath)
                response = server.upload_file(filename, xmlrpc.client.Binary(file_data))
                print(response)
            except FileNotFoundError:
                print("File not found. Please provide a valid file path.")
        
        elif command == 'download':
            filename = input("Enter the name of the file to download: ").strip()
            file_data = server.download_file(filename)
            if isinstance(file_data, str) and file_data.startswith("Error:"):
                print(file_data)
            else:
                with open(f'downloaded_{filename}', 'wb') as f:
                    f.write(file_data.data)  # `data` contains binary content
                print(f"File {filename} downloaded successfully.")
        
        elif command == 'exit':
            response = server.exit_server()
            print(response)
            break

        else:
            print("Invalid command.")

if __name__ == "__main__":
    start_client()
