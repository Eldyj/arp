from shlex import split as sh_split
from os.path import exists
from sys import argv

class Tmp:
    binds = {}
    props = {}
    defs = {}
    tags = map(str,list(range(1,10)))

def parse_defs(tokens):
    return map((lambda x: Tmp.defs.get(x, x)), tokens)

def parse_line(line):
    if line == "": return
    tokens = sh_split(line)
    if len(tokens) == 0: return
    op = tokens.pop(0)
    name = tokens.pop(0)
    if op == "set":
        Tmp.props[name] = ' '.join(parse_defs(tokens))
    elif op == "def":
        Tmp.defs[name] = ' '.join(parse_defs(tokens))
    elif op == "bind":
        Tmp.binds['+'.join(parse_defs(name.split('+')))] = ' '.join(parse_defs(tokens))


def parse_str(s):
    for i in s.split('\n'):
        parse_line(i)

def parse_bind(b):
    mods = []
    key = ""
    fkeys = [f"F{i}" for i in range(1,13)]

    for i in b.split('+'):
        if i in {"modkey","mousekey","Mod1","Mod2","Mod3","Mod4","Shift",*fkeys}:
            mods.append(i)
        else:
            if i in {"enter","return"}:
                i = "Return"
            key = i

    return [mods,key]

def parse_bind_exec(e):
    command="Execute"
    value=e

    tokens = e.split()
    first = tokens[0]
    if first == 'reload':
        command = 'SoftReload'
        value=''
    elif first == 'close':
        command = 'CloseWindow'
        value=''
    elif first == 'exit':
        value = 'killall leftwm'
    elif first == 'focus':
        command = 'FocusWindow' + tokens[1].capitalize()
        value=''
    elif first == 'move':
        command = 'MoveWindow' + tokens[1].capitalize()
        value=''
    elif first == 'goto':
        command = 'GotoTag'
        value = tokens[1]
    elif first == 'moveto':
        command = 'MoveToTag'
        value = tokens[1]
    return [command,value]


def translate_props():
    result = ''
    for i in Tmp.props:
        result += '\t'
        if i == 'tags':
            Tmp.tags = Tmp.props[i].split()
            l = '\",\"'.join(Tmp.tags)
            result += f"tags: [\"{l}\"],"
        elif i == 'layouts':
            l = ','.join(Tmp.props[i].split())
            result += f"layouts: [{l}],"
        elif i in {'layout_mode',
                   'insert_behaviour',
                   'disable_current_tag_swap',
                   'disable_tile_drag',
                   'focus_behaviour',
                   'focus_new_windows',
                   'single_window_border',
                   'sloppy_mouse_follows_focus',
                   'auto_derive_workspaces'}:
            result += f"{i}: {Tmp.props[i]},"
        else:
            result += f"{i}: \"{Tmp.props[i]}\","
        result += '\n'
    return result

def translate_bind(v,b):
    m = map((lambda x: '"'+x+'"'),b[0])
    return f"\t\t(command: {v[0]}, value: \"{v[1]}\", modifier:[{','.join(m)}], key: \"{b[1]}\"),\n"

def translate_binds():
    result = "\tkeybind: [\n"
    for i in Tmp.binds:
        v = parse_bind_exec(Tmp.binds[i])
        b = parse_bind(i)
        result += translate_bind(v,b)

    if 'tag_mod' in Tmp.defs:
        for n,i in enumerate(Tmp.tags,start=1):
            tm = Tmp.defs['tag_mod']
            b1 = parse_bind(f"{tm}+{n}")
            b2 = parse_bind(f"{tm}+Shift+{n}")
            v1 = parse_bind_exec(f"goto {i}")
            v2 = parse_bind_exec(f"moveto {i}")
            result += translate_bind(v1,b1)
            result += translate_bind(v2,b2)
            if n == 9:
                break

    return result + "\t],\n"

def translate_all():
    return '(\n' + translate_props() + translate_binds() + ')\n'

def translate_str(s):
    parse_str(s)
    return translate_all()

if not exists(argv[1]):
    print(f"file {argv[1]} don't exists")
    exit(1)

with open(argv[1],'r') as f1:
    with open(f"{argv[1].replace('.arp','')}.ron",'w') as f2:
        f2.write(translate_str(f1.read()))
