# בוחן — שיעור 3

15 שאלות על Docker Compose, Nginx ו-volumes. עונים לבד, בלי לחפש בחומר, ומגישים למורה לבדיקה.

## איך מגישים

כמו בשיעור הקודם, ישירות באתר של GitHub, בלי התקנות:

1. ב-**fork שלכן** ב-GitHub, לנווט לתיקייה `lessons/03-docker-compose/homework/`.
2. **Add file** ואז **Create new file**. שם הקובץ: `quiz-answers.md`.
3. להעתיק לתוכו את גיליון התשובות שבסוף העמוד, ולמלא.
4. **Commit changes**, עם ההודעה `quiz 3: answers`.

**מועד הגשה:** לפני תחילת שיעור 4.

---

**1. מה Docker Compose עושה?**
- א. בונה image אחד מ-Dockerfile
- ב. מריץ כמה containers יחד לפי קובץ אחד, ומחבר אותם לרשת משותפת
- ג. מעלה images ל-Docker Hub
- ד. מחליף את Docker

**2. ב-ShopList, עם מי הדפדפן מדבר?**
- א. עם כל ארבעת הסרוויסים
- ב. עם ה-backend ועם ה-frontend
- ג. רק עם Nginx, ב-frontend
- ד. רק עם postgres

**3. מה זה reverse proxy? הסבירי במשפט אחד.**

**4. ה-backend מתחבר למסד הנתונים עם `DB_HOST: postgres`. מה זה `postgres` כאן?**
- א. כתובת IP קבועה
- ב. שם ה-service בקובץ, ש-Compose הופך לכתובת ברשת המשותפת
- ג. שם המשתמש במסד הנתונים
- ד. שם ה-image

**5. בקשה מהדפדפן ל-`/api/products` מגיעה ל-backend. באיזה נתיב היא מגיעה, ולמה?**

**6. למה ל-backend אין `ports:` ב-`docker-compose.yml`?**

**7. מה ההבדל בין `docker compose down` ל-`docker compose down -v`?**

**8. עשיתן `docker compose down` ואז `docker compose up`. מה קרה למוצרים?**
- א. נמחקו
- ב. נשמרו, כי הם ב-volume
- ג. נשמרו, כי הם בתוך ה-container
- ד. תלוי בדפדפן

**9. למה `depends_on` לבד לא מספיק כדי שה-backend יחכה למסד הנתונים?**

**10. מתי רץ הקובץ `init.sql`?**
- א. בכל `docker compose up`
- ב. רק בהפעלה הראשונה, כשמסד הנתונים עוד ריק
- ג. בכל בקשה ל-backend
- ד. אף פעם, צריך להריץ אותו ידנית

**11. מה ההבדל בין `- postgres-data:/var/lib/postgresql/data` לבין `- ./init.sql:/docker-entrypoint-initdb.d/init.sql`?**

**12. עצרתן את stats עם `docker compose stop stats`. מה קורה ב-ShopList?**
- א. כל האפליקציה נופלת
- ב. רשימת המוצרים עובדת, רק תיבת הסטטיסטיקות לא זמינה
- ג. רק מסד הנתונים נופל
- ד. שום דבר לא משתנה

**13. ב-`docker-compose.yml` יש שגיאה, ו-Compose לא מוכן לעבוד. איזו פקודה תעזור למצוא אותה?**

**14. למה לא כדאי לכתוב סיסמאות ישירות ב-`docker-compose.yml`, ומה עושים במקום?**

**15. הריצו את ה-image של ה-frontend לבד עם `docker run`, והוא נפל מיד. למה?**

---

## גיליון תשובות (להעתיק לקובץ `quiz-answers.md`)

בשאלות אמריקאיות כותבים רק את האות. בשאלות הפתוחות, משפט או שניים.

```
# בוחן שיעור 3: <שם מלא>

1.
2.
3.
4.
5.
6.
7.
8.
9.
10.
11.
12.
13.
14.
15.
```
