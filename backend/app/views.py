from fastapi import APIRouter, Request
from app.services.medical_facility_service import find_medical_facilities
from app.services.drug_info_service import get_drug_info

router = APIRouter()

@router.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    user_message = data.get('message')
    
    if "医療機関を知りたい" in user_message:
        response = await find_medical_facilities(user_message)
    elif "薬について聞きたい" in user_message:
        response = await get_drug_info(user_message)
    else:
        response = "すみません、理解できませんでした。"
    
    return {"reply": response}
