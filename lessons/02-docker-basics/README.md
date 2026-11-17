# שיעור 2: Docker: images, containers ו-Dockerfile

## מה לומדות בשיעור

- למה containers, ומה ההבדל בינם לבין מכונה וירטואלית
- image מול container: מתכון ועוגה
- הרצת container ראשון: `docker run`, `-p`, `ps`, `logs`
- כתיבת Dockerfile ל-backend (Python) ול-stats (Node.js)
- layer caching: למה הסדר בקובץ משנה
- למה stats לבד לא מספיק, ולמה צריך את Docker Compose (שיעור 3)

## התרגילים

1. container ראשון: Nginx על פורט 8080 (בהרצאה)
2. לשבור ולתקן את ה-Dockerfile ולראות CACHED
3. להריץ את stats לבד ולראות 502
4. בונוס: להיכנס לתוך container עם `docker exec`
5. תרגול פקודות: [commands-practice.md](commands-practice.md)

## שיעורי בית

[homework.md](homework.md): לכתוב Dockerfile לסרוויס חדש ולהגיש את הבוחן, ישירות ב-GitHub. בלי התקנות בבית.

## הקבצים בתיקייה

| קובץ | מה יש בו |
|---|---|
| [guide.md](guide.md) | מדריך שלב אחר שלב |
| [exercises.md](exercises.md) | תרגילים |
| [docker-commands.md](docker-commands.md) | מדריך פקודות Docker עם הסברים ודוגמאות |
| [dockerfile-reference.md](dockerfile-reference.md) | מדריך תחביר Dockerfile: כל ההוראות |
| [commands-practice.md](commands-practice.md) | תרגול פקודות Docker: על דף ובמחשב |
| [quiz.md](quiz.md) | **בוחן להגשה** על שיעורים 1 ו-2 |
| [homework.md](homework.md) | **שיעורי בית:** Dockerfile לסרוויס greeter, דרך GitHub |
