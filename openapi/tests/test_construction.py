"""
Test construction of an API from models.
"""

from openapi.model import (
    BodyParameter,
    Definitions,
    Header,
    Headers,
    Info,
    JsonReference,
    MediaTypeList,
    MimeType,
    Operation,
    ParametersList,
    PathItem,
    PathParameterSubSchema,
    Paths,
    QueryParameterSubSchema,
    Response,
    Responses,
    Schema,
    Swagger,
)


def test_simple_construction():
    """
    Constructing a simple API produces a valid schema.

    """
    # construction works by constructor
    swagger = Swagger(
        swagger="2.0",
        info=Info(
            title="Hello",
            version="1.0.0",
        ),
    )
    # construction works by assignment
    swagger.paths = Paths({
        "/hello": PathItem(
            get=Operation(
                responses=Responses({
                    "200": Response(
                        description="Returns hello",
                    )
                })
            ),
        ),
    })
    # constructed schema validates
    swagger.validate()


Error = dict(
    properties={
        "message": {
            "type": "string",
        },
    },
    required=["message"],
)

NewPerson = dict(
    properties={
        "name": {
            "type": "string",
        },
    },
    required=["name"],
)

Person = dict(
    properties={
        "id": {
            "type": "string",
        },
        "name": {
            "type": "string",
        },
    },
    required=["id", "name"],
)

PersonList = dict(
    properties={
        "items": {
            "type": "string",
        },
    },
    required=["items"],
)


def header(description, header_type="string"):
    return Header(**{
        "description": description,
        "type": header_type,
    })


def response(description, resource=None, headers=None):
    response = Response(
        description=description,
    )
    if resource is not None:
        response.schema = JsonReference({
            "$ref": "#/definitions/{}".format(resource),
        })
    if headers is not None:
        response.headers = headers
    return response


def body_param(resource):
    return BodyParameter(**{
        "name": resource,
        "in": "body",
        "schema": JsonReference({
            "$ref": "#/definitions/{}".format(resource),
        }),
    })


def path_param(description, name, param_type="string"):
    return PathParameterSubSchema(**{
        "description": description,
        "name": name,
        "in": "path",
        "required": True,
        "type": param_type,
    })


def query_param(description, name, param_type="string", required=False):
    return QueryParameterSubSchema(**{
        "description": description,
        "name": name,
        "in": "query",
        "required": False,
        "type": param_type,
    })


def test_crud_construction():
    """
    Constructing a CRUD API from the DSL produces a valid schema.

    """
    swagger = Swagger(
        swagger="2.0",
        info=Info(
            title="Example",
            version="1.0.0",
        ),
        basePath="/api",
        consumes=MediaTypeList([
            MimeType("application/json"),
        ]),
        produces=MediaTypeList([
            MimeType("application/json"),
        ]),
        paths=Paths(),
        definitions=Definitions(),
    )

    # definitions
    swagger.definitions.update(
        Error=Schema(Error),
        NewPerson=Schema(NewPerson),
        Person=Schema(Person),
        PersonList=Schema(PersonList),
    )

    # collection operations
    swagger.paths.update({
        "/person": PathItem(
            get=Operation(
                description="Search the collection of (all) people",
                operationId="get_person_list",
                parameters=ParametersList([
                    query_param("Pagination start index", "index", "integer"),
                    query_param("Pagination size", "size", "integer"),
                ]),
                responses=Responses(**{
                    "200": response("Success", "PersonList"),
                    "400": response("Malformed Syntax", "Error"),
                    "default": response("Unexpected Error", "Error"),
                }),
            ),
            post=Operation(
                description="Create a new person",
                operationId="create_person",
                parameters=ParametersList([
                    body_param("NewPerson"),
                ]),
                responses=Responses(**{
                    "201": response("Created a new person", "Person", headers=Headers(**{
                        "Location": header("URI of created person"),
                    })),
                    "400": response("Malformed Syntax", "Error"),
                    "409": response("Conflict", "Error"),
                    "default": response("Unexpected Error", "Error"),
                }),
            ),
        ),
    })

    # instance operations
    swagger.paths.update({
        "/person/{personId}": PathItem(
            get=Operation(
                description="Get a person",
                operationId="get_person",
                parameters=ParametersList([
                    path_param("The id of the person", "personId"),
                ]),
                responses=Responses(**{
                    "200": response("Success", "Person"),
                    "404": response("Not Found", "Error"),
                    "default": response("Unexpected Error", "Error"),
                }),
            ),
            put=Operation(
                description="Update a person",
                operationId="update_person",
                parameters=ParametersList([
                    path_param("The id of the person", "personId"),
                ]),
                responses=Responses(**{
                    "200": response("Success", "Person"),
                    "400": response("Malformed Syntax", "Error"),
                    "404": response("Not Found", "Error"),
                    "default": response("Unexpected Error", "Error"),
                }),
            ),
            delete=Operation(
                description="Delete a person",
                operationId="delete_person",
                parameters=ParametersList([
                    path_param("The id of the person", "personId"),
                ]),
                responses=Responses(**{
                    "204": response("Success"),
                    "404": response("Not Found", "Error"),
                    "default": response("Unexpected Error", "Error"),
                }),
            ),
        ),
    })

    swagger.validate()
