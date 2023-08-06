# encoding: utf-8
# api: cookiedough
# type: function
# title: roll out
# description: deploy slected cookiecutter template
# category: action
# version: 0.4
# config:
#     { name: no_params, type: bool, value: 0, description: Don't prompt for template vars. Use terminal prompts instead., help: You mgiht as well use cookiecutter directly then. }
#     { name: update_ccjson, type: bool, value: 1, description: Update parameters from cookiecutter.json files, help: avoids extra prompts if template infos outdated }
#     { name: hook_prompt, type: bool, value: 1, description: Display any additional prompts as GUI inputs, help: hook prompt.* functions }
# disabled-config:
#     { name: replay, type: bool, value: 1, description: Use replay/ variables, help: Overrides default values with previous inputs for the same tempalte. }
# priority: core
# depends: python:cookiecutter
#
# Implements the parameter input window before incoking cookiecutter(1)
# for extracting a template. Also hooks cookiecutter.prompt.* functions,
# to avoid terminal prompts.
#


import sys, os, re, json
import PySimpleGUI as sg
import requests, appdirs
from cookiedough import icons
from traceback import format_exc
from textwrap import dedent


# joined to main.conf
conf = {
    "no_params": False,
    "update_ccjson": True,
    "hook_prompt": True,
}


# finally, this is where cookiecutter gets invoked,
# params={} from the input window
# doc: https://cookiecutter.readthedocs.io/en/1.7.2/advanced/calling_from_python.html
def cutting(repo_url, params):
    # params
    ccc = CookieCutterConfig()
    if m := re.match("^(.+)\?(?:d|dir|directory)=(.+)$", repo_url):
        repo_url, directory = m.groups() # from http://repo.git/?dir=template2/
    else:
        directory = None
    if params:
        no_input = True
    else:
        no_input = False # from conf[no_params], set by task.__init__
    # run
    import cookiecutter.main
    dir = cookiecutter.main.cookiecutter(
        template=repo_url,
        #checkout=None,
        no_input=no_input,
        extra_context=params,
        #replay=None,
        #overwrite_if_exists=False,
        #output_dir='.',
        config_file=ccc.fn,
        default_config=ccc.default_config(),
        #password=None,
        directory=directory,
        #skip_if_file_exists=False,
        #accept_hooks=True,
    )
    return dir


# override cookiecutter.prompt.* functions - rather than having click.prompt() CLI inputs
def hijack_prompt():
    
    def yes_no(name, default):
        """ return click.prompt(question, default=default_value, type=click.BOOL) """
        return sg.popup_yes_no(name)

    def variable(name, default):
        """ return click.prompt(var_name, default=default_value) """
        w = sg.Window(f"Prompt for: `{name}`", layout=[
           [sg.T(name)],
           [sg.Input(default, key="_")],
           [sg.B("OK", key="ok")]
        ])
        event, data = w.read()
        w.close()
        return data.get("_")

    def choice(name, options):
        """ click.prompt( prompt, type=click.Choice(choices), default=default, show_choices=False ) """
        w = sg.Window(f"Prompt for: `{name}`", layout=[
           [sg.T(name)],
           [sg.Combo(options, options[0], key="_")],
           [sg.B("OK", key="ok")]
        ])
        event, data = w.read()
        w.close()
        return data.get("_", options[0])

    import cookiecutter.prompt
    cookiecutter.prompt.read_user_yes_no = yes_no
    cookiecutter.prompt.read_user_variable = variable
    cookiecutter.prompt.read_user_choice = choice
    # only run once
    hijack_prompt = lambda *a: ...


# fetch remote cookiecutter.json, and update config[] list
def update_ccjson(config, url):
    try:
        ccjson = requests.get(url, headers={"User-Agent": "cookiedough/0.1.x (Python; amd64; requests)"}).json()
    except:
        return sg.popup(format_exc())

    have = [d["name"] for d in config]
    for k,v in ccjson.items():
        if not re.match("^\w+", k):
            continue
        elif k in have:
            pass
        else:
            config.append({
                "name": k,
                "value": v,
                "type": "str" if isinstance(v, str) else "select",
                "description": "(newly added parameter)"
            })

# scan local ~/.config/cookiecutter/replay/* dir, get override values from there
def update_replay(d):
    replay = {}
    try:
        m = re.search("(/[\w\-]+)(\.git|\.zip)?(\?.+$|$)", d["repo"])
        fn = CookieCutterConfig().replay + m[1] + ".json"
        print(fn)
        with open(fn, "r", encoding="utf-8") as f:
            replay = json.load(f)["cookiecutter"]
        # we could check if _template matches up with d[repo] at this point (likely couldn't account for ?directory=)
    except:
        return
    for e in d["config"]:
        if e["type"] not in ("str", "int", ):
            continue # skip for now (`dict` would require we separate "select" and "value" properly)
        if e["name"] in replay.keys():
            e["value"] = replay[e["name"]]


#-- parameter window
class task():

    def __init__(self, d, main):
        self.d = d  # template meta data
        self.main = main
        if conf["hook_prompt"]:
            hijack_prompt()
        if conf["update_ccjson"]:
            update_ccjson(self.d["config"], self.d["cookiecutterjson_url"])
        if conf["no_params"]:
            cutting(self.d["repo"], {})
        else:
            if conf.get("replay"):
                update_replay(self.d)
            self.w = self.create_win()
            main.win_register(self.w, self.event)

    # pre-invocation window with input fields
    def create_win(self):
        return sg.Window(title=f"Parameters for {self.d['name']}", size=(500,700), margins=(0,0), resizable=0, icon=icons.flame, layout=[
            [sg.Column(size=(500,65), background_color="#343131", pad=(0,0), layout=[
                [sg.T(self.d["name"], font="Sans 16 bold", size=(60,1), pad=(20,15), background_color="#343131", text_color="#f3f3f3")]
            ])],
            [sg.Column(size=(500,560), background_color="#2980b9", pad=(0,0), scrollable=True, vertical_scroll_only=True, layout=[
                [w] for w in self.fields(self.d["config"])
            ])],
            [sg.Column(size=(500,75), pad=(20,10), layout=[
                [sg.B("           Bakin'  \n           time!  ", image_data=icons.bakin, key="#bake", size=(40,2)), sg.Button("Target dir", key="#chdir"), sg.B("Cancel", key="#cancel")],
            ])],
        ])

    # convert config[] list to input widgets
    def fields(self, cfg):
        bg = { "background_color": "#2980b9" }
        pad = { "background_color": "#c6d7e3", "pad": ((20,2),(0)) }
        ls = []
        for e in cfg:
            ls.append(sg.Text(e["name"], font="Sans 12 bold", pad=((10,13),(10,2)), **bg))
            if e["type"] == "select":
                values = e.get("select") or e.get("value") or [""]
                ls.append(sg.Combo(values, default_value=values[0], key=e["name"], font="Roboto 12", text_color="black", **pad))
            elif e["type"] == "dict":
                # display only, not editable, and cookiecutter will source it from the cc.json
                ls.append(sg.Multiline(json.dumps(e["value"], indent=2), size=(50,3), disabled=True, text_color="black", **pad))
            else:
                ls.append(sg.Input(e["value"], key=e["name"], font="Roboto 11", text_color="black", **pad))
            if e.get("description"):
                ls.append(sg.Text(e["description"], font="Sans 9", text_color="#444", pad=(20,1), **bg))
        ls.append(sg.T("", **bg))
        return ls

    # window actions
    def event(self, event, data):
        if event == "#cancel":
            self.w.close()
        elif event == "#chdir":
            self.main.working_directory(...)
        elif event == "#bake":
            params = {k:v for k,v in data.items() if re.match("^\w+", k)}
            if params.get("_extensions"):
                for e in self.d["config"]:
                    if e["name"] == "_extensions":
                        params["_extensions"] = e["value"]
            self.w.close()
            dir = cutting(self.d["repo"], params)
            print("cookiecutting done.")
            self.open_target(dir)
            self.main.status(f"{dir} created")

    # open extracted dir
    def open_target(self, dir):
        if os.path.exists(dir):
            os.system("xdg-open %r &" % dir)


class CookieCutterConfig():
    """ fix xdg support for cookiecutter """
    
    def __init__(self):
        self.dir = appdirs.user_config_dir("cookiecutter", "cookiecutter")
        self.fn = self.dir + "/config"
        self.replay = self.dir + "/replay"
        self.cache = appdirs.user_cache_dir("cookiecutters", "cookiecutters")
    
    def default_config(self):
        """ supply overrides per cookiecutter.main(default_config=…) """
        return {
            "default_context": {
                #"full_name": "Susan Exemplary",
                #"email": "sample@example.com",
                #"github_username": "samp54",
            },
            "cookiecutters_dir": self.cache,
            "replay_dir": self.replay,
        }

    def patch(self):
        """ fix cookiecutter/config.py in-place """
        import cookiecutter.config  # alternatively: `locate "site-packages/cookiecutter/config.py"`
        target_dir = re.sub("[\w.]+$", "", cookiecutter.config.__file__)
        patch_file = re.sub("[\w.]+$", "config.patch", __file__)
        os.system(f"patch -b -d {target_dir} < {patch_file}")

    def move(self):
        """ shuffle old locations to new """
        self.create(self.dir)
        from_to = {
            "~/.cookiecutterrc": self.fn,
            "~/.cookiecutters/": self.cache,
            "~/.cookiecutter_replay/": self.replay,
        }
        for orig, new in from_to.items():
            orig = os.path.expanduser(orig)
            if os.path.exists(orig) and not os.path.exists(new):
                os.rename(orig, new)
                self.nobackup(new)

    def create(self, *dirs):
        """ create config+cache dirs, if missing """
        if not dirs:
            dirs = [self.replay, self.cache]
        for dir in dirs:
            if not os.path.exists(dir):
                os.makedirs(dir, 0o755, True)
                self.nobackup(dir)

    def nobackup(self, dir):
        """ touch .nobackup for cache dir """
        if dir.find("/.cache/") > 0:
             open(dir + "/.nobackup", "a").close()

