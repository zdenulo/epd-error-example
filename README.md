code here demonstrates error when **StructuredProperty** field is used as repeated property for **EndpointsModel**.

see **main.py** for code it's simple and straightforward: There is User model which has Addresses as repeated **StructuredProperty**
and two endpoints **create_user** and **get_user** (input is *entityKey* field)

when running Api Explorer on [localhost:8080/_ah/api/explorer](localhost:8080/_ah/api/explorer) with 
**create_user** endpoint I get response:

    {
     "addresses": [
      {
       "city": "DC",
       "house_no": "10",
       "street": "No name",
       "type": "home"
      }
     ],
     "email": "test@email.com",
     "entityKey": "ag9kZXZ-ZXBkLWV4YW1wbGVyEQsSBFVzZXIYgICAgIDQuwoM"
    }

but when I use **get_user** endpoint, I get:

    {
     "email": "test@email.com",
     "entityKey": "ag9kZXZ-ZXBkLWV4YW1wbGVyEQsSBFVzZXIYgICAgIDQuwoM"
    }

addresses field is ignored in response, which is error.

this can be fixed in **endpoints_proto_datastore/ndb/models.py** line 1218 change from

    if value is None:

to 

    if value is None or value==[]:
    
Now I get correct answer when using **get_user**. 

    {
     "addresses": [
      {
       "city": "DC",
       "house_no": "10",
       "street": "No name",
       "type": "home"
      }
     ],
     "email": "test@email.com",
     "entityKey": "ag9kZXZ-ZXBkLWV4YW1wbGVyEQsSBFVzZXIYgICAgIDQuwoM"
    }

I don't know though if this fix is enough, i.e. if it doesn't break something.
When field is used as StructuredProperty but not repeated everything works OK. 