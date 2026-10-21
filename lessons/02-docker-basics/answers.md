1. docker build -t greeter:v1 app/greeter
2. docker run -p 9000:5000 greeter
3. -e GREETING="shalom"
4. {'messege' : 'shalom, Rivka!'}
5. התקנת התלויות תסומן כCACHED כי היא לא השתנתה ונכתבה בהתחלה של הDockerfile, הקוד הוא שהשתנה וירוץ מחדש.
