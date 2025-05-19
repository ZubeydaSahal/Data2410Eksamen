import socket
import struct
import argparse
import time
import os

HEADER_FORMAT = "!HHHH"
HEADER_SIZE = 8   ##skal være 32 byte 
DATA_SIZE = 992
PACKET_SIZE = 1000
TIMEOUT = 0.4
DEFAULT_WINDOW_SIZE = 3

FLAGS = {
    'SYN': 0b0100,
    'ACK': 0b0010,
    'FIN': 0b1000,
}

def create_header(seq_nr, ack_nr, flags, window):
    return struct.pack(HEADER_FORMAT, seq_nr, ack_nr, flags, window)

def parse_header(packet):
    return struct.unpack(HEADER_FORMAT, packet[:HEADER_SIZE])

def parse_arguments():
    parser = argparse.ArgumentParser("DATA2410 Reliable Transport Protocol (DRTP) Application")
    parser.add_argument('-s', '--server', action='store_true', help="Enable server mode")
    parser.add_argument('-c', '--client', action='store_true', help="Enable client mode")
    parser.add_argument('-i', '--ip', type=str, default='127.0.0.1')
    parser.add_argument('-p', '--port', type=int, default=8088)
    parser.add_argument('-f', '--file', type=str)
    parser.add_argument('-w', '--window', type=int, default=DEFAULT_WINDOW_SIZE)
    parser.add_argument('-d', '--discard', type=int, default=999999)
    return parser.parse_args()

def timestamp():
    return time.strftime("%H:%M:%S", time.localtime()) + f".{int(time.time()*1_000_000)%1_000_000:06d}"

def server(ip, port, discard_seq):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((ip, port))
    print(f"Server kjører på {ip}:{port}")

    # Connection Establishment
    data, client_addr = sock.recvfrom(PACKET_SIZE)
    seq_nr, ack_nr, flags, window = parse_header(data)

    if flags & FLAGS['SYN']:
        print("SYN packet is received")
        syn_ack = create_header(0, 0, FLAGS['SYN'] | FLAGS['ACK'], 15)
        sock.sendto(syn_ack, client_addr)
        print("SYN-ACK packet is sent")

        data, client_addr = sock.recvfrom(PACKET_SIZE)
        _, _, flags, _ = parse_header(data)

        if flags & FLAGS['ACK']:
            print("ACK packet is received")
            print("Connection established")
        else:
            print("Expected ACK, connection failed.")
            sock.close()
            return
    else:
        print("Expected SYN, connection failed.")
        sock.close()
        return

    file = open("received_file", "wb")
    expected_seq = 1
    total_bytes = 0
    start_time = time.time()

    while True:
        try:
            sock.settimeout(10)
            data, client_addr = sock.recvfrom(PACKET_SIZE)
            seq_nr, ack_nr, flags, window = parse_header(data)

            if flags & FLAGS['FIN']:
                print("FIN packet is received")
                fin_ack = create_header(0, 0, FLAGS['FIN'] | FLAGS['ACK'], 0)
                sock.sendto(fin_ack, client_addr)
                print("FIN-ACK packet is sent")
                break

            if seq_nr == discard_seq:
                print(f"Discarding packet {seq_nr} for testing")
                discard_seq = 999999
                continue

            if seq_nr == expected_seq:
                print(f"{timestamp()} -- packet {seq_nr} is received")
                file.write(data[HEADER_SIZE:])
                total_bytes += len(data[HEADER_SIZE:])

                ack = create_header(0, seq_nr, FLAGS['ACK'], 0)
                sock.sendto(ack, client_addr)
                print(f"{timestamp()} -- sending ack for the received {seq_nr}")
                expected_seq += 1
            else:
                print(f"Out of order packet {seq_nr} is received -- ignored")

        except socket.timeout:
            print("Socket timeout, no more packets.")
            break

    file.close()
    end_time = time.time()
    duration = end_time - start_time
    throughput = (total_bytes * 8) / (duration * 1_000_000) if duration > 0 else 0
    print(f"The throughput is {throughput:.2f} Mbps")
    print("Connection closed")
    sock.close()

def client(ip, port, file_path, window_size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    server = (ip, port)

    print("Connection Establishment Phase:\n")
    syn = create_header(0, 0, FLAGS['SYN'], 0)
    sock.sendto(syn, server)
    print("SYN packet is sent")

    try:
        data, _ = sock.recvfrom(PACKET_SIZE)
        _, _, flags, recv_window = parse_header(data)

        if flags & FLAGS['SYN'] and flags & FLAGS['ACK']:
            print("SYN-ACK packet is received")
            ack = create_header(0, 0, FLAGS['ACK'], 0)
            sock.sendto(ack, server)
            print("ACK packet is sent")
            print("Connection established\n")
            window_size = min(window_size, recv_window)
        else:
            print("Invalid SYN-ACK response")
            return
    except socket.timeout:
        print("Timeout during handshake")
        return

    with open(file_path, 'rb') as f:
        file_data = f.read()

    seq = 1
    base = 1
    next_seq = 1
    total_packets = (len(file_data) + DATA_SIZE - 1) // DATA_SIZE
    packets = {}
    start_time = time.time()

    print("Data Transfer:\n")

    while base <= total_packets:
        while next_seq < base + window_size and next_seq <= total_packets:
            start = (next_seq - 1) * DATA_SIZE
            end = start + DATA_SIZE
            chunk = file_data[start:end]
            packet = create_header(next_seq, 0, 0, 0) + chunk
            packets[next_seq] = packet
            sock.sendto(packet, server)
            print(f"{timestamp()} -- packet with seq = {next_seq} is sent, sliding window = {{{', '.join(map(str, range(base, next_seq+1)))}}}")
            next_seq += 1

        try:
            ack_data, _ = sock.recvfrom(PACKET_SIZE)
            _, ack_nr, flags, _ = parse_header(ack_data)
            if flags & FLAGS['ACK']:
                print(f"{timestamp()} -- ACK for packet = {ack_nr} is received")
                if ack_nr >= base:
                    base = ack_nr + 1
        except socket.timeout:
            print("RTO occurred, retransmitting window...")
            for seq in range(base, next_seq):
                sock.sendto(packets[seq], server)
                print(f"{timestamp()} -- retransmitting packet with seq = {seq}")

    # Teardown
    print("\nConnection Teardown:\n")
    fin = create_header(0, 0, FLAGS['FIN'], 0)
    sock.sendto(fin, server)
    print("FIN packet is sent")

    try:
        data, _ = sock.recvfrom(PACKET_SIZE)
        _, _, flags, _ = parse_header(data)
        if flags & FLAGS['FIN'] and flags & FLAGS['ACK']:
            print("FIN-ACK packet is received")
    except socket.timeout:
        print("FIN-ACK packet not received")

    end_time = time.time()
    duration = end_time - start_time
    throughput = (len(file_data) * 8) / (duration * 1_000_000) if duration > 0 else 0
    print(f"The throughput is {throughput:.2f} Mbps")
    print("Connection closed")
    sock.close()

def main():
    args = parse_arguments()
    if args.server:
        server(args.ip, args.port, args.discard)
    elif args.client:
        if not args.file:
            print("Feil: Du må spesifisere fil med -f når du bruker klientmodus")
            return
        client(args.ip, args.port, args.file, args.window)
    else:
        print("Feil: Du må angi --server eller --client")

if __name__ == "__main__":
    main()
