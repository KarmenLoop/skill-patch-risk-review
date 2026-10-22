# Patch Risk Review · 补丁风险线索

[English](README.md) | 简体中文

先从 Git 补丁里找出值得重点看的部分。工具按文件统计增删行，并标出鉴权等审阅方向，方便回到完整差异里进一步检查。

[下载 v0.2.1](https://github.com/KarmenLoop/skill-patch-risk-review/releases/tag/v0.2.1) · [完整教程](docs/tutorial.zh-CN.md) · [输入参考](docs/input.zh-CN.md) · [反馈问题](https://github.com/KarmenLoop/skill-patch-risk-review/issues)

## 能做什么

样例修改 src/auth.py，新增两行、删除一行，并提示检查 authentication。

审阅方向是基于路径的线索，不是安全审计。工具不会应用补丁、检查运行行为或批准合并。

![补丁风险线索 0.2.1 版本样例的真实 JSON 输出](docs/images/example-output-v0.2.1.svg)

*图片来自 v0.2.1 的真实本地输出，采用英文键名；[完整结果](examples/expected.json) · [图片来源记录](docs/images/provenance.json)。*

## 开始使用

在发行页下载 `karmen-patch-risk-review-v0.2.1.zip` 与对应 `.sha256` 文件，核对哈希后解压。在解压目录中使用 Python 3.9 或更新版本：

```sh
python3 scripts/run.py --version
python3 scripts/run.py --input examples/input.json
```

预期版本：`karmen-patch-risk-review 0.2.1`。样例修改 src/auth.py，新增两行、删除一行，并提示检查 authentication。

如果宿主读取 `~/.agents/skills`，可安装完整技能：

```sh
python3 install.py --host agents
```

目标目录已存在时安装器会拒绝覆盖。宿主发现和调用方式可能不同，见[安装与实践教程](docs/tutorial.zh-CN.md)。不使用 AI 宿主也能直接运行本地工具。

## 用于自己的任务

diff 填写完整 Git 统一差异，保留文件头和 hunk 行数。不完整或计数不一致的补丁会被拒绝，不会猜测。

尝试带引号或空格路径的补丁，再与 git diff --stat 对照。回到每个被标记文件审阅，并运行受影响项目自己的检查。

准备新输入前可查看[字段约定](docs/input.zh-CN.md)。工具只依赖 Python 标准库，本身不需要模型账号、API 密钥或网络。使用 AI 宿主时，宿主有自己的数据与权限设置。

## 常见问题

**它能证明补丁可以安全合并吗？** 不能。它帮助确定审阅重点，合并前仍需检查代码、需求和真实测试结果。

**结果保存在哪里？** 默认向终端输出 JSON；使用 `--output` 时只创建新文件，已有输出文件会保留。工具只读取提交的记录和输入约定中明确列出的本地路径。

## 文档与支持

- [下载、安装、配置、练习、升级与卸载](docs/tutorial.zh-CN.md)
- [输入输出约定](docs/input.zh-CN.md)与[兼容性说明](docs/COMPATIBILITY.md)（英文参考）
- [更新记录](CHANGELOG.md)、[参与贡献](CONTRIBUTING.md)、[支持](SUPPORT.md)和[安全反馈](SECURITY.md)

## 许可证

[MIT](LICENSE)。再分发时保留许可证和[声明](NOTICE.md)。由 [KarmenLoop](https://karmenloop.com) 维护。
