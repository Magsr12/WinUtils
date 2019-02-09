### WinUtils ###
```
 Usage: python winutils.py {args}
 
  --disc-usage   Checks for and corrects any possible errors that cause disk usage.
  --enable-dism  Enables DISM to search for possible HD errors
  --clean-apps   Clears ALL applications that come standard by using Windows 10, use --list-apps to list applications
  --list-apps    Lists the applications to be processed.
```

### WHAT IT DO:

[DISABLE SERVICES]

EXTERNAL COMMAND: sc config {service} start= {mode}

#demand = manual

#disable sysmain to start= disabled (superfetch)
#disable msiserver to start= demand ( Windows Installer )
#disable TrustedInstaller to start= demand ( Instalador de drivers )
#disable wuauserv to start= demand ( Windows update )

[TURN OFF WINDOWS DEFENDER]

(AUTO)
Turn_Off_Windows_Defender_Antivirus.reg

(MANUAL)
[HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows Defender]

"DisableAntiSpyware"=dword:00000001

[MORE]
      
If the schedule process is 100% consider to disable task scheduler. ( Agendador de tarefas )


OPTIONS IN --help:

  --disc-usage   Checks for and corrects any possible errors that cause disk usage.
  --enable-dism  Enables DISM to search for possible HD errors
  --clean-apps   Clears ALL applications that come standard by using Windows 10, use --list-apps to list applications
  --list-apps    Lists the applications to be processed.

Requirements:

clint
ctypes ( Installed by default )
colorama

