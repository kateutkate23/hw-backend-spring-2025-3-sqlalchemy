from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.store.database.sqlalchemy_base import BaseModel


class ThemeModel(BaseModel):
    __tablename__ = "themes"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True)
    questions: Mapped[list["QuestionModel"]] = relationship(
        back_populates="theme", cascade="all, delete-orphan"
    )


class AnswerModel(BaseModel):
    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128))
    is_correct: Mapped[bool] = mapped_column(Boolean)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))


class QuestionModel(BaseModel):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(128), unique=True)
    theme_id: Mapped[int] = mapped_column(ForeignKey("themes.id"))
    theme: Mapped["ThemeModel"] = relationship(back_populates="questions")
    answers: Mapped[list["AnswerModel"]] = relationship(cascade="all, delete-orphan")