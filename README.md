# shell 图片展示工具

本工具的用途是在 shell 中打印图片，实验环境为 CentOS 7.4，代码原理已写到知乎[求大神编程怎么printf一张图片？](https://www.zhihu.com/question/423328638/answer/1509029353)

下面介绍分别三个代码文件：


## show_pic.c

在 shell 中打印图片，用 C 编写成，只能展示 24 位 BMP 图片

Windows 下讲普通图片转换为 24 为 BMP 图片方法：

\[使用“画图”打开图片\] -> \[文件\] -> \[另存为\] -> \[24位位图\]

### 使用方法：

```bash
gcc -o show_pic show_pic.c
./show_pic XXX.bmp
```


## show_pic.py

在 shell 中打印图片，用 Python3 编写成，能展示几乎所有类型的图片

### 使用方法：

```bash
python3 show_pic.py pic_file
```


## show_pic_login.c
设置 shell 登录界面为图片，用 C 编写成，只能使用 24 位 BMP 图片进行设置

### 使用方法：

```bash
gcc -o show_pic_login show_pic_login.c
./show_pic_login XXX.bmp
```

