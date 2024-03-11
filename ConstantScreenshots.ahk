#Requires AutoHotkey v2.0

; Set the directory where screenshots will be saved
OutputDir := "E:\QuickBackups\daily-captures"
PythonHelper := "C:/Users/Z/Projects/work-snapshots/"

; Create the directory if it doesn't exist
if not DirExist(OutputDir)
    DirCreate OutputDir

; List of programs for which screenshots will be captured
ProgramList := [
    "Audacity.exe",
    "blender.exe",
    "Code.exe",
    "devenv.exe",
    "GitHubDesktop.exe",
    "inkscape.exe",
    "mintty.exe",
    "Resolve.exe",
    "unity.exe",
    "WindowsTerminal.exe",
    "JupyterLab.exe",
]
ForceTrackFlag := false
ForceIgnoreFlag := false

; Function to check if a program is running
IsProgramRunning(ProgramName) {
    return ProcessExist(ProgramName) || ForceTrackFlag
}

Screenshot(timestamp) {
    cmd := PythonHelper "/.venv/Scripts/python.exe " PythonHelper "/src/take_screenshot.py " OutputDir " -t " timestamp
    Run(cmd, , "Hide")
}
WriteOpenWindowsPy(csv_file, timestamp) {
    cmd := PythonHelper "/.venv/Scripts/python.exe " PythonHelper "/src/get_windows.py " csv_file " " timestamp
    Run(cmd, , "Hide")
}

; Function to capture and save screenshot
CaptureAndSaveScreenshot() {
    if (ForceIgnoreFlag) {
        return
    }
    timestamp := FormatTime(A_Now, "yyyy-MM-dd_HH_mm") ; "%Y-%m-%d_%H_%M"
    for _, ProgramName in ProgramList {
        ; Check if interesting programs are running
        ; and we haven't been idle for 2 mins
        if (IsProgramRunning(ProgramName) && A_TimeIdle < 120000) {
            Screenshot(timestamp)
            WriteOpenWindowsPy(OutputDir "\open-windows.csv", timestamp)
            SoundPlay "nice-camera-click-106269.mp3", 1
            break
        }
    }
}

; Do some cleanup of default options
A_TrayMenu.Delete("1&") ; Open
A_TrayMenu.Delete("1&") ; Help
A_TrayMenu.Delete("1&") ; Line
A_TrayMenu.Delete("1&") ; WindowSpy
A_TrayMenu.Delete("2&") ; Edit Script
A_TrayMenu.Delete("4&") ; Pause Script
A_TrayMenu.Delete("3&") ; Suspend Hot Keys
; Goal is to keep reload and exit

A_TrayMenu.Add()

A_TrayMenu.Add("Force Track Activity", EnableForceTrackMode)
A_TrayMenu.Add("Force Ignore Activity", EnableForceIgnoreMode)

EnableForceTrackMode(ItemName, ItemPos, MyMenu) {
    global ForceTrackFlag
    ForceTrackFlag := !ForceTrackFlag
    if (ForceTrackFlag)
    {
        MyMenu.Check(ItemName)
    }
    else {
        MyMenu.Uncheck(ItemName)
    }
}

EnableForceIgnoreMode(ItemName, ItemPos, MyMenu) {
    global ForceIgnoreFlag
    ForceIgnoreFlag:= !ForceIgnoreFlag
    if (ForceIgnoreFlag)
    {
        MyMenu.Check(ItemName)
    }
    else {
        MyMenu.Uncheck(ItemName)
    }
}
SetTimer(CaptureAndSaveScreenshot, 300000) ; 5 mins in milliseconds

StatusCheck() {
    if (ForceIgnoreFlag) {
        TrayTip "Daily Capture is Suspended",,"Mute"
    }
}
SetTimer(StatusCheck, 120*1000)