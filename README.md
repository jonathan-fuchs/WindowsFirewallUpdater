# WindowsFirewallUpdater

A script I run once a day from the Windows TaskScheduler. 
Botnet IPs taken from the Feodo tracker list compiled by Abuse.ch
My script is a modified version of a proof-of-concept script by the PCSecurity YouTube channel: https://youtu.be/7UWFJGeix_E

My main additions are:
Checking that the entries are properly formatted IP addresses (to prevent remote code execution);
Compiling the IP addresses into just a few entries within the Firewall, instead of creating a new rule for each IP address;
Adding creationflags to prevent PowerShell window pop-ups during execution
