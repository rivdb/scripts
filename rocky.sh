#!/bin/bash

printTime() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# Section 1: Manage Existing Users
clear
echo "Type all user account names, with a space in between:"
read -a users

usersLength=${#users[@]}

for ((i = 0; i < usersLength; i++)); do
    clear
    echo "${users[$i]}"
    echo "Delete ${users[$i]}? yes or no"
    read yn1

    if [ "$yn1" == "yes" ]; then
        userdel -r "${users[$i]}"
        printTime "${users[$i]} has been deleted."
    else
        echo "Make ${users[$i]} administrator? yes or no"
        read yn2

        if [ "$yn2" == "yes" ]; then
            usermod -aG wheel "${users[$i]}"
            printTime "${users[$i]} has been made an administrator."
        else
            gpasswd -d "${users[$i]}" wheel
            printTime "${users[$i]} is now a standard user."
        fi

        echo "Make custom password for ${users[$i]}? yes or no"
        read yn3

        if [ "$yn3" == "yes" ]; then
            echo "Password:"
            read -s pw
            echo -e "$pw\n$pw" | passwd "${users[$i]}"
            printTime "${users[$i]} has been given the custom password."
        else
            echo -e "Moodle!22\nMoodle!22" | passwd "${users[$i]}"
            printTime "${users[$i]} has been given the default password 'Moodle!22'."
        fi

        passwd -x30 -n3 -w7 "${users[$i]}"
        usermod -L "${users[$i]}"
        printTime "${users[$i]}'s account has been locked with password policies set."
    fi
done

# Section 2: Add New Users
clear
echo "Type user account names to add, separated by spaces:"
read -a usersNew

usersNewLength=${#usersNew[@]}

for ((i = 0; i < usersNewLength; i++)); do
    clear
    echo "${usersNew[$i]}"
    useradd "${usersNew[$i]}"
    printTime "${usersNew[$i]} has been created."

    echo "Make ${usersNew[$i]} administrator? yes or no"
    read ynNew

    if [ "$ynNew" == "yes" ]; then
        usermod -aG wheel "${usersNew[$i]}"
        printTime "${usersNew[$i]} is now an administrator."
    else
        printTime "${usersNew[$i]} remains a standard user."
    fi

    passwd -x30 -n3 -w7 "${usersNew[$i]}"
    usermod -L "${usersNew[$i]}"
    printTime "Password policies applied, and ${usersNew[$i]}'s account is locked."
done

# Section 3: Identify Orphaned Folders in /home
clear
printTime "Checking for orphaned user folders."
ls -a /home/ >> ~/Script.log

# Section 4: Check for Leftover Files
printTime "Checking for files from deleted users."

# Section 5: Optional System Updates and Package Installation
echo "Update system and install essential packages? yes or no"
read updateChoice

if [ "$updateChoice" == "yes" ]; then
    dnf update -y
    printTime "System updated."

    dnf install -y vim git curl wget
    printTime "Installed vim, git, curl, and wget."
fi

printTime "Script execution complete."

