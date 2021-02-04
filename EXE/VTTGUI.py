#!/usr/bin/env python3
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime, date, time, timedelta
import os
import re
import math

# root frame
root = Tk()
root.title("VTT CueEdit")

# global variables
file1_path, file2_path = "", ""
file1_name, file1_content = "", ""
mode = StringVar()
mode.set("zero")
delta = timedelta()
delta_hr = StringVar()
delta_hr.set("00")
delta_min = StringVar()
delta_min.set("00")
delta_sec = StringVar()
delta_sec.set("00")
delta_milli = StringVar()
delta_milli.set("000")

# TODO Need to update delta on text entry into spinboxes

def openfile():
    """Creates an Open File dialog window and sets the application
        variables to reflect the new file data."""

    global file1_path, file1_name, file1_content
    file1_path = filedialog.askopenfilename(parent=mainframe,
                                            initialdir=os.getcwd(),
                                            title="Open WEBVTT File",
                                            filetypes={("*.vtt", "*.vtt")})
    file1_name = re.sub(r".*\/", "", file1_path)

    newcue1 = get_cuedelta(get_firstcue())
    newcue2 = get_cuedelta(re.findall(r"(\d\d:\d\d:\d\d\.\d\d\d)",
                                      get_firstcueline())[1])
    update_entry(newcue, get_cueline(newcue1, newcue2))
    update_entry(filelabel, file1_name)
    update_entry(oldcue, get_firstcueline())

    set_zero()


def savefile():
    """Creates a Save As file dialog window and creates a new file
    reflecting the altered cue times"""
    global file2_path
    file2_path = filedialog.asksaveasfilename(parent=mainframe,
                                              initialdir=os.getcwd(),
                                              title="Export Modified VTT "
                                                    "File",
                                              filetypes={("*.vtt", "*.vtt")})

    write_newvtt(file1_path, file2_path)


def get_firstcueline():
    """Retrieves the first cue line found in the file
    :returns string - first cue line in 'hh:mm:ss.mmm --> hh:mm:ss.mmm'
    format"""
    with open(file1_path, 'r', encoding='utf-8') as f1:
        m = re.search(r"(\d\d:.*\.\d\d\d\s)", f1.read())
        return m.group(1)


def get_firstcue():
    """Retrieves the first cue found in the file
    :returns string - the first cue in '00:00:00.000' format"""
    cue = get_firstcueline()
    return cue[0:12]


def ch_mode():
    """reflects changes in the mode StrVar() from the radio dialog buttons"""

    if mode.get() == "add":
        hrspin.state(["!readonly", "!disabled"])
        minspin.state(["!readonly", "!disabled"])
        secspin.state(["!readonly", "!disabled"])
        millispin.state(["!readonly", "!disabled"])
        set_delta()
    elif mode.get() == "subtract":
        hrspin.state(["!readonly", "!disabled"])
        minspin.state(["!readonly", "!disabled"])
        secspin.state(["!readonly", "!disabled"])
        millispin.state(["!readonly", "!disabled"])
        set_delta()
    elif mode.get() == "zero":
        set_zero
        pass


def get_cuedelta(cue="00:00:00.000"):
    """:param: cue - a string in 'hh:mm:ss.mmm' format
    :returns timedelta() """
    hr = int(cue[0:2])
    minute = int(cue[3:5])
    sec = int(cue[6:8])
    micro = int(cue[9:]) * 1000
    return timedelta(hours=hr, minutes=minute, seconds=sec, microseconds=micro)


def get_cue(td=timedelta()):
    """:param td - a timedelta() object
    :returns a string in 'hh:mm:ss.mmm' format"""
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


def set_delta():
    """Updates the delta variable and changes the newcue Entry box to reflect
    what the adjusted cue line will look like with the new delta changes."""

    global delta

    delta = timedelta(hours=int(hrspin.get()), minutes=int(minspin.get()),
                      seconds=int(secspin.get()), milliseconds=int(
            millispin.get()))
    if mode.get() == "add":
        newcue1 = get_cuedelta(get_firstcue()) + delta
        newcue2 = get_cuedelta(re.findall(r"(\d\d:\d\d:\d\d\.\d\d\d)",
                                          get_firstcueline())[1]) + delta
    elif mode.get() == "subtract" and delta <= get_cuedelta(get_firstcue()):
        newcue1 = get_cuedelta(get_firstcue()) - delta
        newcue2 = get_cuedelta(re.findall(r"(\d\d:\d\d:\d\d\.\d\d\d)",
                                          get_firstcueline())[1]) - delta
    else:
        raise OSError

    update_entry(newcue, get_cueline(newcue1, newcue2))


def update_entry(name=Entry(), string=""):
    """Clears the text in an entry box and replaces it with string
    :param name - the name of and Entry box
    :param string - the text string to display in the Entry box"""

    name.state(["!readonly"])
    name.delete(0, 255)
    name.insert(0, string)
    name.state(["readonly"])


def set_zero():
    """Called when the zeroradio buttion is selected.
    Sets the time delta to equal the time of the first cue in the
    file and updates the spinners in the Time Adjustment window to
    become readonly and reflect the new time delta value
    """
    global delta, delta_hr, delta_min, delta_sec, delta_milli

    delta = get_cuedelta(get_firstcue())

    newcue1 = get_cuedelta(get_firstcue()) - delta
    newcue2 = get_cuedelta(re.findall(r"(\d\d:\d\d:\d\d\.\d\d\d)",
                                      get_firstcueline())[1]) - delta
    update_entry(newcue, get_cueline(newcue1, newcue2))

    delta_hr = str(math.floor(delta.seconds / 3600))
    hrspin.set(delta_hr)
    seconds = delta.seconds - int(delta_hr * 3600)
    delta_min = str(math.floor(seconds / 60))
    minspin.set(delta_min)
    seconds -= int(delta_min * 60)
    delta_sec = str(seconds)
    secspin.set(delta_sec)
    delta_milli = str(int(delta.microseconds / 1000))
    millispin.set(delta_milli)

    if int(delta_hr) <= 9:
        hrspin.state(["!readonly", "!disabled"])
        hrspin.set("0" + delta_hr)
        hrspin.state(["readonly", "disabled"])
    else:
        hrspin.state(["!readonly", "!disabled"])
        hrspin.set(delta_hr)
        hrspin.state(["readonly", "disabled"])

    if int(delta_min) <= 9:
        minspin.state(["!readonly", "!disabled"])
        minspin.set("0" + delta_min)
        minspin.state(["readonly", "disabled"])
    else:
        minspin.state(["!readonly", "!disabled"])
        minspin.set(delta_min)
        minspin.state(["readonly", "disabled"])

    if int(delta_sec) <= 9:
        secspin.state(["!readonly", "!disabled"])
        secspin.set("0" + delta_sec)
        secspin.state(["readonly", "disabled"])
    else:
        secspin.state(["!readonly", "!disabled"])
        secspin.set(delta_sec)
        secspin.state(["readonly", "disabled"])

    if 10 <= int(delta_milli) < 100:
        millispin.state(["!readonly", "!disabled"])
        millispin.set("0" + delta_milli)
        millispin.state(["readonly", "disabled"])
    elif int(delta_milli) < 10:
        millispin.state(["!readonly", "!disabled"])
        millispin.set("00" + delta_milli)
        millispin.state(["readonly", "disabled"])
    else:
        millispin.state(["!readonly", "!disabled"])
        millispin.set(delta_milli)
        millispin.state(["readonly", "disabled"])


def print_newcue(cueline):
    hr_regex = r"^(\d\d):(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d):(\d\d).(" \
               r"\d\d\d).*"
    min_regex = r"^(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d).(\d\d\d).*"
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
            cue_start += delta
            cue_end += delta
        elif mode.get() == "subtract" or mode.get() == "zero":
            cue_start -= delta
            cue_end -= delta
        else:
            print(mode)
            print(repr(cue_start))
            print(repr(cue_end))
            print(repr(delta))
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
        cue_start += delta
        cue_end += delta

        return cue_start.isoformat(timespec='milliseconds')[14:] \
               + " --> " + cue_end.isoformat(timespec='milliseconds')[14:] \
               + cueline[23:]
    else:
        raise OSError  # TODO Proper error handling


def write_newvtt(fin, fout):
    hr_regex = r"^(\d\d):(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d):(\d\d).(" \
               r"\d\d\d).*"
    min_regex = r"^(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d).(\d\d\d).*"
    with open(fin, 'r', encoding='utf-8') as f1, open(fout, 'w',
                                                      encoding='utf-8') as f2:
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
                           value="add", command=ch_mode)
subradio = ttk.Radiobutton(radioframe, text="Subtract Time", variable=mode,
                           value="subtract", command=ch_mode)
zeroradio = ttk.Radiobutton(radioframe, text="Zero First Cue", variable=mode,
                            value="zero", command=set_zero)
modelabel = ttk.Label(radioframe, text="")

# radioframe widget layout
addradio.grid(column=0, row=0, padx=5, pady=1, sticky="w")
subradio.grid(column=0, row=1, padx=5, pady=1, sticky="w")
zeroradio.grid(column=0, row=2, padx=5, pady=1, sticky="w")

# timeframe widgets
# spinboxes
hrspin = ttk.Spinbox(timeframe, textvariable=delta_hr, from_=0.0, to=23,
                     width=3, wrap=True, state=["readonly"], validate="key",
                     command=set_delta)
minspin = ttk.Spinbox(timeframe, textvariable=delta_min, from_=0.0, to=59,
                      width=3, wrap=True, state=["readonly"], validate="key",
                      command=set_delta)
secspin = ttk.Spinbox(timeframe, textvariable=delta_sec, from_=0.0, to=59,
                      width=3, wrap=True, state=["readonly"], validate="key",
                      command=set_delta)
millispin = ttk.Spinbox(timeframe, textvariable=delta_milli, from_=0.0,
                        to=999, increment=50, width=4, wrap=True,
                        state=["readonly"], validate="key", command=set_delta)
# spinbox punctuation separators
ttk.Label(timeframe, text=":").grid(column=1, row=1)
ttk.Label(timeframe, text=":").grid(column=3, row=1)
ttk.Label(timeframe, text=".").grid(column=5, row=1)
# spinbox labels
hrlabel = ttk.Label(timeframe, text="hrs")
minlabel = ttk.Label(timeframe, text="mins")
seclabel = ttk.Label(timeframe, text="secs")
microlabel = ttk.Label(timeframe, text="micros")

# timeframe widget layout
# spinboxes
hrspin.grid(column=0, row=1, padx=1, sticky="w")
minspin.grid(column=2, row=1, padx=1, sticky="we")
secspin.grid(column=4, row=1, padx=1, sticky="we")
millispin.grid(column=6, row=1, padx=1, sticky="e")
hrlabel.grid(column=0, row=2, sticky="we")
minlabel.grid(column=2, row=2, sticky="we")
seclabel.grid(column=4, row=2, sticky="we")
microlabel.grid(column=6, row=2, sticky="we")

# run
root.mainloop()