# מדריך פקודות Docker

כל הפקודות שצריך לקורס, מסודרות לפי נושא. בכל טבלה: הפקודה, מה היא עושה, ודוגמה מ-ShopList.

> **טרמינל:** PowerShell, Git Bash או WSL, מה שנוח לכן. ההבדלים הקטנים בטבלה "איזה טרמינל?" ב-[README הראשי](../../README.md#איזה-טרמינל). בדוגמאות כתוב `curl.exe`, שעובד גם ב-PowerShell וגם ב-Git Bash.
> **טיפ:** לכל פקודה יש עזרה מובנית: `docker run --help`, `docker build --help`.
> **שם או ID:** בכל מקום שכתוב `<container>` אפשר לכתוב את השם (`--name`) או את תחילת ה-ID.

---

## 1. Images: בנייה וניהול

| פקודה | מה היא עושה | דוגמה |
|---|---|---|
| `docker build -t <name>:<tag> <dir>` | בונה image מה-Dockerfile שבתיקייה | `docker build -t shoplist-backend:local .` |
| `docker build -f <file> ...` | בונה מ-Dockerfile בשם או במיקום אחר | `docker build -f Dockerfile.dev -t app:dev .` |
| `docker build --no-cache ...` | בונה מאפס, בלי להשתמש ב-cache | `docker build --no-cache -t shoplist-backend:local .` |
| `docker build --build-arg K=V ...` | מעביר ערך להוראת `ARG` ב-Dockerfile | `docker build --build-arg VERSION=1.2 .` |
| `docker images` | רשימת ה-images במחשב (זהה ל-`docker image ls`) | `docker images --filter "reference=shoplist-*"` |
| `docker pull <image>:<tag>` | מוריד image מ-Registry | `docker pull nginx:1.30-alpine` |
| `docker push <image>:<tag>` | מעלה image ל-Registry (מפגשים 7–8) | `docker push ghcr.io/me/shoplist-backend:a1b2c3d4` |
| `docker tag <src> <dst>` | נותן ל-image שם נוסף. לא מעתיק כלום | `docker tag shoplist-backend:local shoplist-backend:v1` |
| `docker history <image>` | מראה את השכבות של ה-image ואת הגודל של כל אחת | `docker history shoplist-backend:local` |
| `docker rmi <image>` | מוחק image (זהה ל-`docker image rm`) | `docker rmi shoplist-backend:broken` |
| `docker image prune` | מוחק images בלי שם (`<none>`) שנשארו מ-builds קודמים | `docker image prune` |

---

## 2. הרצת container: `docker run` והדגלים שלו

`docker run [דגלים] <image> [פקודה]`. הדגלים באים **לפני** שם ה-image.

| דגל | מה הוא עושה | דוגמה |
|---|---|---|
| `-d` | מריץ ברקע ומחזיר את הטרמינל | `docker run -d nginx:1.30-alpine` |
| `--name <name>` | נותן שם ל-container | `--name web` |
| `-p <host>:<container>` | מחבר פורט במחשב לפורט ב-container | `-p 8080:80` |
| `-e KEY=value` | מגדיר משתנה סביבה | `-e BACKEND_URL=http://backend:5000` |
| `--env-file <file>` | טוען משתני סביבה מקובץ | `--env-file .env` |
| `-v <host-path>:<path>` | מחבר תיקייה מהמחשב לתוך ה-container | `-v ${PWD}/html:/usr/share/nginx/html` (PowerShell), `-v "$(pwd -W)/html:/usr/share/nginx/html"` (Git Bash) |
| `-v <volume>:<path>` | מחבר volume בשם (מפגש 3) | `-v pgdata:/var/lib/postgresql/data` |
| `--rm` | מוחק את ה-container אוטומטית כשהוא נעצר | `docker run --rm shoplist-stats:local node --version` |
| `-it` | מצב אינטראקטיבי עם טרמינל | `docker run -it python:3.11-slim bash` |
| `--network <name>` | מחבר לרשת מסוימת (מפגש 3) | `--network shoplist` |
| `--restart <policy>` | מה לעשות כשה-container נופל: `no`, `on-failure`, `always`, `unless-stopped` | `--restart unless-stopped` |
| `-w <dir>` | תיקיית העבודה בתוך ה-container | `-w /app` |
| `--entrypoint <cmd>` | מחליף את ה-`ENTRYPOINT` של ה-image | `--entrypoint sh` |

**כל מה שבא אחרי שם ה-image מחליף את ה-`CMD`:**
```bash
docker run --rm shoplist-stats:local node --check server.js
```

---

## 3. ניהול containers

| פקודה | מה היא עושה | דוגמה |
|---|---|---|
| `docker ps` | containers שרצים עכשיו | `docker ps` |
| `docker ps -a` | כל ה-containers, כולל עצורים | `docker ps -a` |
| `docker logs <container>` | מה האפליקציה הדפיסה | `docker logs stats` |
| `docker logs -f <container>` | ממשיך להציג לוגים חדשים בזמן אמת (יציאה: Ctrl+C) | `docker logs -f web` |
| `docker logs --tail 20 <container>` | רק 20 השורות האחרונות | `docker logs --tail 20 stats` |
| `docker stop <container>` | עוצר בעדינות (מחכה שהתהליך ייסגר) | `docker stop web` |
| `docker start <container>` | מפעיל שוב container עצור | `docker start web` |
| `docker restart <container>` | עוצר ומפעיל | `docker restart web` |
| `docker rm <container>` | מוחק container עצור | `docker rm web` |
| `docker rm -f <container>` | עוצר ומוחק בפקודה אחת | `docker rm -f stats` |
| `docker exec -it <container> sh` | פותח טרמינל בתוך container שרץ (ב-Git Bash לפעמים צריך `winpty` לפני) | `docker exec -it stats sh` |
| `docker exec <container> <cmd>` | מריץ פקודה אחת בתוך ה-container | `docker exec stats ls /app` |
| `docker inspect <container>` | כל הפרטים: IP, משתני סביבה, mounts (פלט JSON) | `docker inspect stats` |
| `docker port <container>` | אילו פורטים מחוברים | `docker port web` |
| `docker stats` | צריכת CPU וזיכרון בזמן אמת | `docker stats` |
| `docker top <container>` | התהליכים שרצים בתוך ה-container | `docker top web` |
| `docker cp <src> <dst>` | מעתיק קבצים בין המחשב ל-container | `docker cp web:/etc/nginx/nginx.conf .` |

---

## 4. Volumes ורשתות (הקדמה למפגש 3)

| פקודה | מה היא עושה |
|---|---|
| `docker volume ls` | רשימת ה-volumes |
| `docker volume create <name>` | יוצר volume |
| `docker volume rm <name>` | מוחק volume. **הנתונים שבו נמחקים** |
| `docker network ls` | רשימת הרשתות |
| `docker network create <name>` | יוצר רשת, שבה containers מוצאים זה את זה לפי שם |

---

## 5. מידע וניקוי

| פקודה | מה היא עושה |
|---|---|
| `docker version` | גרסת Docker, ובדיקה ש-Docker Desktop רץ |
| `docker info` | מידע מלא על ההתקנה |
| `docker system df` | כמה מקום תופסים images, containers ו-volumes |
| `docker container prune` | מוחק את כל ה-containers העצורים |
| `docker system prune` | מוחק containers עצורים, images בלי שם ורשתות לא בשימוש |
| `docker system prune -a --volumes` | **זהירות:** מוחק כמעט הכול, כולל volumes עם נתונים |
| `docker login <registry>` | התחברות ל-Registry (מפגשים 7–8) |

---

## שגיאות נפוצות

| הודעה | מה זה אומר | פתרון |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker Desktop לא רץ | להפעיל אותו ולחכות |
| `port is already allocated` | הפורט במחשב תפוס | `docker ps`, ואז `docker rm -f` או פורט אחר |
| `The container name "/web" is already in use` | כבר יש container בשם הזה, גם אם עצור | `docker rm -f web` |
| `pull access denied` / `not found` | שם image או תגית לא נכונים | לבדוק את השם ואת הגרסה |
| `unable to prepare context: ... Dockerfile` | אין Dockerfile בתיקייה | `cd` לתיקייה הנכונה, או `-f` |
