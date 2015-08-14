
import endpoints
from google.appengine.ext import ndb
from endpoints_proto_datastore.ndb import EndpointsModel


class Address(EndpointsModel):
    street = ndb.StringProperty()
    house_no = ndb.StringProperty()
    city = ndb.StringProperty()
    type = ndb.StringProperty()


class User(EndpointsModel):
    email = ndb.StringProperty()
    addresses = ndb.StructuredProperty(Address, repeated=True)


MyServer = endpoints.api(name='test', version='v1', description='Test API')


@MyServer.api_class(resource_name='user')
class UserService(endpoints.remote.Service):
    @User.method(path='user', http_method='POST', request_fields=('email', 'addresses'),
                 response_fields=('entityKey', 'email', 'addresses'), name='create_user')
    def create_user(self, user):
        """creates user"""

        user.put()
        return user

    @User.method(path='user/{entityKey}', http_method='GET', response_fields=('entityKey', 'email', 'addresses'),
                 name='get_user')
    def get_user(self, user):
        """get user based on key (urlsafe)"""

        if not user.from_datastore:
            raise endpoints.NotFoundException("User not found")
        return user


application = endpoints.api_server([MyServer], restricted=False)

