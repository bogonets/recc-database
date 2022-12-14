# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Optional


@dataclass
class Role:
    """It is mapped to the `role` table in the database."""

    uid: Optional[int] = None
    slug: Optional[str] = None

    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None

    hidden: Optional[bool] = None
    lock: Optional[bool] = None

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class RoleA:
    # Role Table
    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    # RolePermission and Permission Table
    permissions: Optional[List[str]] = None


@dataclass
class CreateRoleQ:
    # Role Table
    slug: str
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None

    # RolePermission and Permission Table
    permissions: Optional[List[str]] = None

    def normalize_booleans(self) -> None:
        self.hidden = True if self.hidden else False
        self.lock = True if self.lock else False


@dataclass
class UpdateRoleQ:
    # Role Table
    slug: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    extra: Optional[Any] = None
    hidden: Optional[bool] = None
    lock: Optional[bool] = None

    # RolePermission and Permission Table
    permissions: Optional[List[str]] = None
