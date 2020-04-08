# Python_WeChat
* 微信小程序_python后台

## 启动
# Windows 启动方式
* set ops_config=local | production
* python manager.py runserver

# linux/centos 启动方式
* export ops_config=local | production && python manager.py runserver 

## git 命令
# 设置
*  git config --list
*  git config --list --show-origin
*  git config --global core.editor "'D:/Program Files/Sublime Text 3/sublime_text.exe' -multiInst -notabbar -nosession -noPlugin"
*  git config --global user.email wangchengbin_2009@vip.163.com 
*  git config --global user.name "Patrick Wang"

# 秘钥设置
*  ssh-keygen -t rsa -C "wangchengbin_2009@vip.163.com"
*  cd ~/.ssh
*  cat id_ras.pud

# 测试
*  ssh -T git@github.com

*  git init
*  git add .
*  git commit -m '微信小程序测试项目'
*  git remote add origin git@github.com:kadin008/Python_WeChat.git
*  git remote set-url git@github.com:kadin008/Python_WeChat.git

# 同步
*  git pull origin master
# 提交
*  git push -u origin master

* 测试修改 






