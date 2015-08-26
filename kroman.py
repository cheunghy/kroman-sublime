import sublime, sublime_plugin

import sys, math

head_jamos = [
    'g',
    'gg',
    'n',
    'd',
    'dd',
    'r',
    'm',
    'b',
    'bb',
    's',
    'ss',
    '',
    'j',
    'jj',
    'c',
    'k',
    't',
    'p',
    'h'
]

body_jamos = [
    'a',
    'ae',
    'ya',
    'yae',
    'eo',
    'e',
    'yeo',
    'ye',
    'o',
    'wa',
    'wae',
    'oe',
    'yo',
    'u',
    'weo',
    'we',
    'wi',
    'yu',
    'eu',
    'eui',
    'i'
]

tail_jamos = [
    '',
    'g',
    'gg',
    'gs',
    'n',
    'nj',
    'nh',
    'd',
    'r',
    'rk',
    'rm',
    'rb',
    'rs',
    'rt',
    'rp',
    'rh',
    'm',
    'b',
    'bs',
    's',
    'ss',
    'ng',
    'j',
    'c',
    'k',
    't',
    'p',
    'h'
]


def parse(text):
    if sys.version_info[0] == 2:
        text = unicode(text, 'utf-8')
    retval = u''
    ga = 0xac00
    hih = 0xd7a3
    interval_head = 588
    interval_body = 28
    last_char_is_hangul = False

    for c in text:
        cint = ord(c)
        if ga <= cint <= hih:
            head = int(math.floor((cint - ga) / interval_head))
            headl = int(math.floor((cint - ga) % interval_head))
            body = int(math.floor(headl / interval_body))
            tail = int(math.floor(headl % interval_body))
            if last_char_is_hangul:
                retval += '-'
            retval += head_jamos[head]
            retval += body_jamos[body]
            retval += tail_jamos[tail]
            last_char_is_hangul = True
        else:
            last_char_is_hangul = False
            retval += c
    return retval

class KromanReplaceRegionCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    view = self.view
    for region in view.sel():
      if not region.empty():
        s = view.substr(region)
        s = parse(s)
        view.replace(edit, region, s)

class KromanReplaceFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    allcontent = sublime.Region(0, self.view.size())
    s = self.view.substr(allcontent)
    s = parse(s)
    self.view.replace(edit, allcontent, s)

class KromanCompareFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    whole_region = sublime.Region(0, self.view.size())
    s = self.view.substr(whole_region)
    s = parse(s)
    self.view.window().run_command("set_layout", {"cells": [[0, 0, 1, 1], [1, 0, 2, 1]], "cols": [0.0, 0.5, 1.0], "rows": [0.0, 1.0]})
    # self.view.window().run_command("focus_neighboring_group")
    v = self.view.window().active_view()
    v.insert(edit, 0, s)
