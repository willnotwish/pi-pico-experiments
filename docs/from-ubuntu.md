# Connecting to the pico from Ubuntu
It works, but there are a few setup gotchas.
To check if you have connectivity, the simplest  tool to use is `screen`.  I'd not used it before.
## Using the `screen` command
Enter this at a command line prompt:
```
screen /dev/ttyACM0
```
It should clear the screen. Once you've pressed Enter a few times you should see the `repl` prompt (three chevrons).
To leave the session, do `ctrl-A K` and confirm (y).

If that doesn't work, and you are returned immediately to the command line, something (simple) is wrong.
In my experience, either the device isn't plugged in, or (more likely) it's a permissions issue.

If 
```
sudo screen /dev/ttyACM0
```
works, it's definitely a permissions issue.

To troubleshoot, check the device shows up on the host. On my Ubuntu PC, it's at `/dev/ttyACM0`.

```
nick@nick-pc:~$ ls -al /dev/ttyA*
crw-rw---- 1 root dialout 166, 0 Mar  7 11:45 /dev/ttyACM0
```
**Note the permissions.** You need to be in the `dialout` group to access the device.

To see what groups you are in, use the `groups` command:
```
nick@nick-pc:~$ groups
nick adm dialout cdrom sudo dip plugdev lpadmin lxd sambashare docker
```
Here you can see that user `nick` is in the `dialout` group. That's why it works.

If you don't see `dialout`, but **you could swear that you've already added yourself**, try
```
groups nick
```
instead. If that shows `dialout`, but `groups` doesn't, you need to reboot the computer. **Seriously.**

I wasted a few hours on this. It's to do with the way groups are allocated.

To add yourself to the `dialout` group in the first place, use `sudo adduser` like so
```
sudo adduser nick dialout
```
Per the above, don't forget to reboot!

## Using PyCharm
I'd not used PyCharm before. I found this [really good video tutorial](https://youtu.be/QywUT3f-_7w)
on getting up and running.

> My advice is to make sure you've got access sorted first, as described above. I did things the other way round;  
> I just wasted my time.

There are still a few things I don't understand. In some ways, PyCharm is not as easy to use as Thonny when it comes to
running code on the pico. But in terms of an IDE, PyCharm looks great so far.

### The main gotcha
When you want to run code on the pico, you click the green `Flash xxx` triangle in PyCharm. This examines the appropriate runtime 
configuration, uploads the file to the pico and performs a "soft reboot" of the device.

**The gotcha is that this will _only_ run the file `main.py`**

Although the file you upload is stored on the pico, it isn't run when the device is rebooted: `main.py` is.
That's how Micropython works. A quick workaround this is to make sure that the code you want to run is stored in 
the file `main.py` in the first place. Then it will run on a soft reboot. This is different from how Thonny works,
and it takes a bit of getting used to.

### Output from print statements
I'm a beginner when it comes to Python and the REPL. I expect that when I do a `print` in my code, I see the output somewhere.
In PyCharm, the `Run` pane at the bottom is not the REPL. You can't type into it: it's read only. It shows output only
from the upload + soft reboot operations. Specifically, it does **not** show my program output like Thonny does.

To repeat, the `Run` pane is *not* the REPL. To get a REPL in PyCharm, choose `Tools/Micropython/Micropython REPL` from the top-level
menu. Then you see the familiar three chevrons and the help message:
```commandline
Device path /dev/ttyACM0
Quit: Ctrl+] | Stop program: Ctrl+C | Reset: Ctrl+D
Type 'help()' (without the quotes) then press ENTER.

>>> 

```
This pane is interactive. From here I can (I think) run my code by importing it.

It's `Ctrl+]` to exit.


---

_I think I lack understanding. It's probably not as simple as the videos would have you believe._

---
## There's another tool: [rshell](https://github.com/dhylands/rshell) 

After following the installation instructions, at the command line I see this:

```commandline
(venv) nick@nick-pc:~/dev/pi-pico-experiments$ rshell
Connecting to /dev/ttyACM0 (buffer-size 512)...
Trying to connect to REPL  connected
Retrieving sysname ... rp2
Testing if sys.stdin.buffer exists ... Y
Retrieving root directories ... /blink.py/ /flasher.py/ /hello.py/ /lib/ /looper.py/ /main.py/ /oled.py/ /pio/ /pwmled.py/ /timer.py/
Setting time ... Mar 07, 2022 13:58:21
Evaluating board_name ... pyboard
Retrieving time epoch ... Jan 01, 1970
Welcome to rshell. Use Control-D (or the exit command) to exit rshell.

```
When in `rshell`, the `/pyboard` directory contains files on the pico, uploaded from the host PC.

> If it helps, think of `rshell` as a simple telnet-like session on the pico.

Enter the REPL loop with `repl` and exit with `exit`. Run code that has been uploaded by `import` ing it:

```commandline
/home/nick/dev/pi-pico-experiments> repl
Entering REPL. Use Control-X to exit.
>
MicroPython v1.18 on 2022-01-17; Raspberry Pi Pico with RP2040
Type "help()" for more information.
>>> 
>>> import hello
Hello world
>>> 

```

Here we see the elusive `print` statement output.

---
I think the mist is clearing!

**To run code on the pico**, there are a few alternatives.

> Whatever you do, you must get the Python (.py) file onto the pico somehow.
* PyCharm calls this "flashing".
* `rshell` has a `cp` command.

There are two alternatives:
1. Name the file `main.py` and make sure it's in the root of the pico's "file system". Issue a soft reboot; 
the code in the file will run automatically.
2. Name the files as you like and put them where you want. Start a REPL and import the runnable file at the prompt.
