import asyncio
import aiohttp
import ipaddress

# Define the subnet
SUBNET = "192.168.1.0/24"

# Function to check if an IP is a Reolink server
async def check_reolink_server(ip):
    print(f"Scanning IP: {ip}")
    try:
        # Ping the IP (ICMP ping is not directly supported in asyncio, so we use a TCP connection as a workaround)
        reader, writer = await asyncio.wait_for(asyncio.open_connection(ip, 80), timeout=1.0)
        writer.close()
        await writer.wait_closed()
        print(f"Host {ip} is alive. Checking for Reolink server...")

        # Make an HTTP request to check for Reolink server
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=2)) as session:
            async with session.get(f"http://{ip}") as response:
                content = await response.text()
                if "Reolink" in content:
                    print(f"Reolink server found at {ip}")
                    return ip
                else:
                    print(f"Not a Reolink server at {ip}.")
    except asyncio.TimeoutError:
        print(f"Host {ip} did not respond to ping or HTTP request.")
    except Exception as e:
        print(f"Error scanning {ip}: {e}")
    return None

# Main function to scan the subnet
async def scan_network():
    print(f"Scanning subnet {SUBNET} for Reolink server...")
    tasks = []
    for ip in ipaddress.IPv4Network(SUBNET, strict=False):
        if ip == ipaddress.IPv4Network(SUBNET).network_address or ip == ipaddress.IPv4Network(SUBNET).broadcast_address:
            continue  # Skip network and broadcast addresses
        tasks.append(asyncio.create_task(check_reolink_server(str(ip))))

    # Wait for all tasks to complete
    results = await asyncio.gather(*tasks)
    for result in results:
        if result:
            print(f"Reolink server found at {result}")
            return

    print("Reolink server not found on the local network.")

# Run the script
if __name__ == "__main__":
    asyncio.run(scan_network())