import requests, csv, subprocess, ipaddress

#source=Abuse CH
response = requests.get("https://feodotracker.abuse.ch/downloads/ipblocklist.csv").text

def executeNewRules(listCount, ip_row, list_of_ips):
    rule="netsh advfirewall firewall add rule name='BadIPOut"+str(listCount)+"' Dir=Out Action=Block RemoteIP="+ip_row
    subprocess.run(["Powershell", "-Command", rule])
    rule="netsh advfirewall firewall set rule name='BadIPOut"+str(listCount)+"' new RemoteIP="+list_of_ips
    print("trying this rule",rule)
    subprocess.run(["Powershell", "-Command", rule])
    rule="netsh advfirewall firewall add rule name='BadIPIn"+str(listCount)+"' Dir=In Action=Block RemoteIP="+ip_row
    subprocess.run(["Powershell", "-Command", rule])
    rule="netsh advfirewall firewall set rule name='BadIPIn"+str(listCount)+"' new RemoteIP="+list_of_ips
    subprocess.run(["Powershell", "-Command", rule])

for i in range(0,100):
    test_rule = "netsh advfirewall firewall show rule name='BadIPOut"+str(i)+"' | findstr 'no rules'"
    test = (subprocess.run(["Powershell", "-Command", test_rule], capture_output=True, text=True).stdout)
    if (test == ''):    
        rule = "netsh advfirewall firewall delete rule name='BadIPOut"+str(i)+"'"
        subprocess.run(["Powershell", "-Command", rule])
        rule = "netsh advfirewall firewall delete rule name='BadIPIn"+str(i)+"'"
        subprocess.run(["Powershell", "-Command", rule])
    else:
        break

list_of_ips = ""
counter = 0
listCount = 0

mycsv = csv.reader(filter(lambda x: not x.startswith("#"), response.splitlines()))
for row in mycsv:
    ip_row = row[1]
    try:
        ip = ipaddress.IPv4Address(ip_row)
    except ipaddress.AddressValueError:
        print("Skipping invalid ip",ip_row)
        continue
    except:
        print("unexpected error for:",ip_row)
        continue
    if (counter == 0):
        counter+=1
        list_of_ips = ip_row
        print("Added Rule to block:",ip_row)
    elif (counter < 400):
        counter+=1
        list_of_ips += ","+ip_row
        print("Added Rule to block:",ip_row)
    else:
        counter=0
        executeNewRules(listCount, ip_row, list_of_ips)
        listCount+=1
        list_of_ips = ""

if counter > 0:
    executeNewRules(listCount, ip_row, list_of_ips)
