# anysell

Welcome! Sell anything on multiple platforms at once.

Features:
- generate item config
- creates posts on bazos
    - supports images
    - mobile 2fa
    - multiple at once

**TODO:**
- fb marketplace
- works only with "clothes", maybe add all/more categories

# install & usage

```bash
pip3 install anysell
```

There are 2 config files we're gonna use:
- **main config file** - stores important global info (name, email etc.) 
- **items config file** - stores info about items you want to sell, at one place. then anysell will propagate it in multiple places

### cfg file

You can provide main config file by passing `--config-path` option to commands. Default path for
your config is `~/.config/anysell/.cfg`. Go ahead, create and fill the file. 

```
name=
password=  # some tmp password, e.g. for edit on bazos
phone=
email=
psc=
img_path=/Users/bla/Desktop/img_clothes  # generate-cfg cmd will use structure to create yaml 
item_config_path=/Users/bla/cfg.yaml  # sell cmd use this to create the item posts
```

To start quickly, do:
```
anysell generate-cfg --config-path /my/cfg/path/.cfg
```

This will generate the file based on structure in `img_path`. It's good to have folder per item and
images for items in that folder. Folder names needs to be unique.

Open file on `item_config_path` and fill it:
```
damske_cierne_nohavice_sportove__40:
  category: 'Športové oblečenie'
  price: '8'
  filepaths:
    - /img/folder/damske_cierne_nohavice_sportove__40.jpg
    - /img/folder/damske_cierne_nohavice_sportove_detail__40.jpg
  title: 'Damske Sportove Cierne Nohavice'
  description: 'Daju sa odopinat na tristvrtove. Velkost 40.'
damske_siroky_golier__detail__36_38:
  category: ''  # fill
  description: ''  # fill
  filepaths:  # fill
    - /img/anotherfolder/damske_siroky_golier__detail__36_38.jpg
  price: ''  # fill
  title: ''  # fill
```

Now, you have the items config (no need to use generate command, you can create your own if you want)

Run
``
anysell sell --config-path /my/cfg/path/.cfg
``

This will read the item config file using `item_config_path` key in your main config and 
create all the posts based on that.

Note - this will prompt you for doing auth. E.g. 2fa with mobile key. When you fill it first time
key will be cached and reused for 1hr.

# bazos 

These are keys you can use for categories.
```json
[
    "Blúzky",
    "Bundy a Kabáty",
    "Čiapky, Šatky",
    "Doplnky",
    "Džínsy",
    "Funkčné prádlo",
    "Hodinky",
    "Kabelky",
    "Košele",
    "Kožené oblečenie",
    "Mikiny",
    "Nohavice",
    "Obleky, Saká",
    "Plavky",
    "Plecniaky a kufre",
    "Rukavice a Šály",
    "Rúška",
    "Šaty, Kostýmy",
    "Šortky",
    "Šperky",
    "Spodná bielizeň",
    "Športové oblečenie",
    "Sukne",
    "Svadobné šaty",
    "Svetre",
    "Tehotenské oblečenie",
    "Topánky, obuv",
    "Tričká, roláky, tielka",
    "Ostatné"
]
```