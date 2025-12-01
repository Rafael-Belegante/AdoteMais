from sqlalchemy.orm import Session

from app.models.log_auditoria import LogAuditoria


def registrar_log(
    db: Session,
    id_usuario: int | None,
    acao: str,
    detalhe: str | None = None,
) -> LogAuditoria:
    """
    Registra ação na auditoria.
    """
    log = LogAuditoria(
        id_usuario=id_usuario,
        acao=acao,
        detalhe=detalhe,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def listar_logs(db: Session, id_usuario: int | None = None) -> list[LogAuditoria]:
    """
    Lista logs, opcionalmente filtrando por usuário.
    """
    query = db.query(LogAuditoria).order_by(LogAuditoria.data_hora.desc())
    if id_usuario is not None:
        query = query.filter(LogAuditoria.id_usuario == id_usuario)
    return query.all()
