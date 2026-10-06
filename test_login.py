from database import authenticate_user

user = authenticate_user(
    "employee",
    "1234"
)

if user:
    print("LOGIN SUCCESS")
    print("Employee ID:", user["employee_id"])
    print("Name:", user["name"])
    print("Role:", user["role"])
else:
    print("LOGIN FAILED")