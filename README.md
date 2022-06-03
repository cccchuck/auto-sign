# 👩🏻‍🎓 我在校园自动化签到加健康打卡

灵感来自：[WoZaiXiaoYuanPuncher](https://github.com/zimin9/WoZaiXiaoYuanPuncher)，看起来比较简单，且各个学校要求不一样，因此自己动手写了一个。

白嫖，🤺 退！白嫖，🤺 退！白嫖，🤺 退！

星星，⭐️ 来！星星，⭐️ 来！星星，⭐️ 来！

## 🔧 Usage

1. 打开 `我在校园`，依次点击 `我的` -> `设置` -> `密码修改`（要是自己记得密码就直接忽略这一步，不过建议还是再修改一下，不然会出现一个莫名其妙的问题）

2. 抓包获取必要信息
   使用电脑微信打开 `我在校园` 小程序，同时打开抓包软件（自己看哪个顺眼用哪个）。点击小程序上面的 `签到` 和 `健康打卡` Tab, 就可以抓取到必要信息了，必要信息如下：

```txt
username - 账号

password - 密码

answers - 健康打卡答案(可在 `/health/save.json` 请求中找到，也可以自己填，example: ["0", "36.1", "1"], 其中"0"代表第一个问题选的第一个选项，"36.1"代表第二个问题填写的为"36.1"，"1"代表第三个问题选的第二个选项)

latitude - 经度(在小程序里面找到定位，然后抓包获得)

longitude - 纬度(在小程序里面找到定位，然后抓包获得)

country - 国家(在小程序里面找到定位，然后抓包获得)

province - 省份(在小程序里面找到定位，然后抓包获得)

city - 城市(在小程序里面找到定位，然后抓包获得)

district - 区(在小程序里面找到定位，然后抓包获得)

township - 镇(在小程序里面找到定位，然后抓包获得)

street - 街道(在小程序里面找到定位，然后抓包获得)

areacode - 区域编码(在小程序里面找到定位，然后抓包获得)

towncode - 镇编码(在小程序里面找到定位，然后抓包获得)

citycode - 城市编码(在小程序里面找到定位，然后抓包获得)
```

3. 拉取代码，安装依赖

```bash
git clone https://github.com/cccchuck/auto-sign.git

cd auto-sign

pip install -r requirements.txt
```

4. 在同目录下配置 `conf.json` 文件

```json
{
  "accounts": [
    {
      // 填入第二步的信息
    }
  ]
}
```

5. 运行

```bash
   python main.py
```

## ⌚️ 定时运行

可以选择 `Github Action`，也可以选择 `云函数`，自行折腾。

## 📮 反馈

[点击加入飞书交流群](https://applink.feishu.cn/client/chat/chatter/add_by_link?link_token=5ean9615-5c1f-4905-b3db-0eb53bdbe0e8)

## 💻 其他

该仓库遵循 MIT 开源协议，可以自由使用，但请保留此信息。

该仓库仅用于学习，违者自负责任。
