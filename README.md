# arp (a ron preprocessor)

## language usage

`bind <key+combo> <action>` - bind `<action>` to `<key+combo>` <br/>
supported actions:
* `move up|down`
* `focus up|down`
* `moveto <tag>`
* `goto <tag>`
* `close` (close active window)
* `reload` (reload wm)
* `exit` (kill leftwm)
* other operations will parsed as shell action
`def <name> <value>` - macros `<name>` defenition with value `<value>` <br/>
`set <name> <value>` - set property `<name>` to value `<value>` <br/>

## preprocessor usage

```sh
python arp.py <file>.arp
```

will save translated file to `<file>.ron`

## why ?

bacause i don't like leftwm ron config nor leftwm toml config format
