import tkinter as tk
import threading


class Pomodoro:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        # Timer
        self.time = 25*60
        self.time_string = tk.StringVar()
        self.thread = None
        self.run = False

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
        self.stop()
        self.master.destroy()

    def reset(self):
        self.stop()
        self.update_time(25*60)

    def short_break(self):
        self.update_time(5*60)
        self.start()

    def start(self):
        if not self.run:
            self.run = True
            self.timer()

    def stop(self):
        if self.run:
            self.run = False
            self.thread.cancel()

    def timer(self):
        if self.run and self.time > 0:
            self.time -= 1
            self.update_time(self.time)
            self.thread = threading.Timer(1, self.timer)
            self.thread.start()
        if self.time == 0:
            self.master.attributes("-topmost", True)
            self.master.attributes("-topmost", False)

    def update_time(self, new_total):
        self.time = new_total
        minutes, seconds = divmod(self.time, 60)
        self.time_string.set(f"{minutes:>02}:{seconds:>02}")

def main(): 
    root = tk.Tk()
    app = Pomodoro(root)
    root.mainloop()

if __name__ == '__main__':
    main()
