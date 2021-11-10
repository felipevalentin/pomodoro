import tkinter as tk
import threading

SECOND = 1
MINUTE_IN_SECONDS = 60 * SECOND
DEFAULT_FOCUS = 25 * MINUTE_IN_SECONDS
DEFAULT_SHORT = 5 * MINUTE_IN_SECONDS
DEFAULT_LONG = 10 * MINUTE_IN_SECONDS


class Timer():
    def __init__(self):
        self.time = DEFAULT_FOCUS
        self.times = {"reset": self.time,
                      "focus": DEFAULT_FOCUS,
                      "long": DEFAULT_LONG,
                      "short": DEFAULT_SHORT}
        self.run = False
        self.thread = None
        self.control = "focus"
        self.time = self.times[self.control]

    def start(self, func):
        if not self.run:
            self.run = True
            self.timer_with_call(func)

    def timer_with_call(self, func):
        if self.run and self.time > 0:
            self.time -= SECOND
            func()
            self.thread = threading.Timer(SECOND, self.timer_with_call, [func])
            self.thread.start()

    def stop(self):
        if self.run:
            self.run = False
            self.thread.cancel()

    def reset(self):
        self.control = "reset"

    @property
    def control(self):
        return self.__control

    @control.setter
    def control(self, control):
        self.stop()
        self.__control = control
        self.time = self.times[control]


class Pomodoro:
    def __init__(self):
        self.master = tk.Tk()
        self.frame = tk.Frame(self.master)
        self.timer = Timer()

        # colors
        self.background_color = "#f6f6f6"

        self.buttons = []
        self.buttons.append(tk.Button(self.frame, text='Focus', command=lambda: self.change_control("focus")))
        self.buttons.append(tk.Button(self.frame, text='Short Break', command=lambda: self.change_control("short")))
        self.buttons.append(tk.Button(self.frame, text='Long Break', command=lambda: self.change_control("long")))
        self.buttons.append(tk.Button(self.frame, text='Start', command=self.start))
        self.buttons.append(tk.Button(self.frame, text='Stop', command=self.stop))
        self.buttons.append(tk.Button(self.frame, text='Reset', command=lambda: self.change_control("reset")))

        # Labels
        self.time_string = tk.StringVar()
        self.time_label = tk.Label(self.frame, textvariable=self.time_string, font=(None, 37,), width=0)

        self.display_on_window()
        self.update_time()
        self.window_config()
        self.button_config()
        self.master.mainloop()

    def display_on_window(self):
        self.time_label.grid(row=1, column=1, pady=17)
        b = 0
        for r in [0, 2]:
            for c in [0, 1, 2]:
                self.buttons[b].grid(row=r, column=c)
                b += 1
        self.frame.pack(pady=4, padx=0)

    def window_config(self):
        self.master.title("Pomodoro")
        self.master.geometry("429x162")
        self.master.resizable(width=False, height=False)
        self.master.config(background=self.background_color)
        self.frame.config(background=self.background_color)
        self.time_label.config(background=self.background_color)
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.eval('tk::PlaceWindow . center')

    def button_config(self):
        for button in self.buttons:
            button["width"] = 14
            button["bg"] = "#dedede"
            button["border"] = 0

    def change_control(self, control):
        self.timer.control = control
        self.update_time()

    def on_closing(self):
        self.timer.stop()
        self.master.destroy()

    def start(self):
        self.timer.start(self.update_time)

    def stop(self):
        self.timer.stop()

    def update_time(self):
        time = self.timer.time
        min, sec = divmod(time, MINUTE_IN_SECONDS)
        self.time_string.set(f"{min:>02}:{sec:>02}")
        if time == 0:
            self.finish()

    def finish(self):
        self.master.bell()
        self.master.attributes("-topmost", True)
        self.master.attributes("-topmost", False)


def main():
    app = Pomodoro()


if __name__ == '__main__':
    main()
