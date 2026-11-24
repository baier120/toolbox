# Windows 故障排查笔记 / Windows Troubleshooting Notes

真实遇到的两个问题：症状、我查过什么、最后怎么解决的。

Two problems I actually hit on Windows 11: the symptoms, what I checked, and what fixed them.

> 环境 / Environment: Windows 11 (build 26300), PowerShell 5.1

---

## 1. 桌面图标消失，右键没反应

### 症状 / Symptoms

- 桌面只剩背景，图标全不见
- 右键桌面没有菜单
- 看起来像文件被删了

### 排查过程 / What I checked

```powershell
# 1. 先确认真实桌面路径 —— 可能不在 C:\Users\<user>\Desktop
(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders').Desktop

# 2. 文件还在不在（关键：在的话就不是数据问题）
(Get-ChildItem "<桌面实际路径>" -Force | Measure-Object).Count

# 3. 有没有壁纸/桌面整理类程序在跑
Get-Process | Where-Object { $_.ProcessName -match 'wallpaper|Lively|desktop' }

# 4. 资源管理器是否正常
Get-Process explorer | Select-Object Responding

# 5. "显示桌面图标"开关是否被关
(Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced').HideIcons
```

排查结果：文件全在、`explorer` 响应正常、`HideIcons = 0`，
但有两个壁纸程序同时在跑。

### 根因 / Root cause

两个动态壁纸软件同时抢桌面层，后启动的那个在图标之上画了一层透明窗口，
挡住了图标和右键菜单。

其中一个是带守护进程的（普通权限杀不掉，杀了立刻被拉起来）。

### 解决 / Fix

```powershell
# 需要用管理员权限执行（普通权限杀不掉守护进程）
Get-Process <壁纸进程名1>,<壁纸进程名2> | Stop-Process -Force

# 重启资源管理器
Stop-Process -Name explorer -Force
Start-Process explorer
```

图标立即恢复。

### 教训 / Takeaway

- **"文件不见了"先确认文件在不在，再怀疑显示层**
- 桌面的真实路径可能是被注册表改过的（比如改到 D 盘），别只看默认路径
- 同类软件（壁纸、桌面整理、悬浮窗）**同时装两个就容易互相盖**
- 强杀带守护的进程要用管理员权限

---

## 2. Electron 应用主进程崩溃，怎么定位

### 症状 / Symptoms

对话框显示"应用无法启动或已意外停止"，旁边还给了一个崩溃日志路径。

### 日志在哪 / Where the log is

Electron 桌面应用通常在：

```
%APPDATA%\<vendor>\<app-name>\logs\crash-<ISO timestamp>-host.log
```

文件名里的 `host` 表示是**主进程**（不是渲染进程）。

### 怎么读 / How to read it

```powershell
# 找最新的一份
Get-ChildItem "$env:APPDATA\<vendor>\<app-name>\logs" -Filter 'crash-*-host.log' |
  Sort-Object LastWriteTime -Descending | Select-Object -First 1

# 定位真正的错误行
Get-Content <那份日志> | Select-String -Pattern 'Error|Exception|FATAL'
```

关键行长这样：

```
Error: dsh desktop host exited with <退出码>: <崩溃前最后几行日志>
```

两个要点：

1. **退出码**能说明是"崩溃"还是"被关闭"
2. **冒号后面那串**是崩溃前最后打印的内容 —— 通常就是崩溃发生的位置

### 根因 / Root cause

那次崩溃前最后打印的是一串工具名（`bootstrap, vision_colors, vision_crop, ...`），
对应一个**前一天刚装的插件**在启动时注册工具。

时间线完全吻合：装插件 → 次日崩溃在工具注册阶段。

### 解决 / Fix

卸载那个插件。卸载后出现了连带错误：

```
no adapter registered for provider "<provider-name>"
NO_ADAPTER
```

原因是会话还指向插件注册的模型路由，切回默认模型就好。

### 教训 / Takeaway

- **崩溃日志的最后一条通常是崩溃点，不是根因**，要结合"最近装了什么"
- 日志里一般有 `--- recent plugin operations ---` 之类的段，直接列出最近变更
- **刚装完东西就崩**，第一嫌疑永远是刚装的那个
- 卸载插件可能留下"孤儿引用"（会话配置还指着它），导致新的报错 —— 这是正常的，改配置即可

---

## 3. 应用内更新按钮不给用时的备用路径

Electron 应用的自动更新配置一般在安装目录：

```
resources\app-update.yml
```

里面有更新源地址。如果应用内更新没反应：

```powershell
# 看更新源
Get-Content "<安装目录>\resources\app-update.yml"

# 直接探测更新源是否可用
curl.exe -sI "https://<更新源域名>/<路径>/latest.yml"
```

如果更新源返回 404（服务端关闭了 nightly 通道之类），
去官网找下载页拿安装包，**不要从第三方"软件下载站"下**——那类站点捆绑严重。

升级前先备份配置：

```powershell
# 典型位置
%USERPROFILE%\.<app-name>\profiles\<profile-name>\
# 备份其中的 patch 配置、package.json、lock 文件
```

---

## 小结 / Summary

| 问题 | 一句话根因 |
|---|---|
| 桌面图标消失 | 两个壁纸软件抢桌面层，文件没事 |
| 主进程崩溃 | 新装插件在启动注册时崩了，看崩溃日志最后一行 |
| 更新按钮失效 | 更新源 404，直接去官网下安装包 |

**通用方法**：先确认"数据是否还在"，再查"是谁在显示/占用"，最后读日志定位"哪一步崩的"。
