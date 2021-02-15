#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, date, time, timedelta
import zlib, base64
import tempfile
import os
import re
import math

# root frame
root = Tk()
root.title("VTT CueEdit")
root.resizable(0, 0)  # root window cannot be resized
ICON=zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))
_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

root.iconbitmap(default=ICON_PATH)

# global variables
file1_path, file2_path = "", ""
file1_name = ""
mode = StringVar()
mode.set("add")
zero = IntVar()
zero.set(0)
delta = timedelta(hours=0, minutes=0, seconds=0, milliseconds=0)
zero_delta = timedelta(hours=0, minutes=0, seconds=0, milliseconds=0)


def openfile():
    """Creates an Open File dialog window and sets the application
        variables to reflect the new file data."""

    global file1_path, file1_name
    file1_path = filedialog.askopenfilename(parent=mainframe,
                                            initialdir=os.getcwd(),
                                            title="Open WEBVTT File",
                                            filetypes={("*.vtt", "*.vtt")})
    file1_name = re.sub(r".*\/", "", file1_path)

    newcue1 = get_cuedelta(get_firstcue())
    newcue2 = get_cuedelta(re.findall(r"(\d\d:.*?.\d\d\d)",
                                      get_firstcueline())[1])
    update_entry(newcue, get_cueline(newcue1, newcue2))
    update_entry(filelabel, file1_name)
    update_entry(oldcue, get_firstcueline())
    enable_widgets()


def enable_widgets():
    zerocheck.state(["!disabled"])
    addradio.state(["!disabled"])
    subradio.state(["!disabled"])
    hrspin.state(["!readonly"])
    minspin.state(["!readonly"])
    secspin.state(["!readonly"])
    millispin.state(["!readonly"])
    hrspin.set(0)
    minspin.set(0)
    secspin.set(0)
    millispin.set(0)
    mode.set("add")


def savefile():
    """Creates a Save As file dialog window and creates a new file
    reflecting the altered cue times"""
    global file2_path, delta

    if file1_name != "":
        default_file2 = file1_name[:len(file1_name) - 4] + "_edit.vtt"
        file2_path = filedialog.asksaveasfilename(parent=mainframe,
                                                  initialdir= \
                                                      os.path.realpath(
                                                          file1_path),
                                                  initialfile=default_file2,
                                                  title="Export Modified VTT "
                                                        "File",
                                                  filetypes={("*.vtt",
                                                              "*.vtt")})
        write_newvtt(file1_path, file2_path)
    elif mode.get() == "subtract" and delta > get_cuedelta(get_firstcue()):
        messagebox.showwarning(title="Negative Time",
                               message="Trying to set a negative time value")
    else:
        messagebox.showwarning(title="No file found",
                               message="No .vtt file found to export. "
                                       "Please open a file first.")


def get_firstcueline():
    """Retrieves the first cue line found in the file
    :returns string - first cue line in 'hh:mm:ss.mmm --> hh:mm:ss.mmm'
    format"""
    try:
        with open(file1_path, 'r', encoding='utf-8') as f1:
            m = re.search(r"(\d\d:.*\.\d\d\d)", f1.read())
            return m.group(1)
    except FileNotFoundError:
        return '00:00:00.000 --> 00:00:00.000'


def get_firstcue():
    """Retrieves the first cue found in the file
    :returns string - the first cue in '00:00:00.000' format"""

    if len(get_firstcueline()) == 29:
        try:
            cue = get_firstcueline()
            return cue[0:12]
        except TypeError:
            return '00:00:00.000'
    elif len(get_firstcueline()) == 23:
        try:
            cue = get_firstcueline()
            return cue[0:9]
        except TypeError:
            return '00:00:00.000'
    else:
        return '00:00:00.000'


def get_cuedelta(cue="00:00:00.000"):
    """:param: cue - a string in 'hh:mm:ss.mmm' format
    :returns timedelta() """
    if len(cue) == 12:
        hr = int(cue[0:2])
        minute = int(cue[3:5])
        sec = int(cue[6:8])
        micro = int(cue[9:]) * 1000
        return timedelta(hours=hr, minutes=minute, seconds=sec,
                         microseconds=micro)
    elif len(cue) == 9:
        minute = int(cue[0:2])
        sec = int(cue[3:5])
        micro = int(cue[7:]) * 1000
        return timedelta(hours=0, minutes=minute, seconds=sec,
                         microseconds=micro)


def get_cue(td=timedelta()):
    """
    :param td - a timedelta() object
    :return a string in 'hh:mm:ss.mmm' format"""
    hh = str(math.floor(td.seconds / 3600))
    remaining = td.seconds - int(hh) * 3600
    mm = str(math.floor(remaining / 60))
    remaining -= int(mm) * 60
    ss = str(remaining)
    mmm = str(int(td.microseconds / 1000))

    while len(hh) < 2:
        hh = "0" + hh
    while len(mm) < 2:
        mm = "0" + mm
    while len(ss) < 2:
        ss = "0" + ss
    while len(mmm) < 3:
        mmm = "0" + mmm
    return hh + ":" + mm + ":" + ss + "." + mmm


def get_cueline(cue1=timedelta(), cue2=timedelta()):
    return get_cue(cue1) + " --> " + get_cue(cue2)


def update_cueline():
    """Updates the newcue Entry box to reflect what the adjusted cue line
    will look like with the new delta changes."""
    if hrspin.get() == '':
        hrspin.set(0)
    if minspin.get() == '':
        minspin.set(0)
    if secspin.get() == '':
        secspin.set(0)
    if millispin.get() == '':
        millispin.set(0)

    new_delta = timedelta(hours=int(hrspin.get()), minutes=int(minspin.get()),
                          seconds=int(secspin.get()),
                          milliseconds=int(millispin.get()))

    if zero.get() == 0:
        if mode.get() == "add":
            newcue1 = get_cuedelta(get_firstcue()) + new_delta
            newcue2 = get_cuedelta(re.findall(r"(\d\d:.*?\.\d\d\d)",
                                              get_firstcueline())[1]) + \
                new_delta
            update_entry(newcue, get_cueline(newcue1, newcue2))
        elif mode.get() == "subtract" and new_delta <= get_cuedelta(
                get_firstcue()):
            newcue1 = get_cuedelta(get_firstcue()) - new_delta
            newcue2 = get_cuedelta(re.findall(r"(\d\d:.*?.\d\d\d)",
                                              get_firstcueline())[1]) - \
                new_delta
            update_entry(newcue, get_cueline(newcue1, newcue2))
        else:
            update_entry(newcue, "***INVALID: Negative Time Value***")
    elif zero.get() == 1:
        newcue1 = get_cuedelta(get_firstcue()) - zero_delta + new_delta
        newcue2 = get_cuedelta(re.findall(r"(\d\d:.*?\.\d\d\d)",
                                          get_firstcueline())[1]) - \
            zero_delta + new_delta
        update_entry(newcue, get_cueline(newcue1, newcue2))


def validate_hour(data):
    """Validation methods to ensure data from the hrspin spinbox is valid.
    Disallows entry if not a hour value between 0 & 23 or backspace
    """
    if data.isdigit():
        if 0 < int(data) <= 23:
            hrspin.set(int(data))
            hrspin.icursor("end")
            update_cueline()
            return True
        else:
            return False
    elif data == "\b":
        return True
    else:
        return False


def validate_min(data):  # validates minute spinbox
    if data.isdigit():
        if 0 < int(data) <= 60:
            minspin.set(int(data))
            minspin.icursor("end")
            update_cueline()
            return True
        else:
            return False
    elif data == "\b":
        return True
    elif data == '':
        return True
    else:
        return False


def validate_sec(data):  # validates second spinbox
    if data.isdigit():
        if 0 < int(data) <= 60:
            secspin.set(int(data))
            secspin.icursor("end")
            update_cueline()
            return True
        else:
            return False
    elif data == "\b":
        return True
    elif data == '':
        return True
    else:
        return False


def validate_milli(data):  # validates millisecond spinbox
    if data.isdigit():
        if 0 < int(data) <= 999:
            millispin.set(int(data))
            millispin.icursor("end")
            update_cueline()
            return True
        else:
            return False
    elif data == "\b":
        return True
    elif data == '':
        return True
    else:
        return False


def update_entry(name=Entry(), string=""):
    """Clears the text in an entry box and replaces it with string
    :param name - the name of and Entry box
    :param string - the text string to display in the Entry box"""

    name.state(["!readonly"])
    name.delete(0, 255)
    name.insert(0, string)
    name.state(["readonly"])


def set_zero():
    """Called when the zerocheck checkbox is selected.
    Sets the time zero_delta to equal the time of the first cue in the
    file, sets the displayed cueline to zero and disables the subtract time
    radio button
    """
    global zero_delta

    if zero.get() == 1:
        zero_delta = get_cuedelta(get_firstcue())
        newcue1 = get_cuedelta(get_firstcue()) - zero_delta
        newcue2 = get_cuedelta(re.findall(r"(\d\d:.*?\.\d\d\d)",
                                          get_firstcueline())[1]) - zero_delta
        update_entry(newcue, get_cueline(newcue1, newcue2))
        hrspin.set(0)
        minspin.set(0)
        secspin.set(0)
        millispin.set(0)
        subradio.config(state=["disabled"])
        mode.set("add")
    elif zero.get() == 0:
        zero_delta = timedelta(0)
        newcue1 = get_cuedelta(get_firstcue())
        newcue2 = get_cuedelta(re.findall(r"(\d\d:.*?\.\d\d\d)",
                                          get_firstcueline())[1])
        update_entry(newcue, get_cueline(newcue1, newcue2))
        subradio.config(state=["!disabled"])


def set_delta():
    global delta
    delta = timedelta(hours=int(hrspin.get()), minutes=int(minspin.get()),
                      seconds=int(secspin.get()),
                      milliseconds=int(millispin.get()))


def print_newcue(cueline):
    """Used in writing the new file. and prints a new cueline with the
    new time value.
    :param a line string from the original file that includes a cue
    :returns string line with the new cue values
    """
    hr_regex = r"^(\d\d):(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d):(\d\d).(" \
               r"\d\d\d).*"
    min_regex = r"^(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d).(\d\d\d).*"
    set_delta()
    # if cues are in format 00:00:00.000
    if m := re.match(hr_regex, cueline):
        # search cueline for start & end cues and group relevant time values
        # (00):(00):(04).(840) --> (00):(00):(06).(990) rest of line
        ms1 = int(
            m.group(4)) * 1000  # convert milliseconds to microseconds
        ms2 = int(
            m.group(8)) * 1000  # convert milliseconds to microseconds

        # getting hour, minute, second, microsecond values from the cue line
        cue_start = datetime.combine(date.today(),
                                     time(hour=int(m.group(1)),
                                          minute=int(m.group(2)),
                                          second=int(m.group(3)),
                                          microsecond=ms1))
        cue_end = datetime.combine(date.today(),
                                   time(hour=int(m.group(5)),
                                        minute=int(m.group(6)),
                                        second=int(m.group(7)),
                                        microsecond=ms2))
        # adjusting the cue time by delta
        if mode.get() == "add":
            if zero.get() == 0:
                cue_start += delta
                cue_end += delta
            elif zero.get() == 1:
                cue_start = cue_start - zero_delta + delta
                cue_end = cue_end - zero_delta + delta
        elif mode.get() == "subtract":
            cue_start -= delta
            cue_end -= delta
        else:
            raise OSError
        return cue_start.isoformat(timespec='milliseconds')[11:] + " --> " \
               + cue_end.isoformat(timespec='milliseconds')[11:] + cueline[29:]

    # if cues are in format 00:00.000
    elif m := re.match(min_regex, cueline):
        # search the input line for two cues and grouping relevant time values
        # (00):(04).(840) --> (00):(06).(990)
        ms1 = int(
            m.group(3)) * 1000  # convert milliseconds to microseconds
        ms2 = int(
            m.group(6)) * 1000  # convert milliseconds to microseconds

        # getting hour, minute, second, microsecond values from the cue line
        cue_start = datetime.combine(date.today(), time(hour=0,
                                                        minute=int(
                                                            m.group(
                                                                1)),
                                                        second=int(
                                                            m.group(
                                                                2)),
                                                        microsecond=ms1))
        cue_end = datetime.combine(date.today(), time(hour=0,
                                                      minute=int(
                                                          m.group(4)),
                                                      second=int(
                                                          m.group(5)),
                                                      microsecond=ms2))
        # adjusting the cue time by delta
        if mode.get() == "add":
            if zero == 0:
                cue_start += delta
                cue_end += delta
            elif zero == 1:
                cue_start = cue_start - zero_delta + delta
                cue_end = cue_end - zero_delta + delta
        elif mode.get() == "subtract":
            cue_start -= delta
            cue_end -= delta
        else:
            raise OSError

        return cue_start.isoformat(timespec='milliseconds')[8:] \
               + " --> " + cue_end.isoformat(timespec='milliseconds')[8:] \
               + cueline[23:]
    else:
        raise OSError


def write_newvtt(fin, fout):
    """Reads through the old file and writes into the new file with the
    altered cue values."""
    # regex strings for locating cues within each line
    hr_regex = r"^\d\d:\d\d:\d\d.\d\d\d --> \d\d:\d\d:\d\d.\d\d\d.*"
    min_regex = r"^\d\d:\d\d.\d\d\d --> \d\d:\d\d.\d\d\d.*"

    with open(fin, 'r', encoding='utf-8') as f1, \
            open(fout, 'w', encoding='utf-8') as f2:
        for line in f1:
            if re.match(hr_regex, line):
                f2.write(print_newcue(line))
            elif re.match(min_regex, line):
                f2.write(print_newcue(line))
            else:
                f2.write(line)


# Frames
mainframe = ttk.Frame(root, padding="5 5 5 5")
radioframe = ttk.Frame(mainframe, padding="5 5 5 5")
timeframe = ttk.LabelFrame(mainframe, padding="5 5 5 5", text="Time "
                                                              "Adjustment")

# Frame layout
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.grid(row=0, sticky="nsew")
radioframe.grid(column=0, row=1, rowspan=2, columnspan=2, sticky="nw")
timeframe.grid(column=2, row=2, sticky="e")

# mainframe widgets
open_button = ttk.Button(mainframe, text="Open File", command=openfile)
export_button = ttk.Button(mainframe, text="Export As...", command=savefile)
filelabel = ttk.Entry(mainframe, text=file1_name)
filelabel.state(["readonly"])
# cue viewer textboxes
oldcuelabel = ttk.Label(mainframe, text="Original First Cue: ")
oldcue = ttk.Entry(mainframe)
oldcue.insert(0, "00:00:00.000 --> 00:00:00.000")
oldcue.state(["readonly"])
newcuelabel = ttk.Label(mainframe, text="Adjusted First Cue: ")
newcue = ttk.Entry(mainframe, text="00:00:00.000")
newcue.insert(0, "00:00:00.000 --> 00:00:00.000")
newcue.state(["readonly"])

# mainframe widget layout
open_button.grid(column=0, row=0, padx=10, pady=5, sticky="w")
export_button.grid(column=2, row=8, padx=5, pady=5, sticky="e")
filelabel.grid(column=1, row=0, columnspan=2, padx=5, sticky="we")
# cue viewer textboxes
oldcuelabel.grid(column=0, row=4, pady=1, sticky="e")
oldcue.grid(column=1, row=4, columnspan=4, pady=1, sticky="we")
newcuelabel.grid(column=0, row=5, sticky="e")
newcue.grid(column=1, row=5, columnspan=4, sticky="we")

# radioframe widgets
addradio = ttk.Radiobutton(radioframe, text="Add Time", variable=mode,
                           value="add", state=["disabled"])
subradio = ttk.Radiobutton(radioframe, text="Subtract Time", variable=mode,
                           value="subtract", state=["disabled"])

# checkbox widget
zerocheck = ttk.Checkbutton(radioframe, text="Zero First Cue", variable=zero,
                            command=set_zero, state=["disabled"])
modelabel = ttk.Label(radioframe, text="")

# radioframe widget layout
zerocheck.grid(column=0, row=0, padx=5, pady=1, sticky="w")
addradio.grid(column=0, row=1, padx=5, pady=1, sticky="w")
subradio.grid(column=0, row=2, padx=5, pady=1, sticky="w")

# timeframe widgets
# spinboxes
range_hour = root.register(validate_hour)
range_min = root.register(validate_min)
range_sec = root.register(validate_sec)
range_milli = root.register(validate_milli)
hrspin = ttk.Spinbox(timeframe, from_=0.0, to=23, width=3, wrap=True,
                     validate="key", validatecommand=(range_hour, '%P'),
                     state=["readonly"], command=update_cueline)
minspin = ttk.Spinbox(timeframe, from_=0.0, to=59, width=3, wrap=True,
                      validate="key", validatecommand=(range_min, '%P'),
                      state=["readonly"], command=update_cueline)
secspin = ttk.Spinbox(timeframe, from_=0.0, to=59, width=3, wrap=True,
                      validate="key", validatecommand=(range_sec, '%P'),
                      state=["readonly"], command=update_cueline)
millispin = ttk.Spinbox(timeframe, from_=0.0, to=999, width=4, wrap=True,
                        increment=50,
                        validate="key", validatecommand=(range_milli, '%P'),
                        state=["readonly"], command=update_cueline)
# spinbox punctuation separators
ttk.Label(timeframe, text=":").grid(column=1, row=1)
ttk.Label(timeframe, text=":").grid(column=3, row=1)
ttk.Label(timeframe, text=".").grid(column=5, row=1)
# spinbox labels
hrlabel = ttk.Label(timeframe, text="hrs")
minlabel = ttk.Label(timeframe, text="mins")
seclabel = ttk.Label(timeframe, text="secs")
millilabel = ttk.Label(timeframe, text="milli")

# timeframe widget layout
# spinboxes
hrspin.grid(column=0, row=1, padx=1, sticky="w")
minspin.grid(column=2, row=1, padx=1, sticky="we")
secspin.grid(column=4, row=1, padx=1, sticky="we")
millispin.grid(column=6, row=1, padx=1, sticky="e")
hrlabel.grid(column=0, row=2, sticky="we")
minlabel.grid(column=2, row=2, sticky="we")
seclabel.grid(column=4, row=2, sticky="we")
millilabel.grid(column=6, row=2, sticky="we")

# run
root.mainloop()
