#!/usr/bin/env python3
# encoding: utf-8
# fmt: off
# api: python
# type: gui
# title: cookiedough
# description: browser and install GUI for cookiecutter templates
# category: viewer
# version: 0.0.7
# state:   alpha
# license: proprietary
# config:
#     { name: colorize, type: bool, value: 1, description: Colorize the readme preview a bit }
#     { name: sort, type: select, value: all, select: all|size|stars|forks|name|vars|files|updated_at, description: Primary scoring/sorting property }
#     { name: show_counts, type: bool, value: 1, description: Show number of entries per language/api category }
# priority: core
# depends: python >= 3.8, python:PySimpleGUI >= 4.37, python:cookiecutter >= 1.7,
#     python:pluginconf, python:ttkthemes, python:appdirs, python:requests
# architecture: all
# classifiers: x11, code generators, packaging
# url: https://fossil.include-once.org/cookiedough/
# freshcode: https://freshcode.club/projects/cookiedough
#
# Still a very basic/alpha GUI tool to uncover project templates.
#
# 🞂 Browse existing cookiecutter templates in the left pane.
# 🞂 Or use the search bar to find them by filenames or supported features.
# 🞂 Inspect the README preview or file list, or open the URL to view its repo.
# 🞂 And finally install the template via cookiecutter(1).
#   It will usually be unpackaged into the current working directory, so be
#   mindful where you started cookiedough from.
#
# There's a few settings in the 🞂File 🞂Settings menu. You can also inspect
# available template infos in the  🞂Template 🞂Details view.
#
# Comes with a precompiled list of templates from GitHub.  See dev/ for aquisition
# tools. (Probably not doing that again. Project certainly requires contributors to
# be sustainable. Or a submission API and storage in e.g. a fossil/sqlite table.)


import sys, os, re, json, subprocess, warnings
import tkinter as tk, PySimpleGUI as sg, ttkthemes  # ⚠ install python3-tk / tkinter in your distro package manager
import pluginconf, pluginconf.gui, appdirs, requests
from operator import itemgetter
from traceback import format_exc


#-- init
__dir__ = re.sub("[\w.-]+$", "", __file__)
__meta__ = pluginconf.plugin_meta(fn=__file__)
conf = {
    "colorize": True,
    "sort": "all",
    "show_counts": True,
    "theme": "DarkBlue2",
    "conf_file": appdirs.user_config_dir("cookiedough", "io") + "/settings.json",
}
try: conf.update(json.load(open(conf['conf_file'], "r", encoding="utf-8")))
except: pass
conf["debug"] = "--debug" in sys.argv


#-- JSON blob of templates
class repos():
    def __init__(self):
        fn = re.sub("[\w.]+$", "uidata.json", __file__)
        self.ls = json.load(open(fn, "r", encoding="utf-8"))
        
    def tree(self, ls=None):
        """ Convert to tree list """
        t = sg.TreeData()
        if not ls:
            ls = self.ls
        if isinstance(ls, dict):
            ls = ls.values()
        # todo: sort by non-existant scoring of course
        self.add_counted_titles(t, ls)
        for d in ls:
            t.insert(parent=d["api"], key=d["name"], text=d["short"], values=[""])
        return t
    
    # sorts d[api] categories/titles by number of entries, and prepopulates tree
    def add_counted_titles(self, t, ls):
        ls = [d["api"] for d in ls]
        counts = { k: ls.count(k) for k in set(ls) }
        counts = sorted(counts.items(), key=itemgetter(1), reverse=True)
        for api, n in counts:
            t.insert(parent="", key=api, text=api.title(), values=[n if conf["show_counts"] else ""])
        
    # filter .ls by given list of strings
    def search(self, keywords):
        new = {}
        for k,d in self.ls.items():
            text = "\n".join([  d["name"], d["name"], d["readme"], d["dir"], d["keywords"], repr(d["config"])  ])
            if all(re.search(m, text) for m in keywords):
                new[k] = d
        return new
    
    def sort(self, dicts, prop="all"):
        if prop in ("size","name","stars","forks"):
            f = lambda d: d.get(prop)
        elif prop in ("vars",):
            f = lambda d: len(d[prop])
        else:
            f = lambda d: d["score"][prop]
        return sorted(dicts, key=f, reverse=True)

repos = repos()


#-- image data
class icons:
    search_bg = b"""iVBORw0KGgoAAAANSUhEUgAAASwAAAAgCAIAAAAnqtLtAAAABmJLR0QAKQCAALlmGuaiAAAACXBIWXMAAAsTAAALEwEAmpwYAAAHLUlEQVR42u2dy28bxxnAv9kd7vL9EmmSomiJYvRgZdVOlLiCLSOKFSBt0NyKAm3QAo0P6aFo/oVeejN66KGIc3FTpAUaFCmKIIiltJYTuDISR3VMPWm9LUskJZoUHyK53Mf0sDKrGJFK0iLpiPM7jaCd/bi78+N8M7uzRMHfjAKFQmkcDD0FFEpjwU9YX6tBXXZOLgqKoqxspbKCRM8p5Rhj5LH/hIVhGJbjw3GhKDdUQpsOu7TScjRhcjhePN3qMnIBp8Gk1dDrRDnGZAri0vZuLFv8NByDXLLXbYsVcDIv1VtCp4lv08kz69uD3/Nf+cmzDMOgR5S22V+mUL7tEELUQgvH2U16QsirpzyKolydWPnL56tnfI61LJPMFavbOap0YsbMMyaS62u1/Ppil0XPsyzLsmzJQOoepRlsJIQQQmRZlmU5lRN+f31hejOVRfq0oNRcwoBDL2Z3RoKuN853siyLMUYIMQzDMAw1kNJUHiqKoigKIUSSJEmS/nhr9Z+zUd5kXdjO1TAdRQD5VOKVU543zndqNBq1DyzlojQLpTRVXsowDCFEURS1H/rFOT8hZHQ6gkBLaifhKQfjNdsuDQUOMpBCOfbs728IIWgfl4YCkVShJS1MxStLSsu9T+g18+GNxFsj3RjjkoGqhPTCUJpWSNUC1QiM8Vsj3eGNhM/K10TCVr38+qC/NBNTGgdSKE3Ofg8tev71Qb9bKx+9hHY9Dt2PXxoKqN1gFQZKCvxrLvXB6Hjosz8AUZI5ePf6v+XZa5Ue8N+nmGsf/Q6EzLciNKXZPMQY//j5k6H78RZ9BQO9sjb12zin26Mmn9WloP/ZQKnF64Neg8l9EQAVZSQLuVTuoZ0QqHFC28DQlGZLTRFCFj3/fIejgLiHOekoJczt7g70+J5kJmZzBxnZxdb+X4FGBwAuE/npyxe1LNRBgwaGpjSVhKqHLMsO97r/NrkOUG4DY53DP/v/6ahGeTnobrMbMcZV9IR/nszp1j+WiePe4nJ+42N3x9lMEV35ZOx8cYa4ggCQyMHVsQ/OaslHS/mZOxPF6B2PrQV4o1o9mYNP7izPh26ieDhV1DH52Wc6BwjLv/tFPD1ztd0XBMwDwM0V9NXEO72etlLFGoVWw1Eo34iiKOmc8Ply/GGx3CFbWdutxdNdLlPVE6HDAcOuNYiZ+Mh3Or09r3zjNwQB3YehqWeZla7AYChjXQ79A4iijuje/3KB2751ocObNp9LJabR3hcPnPE5t4qtaGsWABQCoQfh01ZCjCdqHZpCObxL7HKZ1uLpo5yYYRHKCpJZx0G19+K9VsJbuxEk9W0nnd7gQXnga+3a1jMvnuqx8Z6XFtJZEAsAsJpA5vTcq91ue/C5F/ocvO8HpTuhvU6yzjk2HkwBIdtZhNPhDt/px3Zeo9AUykEGAoBZx2UFCTPoyCSUCTHwuPZrlAjS7KV5eo5XCAZFBIBYFvQkT2wn9z4u+t8H1mrA771wN1GEfGJ2C7WjZeLqq09oCuUQsoJk4LGkkCOTEAA6HOaFWGOm5hUCCBE4QIAzXvSQ+JjI6r2N8AX3CeBNdQtNoRzEQizT4TAfZToKAIhhNlN52PfgXN2w6aBIdJCJqn8WxOz+//osJGnsvLWSsGTuGryn6xm6IIrw6GwcVKY0G6ogm6k8quRGelmbGo2G8bkIaUTb6rSTTd7xWXg5uRi+8VVUExn/2niVgX5ffyRf6ODWieOZuoW+v4P+OjbG3Bs7pExpWg/H5yJGo+GIJVxNFidX4+oz43VWUc/BawNDEa739uJMP57p7v+h+PX8sM9Nogw+5+0ClqtbaJ4FluMIbzqkTGlC/VRBJlfjK8kKFviWu57wBTf+rtfyy5d6NRrNU/Xc9nQUhSev/mhohFh8tB1QGmugKIpvj8+HNlK3oxVMZJabuUYL7HsTS5mCWP/O8NAjhy/XYn3mXWL20nZAabiEmYL43sTSZo6tqG65Eq7vCAGP/fK1aeURT8ORb2WRGL8VPPkcncOkNJCSFJevTXd67BtpoaLqZT22phLPk2w2nc6LA+0tT8kbZYw8DHT3gpUmopQGGyjL8tvj8zfmo2u7Fb88rYIKBCDPmkanHyCE3hzu2RtT0pX1lCZOQdUsVJbldz69Nzr9YJc1EKniJLGCnhAACpICLLcajc9HUgPtLRx+PAmkQlKOvXiPGZjKCb/98O6N+UgWGTJVvW2t4q4zLShp0J1ICd+/PPrzoa43h3vUFRzUQEpTeajOUF65Ef7TzYXetpaoqAOocqIEVf2DMDYd9mjlpWjybMB5MdjaatX3eCxGHtOLRDnGZAUpHElt7uSuz21+sbTtd1ljQiPewK2SzEvJPGiNth2Rff/2mqLIK9vpXfpbFJRjjYHHfqeZYVjMa5HRNr9DAJ60zT9px1UQyVSsoA4vgbdp6HpXyrGmCBDeWypYOKp9/hevhtV25t+UTwAAAABJRU5ErkJggg=="""


#-- widget structure
menu = [
    ["File", ["Working directory", "Settings", "---", "Exit"]],
    ["Template", ["Install", "URL", "Copy Repo URL", "Report", "Update", "Details"]],
    ["Help", ["About", "Wiki", "Help"]],
]
layout = [[
    sg.Menu(menu, key="menu", font="Sans 11"),
    # left pane: blue/gray
    sg.Column(size=(320,725), background_color="#343131", pad=(0,0), layout=[
        [sg.Column(background_color="#2980b9", size=(320,105), pad=(0,0), element_justification="center", layout=[
            [ sg.T("▙  cookiedough", text_color="#fff", pad=((0,0),(10,0)), background_color="#2980b9", font="Sans 12 bold") ],
            [ sg.T(__meta__["version"], text_color="#65a3c8", pad=(0,0), background_color="#2980b9") ],
            [
                sg.Image(data=icons.search_bg, key="search_img", pad=(3,0), background_color="#2980b9", enable_events=True, visible=True),
                sg.Input("", key="search", size=(30,1), pad=(15,4), background_color="#fefefe", enable_events=True, border_width=0, visible=False)
            ],
        ])],
        [sg.Tree(
            repos.tree(), headings=["f"], col0_width=23, col_widths=[3], max_col_width=20, auto_size_columns=False,
            show_expanded=False, background_color="#353232", num_rows=30, pad=((5,0),(10,0)), justification="left",
            header_background_color="#353232", header_text_color="#333", selected_row_colors=("#2e2a2a","#a4a4a4"),
            enable_events=True, key="template"
        )]
    ]),
    # content pane: white
    sg.Column(size=(760,725), background_color="#fafafa", pad=((30,5),(10,5)), layout=[
        [
            sg.Column(background_color="#fafafa", size=(570,90), layout=[
                [sg.T("cookiedough", k="name", font="Sans 20 bold", size=(80,1), pad=(0,3), text_color="#404040", background_color="#fafafa")],
                [sg.T(__meta__["description"], k="description", size=(80,1), text_color="#404040", background_color="#fafafa", pad=(0,0))],
                [sg.T(__meta__["url"], k="url", enable_events=True, size=(80,1), text_color="#196099", background_color="#fafafa", pad=(0,0))],
            ]),
            sg.Column(background_color="#fafafa", layout=[
                [sg.B("Roll out", k="install", size=(10,2), pad=(2,15))],
            ]),
        ],
        [
            sg.Column(background_color="#fafafa", size=(155,230), layout=[
                [sg.T("stars", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.T("0       ", key="stars", text_color="#606060", background_color="#fafafa", pad=(0,0))],
                [sg.T("forks", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.T("0       ", key="forks", text_color="#606060", background_color="#fafafa", pad=(0,0))],
                [sg.T("wiki", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.T("-       ", key="has_wiki", text_color="#606060", background_color="#fafafa", pad=(0,0))],
                [sg.T("updated", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.T("2021-03-20", key="updated_at", text_color="#606060", background_color="#fafafa", pad=(0,0))],
                [sg.T("license", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.T("MITL            ", key="license", text_color="#606060", background_color="#fafafa", pad=(0,0))],
            ]),
            sg.Column(background_color="#fafafa", size=(190,230), layout=[
                [sg.T("size", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.T("0      ", key="size", text_color="#606060", background_color="#fafafa", pad=(0,0))],
                [sg.T("vars", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.Listbox(key="vars", font="monospace", size=(15,8), values=["slug", "version"], background_color="#f9f9f9")],
            ]),
            sg.Column(background_color="#fafafa", layout=[
                [sg.T("structure", text_color="#c3c4c5", background_color="#fafafa", pad=(0,0))],
                [sg.Listbox(key="dir", font="monospace", background_color="#eeffcc", size=(30,10), values="""└── cookiedough\n    ├── cookiecutter\n    │   └── {{template_vars}}\n    └── mainwindow""".split("\n"))],
            ]),
        ],
        [sg.Multiline(
            __meta__["doc"], key="readme", size=(75,17), pad=((5,10),(30,10)), border_width=0,
            text_color="#404040", background_color="#fafafa", font="Lato"
        )],
        [sg.T("hidden status bar (won't be used)", key="status", visible=False)]
    ]),
]]


#-- GUI event loop and handlers
class gui_event_handler:

    # prepare window
    def __init__(self):

        #-- build
        gui_event_handler.mainwindow = self
        #log.init.info("build window")
        sg.theme(conf["theme"])
        self.w = sg.Window(
            title=f"cookiedough", layout=layout, font="Sans 12", #ttk_theme="yaru",
            size=(1080,725), margins=(0,0), resizable=False, use_custom_titlebar=False,
            background_color="#fafafa"
            #, icon=icons.icon
        )
        self.win_map = {}
        # alias functions
        self.status = self.w["status"].update
        # widget patching per tk
        self.w.read(timeout=1)
        self.w["menu"].Widget.configure(borderwidth=0, type="menubar")
        self.w["template"].Widget.configure(show="tree") # borderwidth=0

    
   # add to *win_map{} event loop
    def win_register(self, win, cb=None):
        if not cb:
            def cb(event, data):
                win.close()
        self.win_map[win] = cb
        win.read(timeout=1)

    # demultiplex PySimpleGUI events across multiple windows
    def main(self):
        self.win_register(self.w, self.event)
        while True:
            win_ls = [win for win in self.win_map.keys()]
            #log.event_loop.win_ls_length.debug(len(win_ls))
            # unlink closed windows
            for win in win_ls:
                if win.TKrootDestroyed:
                    #log.event.debug("destroyed", win)
                    del self.win_map[win]
            # all gone
            if len(win_ls) == 0:
                break
            # if we're just running the main window, then a normal .read() does suffice
            elif len(win_ls) == 1 and win_ls==[self.w]:
                self.event(*self.w.read())
            # poll all windows - sg.read_all_windows() doesn't quite work
            else:
                #win_ls = self.win_map.iteritems()
                for win in win_ls:
                    event, data = win.read(timeout=20)
                    if event and event != "__TIMEOUT__" and self.win_map.get(win):
                        self.win_map[win](event, data)
                    elif event == sg.WIN_CLOSED:
                        win.close()
        sys.exit()

    # mainwindow event dispatcher
    def event(self, raw_event, data):
        if not raw_event:
            return
        # prepare common properties
        data = data or {}
        event = self._case(data.get("menu") or raw_event)
        event = gui_event_handler.map.get(event, event)
        if event.startswith("menu_"): raw_event = data[event] # raw Évéńt name for MenuButtons

        # dispatch
        if event and hasattr(self, event):
            #self.status("")
            getattr(self, event)(data)
            return
        # plugins
        elif mod := None: #self._plugin_has(raw_event)
            mod.show(name=event, raw_event=raw_event, data=data, mainwindow=self, main=self)
        else:
            self.status(f"UNKNOWN EVENT: {event} / {data}")

    # find first plugin which has `has` and claims responsibility for raw_event (mixed-case menu entries)
    def _plugin_has(self, raw_event):
        for mod in self.plugins:
            if hasattr(mod, "has") and mod.has(raw_event):
                return mod

    # alias/keyboard map
    map = {
        sg.WIN_CLOSED: "exit",
        "none": "exit",  # happens when mainwindow still in destruction process
    }

    # tree entry selected, update content widgets
    def template(self, data):
        try:
            name = data["template"][0]
            d = repos.ls.get(name)
        except:
            return
        if not d:
            return
        # simple copies
        for field in "name","description","url","size","stars","has_wiki","forks","updated_at","license":
            self.w[field].update(d[field])
        # expando
        self.w["dir"].update(values=d["dir"].split("\n"))
        self.w["vars"].update(values=[v["name"] for v in d["config"]])
        # readme
        if conf["colorize"]:
            self.w["readme"].update("")
            self.colorize_readme(d["readme"].split("\n"), self.w["readme"].print)
            self.w["readme"].Widget.see("1.1")
        else:
            self.w["readme"].update(d["readme"])
    # crude markdown detection and fg/bg colors
    def colorize_readme(self, lines, print):
        ln = len(lines)-2
        col = "#404040"
        line_iter = iter(lines)
        for i,line in enumerate(line_iter):
            if (i<ln) and re.match("^===+|^~~~+|^---+", lines[i+1]):
                print(line, text_color="#210", background_color="#ddd")
                try: next(line_iter)
                except: return
            elif line.startswith("#"):
                print(re.sub("^#+\s*", "", line), text_color="#001", background_color="#cbb")
            elif re.match("^\s*```.*", line):
                try:
                    while (line := next(line_iter)) and not re.match("^\s*```.*", line):
                        print(line, background_color="#eeffcc")
                except:
                    continue # on StopIteration
            else:
                print(line)

    # fake search bar clicked, exchange for real input field
    def search_img(self, data):
        self.w["search_img"].update(visible=False)
        self.w["search"].update(visible=True)
    # search
    def search(self, data):
        keywords = re.findall("\S+", data["search"])
        try:
            ls = repos.search(keywords)
            self.w["template"].update(repos.tree(ls))
        except:
            pass # probably an invalid regex

    # Template: Install (actually do something...)
    def install(self, data):
        print("install", data)
        try:
            repo = repos.ls[data["template"][0]]
        except:
            sg.popup("No valid template selection" + format_exc())
            return
        rollout(repo, main=self)
    # Template: URL / or URL click
    def url(self, data):
        url = self.w["url"].TKStringVar.get()
        os.system("xdg-open %r &" % url)
    # Template: Copy repo url
    def copy_repo_url(self, data):
        try:
            repo = repos.ls[data["template"][0]]["repo"]
            self.w.TKroot.clipboard_clear()
            self.w.TKroot.clipboard_append(repo)
        except:
            pass
    # Template: Update
    def update(self, data):
        sg.popup("Not implemented. If you do want to contribute, send a mail. There's a few dev/ scripts that would allow some automation.")
    # Template: Report
    def report(self, data):
        sg.popup("Not implemented. This kinda hinges on a database for submissions (would be possible in fossil/sqlite repository).")
    # Template: Details
    def details(self, data):
        text = json.dumps(repos.ls[data["template"][0]], indent=4)
        self.win_register(
            sg.Window(layout=[[sg.Multiline(text, size=(90,40), font="monospace 12")]], title="Meta")
        )

    # File: Exit
    def exit(self, data):
        self.w.close()
    # File: CWD
    def working_directory(self, data):
        if dir := sg.popup_get_folder("Change current working directory", "os.chdir()", os.getcwd()):
            os.chdir(dir)
    # File: Settings - remapped to pluginconf window
    def settings(self, data):
        files = [f"{__dir__}/*.py"]
        save = pluginconf.gui.window(conf, {"__init__":1}, files=files, theme="Default1")
        if save:
            os.makedirs(re.sub("[\w.]+$", "", conf["conf_file"]), 0o755, True)
            json.dump(conf, open(conf['conf_file'], "w", encoding="utf8"), indent=4)

    # Help: About
    def about(self, data):
        m = __meta__
        sg.popup(f"{m['title']} {m['version']}\n{m['description']}\n\n{m['doc']}\n")
    # Help: Wiki
    def wiki(self, uu):
        os.system(f"xdg-open '{__meta__['url']}' &")
    # Help: Help
    def help(self, uu):
        from cookiedough import help
        help.help()
        
    # set mouse pointer ("watch" for planned hangups)
    def _cursor(self, s="arrow"):
        self.w.config(cursor=s)
        self.w.read(timeout=1)
    
    # remove non-alphanumeric characters (for event buttons / tab titles / etc.)
    def _case(self, s):
        return re.sub("\(?\w+\)|\W+|_0x\w+$", "_", str(s)).strip("_").lower()

    def status(self, *a, **kw):
        ...#print(a, kw)            


#-- do the actual cookie cutting here
# doc: https://cookiecutter.readthedocs.io/en/1.7.2/advanced/calling_from_python.html
class rollout():
    def __init__(self, d, main):
        self.d = d  # template meta data
        self.main = main
        self.update_ccjson()
        self.w = self.create_win()
        #main.win_register(self.w, self.event)
        self.cutting({})

    def update_ccjson(self):
        ...

    def create_win(self):
        sg.popup("No input dialog yet. Cookiecutter will just prompt on the terminal.")

    def event(self, data):
        ...

    def hijack_click_prompt(self):
        import click
        def prompt(*a, **kw):
            ...
            return sg.popup_get_text("q")
        #click.prompt = prompt
    
    def cutting(self, params):
        from cookiecutter.main import cookiecutter
        cookiecutter(self.d["repo"])


#-- main
def main():
    gui_event_handler().main()
if __name__ == "__main__":
    main()
