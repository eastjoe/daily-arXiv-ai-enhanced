import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import date

def send_email_with_attachment(file_path, recipient_email):
    """
    发送带有附件的邮件。
    从环境变量中读取邮件服务器配置。
    """
    # 从环境变量中获取邮箱配置
    # 在 GitHub 项目中，你应该使用 Secrets 来存储这些敏感信息
    mail_host = os.environ.get('MAIL_HOST')  # 例如: smtp.163.com
    mail_user = os.environ.get('MAIL_USER')  # 例如: your_email@163.com
    mail_pass = os.environ.get('MAIL_PASS')  # 邮箱授权码，而不是登录密码
    sender = mail_user

    if not all([mail_host, mail_user, mail_pass]):
        print("邮件服务器配置不完整 (MAIL_HOST, MAIL_USER, MAIL_PASS)，跳过发送邮件。")
        return

    # --- 创建邮件内容 ---
    message = MIMEMultipart()
    message['From'] = Header(f"Daily arXiv Report <{sender}>", 'utf-8')
    message['To'] = Header(f"Recipient <{recipient_email}>", 'utf-8')
    today_str = date.today().strftime("%Y-%m-%d")
    subject = f'ArXiv Daily Summary - {today_str}'
    message['Subject'] = Header(subject, 'utf-8')

    # 邮件正文
    message.attach(MIMEText('你好，\n\n附件中是今日的 ArXiv 论文摘要，请查收。\n\n祝好！', 'plain', 'utf-8'))

    # --- 读取并添加附件 ---
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            attachment_content = f.read()
        
        # 将 Markdown 内容作为附件
        att = MIMEText(attachment_content, 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        # 使用 os.path.basename 获取文件名
        file_name = os.path.basename(file_path)
        att["Content-Disposition"] = f'attachment; filename="{file_name}"'
        message.attach(att)

    except FileNotFoundError:
        print(f"错误: 找不到 Markdown 文件 at {file_path}")
        return
    except Exception as e:
        print(f"读取附件时出错: {e}")
        return

    # --- 发送邮件 ---
    try:
        # 使用 SSL 加密连接
        smtp_server = smtplib.SMTP_SSL(mail_host, 465) 
        smtp_server.login(mail_user, mail_pass)
        smtp_server.sendmail(sender, [recipient_email], message.as_string())
        smtp_server.quit()
        print(f"邮件已成功发送至 {recipient_email}")
    except smtplib.SMTPException as e:
        print(f"错误: 无法发送邮件。 {e}")

if __name__ == '__main__':
    # 从环境变量获取 Markdown 文件路径和收件人邮箱
    md_file_path = os.environ.get('MD_FILE_PATH')
    recipient = os.environ.get('RECIPIENT_EMAIL')

    if md_file_path and recipient:
        print(f"准备发送文件 '{md_file_path}' 至 '{recipient}'...")
        send_email_with_attachment(md_file_path, recipient)
    else:
        print("未找到 MD_FILE_PATH 或 RECIPIENT_EMAIL 环境变量，跳过发送邮件。")
