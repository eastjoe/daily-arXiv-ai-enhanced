#!/bin/bash

# 获取当前 UTC 日期（与 run.sh 保持一致）
today=$(date -u "+%Y-%m-%d")
md_file="data/${today}.md"

# 检查文件是否存在
if [ ! -f "$md_file" ]; then
  echo "❌ Markdown 文件不存在: $md_file"
  exit 1
fi

# 使用 sendemail 工具发送邮件（你也可以替换为 Python smtplib）
# 注意：GitHub Actions 需要预装 sendemail 工具（或使用 actions 包）

sendemail \
  -f "$EMAIL_FROM" \
  -t "$EMAIL_TO" \
  -u "📄 arXiv 每日报告 - $today" \
  -m "您好，附件是 $today 的 arXiv AI 增强版论文摘要报告，请查收。" \
  -a "$md_file" \
  -s "$EMAIL_SMTP":"$EMAIL_PORT" \
  -xu "$EMAIL_USERNAME" \
  -xp "$EMAIL_PASSWORD" \
  -o tls=yes

