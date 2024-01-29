#Requires AutoHotkey v2.0

bad_window_procs := ["explorer.exe", "Twinkle Tray.exe"]
GetOpenWindows() {
    ids := WinGetList()
    wins := []
    for this_id in ids
    {
        this_title := WinGetTitle(this_id)
        this_class := WinGetClass(this_id)
        this_proc := WinGetProcessName(this_id)
        this_active := WinActive(this_id)
        active := this_active > 0
        ; WinGetPos(&X, &Y, &W, &H, this_id)
        ; if (X > 0 && Y > 0 && W > 0 && H > 0)
        isGood := true
        for bad_proc in bad_window_procs {
            if (bad_proc = this_proc) {
                isGood := false
                break
            }
        }
        if (isGood && this_title != "")
        {
            wins.push({ title: this_title, class: this_class, name: this_proc, isActive: active})
        }
    }
    return wins
}

WriteOpenWindows(filepath, timestamp) {
    Handle := FileOpen(filepath, "a", "UTF-8")
    if (Handle.Length == 0)
    {
        Handle.WriteLine("Datetime, Process, Title, IsActive")
    }

    for win in GetOpenWindows()
    {
        ; Intentionally choosing local time, benefit is to be able to glance at this data
        Handle.WriteLine(
            timestamp ", "
            RemoveCommas(win.name) ", "
            RemoveCommas(win.title) ", "
            win.isActive)
    }
}

RemoveCommas(str)
{
    return StrReplace(str, ",", ";")
}

; for a in GetOpenWindows()
; {
;     MsgBox(a.title " " a.class " " a.name " " a.isActive,,,)
; }

WriteOpenWindows("test2.csv", "test-ts")