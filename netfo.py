#!/usr/bin/env python3

import psutil
import socket
import time

def resolve_ip(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except:
        return None

def monitor_all():
    print("Monitoring ALL outgoing connections on this machine...\n")
    seen = set()

    try:
        while True:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == psutil.CONN_ESTABLISHED and conn.raddr:
                    pid = conn.pid or "N/A"
                    proc_name = "Unknown"
                    try:
                        if conn.pid:
                            proc = psutil.Process(conn.pid)
                            proc_name = proc.name()
                    except:
                        pass

                    key = (conn.raddr.ip, conn.raddr.port, conn.laddr.port, pid)
                    if key not in seen:
                        seen.add(key)
                        hostname = resolve_ip(conn.raddr.ip)
                        print(f"[{proc_name} | PID: {pid}] connected to {conn.raddr.ip}:{conn.raddr.port} from local port {conn.laddr.port}" +
                              (f" ({hostname})" if hostname else ""))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    monitor_all()
