echo Type all user account names, with a space in between
read -a users

usersLength=${#users[@]}	

for (( i=0;i<$usersLength;i++))
do
	clear
	echo ${users[${i}]}
	echo Delete ${users[${i}]}? yes or no
	read yn1
	if [ $yn1 == yes ]
	then
		userdel -r ${users[${i}]}
		printTime "${users[${i}]} has been deleted."
	else	
		echo Make ${users[${i}]} administrator? yes or no
		read yn2								
		if [ $yn2 == yes ]
		then
			gpasswd -a ${users[${i}]} sudo
			gpasswd -a ${users[${i}]} adm
			gpasswd -a ${users[${i}]} lpadmin
			gpasswd -a ${users[${i}]} sambashare
			printTime "${users[${i}]} has been made an administrator."
		else
			gpasswd -d ${users[${i}]} sudo
			gpasswd -d ${users[${i}]} adm
			gpasswd -d ${users[${i}]} lpadmin
			gpasswd -d ${users[${i}]} sambashare
			gpasswd -d ${users[${i}]} root
			printTime "${users[${i}]} has been made a standard user."
		fi
		
		echo Make custom password for ${users[${i}]}? yes or no
		read yn3								
		if [ $yn3 == yes ]
		then
			echo Password:
			read pw
			echo -e "$pw\n$pw" | passwd ${users[${i}]}
			printTime "${users[${i}]} has been given the password '$pw'."
		else
			echo -e "Moodle!22\nMoodle!22" | passwd ${users[${i}]}
			printTime "${users[${i}]} has been given the password 'Moodle!22'."
		fi
		passwd -x30 -n3 -w7 ${users[${i}]}
		usermod -L ${users[${i}]}
		printTime "${users[${i}]}'s password has been given a maximum age of 30 days, minimum of 3 days, and warning of 7 days. ${users[${i}]}'s account has been locked."
	fi
done
clear

echo Type user account names of users you want to add, with a space in between
read -a usersNew

usersNewLength=${#usersNew[@]}	

for (( i=0;i<$usersNewLength;i++))
do
	clear
	echo ${usersNew[${i}]}
	adduser ${usersNew[${i}]}
	printTime "A user account for ${usersNew[${i}]} has been created."
	clear
	echo Make ${usersNew[${i}]} administrator? yes or no
	read ynNew								
	if [ $ynNew == yes ]
	then
		gpasswd -a ${usersNew[${i}]} sudo
		gpasswd -a ${usersNew[${i}]} adm
		gpasswd -a ${usersNew[${i}]} lpadmin
		gpasswd -a ${usersNew[${i}]} sambashare
		printTime "${usersNew[${i}]} has been made an administrator."
	else
		printTime "${usersNew[${i}]} has been made a standard user."
	fi
	
	passwd -x30 -n3 -w7 ${usersNew[${i}]}
	usermod -L ${usersNew[${i}]}
	printTime "${usersNew[${i}]}'s password has been given a maximum age of 30 days, minimum of 3 days, and warning of 7 days. ${users[${i}]}'s account has been locked."
done





clear
printTime "Check for any user folders that do not belong to any users."
ls -a /home/ >> ~/Desktop/Script.log

clear
printTime "Check for any files for users that should not be administrators."
ls -a /etc/sudoers.d >> ~/Desktop/Script.log



clear
chmod 777 /etc/hosts
cp /etc/hosts ~/Desktop/backups/
echo > /etc/hosts
echo -e "127.0.0.1 localhost\n127.0.1.1 $USER\n::1 ip6-localhost ip6-loopback\nfe00::0 ip6-localnet\nff00::0 ip6-mcastprefix\nff02::1 ip6-allnodes\nff02::2 ip6-allrouters" >> /etc/hosts
chmod 644 /etc/hosts
printTime "HOSTS file has been set to defaults."



clear
echo > /etc/mdm/mdm.conf
echo -e "[daemon]\nAutomaticLoginEnable=true\nAutomaticLogin=$USER\nTimedLoginEnable=true\nTimedLogin=$USER\nTimedLoginDelay=10\n\n[security]\nAllowRoot=false\n\n[xdmcp]\n\n[gui]\n\n[greeter]\n\n[chooser]\n\n[debug]\n\n\[servers]" >> /etc/mdm/mdm.conf
printTime "MDM has been secured."

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 






clear
if [ $mediaFilesYN == no ]
then
	find / -name "*.midi" -type f -delete
	find / -name "*.mid" -type f -delete
	find / -name "*.mod" -type f -delete
	find / -name "*.mp3" -type f -delete
	find / -name "*.mp2" -type f -delete
	find / -name "*.mpa" -type f -delete
	find / -name "*.abs" -type f -delete
	find / -name "*.mpega" -type f -delete
	find / -name "*.au" -type f -delete
	find / -name "*.snd" -type f -delete
	find / -name "*.wav" -type f -delete
	find / -name "*.aiff" -type f -delete
	find / -name "*.aif" -type f -delete
	find / -name "*.sid" -type f -delete
	find / -name "*.flac" -type f -delete
	find / -name "*.ogg" -type f -delete
	clear
	printTime "Audio files removed."

	find / -name "*.mpeg" -type f -delete
	find / -name "*.mpg" -type f -delete
	find / -name "*.mpe" -type f -delete
	find / -name "*.dl" -type f -delete
	find / -name "*.movie" -type f -delete
	find / -name "*.movi" -type f -delete
	find / -name "*.mv" -type f -delete
	find / -name "*.iff" -type f -delete
	find / -name "*.anim5" -type f -delete
	find / -name "*.anim3" -type f -delete
	find / -name "*.anim7" -type f -delete
	find / -name "*.avi" -type f -delete
	find / -name "*.vfw" -type f -delete
	find / -name "*.avx" -type f -delete
	find / -name "*.fli" -type f -delete
	find / -name "*.flc" -type f -delete
	find / -name "*.mov" -type f -delete
	find / -name "*.qt" -type f -delete
	find / -name "*.spl" -type f -delete
	find / -name "*.swf" -type f -delete
	find / -name "*.dcr" -type f -delete
	find / -name "*.dir" -type f -delete
	find / -name "*.dxr" -type f -delete
	find / -name "*.rpm" -type f -delete
	find / -name "*.rm" -type f -delete
	find / -name "*.smi" -type f -delete
	find / -name "*.ra" -type f -delete
	find / -name "*.ram" -type f -delete
	find / -name "*.rv" -type f -delete
	find / -name "*.wmv" -type f -delete
	find / -name "*.asf" -type f -delete
	find / -name "*.asx" -type f -delete
	find / -name "*.wma" -type f -delete
	find / -name "*.wax" -type f -delete
	find / -name "*.wmv" -type f -delete
	find / -name "*.wmx" -type f -delete
	find / -name "*.3gp" -type f -delete
	find / -name "*.mov" -type f -delete
	find / -name "*.mp4" -type f -delete
	find / -name "*.avi" -type f -delete
	find / -name "*.swf" -type f -delete
	find / -name "*.flv" -type f -delete
	find / -name "*.m4v" -type f -delete
	clear
	printTime "Video files removed."
	
	find /home -name "*.tiff" -type f -delete
	find /home -name "*.tif" -type f -delete
	find /home -name "*.rs" -type f -delete
	find /home -name "*.im1" -type f -delete
	find /home -name "*.gif" -type f -delete
	find /home -name "*.jpeg" -type f -delete
	find /home -name "*.jpg" -type f -delete
	find /home -name "*.jpe" -type f -delete
	find /home -name "*.png" -type f -delete
	find /home -name "*.rgb" -type f -delete
	find /home -name "*.xwd" -type f -delete
	find /home -name "*.xpm" -type f -delete
	find /home -name "*.ppm" -type f -delete
	find /home -name "*.pbm" -type f -delete
	find /home -name "*.pgm" -type f -delete
	find /home -name "*.pcx" -type f -delete
	find /home -name "*.ico" -type f -delete
	find /home -name "*.svg" -type f -delete
	find /home -name "*.svgz" -type f -delete
	clear
	printTime "Image files removed."
	
	clear
	printTime "All media files deleted."
else
	echo Response not recognized.
fi
printTime "Media files are complete."





clear
chmod 777 /etc/apt/apt.conf.d/10periodic
cp /etc/apt/apt.conf.d/10periodic ~/Desktop/backups/
echo -e "APT::Periodic::Update-Package-Lists \"1\";\nAPT::Periodic::Download-Upgradeable-Packages \"1\";\nAPT::Periodic::AutocleanInterval \"1\";\nAPT::Periodic::Unattended-Upgrade \"1\";" > /etc/apt/apt.conf.d/10periodic
chmod 644 /etc/apt/apt.conf.d/10periodic
printTime "Daily update checks, download upgradeable packages, autoclean interval, and unattended upgrade enabled."






clear
if [[ $(grep root /etc/passwd | wc -l) -gt 1 ]]
then
	grep root /etc/passwd | wc -l
	echo -e "UID 0 is not correctly set to root. Please fix.\nPress enter to continue..."
	read waiting
else
	printTime "UID 0 is correctly set to root."
fi

clear
mkdir -p ~/Desktop/logs
chmod 777 ~/Desktop/logs
printTime "Logs folder has been created on the Desktop."




cp /etc/services ~/Desktop/logs/allports.log
chmod 777 ~/Desktop/logs/allports.log
printTime "All ports log has been created."

dpkg -l > ~/Desktop/logs/packages.log
chmod 777 ~/Desktop/logs/packages.log
printTime "All packages log has been created."

apt-mark showmanual > ~/Desktop/logs/manuallyinstalled.log
chmod 777 ~/Desktop/logs/manuallyinstalled.log
printTime "All manually instealled packages log has been created."

service --status-all > ~/Desktop/logs/allservices.txt
chmod 777 ~/Desktop/logs/allservices.txt
printTime "All running services log has been created."

ps ax > ~/Desktop/logs/processes.log
chmod 777 ~/Desktop/logs/processes.log
printTime "All running processes log has been created."

ss -l > ~/Desktop/logs/socketconnections.log
chmod 777 ~/Desktop/logs/socketconnections.log
printTime "All socket connections log has been created."




cp /var/log/auth.log ~/Desktop/logs/auth.log
chmod 777 ~/Desktop/logs/auth.log
printTime "Auth log has been created."

cp /var/log/auth.log ~/Desktop/logs/syslog.log
chmod 777 ~/Desktop/logs/syslog.log
printTime "System log has been created."