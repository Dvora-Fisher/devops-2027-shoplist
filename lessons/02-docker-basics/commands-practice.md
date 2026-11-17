# שיעור 2 — תרגול פקודות Docker

שני חלקים:
- **חלק א, על דף:** לכתוב את הפקודה המתאימה, בלי מחשב. מתאים גם לחזרה בבית.
- **חלק ב, במחשב הכיתה:** תרגיל רצוף שעובר על כל הפקודות של השיעור.

הפקודות המלאות, עם הסברים: [docker-commands.md](docker-commands.md).

---

## חלק א — מה הפקודה? (על דף)

לכתוב את הפקודה, ורק אחר כך לפתוח את התשובה.

| # | המשימה |
|---|---|
| 1 | להוריד את ה-image `node:24-alpine` בלי להריץ אותו |
| 2 | להציג את כל ה-images במחשב |
| 3 | להריץ את `nginx:1.30-alpine` ברקע, בשם `site`, כך שיהיה זמין ב-`localhost:8081` |
| 4 | להציג רק את ה-containers שרצים עכשיו |
| 5 | להציג את כל ה-containers, כולל עצורים |
| 6 | להציג את הלוגים של `site`, ולהמשיך להציג לוגים חדשים בזמן אמת |
| 7 | לפתוח טרמינל בתוך `site` |
| 8 | לעצור את `site` בלי למחוק אותו |
| 9 | להפעיל שוב את `site` |
| 10 | למחוק את `site`, גם אם הוא רץ |
| 11 | לבנות image בשם `shoplist-stats` עם התגית `v2` מהתיקייה `app/stats` |
| 12 | להריץ את `shoplist-stats:v2` עם משתנה הסביבה `BACKEND_URL=http://backend:5000` |
| 13 | למחוק את ה-image `shoplist-stats:v2` |
| 14 | לראות כמה מקום Docker תופס בדיסק |

<details><summary>תשובות</summary>

| # | הפקודה |
|---|---|
| 1 | `docker pull node:24-alpine` |
| 2 | `docker images` |
| 3 | `docker run -d -p 8081:80 --name site nginx:1.30-alpine` |
| 4 | `docker ps` |
| 5 | `docker ps -a` |
| 6 | `docker logs -f site` (יציאה: Ctrl+C) |
| 7 | `docker exec -it site sh` |
| 8 | `docker stop site` |
| 9 | `docker start site` |
| 10 | `docker rm -f site` |
| 11 | `docker build -t shoplist-stats:v2 app/stats` |
| 12 | `docker run -d -e BACKEND_URL=http://backend:5000 shoplist-stats:v2` |
| 13 | `docker rmi shoplist-stats:v2` |
| 14 | `docker system df` |

</details>

---

## חלק ב — תרגיל רצוף (במחשב הכיתה, 20 דקות)

מתוך התיקייה `devops-2027-shoplist`. כל שלב בונה על הקודם. אחרי כל שלב יש שאלה: לענות עליה לפני שממשיכות.

**1. שני containers מאותו image.**
```shell
docker run -d -p 8081:80 --name site1 nginx:1.30-alpine
docker run -d -p 8082:80 --name site2 nginx:1.30-alpine
docker ps
```
לפתוח בדפדפן את `localhost:8081` ואת `localhost:8082`.
> **שאלה:** כמה images יש, וכמה containers?

**2. התנגשות.**
```shell
docker run -d -p 8081:80 --name site3 nginx:1.30-alpine
```
> **שאלה:** למה זה נכשל? מה צריך לשנות בפקודה כדי שזה יעבוד?

**3. לוגים בזמן אמת.**
```shell
docker logs -f site1
```
לרענן את `localhost:8081` כמה פעמים ולראות שורות חדשות. לצאת עם Ctrl+C.
> **שאלה:** אחרי Ctrl+C, ה-container עדיין רץ? איך בודקים?

**4. להציץ פנימה.**
```shell
docker exec -it site1 sh
```
בתוך ה-container:
```shell
ls /usr/share/nginx/html
cat /etc/os-release
exit
```
> **שאלה:** איזו מערכת הפעלה רצה בתוך ה-container? האם היא מותקנת אצלכן במחשב?

> **ב-Git Bash:** אם מופיע `the input device is not a TTY`, להוסיף `winpty` בתחילת הפקודה.

**5. לעצור ולהפעיל.**
```shell
docker stop site1
docker ps
docker ps -a
docker start site1
```
> **שאלה:** מה ההבדל בין הפלט של `docker ps` לפלט של `docker ps -a` אחרי ה-stop?

**6. פרטים על container.**
```shell
docker port site2
docker inspect site2 --format "{{.Config.Image}}"
docker stats --no-stream
```
> **שאלה:** כמה זיכרון כל container תופס?

**7. משתני סביבה.**
```shell
docker run -d -p 3001:3000 --name stats-a -e BACKEND_URL=http://nowhere:5000 shoplist-stats:local
curl.exe http://localhost:3001/stats
docker logs stats-a
```
> **שאלה:** מה ההבדל בין השגיאה כאן לשגיאה בלי `-e`? מה זה אומר על משתני סביבה?

**8. ניקיון.**
```shell
docker rm -f site1 site2 stats-a
docker ps -a
docker system df
```
> **שאלה:** ה-image של nginx עדיין במחשב? למה?

<details><summary>תשובות לשאלות של חלק ב</summary>

1. image אחד (`nginx:1.30-alpine`), שני containers.
2. פורט 8081 במחשב כבר תפוס על ידי `site1`. צריך פורט אחר במחשב, למשל `-p 8083:80`. הפורט בתוך ה-container יכול להישאר 80.
3. כן. Ctrl+C עוצר רק את הצפייה בלוגים. בודקים עם `docker ps`.
4. Alpine Linux. היא לא מותקנת אצלכן: היא חלק מה-image.
5. אחרי stop, `site1` לא מופיע ב-`docker ps`, אבל מופיע ב-`docker ps -a` עם הסטטוס `Exited`.
6. בעמודה `MEM USAGE` של `docker stats`. בדרך כלל כמה מגה-בייטים בלבד.
7. בלי `-e`, stats מחפש `backend`. עם `-e`, הוא מחפש `nowhere`. אותו image, התנהגות אחרת: ההגדרות מגיעות מבחוץ, לא מהקוד.
8. כן. מחקנו containers, לא images. `docker rmi` מוחק image.

</details>
