import random
import subprocess
import time

web_servers = ["10.0.0.1", "10.0.0.2", "10.0.0.3"]

def send_hping3_packets():
    target_server = random.choice(web_servers)
    min_size = 0  # Minimum packet size
    max_size = 360  # Maximum packet size
    min_repetitions = 2  # Minimum number of launches
    max_repetitions = 10  # Maximum number of launches
    interval = "u100"  # Interval in microseconds
    count = 600  # Number of packets to send per launch

    # Randomly decide how many times to launch the command
    num_launches = random.randint(min_repetitions, max_repetitions)

    for _ in range(num_launches):
        # Generate a random packet size between min_size and max_size
        packet_size = random.randint(min_size, max_size)
        random_count  = random.randint(1,count)

        # Build the hping3 command
        command = [
            "hping3",
            "-S",  # Use the SYN flag
            "-d", str(packet_size),  # Packet size
            "-c", str(random_count),  # Number of packets to send
            "-i", interval,  # Interval between packets,
            "-U",
            target_server  # Target host
        ]

        print(f"Launching: {' '.join(command)}")

        # Execute the hping3 command
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error executing hping3: {e}")

        # Wait a random amount of time between 1 and 3 seconds before the next launch
        time.sleep(0.1)

if __name__ == "__main__":
    send_hping3_packets()
