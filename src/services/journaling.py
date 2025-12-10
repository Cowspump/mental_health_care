"""
Service layer for journaling functionality.
Contains business logic for journal entries management.
"""
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional

from sqlalchemy import and_, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.journal import JournalEntry
from src.schemas.journaling import JournalEntryCreate, JournalEntryUpdate


class JournalingService:
    """
    Service class for journal entries business logic.
    Handles CRUD operations and statistics for journal entries.
    """

    def __init__(self, db: AsyncSession):
        """Initialize service with database session."""
        self.db = db

    async def create_entry(
            self,
            user_id: str,
            entry_data: JournalEntryCreate
    ) -> JournalEntry:
        """
        Create a new journal entry for the user.

        Args:
            user_id: ID of the user creating the entry
            entry_data: Entry data from the request

        Returns:
            Created journal entry
        """
        # Создаём новую запись в журнале
        db_entry = JournalEntry(
            user_id=user_id,
            **entry_data.model_dump()
        )

        self.db.add(db_entry)
        await self.db.commit()
        await self.db.refresh(db_entry)

        return db_entry

    async def get_entry(
            self,
            user_id: str,
            entry_id: str
    ) -> Optional[JournalEntry]:
        """
        Get a specific journal entry by ID.
        Ensures the entry belongs to the user.

        Args:
            user_id: ID of the user
            entry_id: ID of the entry to retrieve

        Returns:
            Journal entry if found and belongs to user, None otherwise
        """
        result = await self.db.execute(
            select(JournalEntry).where(
                and_(
                    JournalEntry.id == entry_id,
                    JournalEntry.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_user_entries(
            self,
            user_id: str,
            skip: int = 0,
            limit: int = 100,
            from_date: Optional[date] = None,
            to_date: Optional[date] = None,
            tags: Optional[str] = None
    ) -> List[JournalEntry]:
        """
        Get paginated list of user's journal entries with optional filtering.

        Args:
            user_id: ID of the user
            skip: Number of entries to skip (pagination)
            limit: Maximum number of entries to return
            from_date: Filter entries from this date
            to_date: Filter entries to this date
            tags: Filter by tags (comma-separated)

        Returns:
            List of journal entries
        """
        # Строим запрос с фильтрами
        query = select(JournalEntry).where(JournalEntry.user_id == user_id)

        # Добавляем фильтр по датам
        if from_date:
            query = query.where(JournalEntry.entry_date >= from_date)
        if to_date:
            query = query.where(JournalEntry.entry_date <= to_date)

        # Добавляем фильтр по тегам (простой поиск подстроки)
        if tags:
            query = query.where(JournalEntry.tags.like(f"%{tags}%"))

        # Сортировка по дате записи (новые сначала)
        query = query.order_by(desc(JournalEntry.entry_date))

        # Пагинация
        query = query.offset(skip).limit(limit)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_entry(
            self,
            user_id: str,
            entry_id: str,
            update_data: JournalEntryUpdate
    ) -> Optional[JournalEntry]:
        """
        Update an existing journal entry.

        Args:
            user_id: ID of the user
            entry_id: ID of the entry to update
            update_data: Updated entry data

        Returns:
            Updated entry if found and belongs to user, None otherwise
        """
        # Получаем запись
        entry = await self.get_entry(user_id, entry_id)
        if not entry:
            return None

        # Обновляем только переданные поля
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(entry, field, value)

        # Обновляем timestamp
        entry.updated_at = datetime.utcnow()

        await self.db.commit()
        await self.db.refresh(entry)

        return entry

    async def delete_entry(
            self,
            user_id: str,
            entry_id: str
    ) -> bool:
        """
        Delete a journal entry.

        Args:
            user_id: ID of the user
            entry_id: ID of the entry to delete

        Returns:
            True if entry was deleted, False if not found
        """
        entry = await self.get_entry(user_id, entry_id)
        if not entry:
            return False

        await self.db.delete(entry)
        await self.db.commit()

        return True

    async def get_user_stats(self, user_id: str) -> Dict:
        """
        Get statistics for user's journal entries.

        Args:
            user_id: ID of the user

        Returns:
            Dictionary with various statistics
        """
        # Текущий месяц для статистики
        current_date = datetime.utcnow().date()
        month_start = current_date.replace(day=1)

        # Общее количество записей
        total_result = await self.db.execute(
            select(func.count(JournalEntry.id)).where(
                JournalEntry.user_id == user_id
            )
        )
        total_entries = total_result.scalar()

        # Записи за текущий месяц
        month_result = await self.db.execute(
            select(func.count(JournalEntry.id)).where(
                and_(
                    JournalEntry.user_id == user_id,
                    JournalEntry.entry_date >= month_start
                )
            )
        )
        entries_this_month = month_result.scalar()

        # Среднее настроение за месяц
        mood_result = await self.db.execute(
            select(func.avg(JournalEntry.mood_rating)).where(
                and_(
                    JournalEntry.user_id == user_id,
                    JournalEntry.entry_date >= month_start,
                    JournalEntry.mood_rating.isnot(None)
                )
            )
        )
        avg_mood = mood_result.scalar()

        # Средняя энергия за месяц
        energy_result = await self.db.execute(
            select(func.avg(JournalEntry.energy_level)).where(
                and_(
                    JournalEntry.user_id == user_id,
                    JournalEntry.entry_date >= month_start,
                    JournalEntry.energy_level.isnot(None)
                )
            )
        )
        avg_energy = energy_result.scalar()

        # Тренд настроения за последние 30 дней
        thirty_days_ago = current_date - timedelta(days=30)
        trend_result = await self.db.execute(
            select(
                JournalEntry.entry_date,
                func.avg(JournalEntry.mood_rating).label('avg_mood')
            ).where(
                and_(
                    JournalEntry.user_id == user_id,
                    JournalEntry.entry_date >= thirty_days_ago,
                    JournalEntry.mood_rating.isnot(None)
                )
            ).group_by(JournalEntry.entry_date).order_by(JournalEntry.entry_date)
        )

        mood_trend = []
        for row in trend_result.fetchall():
            mood_trend.append({
                "date": str(row.entry_date),
                "mood": float(row.avg_mood)
            })

        return {
            "total_entries": total_entries or 0,
            "entries_this_month": entries_this_month or 0,
            "average_mood_this_month": round(float(avg_mood), 2) if avg_mood else None,
            "average_energy_this_month": round(float(avg_energy), 2) if avg_energy else None,
            "most_used_tags": [],  # Реализовать в production
            "mood_trend": mood_trend
        }