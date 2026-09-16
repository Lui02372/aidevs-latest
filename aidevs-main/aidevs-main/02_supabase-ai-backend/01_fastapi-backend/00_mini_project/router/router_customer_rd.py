"""
uvicorn 00_request:app --reload
"""


from fastapi import APIRouter, HTTPException
from scheme.model_common import ApiResponse
from scheme.model_customer import Customer, CustomerDetail

router_rd = APIRouter()

# Path Paramter
# 127.0.0.1:8000/get/id01
# get , delete
@router_rd.delete("/delete/{input_id}")
async def delete(input_id : str):
    if input_id == "id99":
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    # await print("삭제처리 완료")
    response = ApiResponse(
        success = True,
        message = "정상삭제",
        data =  None
    )
    return response

@router_rd.get("/get/{input_id}")
async def get(input_id : str):
    if input_id != "id01":
        # return "없어요"
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    customer_data = {
        "id":"id01",
        "pwd":"xsfafdsa",
        "name":"james",
        "age":20
    }
    response = ApiResponse(
        success = True,
        message = "정상조회",
        data =  CustomerDetail( 
                    id=customer_data["id"],
                    name=customer_data["name"],
                    age=customer_data["age"],
        )
    )
    return response


# Query Parameter
# 검색
@router_rd.get("/search")
async def search(
    id : str | None = None,
    name : str | None = None,
    age : int | None = None,
):
    print(f"{id}로 검색 합니다.")
    print(f"{name}로 검색 합니다.")
    print(f"{age}로 검색 합니다.")
    customers = [
        {
            "id" : "id01",
            "name" : "name1",
            "age" : 10
        },
        {
            "id" : "id02",
            "name" : "name2",
            "age" : 20
        },
        {
            "id" : "id03",
            "name" : "name3",
            "age" : 30
        },
    ]

    response = ApiResponse(
        success = True,
        message = "정상조회",
        data =  customers
    )
    return response

