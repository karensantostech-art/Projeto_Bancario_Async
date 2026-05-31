from fastapi import FastAPI, Depends, HTTPException, status
from pydantic.v1 import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, models, schemas, database, security
from app.database import get_db
from contextlib import asynccontextmanager
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(title='Sistema Bancário Async', lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Não foi possível validar as credenciais", headers={"WWW-Authenticate": "Bearer"},)
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await crud.get_user_by_email(db, email=EmailStr(email))
    if user is None:
        raise credentials_exception
    return user


@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    return await crud.create_user(db=db, user=user)


@app.post("/transactions/", response_model=schemas.Transaction)
async def create_transaction(transaction: schemas.TransactionCreate, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return await crud.create_transaction(db=db, transaction=transaction, user_id=current_user.id)

@app.get("/users/transactions/", response_model=list[schemas.Transaction])
async def read_transactions(current_user: models.User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    transactions = await crud.get_transactions_by_user(db, user_id=current_user.id)
    return transactions


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await crud.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha incorretos", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
