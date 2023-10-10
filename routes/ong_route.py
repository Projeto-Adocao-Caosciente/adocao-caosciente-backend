from fastapi import APIRouter, Header

router = APIRouter(
    prefix="/ong",
    tags=['ongs_data']
)

@router.post("/")
async def create_ong(
    test_par: str,
    authorization: str = Header(None),
    status_code=200
):
    print(test_par)

@router.get("/")
async def read_ong(
    authorization: str = Header(None),
    status_code=200
):
    print("test")
