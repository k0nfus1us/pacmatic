# file pacmate/__main__.py

#import pkg_resources
from sys import argv
import datetime
import os.path
import re
import subprocess
import configparser
from arch_rss import fetchRSS
from arch_ml import fetchML
from pathlib import Path

# configs

warn_time=86400  # seconds
pacman_log="${pacman_log:-/var/log/pacman.log}"
pacdiff_program="${pacdiff_program:-pacdiff}"
pacman_program="pacman"

#logfile="/var/log/arch-news.log"
logfile="./test.log"
cfgfile=os.path.expanduser("~/.config/pacmatic")
rss_url = "https://www.archlinux.org/feeds/news/"
ml_url="https://lists.archlinux.org/pipermail/arch-general/$(LC_ALL=C printf '%(%Y-%B)T\n' -1).txt.gz}"


def printHelp():
    print("Usage: "+ pacman_program + " -options [packages]\n\
    Pacmate is a pacman wrapper (based on pacmatic) that takes care of menial but critial tasks.\n\
These include\n\
    Checking the archlinux.org news RSS feed\n\
    Summarizing the arch-general mailing list\n\
    Reminding if it has been a while since the last sync\n\
    Reporting pacnew files\n\
    Editing pacnew files\n\
    TBD: print help of configured pkg manager)")

def printWarnStale():
    print("Warning: Stale installation, rerun with '-Suy'")

def getLastFetch(logfile):
    check_news_thr=0

    if os.path.isfile(logfile):
        f_log=open(logfile,"r")
        lastFetchDate = re.findall(r'\[\d*-\d*-\d* \d*:\d*\]',f_log.read(),re.MULTILINE)[-1][1:-1]
        f_log.close()
        fetch_date = datetime.datetime.strptime(lastFetchDate, '%Y-%m-%d %H:%M').date()
    else:
        print( "Initializing news archive, expect a flood of news.")
        print( "This will not happen on subsequent launches.")
        fetch_date = datetime.date.today() - datetime.timedelta(days=365*2) # 2 years should be enough RSS history...
    return fetch_date


def checkLastSync(args,logfile):
    for arg in args:
        print("arg=" + arg)
        if arg == "-S":
            print("TBD check sync_t - upgrade_t")
            printWarnStale()
        if arg == "-Sy" or arg == "-Syy":
            print("TBD check current_t - upgrade_t")
            printWarnStale()

    #-S -> check sync-upgrade_time
    #-Sy|-Syy -> check current-upgrade_time

pp_name = 'PackageManager'

pp_sudo='ENABLE'
pp_sudo_name='EnableSudo'

def loadCfg(cfgfile):
    config = configparser.ConfigParser()
    config.read(cfgfile)
    if config['DEFAULT'][pp_name]:
        global pacman_program
        pacman_program = config['DEFAULT'][pp_name]   
        #TBD: check for valid program

    if config['DEFAULT'][pp_sudo_name]:
        global pp_sudo
        pp_sudo = config['DEFAULT'][pp_sudo_name]

def writeCfg(cfgfile):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {pp_name:pacman_program,pp_sudo_name:pp_sudo}
    with open(cfgfile, 'w') as f_config:
        config.write(f_config)

def main():
    print('Calling from __main__.')

    if len(argv) < 2: 
        printHelp()
        exit()

    if os.path.isfile(cfgfile):
        loadCfg(cfgfile)
        print("config loaded")
    else:
        print("config (" + cfgfile + ") not found")
        writeCfg(cfgfile)

    fetch_date=getLastFetch(logfile)
    checkLastSync(argv[1:],logfile)
    fetchRSS(rss_url, logfile,fetch_date)
    fetchML(ml_url, logfile,fetch_date)

    shellCommand = [pacman_program] + argv[1:]
    if pp_sudo == 'ENABLE': #TBD debug
        shellCommand = ['sudo'] + shellCommand
    subprocess.run(shellCommand,shell=True,check=True)

if __name__ == '__main__':
  main()
