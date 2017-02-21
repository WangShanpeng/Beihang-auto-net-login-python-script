# 北航校园网自动拨号Python脚本

![image](images/login.png)
北航实验室上网每天早上四点都会所有电脑下线，再上线需要手工登录。这个脚本是为了自动进行网上注册，解决每天手工登录问题。本脚本分为Python2和Python3两个版本，推荐使用Python3。

## 实现原理

北航校园网需要在https://gw.buaa.edu.cn/上进行账号密码注册。 
用Chrome浏览器的network工具分析。在提交的时候有一条https://gw.buaa.edu.cn:801/include/auth_action.php 正含有注册用的username和password的信息。

![image](images/sniffer_packet.png)
这里username是学号，password是Base64算法加密传输的。至于cookie，who cares。

然后就用Python模拟这次提交。写在[buaaNet.py](https://github.com/sienaiwun/Beihang-auto-net-login-python-script/tree/master/Python3/buaaNet.py)里面。这里是用百度的连接来测试网络是否通畅。在main函数里面每若干分钟判断是否可以联网，如果断线则模拟执行一次提交。

## Windows下自动运行脚本的方法

把[bat文件](https://github.com/sienaiwun/Beihang-auto-net-login-python-script/tree/master/Python3/buaaNet.bat)放到Windows的启动命令里面，或者把快捷方式放到启动菜单里面，就可以随时登录了。

## Linux自动运行脚本的方法

这里以树莓派为例，有两种方法。

### 使用`rc.local`方法添加

原文地址：http://www.raspberrypi.org/documentation/linux/usage/rc-local.md

为了在树莓派启动的时候运行一个命令或程序，你需要将命令添加到rc.local文件中。这对于想要在树莓派接通电源后无需配置直接运行程序，或者不希望每次都手动启动程序的情况非常有用。

另一种替代定时任务的方法是使用[cron](https://www.raspberrypi.org/documentation/linux/usage/cron.md)和crontab。

**编辑`rc.local`文件**

在你的树莓派上，选择一个文本编辑器编辑`/etc/rc.local`文件。你必须使用root权限编辑，例如：
```shell
sudo nano /etc/rc.local
```
在注释后面添加命令，但是要保证`exit 0`这行代码在最后，然后保存文件退出。

**注意**

如果你的命令需要长时间运行（例如死循环）或者运行后不能退出，那么你必须确保在命令的最后添加“&”符号让命令运行在其它进程，例如：
```shell
python /home/pi/myscript.py &  
```
否则，这个脚本将无法结束，树莓派就无法启动。这个“&”符号允许命令运行在一个指定的进程中，然后继续运行启动进程。

另外，确保文件名使用绝对路径，而不是相对于你的home目录的相对路径。例如：使用`/home/pi/myscript.py`而不是用`myscript.py`。

###  窗口系统启动后，自动运行自定义的程序的实现方法
进入当前用户HOME目录下的`.config/autostart`目录，生成一个*.desktop文件（比如：xxx.desktop），命令如下:
```shell
sudo nano ~/.config/autostart/xxx.desktop
```
输入以下文件内容:
```
[Desktop Entry]
Type=Application
Exec=python /home/pi/myscript.py
```
最后一句Exec的值就是要启动的程序名（最好是全路径的可执行文件名），此处是运行一个Python脚本。保存退出，重启机器，脚本就会在进入窗口系统自动运行了。

原理：startx后，LXDE窗口管理器会找到`~/.config/autostart`目录下的所有`.desktop`文件，一一执行。

### 查看进程是否运行
我们就可以使用下面的命令查看Python进程的id：
```shell
ps -ef |grep python
```
或者
```shell
pstree |grep python
```
第二列即为当前进程的id，如果需要直接终止Python程序，执行：
```shell
kill -9 pid
```
再查看一下进程，发现脚本进程已经消失了，搞定。