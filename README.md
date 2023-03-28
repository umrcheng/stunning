# 也可也使用python环境直接运行

# 青龙面板订阅流程

需要这几个依赖

![image](https://user-images.githubusercontent.com/55354489/228259108-46c99473-3505-4ee3-b03d-5422863095d5.png)


名称

```
javbus自动签到
```

类型

```
公开仓库
```

链接

```
https://github.com/umrcheng/stunning.git
```

定时规则

```
2 2 28 * *
```

黑名单

```
analysis|config
```

依赖文件

```
config.json|analysis.py
```

文件后缀

```
py json
```

执行后

```
ln -sf /ql/data/repo/umrcheng_octo/config.json /ql/data/config/
```


# 编辑cookie

登陆用户然后打开这个网址，右键检查，选择控制台，输入 `console.log(document.cookie)` , `xxxxxx` 这个部分你要是能翻墙就填翻墙的地址，不能翻墙就填不翻墙的地址， `sgin` 中的url参数也要改
```
https://xxxxxx/forum/home.php?mod=spacecp&ac=credit
```

![image](https://user-images.githubusercontent.com/55354489/228255682-9c3430de-1616-4882-8ad7-35045c0c1761.png)

把内容复制到`config.json`中
