"""
Inspiration from Bojack Horseman S4 E9 "The Bean System"
Beanary (binary) encoded time
1 bean ~ 1 minute
"""
import datetime
from tkinter import *
from tkinter.ttk import *


def int_to_binary_to_string(intput: int) -> str:
    """Int to binary to string."""
    b_val = bin(intput).replace("0b", "")
    return b_val


def time_to_bean(ut: datetime.datetime.now().time()) -> list:
    """Gets the time and changes the hours, minutes, and seconds into beanary strings."""
    bean_hours = int_to_binary_to_string(ut.hour)
    while len(bean_hours) < 5:  # Max UT hour 24 -> binary length == 5 (11000)
        bean_hours = "0" + bean_hours
    bean_minutes = int_to_binary_to_string(ut.minute)
    while len(bean_minutes) < 6:  # Max UT minute 60 -> binary length == 6 (111100)
        bean_minutes = "0" + bean_minutes
    bean_seconds = int_to_binary_to_string(ut.second)
    while len(bean_seconds) < 6:  # Max UT second 60 -> binary length == 6 (111100)
        bean_seconds = "0" + bean_seconds
    return [bean_hours, bean_minutes, bean_seconds]


def time_to_txt(ut: datetime.datetime.now().time(), bt: list, fina_show: bool = False) -> str:
    """Print real time and bean time in beanary or get the string."""
    viz = "\t| UT \t| The Bean System\n" \
          "Hour:\t| {} \t| {}\n" \
          "Minute:\t| {} \t| {}\n" \
          "Second:\t| {} \t| {}".format(ut.hour,   bt[0].replace("1", "•").replace("0", "·"),
                                        ut.minute, bt[1].replace("1", "•").replace("0", "·"),
                                        ut.second, bt[2].replace("1", "•").replace("0", "·"))
    if fina_show:
        print(viz)
    return viz


def visualize_times() -> None:
    # creating tkinter window
    root = Tk()
    root.title('The Bean System')

    # This function is used to display time on the label
    def time():
        ut = datetime.datetime.now().time()
        bt = time_to_bean(ut)
        string = time_to_txt(ut, bt)
        lbl.config(text=string)
        lbl.after(1000, time)

    # Styling the label widget so that clock will look more attractive <3
    lbl = Label(root, font=('calibri', 20, 'bold'), background='purple', foreground='white')
    lbl.pack(anchor='center')
    time()

    mainloop()


visualize_times()
