Installation:
1.Copy this repository( git pull)
2.Run docker-compose up --build
Usage:
Get database snapshot: http://127.0.0.1:8000/rates
Use api: http://localhost:8000/get-price?d={date}&t={cargo_type}&p={declared price}
You will get insurance price if date/cargo type combination exist in db or 404 error if not.