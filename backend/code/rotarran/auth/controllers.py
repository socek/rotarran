from pyramid.security import forget
from pyramid.security import remember
from sqlalchemy.orm.exc import NoResultFound

from rotarran.application.base.controller import FormController
from rotarran.application.base.controller import JsonController
from rotarran.auth.driver import UserReadDriver
from rotarran.auth.forms import LoginSchema


class LoginController(FormController):

    def post(self):
        fields = self.prepere_context()
        schema = LoginSchema()

        if self.schema_validated(schema, fields):
            if self.authenticated(fields):
                self.on_success(fields)
            else:
                self.on_fail()

    def authenticated(self, fields):
        driver = UserReadDriver(self.request.database)
        try:
            user = driver.get_by_name(fields['username']['value'])
            return user.validate_password(fields['password']['value'])
        except NoResultFound:
            # user can not be authenticated if he/she does not exists
            return False

    def on_success(self, fields):
        self.context['form_error'] = ''
        self.context['validate'] = True
        headers = remember(self.request, fields['username'])
        self.request.response.headerlist.extend(headers)

    def on_fail(self):
        self.context['validate'] = False
        self.context['form_error'] = "Username and/or password do not match."


class LogoutController(JsonController):

    def make(self):
        headers = forget(self.request)
        self.request.response.headerlist.extend(headers)
        self.context['is_authenticated'] = False


class AuthDataController(JsonController):

    def make(self):
        self.context['is_authenticated'] = self.request.authenticated_userid is not None
