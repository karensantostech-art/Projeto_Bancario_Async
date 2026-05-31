from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, security


async def get_user_by_email(db: AsyncSession, email: EmailStr):
    result = await db.execute(select(models.User).filter(models.User.email == email))

    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_pwd = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_pwd)
    db.add(db_user)

    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_transaction(db: AsyncSession, transaction: schemas.TransactionCreate, user_id: int):
    db_transaction = models.Transaction(**transaction.model_dump(), user_id=user_id)
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise ValueError('Usuário não encontrado')

    if transaction.type == "deposito":
        user.balance += transaction.amount
    elif transaction.type == "saque":
        if user.balance < transaction.amount:
            raise ValueError('Saldo Insuficiente')
        user.balance -= transaction.amount

    db.add(db_transaction)
    db.add(user)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


async def get_transactions_by_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(models.Transaction).filter(models.Transaction.user_id == user_id))
    return result.scalars().all()


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user
