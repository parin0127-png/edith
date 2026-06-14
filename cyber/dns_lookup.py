import socket
import time


def dns_look(domain):
    try :
        start = time.time() 
        ip = socket.gethostbyname(domain)
        ms = round((time.time() - start) * 1000 , 2)

        try:
            hostname = socket.gethostbyaddr(ip)[0]
        except :
            hostname = "Not found."

        try : 
            ipv6 = socket.getaddrinfo(domain , None , socket.AF_INET6)[0][4][0]
        except:
            ipv6 = "Not available"

        try : 
            socket.create_connection((ip , 80) , timeout = 3).close()
            status = "Reachable"
        except:
            status = "UnReachable"

        report = f"""
            Domain          :   {domain}
            IPv4            :   {ip}
            IPv6            :   {ipv6}
            Hostname        :   {hostname}
            Status          :   {status}
            LookUp Time     :   {ms} ms
        """

        return report
        
    except socket.gaierror:
        return "Invalid domain or domain not found"