from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    email: EmailStr
    age: int = Field(gt=0, lt=120)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None

users = [
    {"id": 1, "name": "Alex", "email": "alex@gmail.com", "age": 21},
    {"id": 2, "name": "Maks", "email": "john@gmail.com", "age": 18},
    {"id": 3, "name": "Oleg", "email": "john@gmail.com", "age": 27},
    {"id": 5, "name": "Vasya", "email": "john@gmail.com", "age": 19},
    {"id": 6, "name": "Stas", "email": "john@gmail.com", "age": 10},
    {"id": 7, "name": "Sasha", "email": "john@gmail.com", "age": 27},
    {"id": 8, "name": "Misha", "email": "john@gmail.com", "age": 37},
    {"id": 9, "name": "John", "email": "john@gmail.com", "age": 57},
]


@app.get("/users", response_model=list[User])
def get_users():
    return users

@app.get("/users/search")
def search_users(name: str | None = None, min_age: int | None = None):
    result = []

    for u in users:

        if name and name.lower() not in u["name"].lower():
            continue

        if min_age and u["age"] < min_age:
            continue

        result.append(u)

    return result

@app.get("/users/limit_offset")
def limit_offset(
        limit: Optional[int] = Query(default=10, gt=0, le=1000),
        offset: Optional[int] = Query(default=10, gt=0, le=1000)):

    return users[offset:offset + limit]




@app.post("/users")
def create_user(user: UserCreate):
    new_id = max(u["id"] for u in users) + 1 if users else 1

    new_user = {
        "id": new_id,
        "name": user.name,
        "email": user.email,
        "age": user.age
    }

    users.append(new_user)

    return new_user


@app.get("/users/{id_user}", response_model=User)
def get_user(id_user: int):
    for user in users:
        if user.get("id") == id_user:
            return user

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
def delete_user(user_id: int) -> Dict[str, str]:
    for i, u in enumerate(users):
        if u["id"] == user_id:
            users.pop(i)
            return {"message": "User deleted"}

    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
def user_update(user_id: int, new_user: UserCreate) -> Optional[UserCreate]:
    for u in users:
        if u["id"] == user_id:
            u.update(new_user.model_dump())
            return UserCreate(**u)

        else: raise HTTPException(status_code=404, detail="User not found")



@app.patch("/users/{user_id}")
def patch_user(user_id: int, new_user: UserUpdate):

    for u in users:
        if u["id"] == user_id:
            u.update(new_user.model_dump(exclude_unset=True))

            return u

    raise HTTPException(status_code=404, detail="User not found")



