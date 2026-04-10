import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
load_dotenv()
    
class EmailSender:
    def __init__(self):
        self.email_id = os.getenv("email")
        self.apppassword = os.getenv("apppassword")
        self.receipt_email_id = os.getenv("receipt_email")
    
    def message_prep(self, subject:str, email: str, body:str):
        
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = self.email_id
        msg['To'] = email
        
        return msg
        pass
    
    def _send_email(self, msg:MIMEText, recipient:str):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            # use the configured sender id and app password
            smtp_server.login(self.email_id, self.apppassword)
            smtp_server.sendmail(self.email_id, recipient, msg.as_string())
        pass
    
    def send_email(self, reason:str, email:str, body:str):
        
        if reason == "Job Opportunity":
            subject = "Your time has comeee !!!! get up  !!!!"
        elif reason == "Collaboration":
            subject = "Time to build somthing !! getup !"
        elif reason == "General":
            subject = "Someone is saying hii !!"
        else:
            subject = "hmmm !! what could it be :)"
        # send email to self
        reciept_email = self.message_prep(subject=subject, email=self.receipt_email_id, body=body + f"\n \n {email} has contacted you ")
        self._send_email(msg=reciept_email, recipient=self.receipt_email_id)
        # send email to the contact person
        contact_person_email = self.message_prep(subject=os.getenv("contact_subject"), email=email, body=os.getenv("contact_body"))
        self._send_email(msg=contact_person_email, recipient=email)
        pass

    def send_general_email(self, subject:str, email:str, body:str):
        # send email to self 
        reciept_email = self.message_prep(subject=subject, email=self.receipt_email_id, body=body + f"\n \n {email} has contacted you ")
        self._send_email(msg=reciept_email, recipient=self.receipt_email_id)
        # send email to the contact person
        contact_person_email = self.message_prep(subject=os.getenv("contact_subject"), email=email, body=os.getenv("contact_body"))
        self._send_email(msg=contact_person_email, recipient=email)
        
        
        pass

    def send_to_recipient(self, subject: str, content: str):
        """Send a simple email with given subject and content from self.email_id to self.receipt_email_id."""
        if not self.email_id or not self.apppassword or not self.receipt_email_id:
            raise ValueError("Missing email configuration (email, apppassword, or receipt_email).")

        msg = self.message_prep(subject=subject, email=self.receipt_email_id, body=content)
        self._send_email(msg=msg, recipient=self.receipt_email_id)
        return True

    def send_to_custom_recipient(self, target_email: str, subject: str, content: str):
        """Send a simple email with given subject and content from self.email_id to a custom target email."""
        if not self.email_id or not self.apppassword:
            raise ValueError("Missing email configuration (email or apppassword).")

        msg = self.message_prep(subject=subject, email=target_email, body=content)
        self._send_email(msg=msg, recipient=target_email)
        return True