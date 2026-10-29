# 词库、排序与导入

## 公开版与个人资料

公开版自带 10 条原创示例词。个人开发环境中的资料规模如下，仅说明已实现的集成能力，不随公开 EXE / 源码重新分发：词汇真经 3744 条 / 22 章、听力179条、阅读376条主词条及同义替换、训练营全1488条去重词 / 短语、念念有词自测表307条去重表达、写作念念有词389条核心表达、100句翻译参考。

“538”名称包含同义替换体系，不代表能从 PDF 得到538行主词条。个人版按用户所给 PDF 由 resemble、recognize、adjust、approach、fundamental、rely on 开始的顺序整理。教材可能含排印 / OCR 错误，应结合原页校对。

自测表只有中文，需自行补足英文参考。英语句子可能有多种正确译法，使用同义答案或本地 AI 复核；自动字面匹配不代表完整语义判断。

## 应用内导入

词汇实验室 → 本地 OCR / 文件导入 → 选择自己的文件 → 校对提取结果 → 命名词书并保存。词条需要英文和中文；词性可为空。

推荐 TSV 或竖线格式，一行一个词：

```text
focus | v. | 专注
progress | n. | 进步
make progress | phr. | 取得进步
```

英文、词性、释义之间使用 Tab、竖线或至少两个空格。避免在 CSV 英文短语内部放未转义的逗号。可先使用 examples/vocabulary.tsv 验证。当前文本解析器不是通用 CSV 引擎；复杂表格建议预先整理为 TSV。

支持 TXT / CSV / TSV / DOCX / 带文字层 PDF、PNG / JPG / JPEG / WEBP / BMP。扫描 PDF 请先导出图片；旧 DOC 需转换 DOCX。Tesseract 英文 / 简体中文模型随公开版提供，OCR 不向云端上传图片。字母连字、表格换行、短语空格可能识别错误，保存前务必校对。

## 高级：配置有权使用的顺序词书

应用内简单导入只保存 english、pos、translation、book，按插入 ID 展示，不会自动理解阅读 / 听力 / 写作分类。需要课程模块入口、严格顺序和可接受答案时，在构建前编辑 assets/curriculum/personal.json：

```json
{
  "version": "my-library-v1",
  "books": [{"name":"我的语句块","module":"writing","count":1,"pdf":"public/personal/my-notes.pdf"}],
  "words": [{"english":"make progress","translation":"取得进步","pos":"phr.","book":"我的语句块","module":"writing","order":0,"accepted":["make some progress"]}]
}
```

module 可为 listening / reading / writing。order 从0递增，book 与 books.name 完全一致，count 填实际去重数量。参考 PDF 可选；没有资料时不要使用“打开原 PDF”。

如需个人本地打包资料，放入 assets/curriculum/upstream/public/ 下，并自行在 electron-builder extraResources 添加 upstream → curriculum 目录复制规则。公开发行配置默认不复制这些文件。更改种子词库时，应更新 curriculum.cjs 中迁移标记或使用全新测试数据目录；仅改 JSON.version 不会重新导入已存在的数据库。先备份，避免覆盖用户修改。

## 发音

本地 MP3 优先；没有本地音频时使用原 my-ielts 阅读页相同的有道 dictvoice 英音接口并缓存到用户目录。网络失败时使用 Windows speechSynthesis。系统需有英语语音；它不等于教材原声。在线发音会向服务方发送要朗读的英文文字。

## 资料边界

请使用自己有权使用的教材和试卷。上游仓库能访问、个人持有 PDF 或添加鸣谢，均不自动授予公开再分发教材与录音的权利。不要把自己的数据库备份、私人 PDF 或录音提交到 GitHub。
