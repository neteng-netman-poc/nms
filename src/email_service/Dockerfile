FROM python:3.11-slim

# Set a working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables (provided as requested)
ENV email=<sending from email>
ENV apppassword=<sending email app password>
ENV receipt_email=<target email>

# note : there is an end point to send emails to custom email as well, you dont need to populate the last env variable, but its gonna default to it if email is invalid

# Expose port 9999 and run the FastAPI app with uvicorn
EXPOSE 9999
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9999"]
