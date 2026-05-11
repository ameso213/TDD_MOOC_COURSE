# 04_BasicStrategy.py
# Real-life example: Updating a legacy CRM system's email sending logic.
# Identify change, break dependencies, introduce seam, test, change, refactor.

class EmailSender:
    def send_email(self, to, subject, body):
        import smtplib
        server = smtplib.SMTP('smtp.ameso.com')
        server.sendmail('ameso@gmail.com', to, f"Subject: {subject}\n\n{body}")
        server.quit()

# Step: Extract dependency
class EmailService:
    def __init__(self, smtp_client):
        self.smtp_client = smtp_client  # Seam

    def send(self, to, subject, body):
        self.smtp_client.send(to, subject, body)

class MockSMTP:
    def send(self, to, subject, body):
        print(f"Mock sent to {to}: {subject}")

# Now testable: EmailService(MockSMTP()).send(...)

# Real-life example: Migrating a file parser in a document management tool.
# Break file I/O dependencies.

class FileParser:
    def parse(self, filename):
        with open(filename, 'r') as f:  # Dependency
            content = f.read()
        return content.upper()

# Extract: Make content injectable
class Parser:
    def parse_content(self, content):
        return content.upper()

# In legacy wrapper
def parse_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return Parser().parse_content(content)

# Tests can call Parser().parse_content("test")