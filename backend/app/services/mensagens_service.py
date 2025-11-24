from sqlalchemy.orm import Session
from app.models.mensagem import Mensagem
from app.schemas.mensagem import MensagemCreate

def criar_mensagem(db: Session, data: MensagemCreate) -> Mensagem:
    msg = Mensagem(
        assunto=data.assunto,
        mensagem=data.mensagem,
        telefone=data.telefone,
        email_remetente=data.email_remetente,
        nome_remetente=data.nome_remetente,
        id_ong=data.id_ong,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg
