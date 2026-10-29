# Windows 部署与维护

## 普通用户：运行 Release

下载 Releases 中的 Windows x64 单文件 EXE，放在自己选择的文件夹启动。它会在临时目录解压运行组件，首次打开可能较慢。无需 Node.js，不含 Ollama / 模型权重。也可对 EXE 右键创建桌面快捷方式。

先设置考试日期、开始备考日期、目标分数，再设置每日单词 / 听写 / 阅读 / 写作目标。0 表示不设该项目标。完成练习后回到首页查看统计。

单文件 EXE 未进行付费代码签名；下载后可对照 Release 的 SHA256SUMS.txt 校验。不要关闭系统安全保护。若系统阻止启动，请核对下载来源和文件哈希，再按自己的设备管理要求决定是否运行。

```powershell
Get-FileHash '.\IELTSUC-1.3.1-win-x64.exe' -Algorithm SHA256
```

## 源码启动

Windows x64，Node.js 22+，npm，Git。首次安装依赖、Electron 和 OCR 语言数据需要网络。postinstall 从固定提交下载语言数据并校验 SHA256；发行 EXE 已内置这些数据。

```powershell
git clone https://github.com/Lidazou/IELTSUC.git
cd IELTSUC
npm ci
npm test
npm start
```

如果 Electron 首次下载失败，请检查自己的网络 / 代理设置后重新执行 npm ci。不要禁用 TLS 校验。项目不依赖全局 Electron。

## 构建

```powershell
npm run dist
npm run portable
```

`dist/win-unpacked/` 是完整目录版，应复制整个文件夹；`dist/IELTSUC-1.3.1-win-x64.exe` 是便携单文件版。公开构建不打包第三方教材和录音。

## 数据备份与升级

偏好设置 → 导出数据库备份。升级前备份，随后用新版 EXE 启动。数据在 Electron 用户目录，而非源码目录。恢复备份会替换当前词库、记录、试卷和笔记，请先保存当前备份。

## 常见情况

- 无单词：公开版只有示例，使用词汇模块导入自己的词书。
- 无 AI：按 OLLAMA.md 配置本机服务；基础打字与记录不依赖 AI。
- 没声音：检查系统音量、网络、英语语音包；在线发音失败会使用系统语音。
- PDF 导入空白：扫描件需要先导出 PNG / JPG，再使用 OCR。
- 模考解析不准确：先检查提取的试卷文字与题号，再校对本地模型返回的题目和答案。
- 高分辨率显示：可调整窗口大小，界面会响应布局；支持黑白主题。

## GitHub 发布维护

用 GitHub CLI 登录后，可执行根目录 publish.ps1，创建仓库（若尚不存在）、推送当前源码并上传 EXE、部署文档、词库文档、模型指南及 SHA256SUMS.txt。执行前应完成测试和构建。不要上传个人版目录、数据库和第三方教材。
