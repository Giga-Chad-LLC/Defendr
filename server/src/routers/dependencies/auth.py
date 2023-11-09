import bcrypt
import mysql.connector
from fastapi import Header, HTTPException
from server.src.db.connection import get_connection



def require_auth(x_email: str = Header(None), x_password: str = Header(None)):
    # Access x_email and x_password here
    print(f"x_email={x_email}, x_password={x_password}")

    if not x_email or not x_password:
        raise HTTPException(status_code=400, detail="Missing required auth headers")

    connection = get_connection()
    cursor = connection.cursor()

    try:
        query = "SELECT email, password, is_admin FROM users WHERE email = %s;"

        cursor.execute(query, (x_email,))

        row = cursor.fetchone()

        # email must be correct
        if cursor.rowcount <= 0:
            raise HTTPException(status_code=403, detail="Auth email is incorrect")

        _, hashed_password, is_admin = row

        # password must be correct
        if not bcrypt.checkpw(x_password.encode(), hashed_password.encode()):
            raise HTTPException(status_code=403, detail="Auth password is incorrect")

        # user must be an admin
        if not is_admin:
            raise HTTPException(status_code=403, detail="Unpriviledged user")

    except mysql.connector.Error as err:
        print(err)
        raise HTTPException(status_code=500, detail=f"Something went wrong: {err}")
    finally:
        cursor.close()
