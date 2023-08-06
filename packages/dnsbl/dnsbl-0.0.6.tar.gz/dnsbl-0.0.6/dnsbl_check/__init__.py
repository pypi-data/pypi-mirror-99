from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import dns.resolver

allData = {
    "blacklists" : []
}

dnsbl_list = []

def check(dnszone,ip):
    ptrl = [x for x in ip.split(".")][::-1]
    ptr = f"{ptrl[0]}.{ptrl[1]}.{ptrl[2]}.{ptrl[3]}."
    try:
        result = dns.resolver.resolve(ptr+dnszone, 'TXT')
        response = str(list(result)[0])[1:-1].split(" ")
        for i in response:
            if "http:" in i.lower():
                return {"ip" : ip , "dnszone" : dnszone , "txt" : i}
        return {"ip" : ip , "dnszone" : dnszone , "txt" : "No link is given"}
    except:
        return False

def run(ip):
    bl = []
    with ThreadPoolExecutor(max_workers = 100) as executor:
        results = executor.map(check, dnsbl_list,len(dnsbl_list)*[ip])
        for res in results:
            if(res != False):
                bl.append(res)
    print(f"scan done for ip {ip}")
    return bl

def classify_data():
    filtered_arr = {
        "blacklists" : []
    }
    all_ips = list(set([x["ip"] for x in allData["blacklists"]]))
    for ip in all_ips:
        ip_chunck = list(filter(lambda x: (x["ip"] == ip), allData["blacklists"]))
        filtered_arr["blacklists"].append({ip : ip_chunck})
    return filtered_arr


def batch(ips,bls):
    global dnsbl_list
    dnsbl_list = bls
    with ThreadPoolExecutor(max_workers = 2000) as mainexe:
        jobs = mainexe.map(run, ips)
        for job in jobs:
            if(len(job)>0):
                allData["blacklists"].extend(job)
    f_data = classify_data()
    return f_data
