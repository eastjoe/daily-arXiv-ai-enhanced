import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import date
# 导入新添加的 markdown 库
import markdown

def send_email_with_markdown_content(file_path, recipient_email):
    """
    读取Markdown文件的内容，将其转换为HTML并作为邮件正文发送。
    """
    # 从环境变量中获取邮箱配置
    mail_host = os.environ.get('MAIL_HOST')
    mail_user = os.environ.get('MAIL_USER')
    mail_pass = os.environ.get('MAIL_PASS')
    sender = mail_user

    if not all([mail_host, mail_user, mail_pass]):
        print("邮件服务器配置不完整 (MAIL_HOST, MAIL_USER, MAIL_PASS)，跳过发送邮件。")
        return

    # --- 读取Markdown文件内容 ---
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"错误: 找不到 Markdown 文件 at {file_path}")
        return
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return

    # --- 将Markdown转换为HTML ---
    # 添加了 'tables' 和 'fenced_code' 扩展，以更好地支持表格和代码块
    html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

    # --- 创建邮件内容 ---
    # 使用 'alternative' 类型，邮件客户端会优先显示HTML版本
    message = MIMEMultipart('alternative')
    message['From'] = Header(f"Daily arXiv Report <{sender}>", 'utf-8')
    message['To'] = Header(f"Recipient <{recipient_email}>", 'utf-8')
    
    today_str_cn = date.today().strftime("%Y年%m月%d日")
    subject = f'【{today_str_cn}】的ArXiv报告'
    message['Subject'] = Header(subject, 'utf-8')

    # 创建纯文本部分 (作为备用，内容为原始Markdown)
    plain_text_part = MIMEText(md_content, 'plain', 'utf-8')
    
    # 创建HTML部分
    html_part = MIMEText(html_content, 'html', 'utf-8')

    # 将两个部分都添加到邮件中
    # 邮件客户端会优先尝试显示最后一个部分（HTML）
    message.attach(plain_text_part)
    message.attach(html_part)

    # --- 发送邮件 ---
    try:
        smtp_server = smtplib.SMTP_SSL(mail_host, 465) 
        smtp_server.login(mail_user, mail_pass)
        smtp_server.sendmail(sender, [recipient_email], message.as_string())
        smtp_server.quit()
        print(f"邮件已成功发送至 {recipient_email}")
    except smtplib.SMTPException as e:
        print(f"错误: 无法发送邮件。 {e}")

if __name__ == '__main__':
    md_file_path = os.environ.get('MD_FILE_PATH')
    recipient = os.environ.get('RECIPIENT_EMAIL')

    if md_file_path and recipient:
        print(f"准备将文件 '{md_file_path}' 的内容作为邮件正文发送至 '{recipient}'...")
        # 调用更新后的函数
        send_email_with_markdown_content(md_file_path, recipient)
    else:
        print("未找到 MD_FILE_PATH 或 RECIPIENT_EMAIL 环境变量，跳过发送邮件。")
