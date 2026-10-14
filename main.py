
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

DURATA_IMPLICITA = 25
CULOARE_FUNDAL = "#1e1e1e"
CULOARE_BUTON = "#333333"
CULOARE_TEXT = "#ffffff"
CULOARE_ACCENT = "#192ac5"

fereastra = tk.Tk()
fereastra.title("POMODORO Timer")
fereastra.geometry("400x380")
fereastra.configure(bg=CULOARE_FUNDAL)
fereastra.resizable(False, False)

secunde_ramase = DURATA_IMPLICITA * 60
timer_pornit = False
after_id = None

titlu_label = tk.Label(
    fereastra,
    text="POMODORO TIMER",
    font=("Arial", 18, "bold"),
    bg=CULOARE_FUNDAL,
    fg=CULOARE_TEXT,
)
titlu_label.pack(pady=(20, 10))

durata_var = tk.StringVar(value=str(DURATA_IMPLICITA))

durata_label = tk.Label(
    fereastra,
    text="Durata sesiunii",
    font=("Arial", 11),
    bg=CULOARE_FUNDAL,
    fg=CULOARE_TEXT,
)
durata_label.pack()

durata_selectata = ttk.Combobox(
    fereastra,
    textvariable=durata_var,
    values=("5", "15", "25", "45", "60"),
    state="readonly",
    width=8,
    font=("Arial", 12),
)
durata_selectata.pack(pady=8)

timp_label = tk.Label(
    fereastra,
    text="25:00",
    font=("Arial", 42, "bold"),
    bg=CULOARE_FUNDAL,
    fg=CULOARE_ACCENT,
)
timp_label.pack(pady=15)


def actualizeaza_afisaj():
    minute = secunde_ramase // 60
    secunde = secunde_ramase % 60
    timp_label.config(text=f"{minute:02d}:{secunde:02d}")


def actualizeaza_timp():
    global secunde_ramase, timer_pornit, after_id

    after_id = None

    if not timer_pornit:
        return

    if secunde_ramase > 0:
        secunde_ramase -= 1
        actualizeaza_afisaj()

        if secunde_ramase > 0:
            after_id = fereastra.after(1000, actualizeaza_timp)
        else:
            timer_pornit = False
            messagebox.showinfo("Pomodoro", "Timpul a expirat!")
    else:
        timer_pornit = False
        messagebox.showinfo("Pomodoro", "Timpul a expirat!")


def porneste_timer():
    global timer_pornit, after_id

    if timer_pornit:
        return

    if secunde_ramase <= 0:
        messagebox.showinfo("Pomodoro", "Apasă Reset pentru o sesiune nouă.")
        return

    timer_pornit = True
    after_id = fereastra.after(1000, actualizeaza_timp)


def pauza_timer():
    global timer_pornit, after_id

    timer_pornit = False

    if after_id is not None:
        fereastra.after_cancel(after_id)
        after_id = None


def resetare_timer():
    global secunde_ramase, timer_pornit, after_id

    pauza_timer()
    secunde_ramase = int(durata_var.get()) * 60
    actualizeaza_afisaj()


def schimba_durata(event=None):
    resetare_timer()


durata_selectata.bind("<<ComboboxSelected>>", schimba_durata)

butoane_frame = tk.Frame(fereastra, bg=CULOARE_FUNDAL)
butoane_frame.pack(pady=10)

buton_pornire = tk.Button(
    butoane_frame,
    text="Start",
    font=("Arial", 11, "bold"),
    bg=CULOARE_ACCENT,
    fg=CULOARE_TEXT,
    activebackground="#6545db",
    activeforeground=CULOARE_TEXT,
    width=9,
    relief="flat",
    command=porneste_timer,
)
buton_pornire.grid(row=0, column=0, padx=5)

buton_pauza = tk.Button(
    butoane_frame,
    text="Pause",
    font=("Arial", 11),
    bg=CULOARE_BUTON,
    fg=CULOARE_TEXT,
    activebackground="#444444",
    activeforeground=CULOARE_TEXT,
    width=9,
    relief="flat",
    command=pauza_timer,
)
buton_pauza.grid(row=0, column=1, padx=5)

buton_resetare = tk.Button(
    butoane_frame,
    text="Reset",
    font=("Arial", 11),
    bg=CULOARE_BUTON,
    fg=CULOARE_TEXT,
    activebackground="#444444",
    activeforeground=CULOARE_TEXT,
    width=9,
    relief="flat",
    command=resetare_timer,
)
buton_resetare.grid(row=0, column=2, padx=5)

actualizeaza_afisaj()
fereastra.mainloop()
