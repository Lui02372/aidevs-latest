"""
uvicorn 00_request:app --reload
"""


from fastapi import FastAPI, HTTPException
from mymodels import Customer, CustomerDetail, ApiResponse


app = FastAPI(
    title = "Request Test",
    description = "request test",
    version = "0.1"
)


@app.get("/health")
async def health():
    response = ApiResponse(
        success=True,
        message="OK",
    )
    return response

# Request Body
# insert, update
@app.put("/update")
async def update(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    if customer.id == "id88":
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    await print("수정 진행 ...")
    response = ApiResponse(
        success = True,
        message = f"{customer.name} 수정 완료!",
        data = customer
    )
    return response
@app.post("/register")
async def register(customer:Customer):
    print(customer.id)
    print(customer.name)
    print(customer.age)
    response = None
    await response = ApiResponse(
        success = True,
        message = f"{customer.name} 가입축하!",
    )
    return response

# Path Paramter
# 127.0.0.1:8000/get/id01
# get , delete
@app.delete("/delete/{input_id}")
async def delete(input_id : str):
    if input_id == "id99":
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    await print("삭제처리 완료")
    response = ApiResponse(
        success = True,
        message = "정상삭제",
        data =  None
    )
    return response

@app.get("/get/{input_id}")
async def get(input_id : str):
    if input_id != "id01":
        # return "없어요"
        raise HTTPException(status_code=404, detail="ID가 존재 안함")
    customer_data = None
    await customer_data = {
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
@app.get("/search")
async def search(
    id : str | None = None,
    name : str | None = None,
    age : int | None = None,
):
    print(f"{id}로 검색 합니다.")
    print(f"{name}로 검색 합니다.")
    print(f"{age}로 검색 합니다.")
    customers = None
    await customers = [
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

