//	image בסיס: Python 3.11 מוכן, בגרסה קטנה
FROM python:3.11-slim

# --- NetFree://אלו הוראות התקנת תעודת האבטחה של נטפרי
ADD https://netfree.link/dl/unix-ca.sh /home/netfree-unix-ca.sh
RUN cat /home/netfree-unix-ca.sh | sh
ENV NODE_EXTRA_CA_CERTS=/etc/ca-bundle.crt
ENV REQUESTS_CA_BUNDLE=/etc/ca-bundle.crt
ENV SSL_CERT_FILE=/etc/ca-bundle.crt
ENV PIP_CERT=/etc/ca-bundle.crt
# --- סוף NetFree ---

//תיקיית העבודה בתוך ה-container. נוצרת אם לא קיימת
WORKDIR /app

COPY requirements.txt .//תפנה לקובץ הדרישות, קודם רק רשימת התלויות
RUN pip install --no-cache-dir -r requirements.txt//מתקינים את התלויות. השכבה נשמרת ב-cache

COPY app.py .//רק עכשיו - תפנה לקובץ קוד

EXPOSE 5000//תיעוד בלבד. לא פותח את הפורט 

CMD ["python", "app.py"]//	מה רץ כשה-container עולה
