from collections.abc import Iterable, Sequence

from sqlalchemy import select

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> ThemeModel:
        theme = ThemeModel(title=title)

        async with self.app.database.session() as session:
            session.add(theme)
            await session.commit()

            return theme

    async def get_theme_by_title(self, title: str) -> ThemeModel | None:
        async with self.app.database.session() as session:
            return await session.scalar(select(ThemeModel).where(ThemeModel.title == title))

    async def get_theme_by_id(self, id_: int) -> ThemeModel | None:
        async with self.app.database.session() as session:
            return await session.scalar(select(ThemeModel).where(ThemeModel.id == id_))

    async def list_themes(self) -> Sequence[ThemeModel]:
        async with self.app.database.session() as session:
            result = await session.execute(select(ThemeModel))
            return result.scalars().all()

    async def create_question(
            self, title: str, theme_id: int, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        question = QuestionModel(title=title, theme_id=theme_id, answers=list(answers))

        async with self.app.database.session() as session:
            session.add(question)
            await session.commit()

            return question

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        async with self.app.database.session() as session:
            return await session.scalar(select(QuestionModel).where(QuestionModel.title == title))

    async def list_questions(
            self, theme_id: int | None = None
    ) -> Sequence[QuestionModel]:
        async with self.app.database.session() as session:
            result = await session.execute(select(QuestionModel))
            return result.scalars().all()
