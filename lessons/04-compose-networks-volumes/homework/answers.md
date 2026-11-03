תשובות לשיעור 4

1.
stats מגיע ל-backend דרך הרשת ש-Compose יוצר, לפי השם של ה-service: http://backend:5000. בתוך הרשת השם backend מתורגם לכתובת של ה-container, אז לא צריך ports בשביל זה. ports צריך רק כדי לפתוח פורט החוצה למחשב.
הדפדפן לא מגיע ל-backend ישירות. הוא פונה ל-frontend ב-localhost:8080/api, ו-nginx מעביר את הבקשה הלאה ל-backend.

2.
אחרי down ו-up המוצרים נשארו, כי הנתונים של postgres שמורים ב-named volume (postgres-data), ו-down מוחק רק את ה-containers ואת הרשת.
עם down -v נמחק גם ה-volume, ואז כל המוצרים נעלמים. ב-up הבא המסד נוצר מחדש ריק ו-init.sql רץ שוב.

3.
זה bind mount. רואים את זה כי בצד השמאלי יש נתיב לקובץ במחשב (מתחיל ב-../) ולא שם של volume.
אם משנים את init.sql אחרי שהמסד כבר נוצר, זה לא ישפיע, כי postgres מריץ את הקובץ רק בפעם הראשונה כשאין עדיין נתונים. כדי שהשינוי ייכנס צריך down -v ואז up, וזה מוחק את הנתונים.

4.
הרשת נקראת docker_default וה-volume נקרא docker_postgres-data.
Compose מוסיף לפני כל שם את שם הפרויקט, ושם הפרויקט הוא השם של התיקייה שבה נמצא קובץ ה-compose, אצלי docker. default זה השם של הרשת ש-Compose יוצר לבד, ו-postgres-data זה השם שנתתי ל-volume בקובץ.

5.
ב-image הסופי יש רק nginx, את הקבצים שנבנו בתיקייה dist (index.html, app.js, style.css) ואת nginx.conf. אין בו node, אין את build.js ואין את קבצי המקור, הם נשארו בשלב הראשון.
אין CMD כי הוא יורש את ה-CMD של nginx מה-image הבסיסי, ובשלב הראשון לא צריך CMD כי אף אחד לא מריץ אותו, הוא רק בונה.
ל-stats לא צריך multi-stage כי אין לו שלב בנייה, ובכל מקרה הוא צריך node גם כשהוא רץ, אז אין מה להשאיר בחוץ.

6.
single: 101MB, multi: 101MB, kitchen: 244MB.
multi כמעט באותו גודל כמו single כי שניהם בנויים על nginx:1.30-alpine עם עוד כמה קבצים קטנים. node, שהוא מה שעושה את kitchen גדול, לא נכנס ל-image הסופי.

7.
nginx בוחר את ה-location עם הקידומת הכי ארוכה שמתאימה. /api/stats יותר ארוך ויותר ספציפי מ-/api/, אז הבקשה הולכת ל-stats.
בגלל הלוכסן בסוף http://backend:5000/ החלק /api/ מוחלף ב-/, אז /api/products מגיע ל-backend בתור /products. זה חשוב כי ב-backend הנתיבים הם בלי /api, ובלי הלוכסן היינו מקבלים 404.
