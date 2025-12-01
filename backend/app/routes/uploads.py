import os
import uuid
from io import BytesIO

from fastapi import APIRouter, UploadFile, File, HTTPException, status
from PIL import Image

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# maior lado da imagem final (em px)
TARGET_MAX_SIDE = 800  # todas as imagens terão o maior lado = 800px
MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB brutos de upload


@router.post("/foto-animal")
async def upload_foto_animal(file: UploadFile = File(...)):
    # valida tipo MIME
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Arquivo deve ser uma imagem",
        )

    # lê conteúdo bruto
    contents = await file.read()

    # limite bruto pra não aceitar porcaria gigante
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Imagem muito grande (máx. 2MB)",
        )

    try:
        # abre a imagem com Pillow
        img = Image.open(BytesIO(contents))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível ler a imagem enviada",
        )

    # converte para RGB (garante compatibilidade com JPEG)
    if img.mode != "RGB":
        img = img.convert("RGB")

    # normaliza tamanho:
    # escala proporcionalmente para que o MAIOR lado seja exatamente TARGET_MAX_SIDE
    w, h = img.size
    max_side = max(w, h)

    if max_side != TARGET_MAX_SIDE:
        scale = TARGET_MAX_SIDE / float(max_side)
        new_size = (int(w * scale), int(h * scale))
        img = img.resize(new_size, Image.LANCZOS)

    # gera nome único .jpg
    filename = f"{uuid.uuid4().hex}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)

    # salva como JPEG otimizado
    try:
        img.save(filepath, format="JPEG", quality=85, optimize=True)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao salvar imagem processada",
        )

    # retorna URL relativa servida pelo /media
    return {"url": f"/media/{filename}"}
