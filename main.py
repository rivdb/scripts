import os
from colorama import*


'''
TODO:

[*] in the future: Windows EDR for Linux Mint
[*] os.system("locate .service") and investigate
[*] uninstall PHP --> if web (http/https services not needed)
[*] find installed RPMs (and any sus ones GEM)

'''

init(autoreset=True)

class Colors:
    BRIGHT = f"{Style.BRIGHT}"
    RED = f"{BRIGHT}{Fore.RED}"
    MAGENTA = f"{BRIGHT}{Fore.MAGENTA}"
    YELLOW = f"{BRIGHT}{Fore.YELLOW}"
    CYAN = f"{BRIGHT}{Fore.CYAN}"
    GREEN = f"{BRIGHT}{Fore.GREEN}"
    WHITE = f"{Fore.WHITE}"
Cols = Colors()

TITLE = f'''

 █████╗ ██╗     ██╗   ███████╗███████╗ ██████╗
██╔══██╗██║     ██║   ██╔════╝██╔════╝██╔════╝
███████║██║     ██║   ███████╗█████╗  ██║     
██╔══██║██║     ██║   ╚════██║██╔══╝  ██║     
██║  ██║███████╗██║██╗███████║███████╗╚██████╗
╚═╝  ╚═╝╚══════╝╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝
                                              
'''

def ufw_allow(service_names: list):
    print(f"{Cols.WHITE}")
    for name in service_names:
        os.system(f"ufw allow {name}")
def restart_services(service_names: list):
    print(f"{Cols.WHITE}")
    for name in service_names:
        os.system(f"systemctl restart {name}")

def purge_packages(package_names: list):
    print(f"{Cols.WHITE}")
    for name in package_names:
        os.system(f"apt purge {name} -y")

# TODO: for GRUB
input('*** TODO: for GRUB ***')
print(f"{Cols.YELLOW}[ Setting proper permissions on files ]:")




input(f"{Cols.YELLOW} [ Going to restore /etc/apt/sources.list.d/official-packages-respositories.list and complete this ]")
sources_data = open("correct_sources.list", 'r').read()
with open('/etc/apt/sources.list.d/official-packages-respositories.list', 'w') as f:
    f.write(sources_data)
os.system('apt update -y')


print(f"{Cols.YELLOW}[ Making back-up directory... ]")
os.makedirs("/backups", exist_ok=True)
os.system(f"chmod 700 /backups")

# needed for some of those network commands and stuff as well as pretty much everything else:
os.system('apt install coreutils -y -qq')
# in case they messed or backdoored one of the coreutils
os.system('apt reinstall coreutils')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# User shenangians
# passwords, ACLs, groups, sudoers, etc


os.system("chmod 640 /etc/shadow")
os.system("chmod 644 /etc/passwd")
os.system("chmod 644 /etc/group")


sudoers_file = open(f"/etc/sudoers", 'r').read()
if '!' in sudoers_file or 'authenticate' in sudoers_file:
    print(f'''{Cols.YELLOW}[ Either \'\' or \'\' was found in the \'/etc/sudoers\' please check for anything suspicious
            {Cols.YELLOW}[*] {Cols.RED}!authenticate {Cols.YELLOW}(anyone in the sudoers group can use SUDO without authentication!)
          
          ]''')
    input(f"{Cols.YELLOW}[ Okay I fixed the bad config! ]")



print(f"{Cols.YELLOW}[ Securing Kernel Parameters \"/etc/sysctl.conf\" ]")
input(f"{Cols.RED}[ You may want to make a snapshot now ]")
input(f"{Cols.RED}[ You sure you did it. OK. ]")
secure_sysctl = open(f"/etc/sysctl.conf", 'r').read()
with open(f"/etc/sysctl.conf", 'w') as f:
    f.write(secure_sysctl)
os.system("sysctl -p")
print(f"{Cols.YELLOW}[ I just hardened the kernel, anything break? ]")
input(f"{Cols.YELLOW}[ OK. ]")



print(f"{Cols.WHITE}")
os.system(f"cat /etc/sudoers")
input(f"{Cols.YELLOW}[ Okay, sudoers file looks OK. ]")

print(f"{Cols.YELLOW}[ In a non-privileged (no SUDO) terminal tab run this: \"chmod 640 ~/.bash_history\"]")
input(f"{Cols.YELLOW}[ Ok. ]")
os.system("chmod 640 ~/.bash_history")

print(f"[ Removing Aliases... ]")
os.system("unalias -a")


print(f"{Cols.YELLOW}[ Finding any world-writable files  ]")
os.system('find / -type f -perm /o+w 2>/dev/null | grep -v "/proc" ')
print(f"{Cols.YELLOW}[ Run chmod 644 on these files! ]")
input(f"{Cols.YELLOW}[ Anything that shouldn't be world-writeable here? ^ ]")
input(f"{Cols.YELLOW}[ I did the chmod stuff. OK. ]")



print(f"{Cols.YELLOW} Lock root account? (y/n)")
option = input(">>> ")
if option == "y":
    os.system("usermod -L root")



# User owned configuration files in /etc (users can change them, big NO-NO)


print(f"{Cols.WHITE}")
os.system(r'''find /etc/ -exec ls -l {} \; | awk '{print $3":"$4,$9}' | grep -v "^root:root" | grep -v "^:" 2>/dev/null''')
print(f"{Cols.YELLOW}[ Anything critical in /etc NOT OWNED BY ROOT?? If so run CHOWN. ]")
input(f"{Cols.YELLOW}[ OK. ]")

print(f"{Cols.WHITE}")
os.system(r'''ls -l /bin/ | awk '{print $3":"$4,$9}' | grep -v "^root:root" | grep -v "^:"''')
print(f"{Cols.YELLOW}[ Anything critical in /bin NOT OWNED BY ROOT?? If so run CHOWN. ]")
input(f"{Cols.YELLOW}[ OK. ]")


print(f"{Cols.YELLOW}[ World writable /proc files: ]")
os.system('find / -type f -perm /o+w 2>/dev/null | grep -v "/proc"')
input(f"{Cols.YELLOW}[ Ok anything critical I've \"chown root:root /proc/PATH_HERE\"  ]")
input(f"{Cols.YELLOW}[ OK. ]")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

os.system("ss -tulpn")
os.system("netstat -tulpn")
print(f"{Cols.YELLOW} [ Are there any suspicious TCP connections? ]")
print(f"{Cols.YELLOW} [ Even if there are UFW will block all of them, but this will give you insight as to  ]")
print(f"{Cols.YELLOW} [ which ports are tied to which PIDs, and in turn, the program path (shell, malware, etc) ]")
print(f"{Cols.YELLOW} [ to which you can then investigate and remove ]")
input(f"{Cols.YELLOW} [ hmm... looks good ]")




print(f"{Cols.YELLOW} [ Below will be the local startup scripts ]:")
input(f"{Cols.YELLOW} [ Ok. ]")

print(f"{Cols.YELLOW} === *** /etc/rc.local *** === ")
print(f"{Cols.WHITE}")
os.system("cat /etc/rc.local")
input(f'{Cols.YELLOW} [ Next. ]')

print(f"{Cols.YELLOW} === *** /etc/init.d/*.sh *** === ")
print(f"{Cols.WHITE}")
os.system("ls -lah /etc/init.d")
input(f'{Cols.YELLOW} [ Next. ]')

print(f"{Cols.YELLOW} === *** /etc/systemd/system/*.system *** === ")
os.system("ls -lah /etc/systemd/system")
input(f'{Cols.YELLOW} [ Next. ]')



# print(f"[ Do you need any of the above local startup scripts? (y/n)]")
# option = input(">>> ")
# if option == 'y':
#     input(f"[ I went through and removed any I don't need/recognize. ]")
# else:
#     os.system("echo 'exit 0' >> /etc/rc.local")



print(f"{Cols.YELLOW} [ Installing UFW & Blocking common malicious ports... ]")
print(f"{Cols.WHITE}")
os.system("apt install ufw -y -qq")
os.system("ufw enable")
# deny any ports unless we explicitly allowed them already from above hardening.
os.system("ufw default deny incoming")

print(f"{Cols.YELLOW} [ Take a look at UFW status for anything weird: ]")
input(f"{Cols.YELLOW} [ Ok. ]")

print(f"{Cols.WHITE}")
os.system("ufw status verbose")
input(f"{Cols.YELLOW} [ Next. ]")

print(f'''{Cols.YELLOW} [ Please read the UFW config, is there anything suspicious/insecure? ]
    {Cols.YELLOW} [-] Anything that usually isn't there in UFW and not needed? such as:
    {Cols.YELLOW} [-] ICMP?
    ''')

input(f"{Cols.YELLOW} [ Ok. ]")
print(f"{Cols.WHITE}")
os.system(f"cat /etc/ufw/before.rules")

input(f"{Cols.YELLOW} [ Next. ]")
print(f"{Cols.WHITE}")
os.system(f"cat /etc/ufw/after.rules")

input(f"{Cols.YELLOW} [ Next. ]")
print(f"{Cols.WHITE}")
os.system(f"cat /etc/ufw/applications.d/*")

input(f"{Cols.YELLOW} [ Next. ]")
print(f"{Cols.WHITE}")
os.system(f"cat /etc/ufw/user.rules")




# os.system('find /bin/ -name "*.sh*" -type f')
print(f"{Cols.WHITE}")

for file_name in os.listdir("/bin"):
    if ".sh" in file_name:
        print(f"{Cols.YELLOW}File: {Cols.RED}{file_name}")
        print(f"="*25)
        print(f"{Cols.WHITE}")
        os.system(f"head -n 10 /bin/{file_name}")
        print(f"="*25)

print(f"{Cols.YELLOW} [ Take note of these, any suspicious scripts? ]")
input(f"{Cols.YELLOW} [ Ok. ]")

os.system(f"ls -lah /dev/shm")
print(f"{Cols.YELLOW} [ Take note of these, any suspicious scripts? ]")
input(f"{Cols.YELLOW} [ Ok. ]")

option = input(f"{Cols.YELLOW} Do you need Samba? (y/n)")
if option == 'n':
    print(f"{Cols.WHITE}")
    os.system("apt purge samba -y -qq")
    os.system("apt purge samba-common -y  -qq")
    os.system("apt purge samba-common-bin -y -qq")
    os.system("apt-get purge samba4 -y -qq")
    print(f"{Cols.YELLOW} [ Deleted Sambda ]")
else:

    print(f'''{Cols.YELLOW}
        ==================================================================
            {Cols.RED}Samba hardening:
            {Cols.YELLOW}
            {Cols.RED}- allow guests to no
            {Cols.RED}- read only = no set to YES
            {Cols.RED}- server min protocol is NT1 should be SMB2 I think
            {Cols.RED}- usershare allow guests to no
            
            {Cols.YELLOW}[+] - Backed up this directory: \"{Cols.RED}/etc/samba\" at /backups/samba

        ==================================================================
        ''')
    os.system(f"chown -R root:root /srv/samba")
    os.system(f"chmod 700 /srv/samba")
    os.system(f"cp -r /etc/samba /backups/samba")

    input(f"{Cols.YELLOW}[ Alrighty, I hardened samba! ]")

    print(f"{Cols.WHITE}")
    os.system("ls -lah /var/lib/samba/private/ | grep -i 'db'")
    print(f"{Cols.YELLOW}[ Please investigate any DB files for insecure configs, backdoors, etc.]")
    print(f"{Cols.YELLOW}[ I did it. OK. ]")
    
    print(f"{Cols.YELLOW} [ Run this command and give each user a UNIQUE password: \"gedit /etc/samba/smb.conf\" ]")
    input(f"{Cols.YELLOW} [ Ok. ]")
    restart_services(["sambda"])
    ufw_allow(["samba"])





option = input(f"{Cols.YELLOW} Do you need FTP? (y/n)")
if option == "n":
    print(f"{Cols.YELLOW} [ Deleting FTP... ]")
    print(f"{Cols.WHITE}")
    os.system("apt-get purge vsftpd -y -qq")
    print(f"{Cols.YELLOW} [ VSFTPD removed ]")

else:
    print(f"{Cols.YELLOW} [ Allowing FTP... ]")
    ufw_allow(["ftp",
               "sftp",
               "ftps-data",
               "ftps",
               "vsftpd"])
    print(f"{Cols.WHITE}")
    os.system("cat /etc/vsftpd.conf")
    print(f"{Cols.YELLOW} [ Is there any suspicious data in the VSFTPD configuration file? ]")
    input(f"{Cols.YELLOW} [ Ok. ]")
    restart_services(["vsftpd"])

option = input(f"{Cols.YELLOW} [ Do you need SSH? (y/n) ]")
if option == "y":
    ufw_allow(["ssh"])

    # good practice, won't save us from their shells. ensures connecting client has proper permissions
    # and not a world writeable home directory (might just be a little annoying to some red teamers)
    # depending on how they have their setup bcs they have to pwn many servers
    print(f"{Cols.WHITE}")
    os.system('grep -q "^StrictModes yes" /etc/ssh/sshd_config || echo "StrictModes yes" | sudo tee -a /etc/ssh/sshd_config')
    print(f'''
        {Cols.YELLOW} As per your needs and requirements for Hivestorm please look at the below settings for 
        {Cols.RED}/etc/ssh/sshd_config:

        
        {Cols.YELLOW} Change to these {Cols.RED}unless {Cols.YELLOW}otherwise specified:
        {Cols.YELLOW} 1) PermitRootLogin {Cols.RED}no
        {Cols.YELLOW} 2) PermitRootLogin without-password {Cols.RED}no
        {Cols.YELLOW} 3) PermitEmptyPasswords {Cols.RED}no
        {Cols.YELLOW} 4) PasswordAuthenication {Cols.RED}no
        {Cols.YELLOW} 5) X11Forwarding {Cols.RED}no
        {Cols.YELLOW} 6) Protocol 2,1 ==> Protocol {Cols.RED}2 {Cols.YELLOW}(this is the SECUREST for ssh)

        
        
    ''')
    input(f"{Cols.YELLOW} [ I have made changes, restart sshd please... ]")
    restart_services(["sshd",
                      "ssh"])
    
    print(f"{Cols.WHITE}")
    os.system(f"cat ~/.ssh/authorized")
    input(f"{Cols.YELLOW} [ Hmm, authorized SSH keys look OK (none of the UNAUTHORIZED user accounts have any... ) ]")


else:
    print(f"{Cols.WHITE}")
    os.system("apt purge openssh-server -y -qq")



option = input(f"{Cols.YELLOW} [ Do you need telnet? (y/n) ]")
if option == "n":
    print(f"{Cols.WHITE}")
    telnet_packages = [
        'telnet',
        'telnetd',
        'inetutils-telnetd',
        'telnetd-ssl'
    ]
    purge_packages(telnet_packages)
else:
    telnet_services = [
        "telnet",
        "rtelnet",
        "telnets"
    ]
    ufw_allow([
        telnet_services
    ])
    restart_services([
        telnet_services
    ])


option = input(f"{Cols.YELLOW} [ Do you need mailing services? (y/n) ]")
print(f"{Cols.WHITE}")
if option == 'y':
    mail_services = ["smtp",
     "pop2",
     "pop3",
     "imap2",
     "imaps",
     "pop3s"]
    ufw_allow(mail_services)
    restart_services(mail_services)
else:
    purge_packages([
        # SMTP:
        "postfix",
        "sendmail",
        "exim4",
        # IMAP(S)/POP(3s)
        "dovecot-core",
        "dovecot-imapd",
        "dovecot-pop3d",
        "courier-imap",
        "courier-pop"
    ])


option = input(f"{Cols.YELLOW} [ Do you need printer services? (y/n) ]")
print(f"{Cols.WHITE}")
if option == 'y':
    printer_services = ["ipp",
    "printer",
    "cups"]
    ufw_allow(printer_services)
    restart_services(printer_services)


option = input(f"{Cols.YELLOW} [ Do you need MySQL? (y/n) ]")
print(f"{Cols.WHITE}")
if option == 'n':
    mysql_packages = [
        'mysql',
        'mysql-client-core-*',
        'mysql-server',
        'mysql-server-*',
        'mysql-client-*'
    ]
    purge_packages(mysql_packages)
else:
    mysql_services = [
        'ms-sql-s',
        'ms-sql-m',
        'mysql',
        'mysql-proxy',
        'mysqld'
    ]

    ufw_allow('mysql')
    print(f"{Cols.YELLOW} [ We are now going to start secure mysql installation process ]")
    print(f"{Cols.YELLOW} [ test databases, root logons, etc may be removed, read closely ]:")
    print(f"{Cols.WHITE}")
    os.system("sudo mysql_secure_installation")

    print(f"{Cols.YELLOW} [ I know want you to keep a close eye and see these MySQL configuration files ]: ")
    input(f"{Cols.YELLOW} [ Ok. ]")
    print(f"{Cols.WHITE}")
    os.system(f"cat /etc/my.cnf")
    input(f"{Cols.YELLOW} [ \"/etc/my.cnf\" ]")

    print(f"{Cols.WHITE}")
    os.system(f"cat /etc/mysql/my.cnf")
    input(f"{Cols.YELLOW} /etc/mysql/my.cnf")

    print(f"{Cols.WHITE}")
    os.system(f"cat /usr/etc/my.cnf")
    input(f"{Cols.YELLOW} /usr/etc/my.cnf")

    print(f"{Cols.WHITE}")
    os.system("cat ~/.my.cnf")
    input(f"{Cols.YELLOW} ~/.my.cnf")

    input(f"{Cols.YELLOW} [ I looked at them and changed if anything was off, restart MySQL service now please. ]")
    restart_services(mysql_services)


option = input(f"{Cols.YELLOW} [ Do you need http/https services enabled? (y/n) ]")
if option == 'n':
    # TODO: PHP as well (some older versions have some nasty vulns + exploits, remember LockBit... )
    purge_packages(["apache2",
                    "nginx",
                    "nginx-common"])

    print(f"{Cols.YELLOW} [ Will now remove everything in /var/www/* ]")
    input(f"{Cols.YELLOW} [ Ok. ]")
    print(f"{Cols.WHITE}")
    os.system("rm -r /var/www/*")
else:
    https_services = [
        "http",
        "https"
    ]
    ufw_allow(https_services)

    print(f"{Cols.YELLOW} [ We will now take a look at apache configuration file \"/etc/apache2/apache2.conf\" ]")
    input(f"{Cols.YELLOW} [ Ok. ]")
    print(f"{Cols.WHITE}")
    os.system(f"cat /etc/apache2/apache2.conf")

    print(f'''{Cols.YELLOW} 
        Some suggestions:
        ===================================================
            <Directory >
                AllowOverride None
                Order Deny,Allow
                Deny from all
            <Directory />

            Ensure this is set:
            UserDir disabled root
            ^^^^^ will stop root directory from being accessible via apache web URL
        ===================================================
    ''')
    input(f"{Cols.YELLOW} [ Ok I actually looked at the configuration file, and made any changes, let's keep going! ]")
    
    os.system("chown -R root:root /etc/apache2")

    apache_services = [
        "apache2",
        "apache"
    ]
    restart_services(https_services + apache_services)

    print(f'''{Cols.YELLOW}
        By default, the configuration file is named 
          [*] nginx. conf and placed in the directory /usr/local/nginx/conf , /etc/nginx , or /usr/local/etc/nginx .
          [*] if need be run {Cols.RED}\"locate *nginx*\"
    ''')
    input(f"{Cols.YELLOW}[ I took a look at them! ]")


option = input(f"{Cols.YELLOW} [ Is DNS needed? (y/n) ]")
if option == 'n':
    purge_packages(['bind9'])
else:
    ufw_allow(['domain'])


print(f"{Cols.YELLOW} [ Uninstalling known cracking tools... ]")
# if there is metasploit we'll see it when we see /opt
blacklisted_packages = [
    'netcat', 'netcat-openbsd', 'netcat-traditional',
    'ncat', 'pnetcat', 'socat', 'sock', 'socket', 
    'sbd', 'pwncat', 'john', 'john-data', 'hydra',
    'hydra-gtk', 'aircrack-ng', 'fcrackzip', 'lcrack',
    'ophcrack', 'ophcrack-cli', 'pdfcrack', 'pyrit',
    'rarcrack', 'sipcrack', 'irpas'
    
]
print(f"{Cols.WHITE}")
os.system(f"{Cols.YELLOW} rm -rf /usr/bin/nc")
purge_packages(blacklisted_packages)

print(f"{Cols.WHITE}")
os.system('dpkg -l | egrep "crack|hack|malware|spyware|backdoor|reverse|katz|dump"')
print(f'''{Cols.YELLOW} 
        Are there any malicious binaries related to cracking or hacking?
        Ignore these:
            [*] libcrack2:amd64
            [*] cracklib-runtime
      
      ''')
input(f"{Cols.YELLOW} [ I got rid of 'em if there were any. Let's keep going. ]")



print(f"{Cols.YELLOW} [ Removing the monitoring package zeitgeist if it exists... ]")
monitoring_packages = [
    'zeitgeist-core',
    'zeitgeist-datahub',
    'python-zeitgeist',
    'rhythmbox-plugin-zeitgeist',
    'zeitgeist',
]
purge_packages(monitoring_packages)


# Password policies, lockouts, password restrictions, etc
print(f"{Cols.WHITE}")
os.system(f"cat /etc/pam.d")
print(f'''{Cols.YELLOW} 
      [ The above \"/etc/pam.d\" are some password state policies, take a look and make changes as necessary ]
      [ Such as setting an expiry on passwords, how long until they can reset, days before to warn them to change, etc ]
      
      ''')
input(f"{Cols.YELLOW} [ Did it. ]")


print(f"{Cols.WHITE}")
os.system("apt install libpam-cracklib -y -qq")
common_auth = open(f"/etc/pam.d/common-auth", 'r').read()
if 'auth optional pam_tally.so deny=5 unlock_time=900 onerr=fail audit even_deny_root_account silent' not in common_auth:
    # will apply even for the root account:
    print(f"{Cols.WHITE}")
    os.system('echo "auth optional pam_tally.so deny=5 unlock_time=900 onerr=fail audit even_deny_root_account silent " >> /etc/pam.d/common-auth')
    os.system('echo -e "password requisite pam_cracklib.so retry=3 minlen=8 difok=3 reject_username minclass=3 maxrepeat=2 dcredit=1 ucredit=1 lcredit=1 ocredit=1\npassword requisite pam_pwhistory.so use_authtok remember=24 enforce_for_root" >>  /etc/pam.d/common-password')

print(f"{Cols.WHITE}")
os.system(f"cat /etc/pam.d/common-auth")
print(f"{Cols.YELLOW} [ /etc/pam.d/common-auth -> anything sus? ]")
input(f"{Cols.YELLOW} [ Everything does look ok... ]")


print(f"{Cols.WHITE}")
os.system(f"cat /etc/pam.d/common-password")
print(f"{Cols.YELLOW} [ /etc/pam.d/common-password -> anything sus? ]")
input(f"{Cols.YELLOW} [ Everything does look ok... ]")


# ***** TODO: make a script that one by one changes everyone's passwords (asks us first) *****
input(f"{Cols.RED} ***** TODO: make a script that creates users if not in list *****")
input(f"{Cols.RED} ***** TODO: make a script that one by one changes everyone's passwords (asks us first) *****")
input(f"{Cols.RED} ***** TODO: make a script that enforces permission ACLs *****")

print(f"{Cols.WHITE}")
os.system('apt install iptables -y -qq')
os.system('iptables -A INPUT -p all -s localhost  -i eth0 -j DROP')
print(f"{Cols.YELLOW}[ Any packets coming from the internet (eth0 interface) that are spoofed to be localhost will be dropped. ]")
input(f"{Cols.YELLOW} [ Let me check if any points / services went down... ]")
input(f"{Cols.YELLOW} [ Nope, we're good. ]")


print(f"{Cols.WHITE}")
print(f"{Cols.YELLOW}[ Installing AppArmor... ]")
os.system("apt install apparmor-profiles -y -qq")

# AV stuff:
print(f"{Cols.YELLOW}[ Setting up ClamAV... ]")
os.system("apt install clamav -y -qq")
os.system("apt install clamav-daemon -y -qq")
print(f'''{Cols.YELLOW} 
      [*] - I have just installed ClamAV for you, 
        - run \"clamscan -r /path/to/directory --heuristic-scan-precedence=yes\" to find infected files or malware
        - to auto remove run: \"clamscan -r --remove /path/to/directory --heuristic-scan-precedence=yes\"
        - to update signatures library: \"sudo freshclam\"
      ''')
input(f"{Cols.YELLOW} [ Got it! ]")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Crontab shenanigans:
print(f"{Cols.WHITE}")
os.system("crontab -l")
print(f"{Cols.YELLOW} [ I have just listed all of the crontabs above, anything unusual? check the scripts, be on the lookout for Cryllic letters! ]")

option = input(f"{Cols.YELLOW} [ Delete all Crontabs? (y/n) ]")
if option == 'y':
    print(f"{Cols.WHITE}")
    os.system(f"crontab -r")



os.system(f"ls -lah /var/spool/cron/crontabs")
print(f"{Cols.YELLOW}[ Anything suspicious in the cron (may show other user's crons as well)? ]")
input(f"[ Nope! We're good to go. ]")


print(f"{Cols.YELLOW}[ Restricting the Crontab to root user only... ]{Cols.WHITE}")
# only allow the root user to execute crontabs
os.system("echo root >/etc/cron.allow")
os.system("echo root >/etc/at.allow")
os.system("rm -rf /etc/at.deny")
os.system("rm -rf /etc/cron.deny")

# change ownership of important cron files to the root user:
# this is important in case these files are owned by a different user
# os.system("chown root:root cron.allow at.allow")

# all ownership of cron stuff is given to the root:
os.system("chown -R root:root /etc/cron.*")

# making sure this file is only readable by root since we created it
os.system("chmod 400 /etc/at.allow")
# any cron shenangians should only be readable by the rootuser:
os.system("chmod 400 /etc/cron.*")


# restrict cron directory permissions to root only:
os.system(f"chmod 700 /etc/cron.*")

# restrict crontab to only the root user:
os.system("sudo chmod 700 /usr/bin/crontab")




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




print(f"{Cols.WHITE}")
os.system("ss -tulpn")
os.system("netstat -tulpn")




print(f"{Cols.YELLOW} [ Upgrades/Updates will now be made, this may cause your critical services to go down  ]")
print(f"{Cols.YELLOW} [ and in turn show up as a penalty in the HiveStorm scoreboard, do not worry simply just wait ]")
print(f"{Cols.YELLOW} [ *** DO NOT CANCEL mid-update IT MAY CAUSE UNEXPECTED BEHAVIOR *** ]")
input(f'{Cols.YELLOW} [ Understood. ]')
# no -qq (I like to see everything and what's happening)
print(f"{Cols.WHITE}")


# Repository .list file in case they messed with it
# os.system("")


os.system('apt-get upgrade -y')
os.system('apt dist-upgrade -y')


print(f"{Cols.YELLOW} [ Removing unused packages... ]")
print(f"{Cols.WHITE}")
os.system('apt autoremove -y -qq')
os.system('apt autoclean -y -qq')
os.system('apt clean -y -qq')
print(f"{Cols.YELLOW} [ Unused packages have just been removed. ]")


# process monitoring (glorified task manager/HTOP for linux )
print(f"{Cols.WHITE}")
os.system(f"apt install btop -y -qq")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Things that tend to take awhile to run: #


# Rootkit hunter
print(f"{Fore.YELLOW}[ Setting up root-kit hunter... ]")
os.system(f"apt install rkhunter -y -qq")
print(f'''{Cols.YELLOW} 
      [*] - I have just installed ClamAV for you, 
        - run \"sudo rkhunter --check\" to find infected files or malware/rootkits
        - to investigate further:  
            [-] \"/var/log/rkhunter.log\"
            [-] \"sudo nano /var/log/rkhunter.log\"
        - creates a reference database (ONLY RUN AFTER SYSTEM IS CLEAN)
            [-] \"sudo rkhunter --propupd\""
      ''')
input(f"{Cols.YELLOW} [ Ok I just ran it and remediated any threats. ]")


# -ac checks all files even those typically not checked (subfiles, configurations, etc --> takes longer to complete)
print(f"{Cols.WHITE}")
os.system("apt install debsums -y -qq")
print(f"{Cols.YELLOW} [ Checking for any tampered packages... ]")

print(f"{Cols.WHITE}")
os.system("debsums -ac")
print(f"{Cols.YELLOW} [ If there are any tampered packages please take note of them and reinstall them ^ ]")
# would be fixed by upgrade, but if PAM.so is tampered with we now in the back of our minds will
# know to keep an extra eye out for SSH shenanigans
input(f"{Cols.YELLOW} [ We're good to go! ]")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



next_steps = open("next_steps.yaml", 'r').read()
your_turn = f'''

{Cols.MAGENTA}{TITLE}

{Cols.RED}========================================================================

{Cols.MAGENTA}
{next_steps}


{Cols.RED}========================================================================
'''