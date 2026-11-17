# מדריך תחביר Dockerfile

Dockerfile הוא קובץ טקסט עם הוראות. Docker קורא אותו מלמעלה למטה, וכל הוראה יוצרת שכבה ב-image.

```dockerfile
# הערה מתחילה ב-#
INSTRUCTION arguments
```

- ההוראות נכתבות באותיות גדולות. זו מוסכמה, לא חובה.
- הקובץ נקרא `Dockerfile`, בלי סיומת.
- הוראה ראשונה (חוץ מ-`ARG` והערות) היא תמיד `FROM`.

---

## שתי צורות כתיבה: shell ו-exec

| צורה | דוגמה | מה קורה |
|---|---|---|
| **exec** (מומלצת) | `CMD ["python", "app.py"]` | Docker מריץ את התוכנית ישירות. האפליקציה מקבלת את אות העצירה של `docker stop` |
| **shell** | `CMD python app.py` | Docker מריץ דרך `/bin/sh -c`. אפשר להשתמש ב-`&&`, משתנים ו-pipe |

ב-`RUN` משתמשים בדרך כלל בצורת shell. ב-`CMD` וב-`ENTRYPOINT` בצורת exec.

---

## ההוראות הבסיסיות (משתמשים בהן ב-ShopList)

### `FROM`: image הבסיס
```dockerfile
FROM python:3.11-slim
FROM node:24-alpine AS build      # שם לשלב (multi-stage, בהמשך)
```
- תמיד עם גרסה. אף פעם לא `latest`.
- `slim` ו-`alpine` הם גרסאות קטנות יותר של אותו image.

### `WORKDIR`: תיקיית העבודה
```dockerfile
WORKDIR /app
```
- כל ההוראות שאחריה רצות מהתיקייה הזו. אם היא לא קיימת, Docker יוצר אותה.
- עדיף על `RUN cd /app`, שלא נשמר בין הוראות.

### `COPY`: העתקה מהמחשב לתוך ה-image
```dockerfile
COPY requirements.txt .
COPY app.py .
COPY src/ ./src/
COPY --chown=node:node server.js .   # עם בעלות על הקובץ
```
- המקור יחסי לתיקייה שנתתם ל-`docker build` (ה-build context).
- `.` כיעד הוא ה-`WORKDIR`.

### `RUN`: הרצת פקודה בזמן ה-build
```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
```
- רץ **פעם אחת, בזמן ה-build**, והתוצאה נשמרת כשכבה.
- מחברים פקודות קשורות עם `&&` כדי לקבל שכבה אחת במקום כמה.

### `EXPOSE`: תיעוד הפורט
```dockerfile
EXPOSE 5000
EXPOSE 53/udp
```
- **רק מתעד.** לא פותח את הפורט. מי שפותח הוא `-p` ב-`docker run`.

### `CMD`: הפקודה שרצה כשה-container עולה
```dockerfile
CMD ["python", "app.py"]
```
- רק ה-`CMD` האחרון בקובץ נחשב.
- כל מה שכותבים אחרי שם ה-image ב-`docker run` מחליף אותו.

---

## הגדרות וסביבה

### `ENV`: משתנה סביבה קבוע
```dockerfile
ENV PORT=3000
ENV PYTHONUNBUFFERED=1
```
- קיים גם בזמן ה-build וגם כשה-container רץ.
- אפשר לדרוס ב-`docker run -e PORT=4000`.
- **לא שמים סיסמאות ב-`ENV`.** הן נשמרות בתוך ה-image ונגישות לכל מי שיש לו אותו.

### `ARG`: משתנה לזמן ה-build בלבד
```dockerfile
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim
```
```bash
docker build --build-arg PYTHON_VERSION=3.12 .
```
- קיים **רק בזמן ה-build**. ה-container שרץ לא רואה אותו.

| | `ARG` | `ENV` |
|---|---|---|
| זמין ב-build | כן | כן |
| זמין כשה-container רץ | לא | כן |
| איך משנים | `--build-arg` | `-e` ב-`docker run` |

### `LABEL`: מידע על ה-image
```dockerfile
LABEL maintainer="devops-course" version="1.0"
```
רואים אותו ב-`docker inspect`.

### `USER`: לרוץ כמשתמש שאינו root
```dockerfile
USER node
```
- כל ההוראות שאחריה, וה-container עצמו, רצים כמשתמש הזה.
- נוהג בטיחות טוב: אם מישהו פורץ לאפליקציה, אין לו הרשאות root.

---

## הוראות מתקדמות

### `ENTRYPOINT`: התוכנית הקבועה
```dockerfile
ENTRYPOINT ["python", "app.py"]
CMD ["--port", "5000"]
```
- כשיש גם `ENTRYPOINT` וגם `CMD`, ה-`CMD` הופך לפרמטרים של ה-`ENTRYPOINT`.

| | `CMD` | `ENTRYPOINT` |
|---|---|---|
| תפקיד | פקודת ברירת מחדל | התוכנית שתמיד רצה |
| `docker run image X` | `X` מחליף את ה-`CMD` | `X` מתווסף כפרמטר |
| איך דורסים | פשוט כותבים פקודה אחרת | רק עם `--entrypoint` |

### `ADD`: כמו `COPY`, עם יכולות נוספות
```dockerfile
ADD app.tar.gz /app/            # פורס ארכיון tar אוטומטית
ADD https://example.com/file /tmp/
```
**ההמלצה: להשתמש ב-`COPY`.** `ADD` רק כשצריך לפרוס ארכיון.

### `VOLUME`: נקודת חיבור לנתונים
```dockerfile
VOLUME ["/var/lib/postgresql/data"]
```
מסמן תיקייה שהנתונים בה צריכים לשרוד גם אחרי מחיקת ה-container. נרחיב במפגש 3.

### `HEALTHCHECK`: בדיקת תקינות
```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:3000/health || exit 1
```
- Docker מריץ את הבדיקה כל פרק זמן. ב-`docker ps` רואים `healthy` או `unhealthy`.
- `HEALTHCHECK NONE` מבטל בדיקה שהגיעה מ-image הבסיס.

### `SHELL`: החלפת ה-shell של צורת ה-shell
```dockerfile
SHELL ["/bin/bash", "-c"]
```

### `STOPSIGNAL`: איזה אות עוצר את ה-container
```dockerfile
STOPSIGNAL SIGTERM
```

### `ONBUILD`: הוראה שרצה כשמישהו אחר בונה מעל ה-image
```dockerfile
ONBUILD COPY . /app
```
נדיר. שימושי ב-images שנועדו לשמש כבסיס לאחרים.

---

## `.dockerignore`

קובץ ליד ה-Dockerfile שאומר ל-Docker מה **לא** לשלוח ל-build. הוא חוסך זמן, ומונע העתקה בטעות של סודות לתוך ה-image.

```
.git
__pycache__/
*.pyc
node_modules/
.env
```

---

## Multi-stage build: image סופי קטן

שלב אחד בונה, ושלב שני לוקח רק את התוצאה. הכלים של שלב הבנייה לא נכנסים ל-image הסופי.

```dockerfile
FROM node:24-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.30-alpine
COPY --from=build /app/dist /usr/share/nginx/html
```

---

## כללי אצבע

1. גרסה מדויקת ב-`FROM`, אף פעם לא `latest`.
2. מה שמשתנה לעיתים רחוקות למעלה (תלויות), מה שמשתנה כל הזמן למטה (קוד).
3. לחבר פקודות `RUN` קשורות עם `&&`.
4. `COPY` ולא `ADD`.
5. צורת exec ב-`CMD` וב-`ENTRYPOINT`.
6. אין סיסמאות ב-Dockerfile. מעבירים אותן בזמן ההרצה.
7. `.dockerignore` בכל פרויקט.
8. כשאפשר, לרוץ כמשתמש שאינו root (`USER`).
