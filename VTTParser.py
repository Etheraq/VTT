#!/usr/bin/env python3

import re
from datetime import datetime, date, time, timedelta

fin = "B:\\Python\\VTT\\VTT Files\\XP2_Opening.vtt"
fout = "B:\\Python\\VTT\\VTT Files\\VTT_Edited.vtt"

hr_regex = "^(\d\d):(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d):(\d\d).(\d\d\d).*"
min_regex = "^(\d\d):(\d\d).(\d\d\d) --> (\d\d):(\d\d).(\d\d\d).*"

delta = timedelta(seconds=-10)
cue_start = date.today()
cue_end = date.today()


def print_cue(cue1, cue2):
    cue1_time = cue1.time()
    cue2_time = cue2.time()

    cue_string = cue1_time.isoformat(timespec='milliseconds') + " --> " + \
        cue2_time.isoformat(timespec='milliseconds')

    return cue_string


with open(fin, 'r') as f1, open(fout, 'w') as f2:
    for line in f1:
        if m := re.match(hr_regex, line):
            # print("[cue_start]h: " + m.group(1) + " m: " + m.group(2) + " s:"
            #       + m.group(3) + " mm: " + m.group(4) + "     [cue_end]h: "
            #       + m.group(5) + " m: " + m.group(6) + " s: " + m.group(7)
            #       + " mm: " + m.group(8))

            ms1 = int(m.group(4)) * 1000
            ms2 = int(m.group(8)) * 1000

            cue_start = datetime.combine(date.today(), time(int(m.group(1)),
                                                            int(m.group(2)),
                                                            int(m.group(3)),
                                                            ms1))
            cue_end = datetime.combine(date.today(), time(int(m.group(5)),
                                                          int(m.group(6)),
                                                          int(m.group(7)),
                                                          ms2))
            new_start = cue_start + delta
            new_end = cue_end + delta

            # f2.write(line)
            # f2.write(print_cue(cue_start, cue_end) + line[29:])
            f2.write(print_cue(new_start, new_end) + line[29:])

        elif m := re.match(min_regex, line):
            print("[cue_start]m: " + m.group(1) + " s: " + m.group(2) + "mm: "
                  + m.group(3) + "     [cue_end]m: " + m.group(4) + " s: "
                  + m.group(5) + " mm: " + m.group(6))
            f2.write("**mm:ss.mmm**" + line)
        else:
            f2.write(line)
