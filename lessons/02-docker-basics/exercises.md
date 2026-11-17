# שיעור 2 — תרגילים
## Docker: images, containers ו-Dockerfile

**הנחיות:**
- לפתור לפי הסדר
- להסתכל במדריך רק אם נתקעתן
- לבדוק כל תרגיל לפני שעוברים לבא
- הפקודות רצות בטרמינל שבחרתן (PowerShell, Git Bash או WSL), מהתיקייה `devops-2027-shoplist`

---

## תרגיל 1 — container ראשון (קל) · נעשה בהרצאה

**המשימה:**
1. להריץ את Nginx ברקע, על פורט 8080 במחשב שלכן:
   `docker run -d -p 8080:80 --name web nginx:1.30-alpine`
2. לפתוח בדפדפן את `http://localhost:8080`.
3. להציג את ה-containers שרצים ואת ה-images שבמחשב.
4. להציג את הלוגים של ה-container. לרענן את הדפדפן, ולהציג שוב.
5. לעצור ולמחוק את ה-container, ולבדוק שה-image עדיין קיים.

**פקודות שכדאי לבדוק:** `docker ps`, `docker images`, `docker logs`, `docker stop`, `docker rm`

**מה רואים כאן:**
image הוא המתכון, container הוא העוגה. מחיקת container לא מוחקת את ה-image. `-p 8080:80` מחבר את פורט 8080 במחשב לפורט 80 בתוך ה-container.

**התוצאה הצפויה:**
- דף הפתיחה של Nginx ב-`http://localhost:8080`
- שורת לוג חדשה בכל רענון של הדפדפן
- אחרי המחיקה: `web` לא מופיע ב-`docker ps -a`, אבל `nginx:1.30-alpine` מופיע ב-`docker images`

**בדיקה:**
```shell
docker ps -a --filter name=web     # ריק
docker images nginx                # מופיע nginx 1.30-alpine
```

---

## תרגיל 2 — לשבור ולתקן את ה-Dockerfile (בינוני)

**המשימה:**
לעשות טעות בכוונה בקובץ `app/backend/Dockerfile`: להעביר את השורה `COPY requirements.txt .` אל **אחרי** השורה `COPY app.py .`

ואז:
1. לבנות: `docker build -t shoplist-backend:broken app/backend`, ולשים לב כמה זמן זה לוקח.
2. לשנות שורה אחת ב-`app/backend/app.py`, למשל להוסיף רווח.
3. לבנות שוב, באותה פקודה, ולראות מה קורה לשלב ה-`pip install`.

אחר כך להחזיר את ה-Dockerfile לסדר הנכון, ולחזור על שלבים 2–3.

**מה רואים כאן:**
- **בסדר הלא נכון:** pip install רץ מחדש בכל שינוי בקוד.
- **בסדר הנכון:** pip install מסומן `CACHED` ונלקח מהזיכרון, כל עוד `requirements.txt` לא השתנה.

**התוצאה הצפויה:**
- **בסדר הלא נכון:** כל build מתקין את הספריות מחדש.
- **בסדר הנכון:** ב-build השני מופיע `CACHED` ליד שורת ה-pip, וה-build לוקח שניות.

**בדיקה:**
```shell
docker build -t shoplist-backend:local app/backend
```
בפלט, ליד השלב של `RUN pip install`, צריך להופיע `CACHED`.

---

## תרגיל 3 — להריץ את stats לבד (בינוני)

**המשימה:**
1. לבנות את ה-image של stats, אם עוד לא בניתן: `docker build -t shoplist-stats:local app/stats`
2. להריץ אותו על פורט 3000: `docker run -d -p 3000:3000 --name stats shoplist-stats:local`
3. לפתוח בדפדפן את `http://localhost:3000/health`, ואחר כך את `http://localhost:3000/stats`.
4. לקרוא את הלוגים של ה-container.
5. למחוק את ה-container ולהריץ אותו שוב, הפעם עם כתובת אחרת ל-backend:
   `docker run -d -p 3000:3000 --name stats -e BACKEND_URL=http://nowhere:5000 shoplist-stats:local`
   לפתוח שוב את `/stats` ולהשוות את השגיאה.

**מה רואים כאן:**
סרוויס ה-stats רץ מצוין לבד: `/health` עונה. אבל `/stats` נכשל, כי stats צריך את ה-backend, ואין container של backend. מיקרו-סרוויס הוא עצמאי מבחינת ההרצה, אבל לא מבחינת מה שהוא יכול לעשות. הדגל `-e` מגדיר משתנה סביבה: אותו image מתנהג אחרת עם הגדרות אחרות.

**התוצאה הצפויה:**
- `/health`: `{"status":"ok"}`
- `/stats`: `{"error":"backend unavailable", ...}` עם קוד 502
- בלוגים: `stats service listening on 0.0.0.0:3000`

**בדיקה:**
```shell
curl.exe -i http://localhost:3000/health    # HTTP/1.1 200 OK
curl.exe -i http://localhost:3000/stats     # HTTP/1.1 502 Bad Gateway
docker rm -f stats
```

**שאלה:** מה צריך כדי ש-`/stats` יעבוד? (רמז: שיעור 3)

---

## תרגיל בונוס — להציץ לתוך container (רשות)

**המשימה:**
1. להריץ שוב את stats (תרגיל 3, שלב 2).
2. לפתוח טרמינל בתוך ה-container: `docker exec -it stats sh`
   (ב-Git Bash, אם מופיע `the input device is not a TTY`: `winpty docker exec -it stats sh`)
3. להריץ בפנים `ls /app`, `node --version` ו-`cat /etc/os-release`. ליציאה: `exit`.
4. להריץ container שני מאותו image, בשם `stats2` ועל פורט 3001.

**מה רואים כאן:**
ל-container יש מערכת קבצים משלו וגרסת Node.js משלו, ושום דבר מזה לא מותקן במחשב שלכן. מ-image אחד אפשר להריץ כמה containers בבת אחת.

**בדיקה:**
```shell
docker ps --filter ancestor=shoplist-stats:local    # שני containers
docker rm -f stats stats2
```
