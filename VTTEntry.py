#!/usr/bin/env python3
"""VTTLine Class Object definition

Defines a VTTEntry class to track each entry from a VTT file

Example entry:

'1
00:00:11.288 --> 00:00:14.460 align:middle line:90%
But this has not been without its price.'

VTTEntry variable format analogy:
<sequence>
<cue_start> --> <cue_end> <style>
<text>
"""
import re
from datetime import time


class VTTEntry:
    def __init__(self, index=0, line=1, sequence="",
                 cue_start=time(), cue_end=time(), style={}, text=""):
        """
        Constructor for new VTTEntry object.

        :type index: int
        :param index: class variable to track the order of VTTEntries
                within a given .vtt file

            index does not occur in the .vtt file and is local to the
            VTTEntry class object

            index = 0 should represent "WEBVTT" declaration on line 1

            index should be incremented for each additional entry in the
            vtt file

        :type line: int
        :param line: The line number in the .vtt file where the VTTEntry
                sequence title occurs

            line = 1 should represent "WEBVTT" declaration on line 1
            of every .vtt file

        :type sequence: str
        :param sequence:  The sequence title of the VTTEntry, which
                cannot contain /n or /r

            Sequence title is optional and will mostly appear as ordered
            integers indicating chapter titles. However, sequence may
            be any string.

            For the initial line in the VTT file, sequence = "WEBVTT"
            followed by whitespace and any string. This line declares
            the .vtt file and must appear on line 1 of every .vtt file.

            Example:
            'WEBVTT - Super Movie Subtitles'

            For any comment within the VTT file, sequence="NOTE"
            followed by whitespace and any string.

            Example:
            'NOTE This is a comment.'

        :type cue_start: time
        :type cue_end: time
        :param cue_start: time code when caption is displayed on screen
        :param cue_end: time code when caption is removed from screen

            Cues should use the datetime.time class
            It is a part of the VTT specification that cues use the
            hh:mm:ss.mmm format

            Every caption must have cues, where cue_end >= cue_start

            Example cue entry:
            '00:00:28.314 --> 00:00:31.818'

            cue_start, cue_end=None in WEBVTT declaration, or in NOTE

        :type style: dict
        :param style: CSS-style parameters for aligning and positioning
            captions on the screen

            style should be implemented as a dictionary with
            setting:value pair

            valid settings are:
                'line', 'position', 'align', 'size', 'vertical'

        :type text: str
        :param text: the body of text of the entry
        """
        self.index = index
        self.line = line
        self.sequence = sequence
        self.cue_start = cue_start
        self.cue_end = cue_end
        self.style = style
        self.text = text

    def is_declaration(self):
        """ Tests whether or not the VTTEntry is the initial WEBVTT
            declaration.
            :returns True if entry is the WEBVTT declaration,
                False if not
        """
        if re.match(r"^WEBVTT", self.sequence):
            return True
        else:
            return False

    def is_note(self):
        """Tests whether or not the VTTEntry is a comment
            :returns True if entry is a comment, False if not
        """
        if re.match(r"^NOTE", self.sequence):
            return True
        else:
            return False

    def is_caption(self):
        """Tests whether or not the VTTEntry is a caption
            :returns True if entry is a caption

        """
        if not self.is_declaration() and not self.is_note():
            if self.cue_start is not None \
                    and self.cue_start is not None:
                return True
        else:
            return False

    def is_valid(self):
        """Tests whether or not the VTTEntry is a validly formatted
            WEBVTT entry.
        """
        # TODO Write is_valid function
