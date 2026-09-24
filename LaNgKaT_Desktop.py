import tkinter as tk
import os
import socket
import platform
from pathlib import Path
from PIL import Image, ImageTk

BASE = Path.home() / "myprogram"

def submit():
    status.config(text="SUBMIT: " + entry.get())

def clear():
    entry.delete(0, tk.END)
    status.config(text="Ready")

def system_info():
    status.config(text=f"CPU: {os.cpu_count()} cores | OS: {platform.system()}")

def network_info():
    try:
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        status.config(text=f"Host: {host} | IP: {ip}")
    except:
        status.config(text="Network info unavailable")




def memory_info():
    win = tk.Toplevel(app)
    win.title("RAM / Memory Info")
    win.geometry("500x350")

    text = tk.Text(win, font=("Arial", 13))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    try:
        mem = {}

        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    mem[parts[0].rstrip(":")] = int(parts[1]) * 1024

        total = mem.get("MemTotal", 0)
        available = mem.get("MemAvailable", 0)
        used = total - available

        def gb(n):
            return n / (1024 ** 3)

        info = [
            "RAM / MEMORY INFO",
            "",
            f"Total RAM:     {gb(total):.2f} GB",
            f"Used RAM:      {gb(used):.2f} GB",
            f"Available RAM: {gb(available):.2f} GB",
        ]

        text.insert("1.0", "\n".join(info))
    except Exception as e:
        text.insert("1.0", f"Memory info unavailable\n\n{e}")

    text.config(state="disabled")

def storage_analyzer():
    win = tk.Toplevel(app)
    win.title("Storage Analyzer")
    win.geometry("500x350")

    text = tk.Text(win, font=("Arial", 13))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    try:
        st = os.statvfs("/")
        total = st.f_frsize * st.f_blocks
        free = st.f_frsize * st.f_bavail
        used = total - free

        def gb(n):
            return n / (1024 ** 3)

        info = [
            "STORAGE ANALYZER",
            "",
            f"Total: {gb(total):.2f} GB",
            f"Used:  {gb(used):.2f} GB",
            f"Free:  {gb(free):.2f} GB",
        ]

        text.insert("1.0", "\n".join(info))
    except Exception as e:
        text.insert("1.0", f"Storage info unavailable\n\n{e}")

    text.config(state="disabled")

def device_info():
    win = tk.Toplevel(app)
    win.title("Device Info")
    win.geometry("500x400")

    info = [
        f"OS: {platform.system()} {platform.release()}",
        f"Machine: {platform.machine()}",
        f"Processor: {platform.processor() or 'Unknown'}",
        f"CPU Cores: {os.cpu_count()}",
        f"Hostname: {socket.gethostname()}",
        f"Python: {platform.python_version()}",
    ]

    text = tk.Text(win, font=("Arial", 13))
    text.pack(expand=True, fill="both", padx=10, pady=10)
    text.insert("1.0", "\n".join(info))
    text.config(state="disabled")

def file_manager():
    win = tk.Toplevel(app)
    win.title("File Manager")
    win.geometry("450x350")
    tk.Label(win, text="MYPROGRAM FILES", font=("Arial",16,"bold")).pack(pady=10)
    lb = tk.Listbox(win, width=55, height=12)
    lb.pack(padx=10, pady=5)

    def refresh():
        lb.delete(0, tk.END)
        for name in os.listdir(BASE):
            lb.insert(tk.END, name)

    def open_selected(event):
        sel = lb.curselection()
        if sel:
            name = lb.get(sel[0])
            os.system("xdg-open " + repr(str(BASE / name)))

    tk.Button(win, text="Refresh", width=15, command=refresh).pack(pady=8)
    lb.bind("<Double-Button-1>", open_selected)
    refresh()

def notes():
    win = tk.Toplevel(app)
    win.title("Notes")
    win.geometry("500x400")
    text = tk.Text(win, font=("Arial",13))
    text.pack(expand=True, fill="both", padx=10, pady=10)

    def save():
        (BASE / "notes.txt").write_text(text.get("1.0",tk.END))
        status.config(text="Notes saved")

    tk.Button(win,text="Save",width=12,command=save).pack(side="left",padx=10,pady=5)
    tk.Button(win,text="Clear",width=12,command=lambda:text.delete("1.0",tk.END)).pack(side="left",padx=10,pady=5)

def calculator():
    win = tk.Toplevel(app)
    win.title("Calculator")
    win.geometry("350x450")
    display = tk.Entry(win,font=("Arial",20),justify="right")
    display.pack(fill="x",padx=15,pady=15)

    def add(v):
        display.insert(tk.END,v)

    def calc():
        try:
            result=eval(display.get(),{"__builtins__":{}},{})
            display.delete(0,tk.END)
            display.insert(0,str(result))
        except:
            display.delete(0,tk.END)
            display.insert(0,"Error")

    for row in [["7","8","9","/"],["4","5","6","*"],["1","2","3","-"],["0",".","=","+"]]:
        f=tk.Frame(win)
        f.pack()
        for v in row:
            cmd=calc if v=="=" else lambda x=v:add(x)
            tk.Button(f,text=v,width=6,height=2,command=cmd).pack(side="left",padx=2,pady=2)

    tk.Button(win,text="CLEAR",width=25,command=lambda:display.delete(0,tk.END)).pack(pady=15)

def text_editor():
    win=tk.Toplevel(app)
    win.title("Text Editor")
    win.geometry("600x450")
    text=tk.Text(win,font=("Arial",13))
    text.pack(expand=True,fill="both",padx=10,pady=10)

    def save():
        (BASE/"editor.txt").write_text(text.get("1.0",tk.END))
        status.config(text="Editor file saved")

    def open_file():
        f=BASE/"editor.txt"
        if f.exists():
            text.delete("1.0",tk.END)
            text.insert("1.0",f.read_text())

    b=tk.Frame(win)
    b.pack(pady=8)
    tk.Button(b,text="Save",width=12,command=save).pack(side="left",padx=5)
    tk.Button(b,text="Open",width=12,command=open_file).pack(side="left",padx=5)
    tk.Button(b,text="Clear",width=12,command=lambda:text.delete("1.0",tk.END)).pack(side="left",padx=5)

def file_search():
    win=tk.Toplevel(app)
    win.title("File Search")
    win.geometry("500x400")
    tk.Label(win,text="SEARCH FILES",font=("Arial",16,"bold")).pack(pady=10)
    se=tk.Entry(win,font=("Arial",13))
    se.pack(fill="x",padx=10,pady=5)
    results=tk.Listbox(win,width=60,height=15)
    results.pack(padx=10,pady=5,expand=True,fill="both")

    def search():
        q=se.get().lower().strip()
        results.delete(0,tk.END)
        if not q:
            results.insert(tk.END,"Type a filename to search.")
            return
        for f in sorted(BASE.rglob("*")):
            if q in f.name.lower():
                results.insert(tk.END,str(f.relative_to(BASE)))
        if results.size()==0:
            results.insert(tk.END,"No files found.")

    tk.Button(win,text="Search",width=12,command=search).pack(side="left",padx=10,pady=8)
    tk.Button(win,text="Clear",width=12,command=lambda:(se.delete(0,tk.END),results.delete(0,tk.END))).pack(side="left",padx=10,pady=8)

app=tk.Tk()
app.withdraw()
app_icon=tk.PhotoImage(file="/home/tuxspan/myprogram_android/langkat_icon.png")
app.iconphoto(True,app_icon)

splash=tk.Toplevel()
splash.overrideredirect(True)
splash.geometry("500x300")
splash.configure(bg="#080808")

tk.Label(splash,text="LaNgKaT",font=("Noto Sans",38,"bold"),bg="#080808",fg="#ff2222").pack(pady=(75,0))
tk.Label(splash,text="UTILITY TOOLS",font=("Noto Sans",14,"bold"),bg="#080808",fg="white").pack()
tk.Label(splash,text="Loading...",font=("Arial",9),bg="#080808",fg="#888888").pack(pady=15)

splash.update()
app.after(1500,lambda:(splash.destroy(),app.deiconify()))
app.title("LaNgKaT Utility Tools")
app.geometry("700x500")

# TRUE BACKGROUND
bg=Image.open(BASE/"premium_bg.png").resize((700,500))
bg_photo=ImageTk.PhotoImage(bg)

background=tk.Label(app,image=bg_photo,bd=0)
background.place(x=0,y=0,relwidth=1,relheight=1)

# DARK PANELS
sidebar=tk.Frame(app,bg="#080808")
sidebar.place(x=10,y=10,width=180,height=480)

tk.Label(sidebar,text="TOOLS",font=("Arial",18,"bold"),
         bg="#080808",fg="#ff2222").pack(pady=12)

def settings_app():
    win=tk.Toplevel(app)
    win.title("Settings")
    win.geometry("420x330")
    win.configure(bg="#080808")

    tk.Label(win,text="SETTINGS",font=("Noto Sans",24,"bold"),
             bg="#080808",fg="#ff2222").pack(pady=(25,15))

    tk.Label(win,text="Theme",font=("Arial",11,"bold"),
             bg="#080808",fg="white").pack()

    theme=tk.StringVar(value="Dark / Red")

    tk.OptionMenu(win,theme,"Dark / Red","Dark").pack(pady=8)

    tk.Label(win,text="Window Size",font=("Arial",11,"bold"),
             bg="#080808",fg="white").pack(pady=(10,0))

    size=tk.StringVar(value="670x520")
    tk.OptionMenu(win,size,"670x520","800x600","1024x768").pack(pady=8)

    def apply_settings():
        app.geometry(size.get())

        if theme.get()=="Dark":
            app.configure(bg="#111111")
        else:
            app.configure(bg="#080808")

        win.destroy()

    tk.Button(win,text="APPLY",width=16,height=1,
              command=apply_settings,
              bg="#111111",fg="#ff3333",
              activebackground="#ff2222",
              activeforeground="white",
              relief="flat",bd=0,
              font=("Arial",10,"bold")).pack(pady=18)

def about_app():
    win=tk.Toplevel(app)
    win.title("About LaNgKaT")
    win.geometry("420x300")
    win.configure(bg="#080808")

    tk.Label(win,text="LaNgKaT",font=("Noto Sans",32,"bold"),
             bg="#080808",fg="#ff2222").pack(pady=(35,0))

    tk.Label(win,text="UTILITY TOOLS",font=("Noto Sans",13,"bold"),
             bg="#080808",fg="white").pack()

    tk.Frame(win,bg="#ff2222",height=2,width=150).pack(pady=10)

    tk.Label(win,text="Version 1.0",font=("Arial",11,"bold"),
             bg="#080808",fg="#cccccc").pack(pady=3)

    tk.Label(win,text="10 Utility Tools",font=("Arial",10),
             bg="#080808",fg="#888888").pack(pady=3)

    tk.Label(win,text="LaNgKaT Utility Tools",font=("Arial",10),
             bg="#080808",fg="#888888").pack(pady=3)

buttons=[
("[RAM]  RAM / Memory",memory_info),
("[DISK] Storage Analyzer",storage_analyzer),
("[DEV]  Device Info",device_info),
("[SYS]  System Info",system_info),
("[NET]  Network Info",network_info),
("[FILE] File Manager",file_manager),
("[NOTE] Notes",notes),
("[CALC] Calculator",calculator),
("[EDIT] Text Editor",text_editor),
("[FIND] File Search",file_search),
("[INFO] About",about_app),
("[SET] Settings",settings_app)
]

page=[0]

def show_tools():
    for w in tool_frame.winfo_children():
        w.destroy()

    first=page[0]*7
    for name,cmd in buttons[first:first+7]:
        tk.Button(tool_frame,text=name,width=18,command=cmd,
                  bg="#151515",fg="#ff2222",
                  activebackground="#ff2222",
                  activeforeground="white").pack(pady=6)

    up_btn.config(state="normal" if page[0]>0 else "disabled")
    down_btn.config(state="normal" if first+7<len(buttons) else "disabled")

tool_frame=tk.Frame(sidebar,bg="#080808")
tool_frame.pack(fill="x")

up_btn=tk.Button(sidebar,text=" UP",
                 command=lambda: (page.__setitem__(0,page[0]-1),show_tools()),
                 bg="#151515",fg="#ff2222",
                 activebackground="#ff2222",
                 activeforeground="white")
up_btn.place(x=5,y=438,width=80,height=35)

down_btn=tk.Button(sidebar,text=" DOWN",
                   command=lambda: (page.__setitem__(0,page[0]+1),show_tools()),
                   bg="#151515",fg="#ff2222",
                   activebackground="#ff2222",
                   activeforeground="white")
down_btn.place(x=95,y=438,width=80,height=35)

show_tools()

content=tk.Frame(app,bg="#080808")
content.place(x=220,y=30,width=450,height=440)


tk.Label(content,text="LaNgKaT",font=("Noto Sans",38,"bold"),
         bg="#080808",fg="#ff2222").pack(pady=(22,0))

tk.Label(content,text="UTILITY TOOLS",font=("Noto Sans",14,"bold"),
         bg="#080808",fg="white").pack(pady=(0,2))

tk.Frame(content,bg="#ff2222",height=2,width=180).pack(pady=(6,5))

tk.Label(content,text="v1.0",font=("Noto Sans",9),
         bg="#080808",fg="#888888").pack(pady=(0,15))

entry=tk.Entry(content,font=("Arial",14),width=35)
entry.pack(pady=10)

b=tk.Frame(content,bg="#080808")
b.pack(pady=8)

tk.Button(b,text="SUBMIT",width=14,height=1,command=submit,
          bg="#111111",fg="#ff3333",
          activebackground="#ff2222",
          activeforeground="white",
          relief="flat",bd=0,
          font=("Arial",10,"bold")).pack(side="left",padx=5)

tk.Button(b,text="CLEAR",width=14,height=1,command=clear,
          bg="#111111",fg="#ff3333",
          activebackground="#ff2222",
          activeforeground="white",
          relief="flat",bd=0,
          font=("Arial",10,"bold")).pack(side="left",padx=5)

tk.Frame(content,bg="#ff2222",height=1).pack(fill="x",side="top",pady=(0,5))

status_frame=tk.Frame(content,bg="#111111",height=42)
status_frame.pack(fill="x",side="bottom",pady=10)
status_frame.pack_propagate(False)

status=tk.Label(status_frame,
                text=" READY  |  10 TOOLS  |  LaNgKaT Utility Tools v1.0",
                font=("Arial",9,"bold"),
                bg="#111111",fg="#ff3333")
status.pack(expand=True)

app.mainloop()
