# 接入本地 Ollama

## 1. 安装与准备模型

从 https://ollama.com/download 安装 Windows 版。打开 Ollama 后，在 PowerShell 检查：

```powershell
ollama --version
ollama list
```

在 https://ollama.com/library 选择可用于文本对话的本地模型，复制其完整标签，用以下方式下载（将 YOUR_MODEL 替换为真实标签）：

```powershell
ollama pull YOUR_MODEL
ollama run YOUR_MODEL
```

先在命令行发送一句中文，确认能收到回答。模型大小、量化格式、上下文长度影响内存与速度；选择与自己 RAM / VRAM 匹配的模型。软件不绑定某个 Qwen 版本，也不会自动安装界面预填的模型。

## 2. 确认本地 API

Ollama 未启动时运行 `ollama serve`；若已经运行出现端口占用，不要重复启动。

```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

IELTSUC → 偏好设置：服务地址 `http://127.0.0.1:11434`，模型名称填写 ollama list 中的完整 NAME。点击“检测已安装模型”，然后“测试连接”。当前模型检测按钮读取默认 11434 端口；使用其他本地端口时手工填写模型名即可。

## 3. 使用范围

AI 参与句子 / 语句块点评、Task 1 / Task 2 建议、话题生成、试卷解析。单词精确匹配、计时和每日目标不依赖模型。

后端使用 Ollama 原生 POST /api/chat，stream=false；试卷解析要求 JSON 输出。当前超时为 240 秒。本机首次加载模型可能较慢。仅接受 localhost、127.0.0.1、[::1] 地址，不接受远程服务器或 OpenAI API 地址。

```powershell
$body = @{ model = 'YOUR_MODEL'; stream = $false; messages = @(@{role='user';content='请用一句话确认连接成功'}) } | ConvertTo-Json -Depth 6
Invoke-RestMethod http://127.0.0.1:11434/api/chat -Method Post -ContentType 'application/json' -Body ([Text.Encoding]::UTF8.GetBytes($body))
```

## 4. 排错

| 现象 | 处理 |
| --- | --- |
| 无法连接 | 启动 Ollama，检查本地端口 |
| model not found | 对照 ollama list，检查名称与标签 |
| 超时 | 先用短句验证，选择较小模型，关闭占用显存的程序 |
| 试卷 JSON 无效 | 缩短材料、提供清晰题号和答案、换用支持结构化输出的文本模型 |
| 建议与教材不同 | AI 不是标准答案；根据题意和教材核对，不以措辞相同作为唯一依据 |

部署参考：[Ollama 官方文档](https://docs.ollama.com/quickstart)。不需要把 API 暴露到公网，也不需要云端 API key。
