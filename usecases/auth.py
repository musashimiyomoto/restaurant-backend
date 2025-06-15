import random
import smtplib
from datetime import UTC, datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from fastapi import HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from enums.auth import AuthTypeEnum
from enums.role import UserRoleEnum
from repositories import ClientRepository, UserRepository
from schemas import ClientCreateSchema, ClientResponseSchema, TokenSchema, admin
from settings import auth_settings, smtp_settings
from utils import crypto, redis


class BaseAuthUsecase:
    def __init__(self):
        self._credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or user is inactive",
            headers={"WWW-Authenticate": auth_settings.token_type},
        )

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify the password.

        Args:
            plain_password: The plain password.
            hashed_password: The hashed password.

        Returns:
            True if the password is valid, False otherwise.

        """
        return crypto.pwd_context.verify(secret=plain_password, hash=hashed_password)

    @staticmethod
    def _get_password_hash(password: str) -> str:
        """Get the password hash.

        Args:
            password: The password.

        Returns:
            The password hash.

        """
        return crypto.pwd_context.hash(secret=password)

    @staticmethod
    def _create_access_token(
        data: dict,
        expires_delta: timedelta | None = None,
        is_user: bool = False,
    ) -> str:
        """Create an access token.

        Args:
            data: The data to encode.
            expires_delta: The expiration time.
            is_user: Whether the token is for a user.

        Returns:
            The access token.

        """
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(tz=UTC) + expires_delta
        else:
            expire = datetime.now(tz=UTC) + timedelta(
                minutes=auth_settings.access_token_expire_minutes
            )

        to_encode.update({"exp": expire})

        return jwt.encode(
            claims=to_encode,
            key=auth_settings.user_secret_key if is_user else auth_settings.secret_key,
            algorithm=auth_settings.algorithm,
        )

    def _get_payload(self, token: str, is_user: bool = False) -> dict:
        """Get the payload from the token.

        Args:
            token: The token.
            is_user: Whether the token is for a user.

        Returns:
            The payload.

        """
        try:
            payload = jwt.decode(
                token=token,
                key=(
                    auth_settings.user_secret_key
                    if is_user
                    else auth_settings.secret_key
                ),
                algorithms=[auth_settings.algorithm],
            )
            return payload
        except JWTError:
            raise self._credentials_exception

    @staticmethod
    def _generate_code() -> str:
        """Generate a code.

        Returns:
            The code.

        """
        return str(random.randint(100000, 999999))


class ClientAuthUsecase(BaseAuthUsecase):
    def __init__(self):
        super().__init__()
        self._client_repository = ClientRepository()

    async def _authenticate(
        self,
        session: AsyncSession,
        email: str | None,
        telegram_id: int | None,
        password: str,
    ) -> ClientResponseSchema | bool:
        """Authenticate a client.

        Args:
            session: The session.
            email: The email.
            telegram_id: The telegram ID.
            password: The password.

        Returns:
            The client.

        """
        if email:
            client = await self._client_repository.get_by(session=session, email=email)
        elif telegram_id:
            client = await self._client_repository.get_by(
                session=session, telegram_id=telegram_id
            )
        else:
            raise self._credentials_exception

        if not client:
            return False

        if not self._verify_password(
            plain_password=password, hashed_password=client.hashed_password
        ):
            return False

        return ClientResponseSchema.model_validate(client)

    async def get_current(
        self, session: AsyncSession, token: str
    ) -> ClientResponseSchema:
        """Get the current client.

        Args:
            session: The session.
            token: The token.

        Returns:
            The current client.

        """
        payload = self._get_payload(token=token)
        sub, sub_type = payload.get("sub"), payload.get("sub_type")

        if sub is None or sub_type is None:
            raise self._credentials_exception

        if sub_type == AuthTypeEnum.EMAIL.value:
            client = await self._client_repository.get_by(session=session, email=sub)
        elif sub_type == AuthTypeEnum.TELEGRAM_ID.value:
            client = await self._client_repository.get_by(
                session=session, telegram_id=sub
            )
        else:
            raise self._credentials_exception

        if client is None:
            raise self._credentials_exception
        if not client.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )

        return ClientResponseSchema.model_validate(client)

    async def login(
        self,
        session: AsyncSession,
        email: str | None,
        telegram_id: int | None,
        password: str,
    ) -> TokenSchema:
        """Login a client.

        Args:
            session: The session.
            email: The email.
            telegram_id: The telegram ID.
            password: The password.

        Returns:
            The token.

        """
        client = await self._authenticate(
            session=session,
            email=email,
            telegram_id=telegram_id,
            password=password,
        )

        if not client:
            raise self._credentials_exception

        if client.email:
            sub = client.email
            sub_type = AuthTypeEnum.EMAIL.value
        elif client.telegram_id:
            sub = client.telegram_id
            sub_type = AuthTypeEnum.TELEGRAM_ID.value
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Client has no email or telegram ID",
            )

        await self._client_repository.update_by(
            session=session,
            data={"last_login": datetime.now(tz=UTC)},
            id=client.id,
        )

        return TokenSchema(
            access_token=self._create_access_token(
                data={"sub": sub, "sub_type": sub_type},
                expires_delta=timedelta(
                    minutes=auth_settings.access_token_expire_minutes
                ),
            ),
            token_type=auth_settings.token_type,
        )

    async def register(
        self, session: AsyncSession, data: ClientCreateSchema
    ) -> ClientResponseSchema:
        """Register a client.

        Args:
            session: The session.
            data: The data.

        Returns:
            The client.

        """
        if data.email and await self._client_repository.get_by(
            session=session, email=data.email
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        if data.telegram_id and await self._client_repository.get_by(
            session=session, telegram_id=data.telegram_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Telegram ID already registered",
            )

        return ClientResponseSchema.model_validate(
            await self._client_repository.create(
                session=session,
                data={
                    **data.model_dump(exclude_none=True, exclude={"password"}),
                    "hashed_password": self._get_password_hash(password=data.password),
                    "is_active": True,
                },
            )
        )


class UserAuthUsecase(BaseAuthUsecase):
    def __init__(self):
        super().__init__()
        self._user_repository = UserRepository()

    async def _authenticate(
        self, session: AsyncSession, email: str, password: str
    ) -> admin.UserResponseSchema | bool:
        """Authenticate a user.

        Args:
            session: The session.
            email: The email.
            password: The password.

        Returns:
            The user.

        """
        user = await self._user_repository.get_by(session=session, email=email)

        if not user or not user.is_active:
            return False

        if not self._verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return False

        return admin.UserResponseSchema.model_validate(user)

    async def _get_user_by_email(
        self, session: AsyncSession, email: str
    ) -> admin.UserResponseSchema:
        """Get a user by email.

        Args:
            session: The session.
            email: The email.

        Returns:
            The user.

        """
        user = await self._user_repository.get_by(session=session, email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
            )

        return admin.UserResponseSchema.model_validate(user)

    async def _check_code(self, email: str, code: str) -> bool:
        """Check the code.

        Args:
            email: The email.
            code: The code.

        Returns:
            True if the code is valid, False otherwise.

        """
        return await redis.get_verify_code(identifier=email) == code

    async def get_current(
        self, session: AsyncSession, token: str
    ) -> admin.UserResponseSchema:
        """Get the current user.

        Args:
            session: The session.
            token: The token.

        Returns:
            The current user.

        """
        payload = self._get_payload(token=token, is_user=True)
        email = payload.get("sub")

        if email is None:
            raise self._credentials_exception

        user = await self._user_repository.get_by(session=session, email=email)

        if not user or not user.is_active:
            raise self._credentials_exception

        return admin.UserResponseSchema.model_validate(user)

    async def login(
        self, session: AsyncSession, email: str, password: str
    ) -> TokenSchema:
        """Login a user.

        Args:
            session: The session.
            email: The email.
            password: The password.

        Returns:
            The token.

        """
        user = await self._authenticate(
            session=session,
            email=email,
            password=password,
        )

        if not user:
            raise self._credentials_exception

        return TokenSchema(
            access_token=self._create_access_token(
                data={"sub": user.email},
                expires_delta=timedelta(
                    minutes=auth_settings.access_token_expire_minutes
                ),
                is_user=True,
            ),
            token_type=auth_settings.token_type,
        )

    async def register(
        self,
        data: admin.UserCreateSchema,
        role: UserRoleEnum,
        session: AsyncSession,
        parent_id: int | None = None,
        is_active: bool = False,
    ) -> admin.UserResponseSchema:
        """Register a user.

        Args:
            data: The data.
            role: The role.
            session: The session.
            parent_id: The parent ID.
            is_active: Whether the user is active.

        Returns:
            The user.

        """
        if await self._user_repository.get_by(session=session, email=data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        return admin.UserResponseSchema.model_validate(
            await self._user_repository.create(
                session=session,
                data={
                    **data.model_dump(exclude_none=True, exclude={"password"}),
                    "hashed_password": self._get_password_hash(password=data.password),
                    "is_active": is_active,
                    "role": role,
                    "parent_id": parent_id,
                },
            )
        )

    async def send_email_code(self, session: AsyncSession, email: str) -> None:
        """Send an email code.

        Args:
            session: The session.
            email: The email.

        """
        user = await self._get_user_by_email(session=session, email=email)

        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User is active"
            )

        code = self._generate_code()
        await redis.set_verify_code(identifier=user.email, code=code)

        html = (
            "<html><body><p>Код, который следует скопировать и испольовать для авторизации:"
            f"</p><h3>{code}</h3><p>Это письмо отправил робот, который не проверяет входящую"
            " почту</p></body></html>"
        )

        message = MIMEMultipart()
        message["Subject"] = "Ваш код для верификации"
        message["From"] = smtp_settings.username
        message["To"] = user.email
        message.attach(payload=MIMEText(html, "html"))

        with smtplib.SMTP_SSL(
            host=smtp_settings.host, port=smtp_settings.port
        ) as server:
            server.login(user=smtp_settings.username, password=smtp_settings.password)
            server.sendmail(
                from_addr=smtp_settings.username,
                to_addrs=user.email,
                msg=message.as_string(),
            )

    async def verify_email(self, email: str, code: str, session: AsyncSession) -> None:
        """Verify an email.

        Args:
            email: The email.
            code: The code.
            session: The session.

        """
        user = await self._get_user_by_email(session=session, email=email)

        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User is active"
            )

        if not await self._check_code(email=user.email, code=code):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code"
            )

        await self._user_repository.update_by(
            session=session,
            data={"is_active": True},
            id=user.id,
        )
