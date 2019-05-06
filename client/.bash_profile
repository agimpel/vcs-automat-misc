
# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

let upSeconds="$(/usr/bin/cut -d. -f1 /proc/uptime)"
let secs=$((${upSeconds}%60))
let mins=$((${upSeconds}/60%60))
let hours=$((${upSeconds}/3600%24))
let days=$((${upSeconds}/86400))
UPTIME=`printf "%d days, %02dh%02dm%02ds" "$days" "$hours" "$mins" "$secs"`

# get the load averages
read one five fifteen rest < /proc/loadavg

echo "$(tput setaf 3)"
echo " __      _______  _____            ____  _                      _                        _   ";
echo " \ \    / / ____|/ ____|          |  _ \(_)                    | |                      | |  ";
echo "  \ \  / / |    | (___    ______  | |_) |_  ___ _ __ __ _ _   _| |_ ___  _ __ ___   __ _| |_ ";
echo "   \ \/ /| |     \___ \  |______| |  _ <| |/ _ \ '__/ _\` | | | | __/ _ \| '_ \` _ \ / _\` | __|";
echo "    \  / | |____ ____) |          | |_) | |  __/ | | (_| | |_| | || (_) | | | | | | (_| | |_ ";
echo "     \/   \_____|_____/           |____/|_|\___|_|  \__,_|\__,_|\__\___/|_| |_| |_|\__,_|\__|";
echo "                                                                                             ";
echo "$(tput setaf 4)
`date +"%A, %e %B %Y, %R"`
`uname -srmo`
$(tput setaf 1)
Uptime.............: ${UPTIME}
Memory.............: `cat /proc/meminfo | grep MemFree | awk {'print $2'}`kB (Free) / `cat /proc/meminfo | grep MemTotal | awk {'print $2'}`kB (Total)
Load Averages......: ${one}, ${five}, ${fifteen} (1, 5, 15 min)
IP Address.........: `wget -q -O - http://icanhazip.com/ | tail`
Running Processes..: `ps ax | wc -l | tr -d " "`
Temperature........: `vcgencmd measure_temp | sed 's/.*=//' | sed 's/\SC//'`°C
$(tput sgr0)
"

alias automat-stop="systemctl disable automat"
alias automat-start="systemctl enable automat && systemctl start automat"
alias automat-reload="systemctl restart automat"
alias automat-log="journalctl -f -u automat"