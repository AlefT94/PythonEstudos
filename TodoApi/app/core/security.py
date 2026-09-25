from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash

# 1. Configuração do algoritmo de Hashing de Senhas
password_hash = PasswordHash.recommended()

# 2. Configurações do JWT
SECRET_KEY = "sua_chave_secreta_super_forte_para_desenvolvimento_troque_em_producao"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha em texto plano em um hash unidirecional seguro com bcrypt."""
    return password_hash.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Valida se a senha digitada no login confere com o hash salvo no banco."""
    return password_hash.verify(senha_plana, senha_hash)


def criar_token_acesso(dados: dict, tempo_expiracao: timedelta | None = None) -> str:
    """Gera um JWT assinado contendo os dados (claims) e tempo de validade."""
    payload = dados.copy()
    agora = datetime.now(timezone.utc)

    if tempo_expiracao:
        expira = agora + tempo_expiracao
    else:
        expira = agora + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload.update({"exp": expira, "iat": agora})
    token_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt