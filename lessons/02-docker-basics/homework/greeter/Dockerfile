FROM python:3.11-slim//IMAGE בסיסי של פייתון
# --- NetFree://אלו הוראות התקנת תעודת האבטחה של נטפרי
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh
RUN cat /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
ENV PIP_CERT=/etc/ca-bundle.crt
# --- סוף NetFree ---

WORKDIR /app//את הפקודות הבאות מבצעים בניתוב הזה

COPY requirements.txt .//תפנה לקובץ הדרישות
RUN pip install --no-cache-dir -r requirements.txt//תתקין

COPY app.py .//תפנה לקובץ קוד

EXPOSE 5000//פורט מתאים

CMD ["python", "app.py"]//תתחיל להריץ כשהדוקר עולה
