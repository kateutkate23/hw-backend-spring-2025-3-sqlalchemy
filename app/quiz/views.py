from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import querystring_schema, request_schema, response_schema

from app.quiz.models import AnswerModel
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
    ThemeIdSchema,
    ThemeListSchema,
    ThemeSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class ThemeAddView(AuthRequiredMixin, View):
    @request_schema(ThemeSchema)
    @response_schema(ThemeSchema)
    async def post(self):
        title = self.data["title"]

        theme = await self.store.quizzes.get_theme_by_title(title)
        if theme:
            raise HTTPConflict

        theme = await self.store.quizzes.create_theme(title)
        return json_response(
            data=ThemeSchema().dump(theme),
        )


class ThemeListView(AuthRequiredMixin, View):
    @response_schema(ThemeListSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()

        return json_response(
            data={
                "themes": [{"id": theme.id, "title": theme.title} for theme in themes],
            }
        )


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        title = self.data["title"]
        theme_id = self.data["theme_id"]
        answers_data = self.data["answers"]

        question = await self.store.quizzes.get_question_by_title(title)
        if question:
            raise HTTPConflict

        theme = await self.store.quizzes.get_theme_by_id(theme_id)
        if not theme:
            raise HTTPNotFound

        answers = [
            AnswerModel(title=answer["title"], is_correct=answer["is_correct"])
            for answer in answers_data
        ]

        if len(answers) < 2:
            raise HTTPBadRequest
        correct_answers = sum(1 for answer in answers if answer.is_correct)
        if correct_answers == 0:
            raise HTTPBadRequest
        if correct_answers > 1:
            raise HTTPBadRequest

        question = await self.store.quizzes.create_question(title, theme_id, answers)
        return json_response(
            data=QuestionSchema().dump(question),
        )


class QuestionListView(AuthRequiredMixin, View):
    @querystring_schema(ThemeIdSchema)
    @response_schema(ListQuestionSchema)
    async def get(self):
        theme_id = self.data.get("theme_id")

        questions = await self.store.quizzes.list_questions(theme_id)
        return json_response(
            data={
                "questions": [
                    {
                        "id": question.id,
                        "title": question.title,
                        "theme_id": question.theme_id,
                        "answers": [
                            {"title": answer.title, "is_correct": answer.is_correct}
                            for answer in question.answers
                        ]
                    }
                    for question in questions
                ]
            }
        )
