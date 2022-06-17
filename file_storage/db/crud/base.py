"""Base CRUD classes."""
from abc import ABCMeta, abstractmethod
from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from file_storage.db.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
DeleteSchemaType = TypeVar("DeleteSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        ReadSchemaType,
        UpdateSchemaType,
        DeleteSchemaType,
    ],
    metaclass=ABCMeta,
):
    """Base CRUD class with usefull methods."""

    @property
    @abstractmethod
    def model(self) -> Type[Base]:
        """Abstract get model, need to implement."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        limit: int = 10,
        offset: int = 0,
    ) -> list[ModelType]:
        """
        Get all entry models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of model objects.
        """
        raw_objects = await self.session.execute(
            select(self.model).limit(limit).offset(offset),
        )
        return raw_objects.scalars().fetchall()

    async def create(
        self,
        obj_in: CreateSchemaType,
    ) -> CreateSchemaType:
        """Create model in DB."""
        db_obj = self.model(**obj_in.dict())
        self.session.add(db_obj)
        await self.session.flush()
        return obj_in
