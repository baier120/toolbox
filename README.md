# toolbox

Small scripts I actually use on my Windows laptop.
No frameworks, no dependencies — each one solved a real problem I ran into.

我平时在 Windows 上真的会用的小脚本。没有框架、没有依赖，每一个都对应一个实际踩过的坑。

## Contents

### `GLOSSARY.md`

English words I kept meeting in code and on GitHub, with Chinese notes.
Written for myself, shared in case someone else needs it too.

写代码和用 GitHub 时反复遇到的英文词，附中文解释。给自己查的，顺便公开。

### `WINDOWS-TROUBLESHOOTING.md`

Two real Windows 11 problems: desktop icons disappearing, and an Electron app's
main process crashing. Each one written up as symptom → what I checked →
root cause → fix, with the actual PowerShell commands.

Windows 11 上真遇到的两个故障：桌面图标消失、Electron 应用主进程崩溃。
每篇都按「症状 → 我查了什么 → 根因 → 怎么解决」写，附上实际用过的 PowerShell 命令。

### `batch_rename.py`

Replace spaces in file names with underscores.

Preview by default — it only prints `old -> new` and never touches your files.
To actually rename, set `APPLY = True` inside the script and run it again.

把文件名里的空格换成下划线。

默认只预览：打印 `旧名 -> 新名`，不动任何文件。
确认无误后，把脚本里的 `APPLY = False` 改成 `True`，再运行一次才会真正改名。

```bash
python batch_rename.py
# 请输入文件夹路径： C:\Users\me\Pictures
```

Written with basic Python only: `import`, `input`, `for`, `if`, string methods,
and two functions from the `os` module. No external packages.

只用了基础语法：`import`、`input`、`for`、`if`、字符串方法，以及 `os` 模块的两个函数。没有第三方包。

## Why this repo

I'm a math undergraduate moving toward systems and AI.
I write things down here so I don't have to figure them out twice,
and so the work is visible instead of living in scattered scratch files.

## License

MIT
