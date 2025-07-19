# xFi gateway port forward editor

## A python script for editing port on Xfinity xFi gateway without installing spyware on your phone

### usage:

Enable port forwarding:
```sh
python main.py --username=admin --password=[PASSWORD] enable
```


Disable port forwarding:

```sh
➜ python main.py --username=admin --password=[PASSWORD] disable
```

Add port forward:
```sh
➜ python main.py --username admin --password [PASSWORD] add [NAME] [TCP,UDP,TCP/UDP] [local ip] [port]
```

Clear all port forwarding:
```sh
➜ python main.py --username admin --password [PASSWORD] clear
```


No, you can not see what you add or delete one entry(well you can but there is no way to get the id) because Xfinity didn't add an API for it

If something break, good luck, no warranty is provided

Tested on TG4482A (XB7) with software image TG4482PC2_6.3p24s1_PROD_sey

username and password is the username and password for the web panel

# Resources:

[Thank to asentientbot for finding the firmware file](https://github.com/hack-technicolor/hack-technicolor/issues/181#issuecomment-1734415959)

Thank to Xfinity(or whoever made this shitty router) for not deleting the JavaScript so I don't have to pull up an Android debugger, which prove there is no reason this cannot be done from the web panel other then they can spy on you.


