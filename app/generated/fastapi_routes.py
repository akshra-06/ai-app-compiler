
from fastapi import APIRouter, Body

router = APIRouter()


@router.post("/login")
def post_login(
    payload: dict = Body(default={})
):
    return {
        "message": "Login successful",
        "token": "demo-jwt-token"
    }


contacts_db = [
    {
        "id": 1,
        "first_name": "Akshra",
        "last_name": "Ahuja",
        "email": "akshra@test.com"
    },
    {
        "id": 2,
        "first_name": "Rahul",
        "last_name": "Sharma",
        "email": "rahul@test.com"
    }
]


@router.get("/contacts")
def get_contacts():

    return {
        "contacts": contacts_db
    }


@router.post("/contacts")
def post_contacts(
    payload: dict = Body(default={})
):

    new_contact = {
        "id": len(contacts_db) + 1,
        "first_name": payload.get("first_name"),
        "last_name": payload.get("last_name"),
        "email": payload.get("email")
    }

    contacts_db.append(
        new_contact
    )

    return {
        "message": "Contact created",
        "contact": new_contact
    }


@router.get("/subscriptions")
def get_subscriptions():

    return {
        "subscriptions": []
    }


@router.get("/analytics")
def get_analytics():

    return {
        "users": 10,
        "revenue": 5000
    }
