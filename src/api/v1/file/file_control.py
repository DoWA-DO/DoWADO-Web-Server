# file_control.py

import datetime
import logging
import os
import secrets
from typing import List
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/file", tags=["파일 업로드"])

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR,'static/')
IMG_DIR = os.path.join(STATIC_DIR,'images/')
SERVER_IMG_DIR = os.path.join('http://localhost:8000/','static/','images/')
     
# 이미지 저장 폴더 생성 (없는 경우)
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)
    
@router.post('/upload')
async def upload_board(in_files: List[UploadFile] = File(...)):
    file_urls=[]
    for file in in_files:
        currentTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        saved_file_name = ''.join([currentTime,secrets.token_hex(16)])
        print(saved_file_name)
        file_location = os.path.join(IMG_DIR,saved_file_name)
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        file_urls.append(SERVER_IMG_DIR+saved_file_name)
    result={'fileUrls' : file_urls}
    logger.info(f"{file_urls}에 이미지 업로드가 완료되었습니다.")
    return result

@router.get('/images/{file_name}')
def get_image(file_name:str):
    return FileResponse(''.join([IMG_DIR,file_name]))

'''
# File을 그냥 Optional로 지정했음
async def upload_image(file: UploadFile | None = File(None)):
    """
    이미지 업로드 테스트
    - 1. 클라이언트에서 서버로 이미지를 업로드한다.
    - 2. 이미지 확장자가 업로드 가능한지 확인한다.
    - 3. 이미지 사이즈가 업로드 가능한 크기인지 확인한다.
    - 4. 이미지 이름을 변경한다.
    - 5. 이미지를 최적화하여 저장한다.
    """
    if not file:
        raise HTTPException(status_code=400, detail="이미지가 제공되지 않았습니다.")
 
    file = await images.validate_image_type(file)
    file = await images.validate_image_size(file)
    file = images.change_filename(file)
    filename = file.filename
    image = images.resize_image(file)
    image = images.save_image_to_filesystem(image, f"./{filename}")
    return {"detail": "이미지 업로드 성공"}
 
ImageUploader = Annotated[dict, Depends(upload_image)]
 
@router.post("/upload")
async def upload_image(image: dict):
    return image
    '''