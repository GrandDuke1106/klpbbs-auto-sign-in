# [KLPBBS_auto_sign_in](https://github.com/xyz8848/KLPBBS_auto_sign_in)
基于 GitHub Action 的苦力怕论坛自动签到脚本  
[![GitHub Stars](https://img.shields.io/github/stars/GrandDuke1106/KLPBBS_auto_sign_in)](https://github.com/GrandDuke1106/KLPBBS_auto_sign_in/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/GrandDuke1106/KLPBBS_auto_sign_in)](https://github.com/GrandDuke1106/KLPBBS_auto_sign_in/network/members)

## 如何使用

1. [Fork](https://github.com/GrandDuke1106/KLPBBS_auto_sign_in/fork) 这个仓库
2. 授予工作流读取和写入权限（用于工作流保活，如果仓库中在过去 60 天内没有提交，GitHub 将暂停 GitHub 工作流的计划触发器。除非进行新的提交，否则基于 cron 的触发器不会运行。）
![step2.webp](img/step2.webp)
3. 打开 Actions secrets and variables  
![step3.webp](img/step3.webp)
4. 添加以下 secret：[`USERNAME`](docs/secrets.md#username)，[`PASSWORD`](docs/secrets.md#password)

## 更多功能
### 自定义签到时间
（默认每天 00:01 签到）
1. 到 [`.github/workflows/sign_in.yml`](.github/workflows/sign_in.yml) 中修改签到时间

### 用户组到期后自动续费
1. 打开 Actions secrets and variables
2. 添加以下 secret：[`SWITCH_USER`](docs/secrets.md#switch_user) 或 [`RENEWAL_VIP`](docs/secrets.md#renewal_vip) 或 [`RENEWAL_SVIP`](docs/secrets.md#renewal_svip)

### 签到后邮件提示
1. 打开 Actions secrets and variables
2. 添加以下 secret：[`MAIL_ENABLE`](docs/secrets.md#mail_enable)，[`MAIL_HOST`](docs/secrets.md#mail_host)，[`MAIL_PORT`](docs/secrets.md#mail_port)，[`MAIL_USERNAME`](hdocs/secrets.md#mail_username)，[`MAIL_PASSWORD`](docs/secrets.md#mail_password)，[`MAIL_TO`](docs/secrets.md#mail_to)

### 签到后企业微信提示
1. 打开 Actions secrets and variables
2. 添加以下 secret：[`WECHAT_ENABLE`](docs/secrets.md#wechat_enable)，[`WECHAT_WEBHOOK`](docs/secrets.md#wechat_webhook)，[`WECHAT_MENTIONED`](docs/secrets.md#wechat_mentioned)

### 签到后Server酱提示
1. 打开 Actions secrets and variables
2. 添加以下 secret：[`SERVERCHAN_ENABLE`](docs/secrets.md#serverchan_enable)，[`SERVERCHAN_KEY`](hdocs/secrets.md#serverchan_key)

### 签到后 Ntfy 提示
1. 打开 Actions secrets and variables
2. 添加以下 secret：[`NTFY_ENABLE`](docs/secrets.md#ntfy_enable)，[`NTFY_URL`](docs/secrets.md#ntfy_url)，[`NTFY_TOPIC`](docs/secrets.md#ntfy_topic)
3. 认证 **（以下方法任选一个）**
    1. 如果要使用**用户名+密码**认证，添加以下 secret：[`NTFY_USERNAME`](docs/secrets.md#ntfy_username)，[`NTFY_PASSWORD`](docs/secrets.md#ntfy_password)
    2. 如果要使用 **Token** 认证，添加以下 secret：[`NTFY_TOKEN`](docs/secrets.md#ntfy_token)

## 统计数据
![](https://repobeats.axiom.co/api/embed/61dc140b2e19a099f83e593318024e98f7b66be5.svg)
