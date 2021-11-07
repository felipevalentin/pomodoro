import tkinter as tk

import time

import threading


class Pomodoro:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        # Timer
        self.time_thread = threading.Thread()
        self.time = 25*60
        self.time_string = tk.StringVar()
        self.run = True

        # Buttons
        self.focus_button = tk.Button(self.frame, text = 'Focus', command=self.focus, width=17)
        self.long_break_button = tk.Button(self.frame, text = 'Long Break', command=self.long_break, width=17)
        self.reset_button = tk.Button(self.frame, text = 'reset', command = self.reset, width=17)
        self.short_break_button = tk.Button(self.frame, text = 'Short Break', command=self.short_break, width=17)
        self.start_button = tk.Button(self.frame, text = 'start', command = self.start, width=17)
        self.stop_button = tk.Button(self.frame, text = 'stop', command = self.stop, width=17)

        # Labels
        self.time_label = tk.Entry(self.frame, textvariable=self.time_string, font=(None, 40,), width=0)

        self.display_on_window()
        self.window_config()
        self.update_time(self.time)

    def display_on_window(self):
        self.time_label.grid(row=1, column=1, pady=25)
        self.focus_button.grid(row=0, column=0)
        self.short_break_button.grid(row=0, column=1)
        self.long_break_button.grid(row=0, column=2)
        self.start_button.grid(row=2, column=0)
        self.stop_button.grid(row=2, column=1)
        self.reset_button.grid(row=2, column=2)
        self.frame.pack()

    def window_config(self):
        self.master.title("Pomodoro")
        self.master.geometry("500x185")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def focus(self):
        self.update_time(25*60)
        self.start()

    def long_break(self):
        self.update_time(10*60)
        self.start()

    def on_closing(self):
        if self.time_thread.is_alive():
            self.run = False
            self.time_thread.join()
        self.master.destroy()

    def reset(self):
        self.stop()
        self.update_time(25*60)

    def short_break(self):
        self.update_time(5*60)
        self.start()

    def start(self):
        if self.time_thread.is_alive():
            return
        self.update_entry()
        self.run = True
        self.time_thread = threading.Thread(target=self.timer)
        self.time_thread.start()

    def stop(self):
        self.run = False

    def timer(self):
        while self.run and self.time > 0:
            self.update_time(self.time - 1)
            time.sleep(1)
        if self.time == 0:
            self.master.attributes("-topmost", True)
            self.master.attributes("-topmost", False)

    def update_time(self, new_total):
        self.time = new_total
        minutes, seconds = divmod(self.time, 60)
        self.time_string.set(f"{minutes:>02}:{seconds:>02}")

    def update_entry(self):
        minutos, segundos = self.time_label.get().split(":")
        self.update_time(int(minutos) * 60 + int(segundos))


def main(): 
    root = tk.Tk()
    app = Pomodoro(root)
    root.mainloop()

if __name__ == '__main__':
    main()
