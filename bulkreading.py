# -*- coding: utf-8 -*-
# Copyright: Damien Elmes <anki@ichi2.net>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
# Bulk update of readings.
#

from aqt.qt import *
from anki.hooks import addHook
from .reading import mecab, srcFields, dstFields
from .notetypes import isJapaneseNoteType
from aqt import mw

# Bulk updates
##########################################################################

def regenerateReadings(nids):
    global mecab
    mw.checkpoint("Bulk-add Readings")
    mw.progress.start()
    for nid in nids:
        note = mw.col.getNote(nid)
        # Amend notetypes.py to add your note types
        _noteName = note.model()['name'].lower()
        if not isJapaneseNoteType(_noteName):
            continue

        for src, dst in zip(srcFields, dstFields):
            if src in note and dst in note:
                if note[dst]:
                    # already contains data, skip
                    continue

                srcTxt = mw.col.media.strip(note[src])
                if not srcTxt.strip():
                    continue
                try:
                    note[dst] = mecab.reading(srcTxt)
                except Exception as e:
                    mecab = None
                    raise
                note.flush()

    mw.progress.finish()
    mw.reset()

def setupMenu(browser):
    a = QAction("Bulk-add Readings", browser)
    a.triggered.connect(lambda: onRegenerate(browser))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onRegenerate(browser):
    regenerateReadings(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
