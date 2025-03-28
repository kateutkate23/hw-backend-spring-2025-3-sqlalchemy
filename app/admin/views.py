import hashlib

from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session, get_session

from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        data = self.request["data"]
        email = data["email"]
        password = data["password"]

        admin = await self.store.admins.get_by_email(email)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if not admin or hashed_password != admin.password:
            raise HTTPForbidden

        session = await new_session(self.request)
        session["admin_id"] = admin.id
        session["admin_email"] = admin.email

        return json_response(
            data={
                "id": admin.id,
                "email": admin.email,
            }
        )


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        current_admin = self.request.admin
        return json_response(
            data={
                "id": current_admin.id,
                "email": current_admin.email,
            }
        )
