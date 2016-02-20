# openapi

Python OpenAPI 2.0 (Swagger) object model

There are any number of good libraries for using OpenAPI/Swagger in specific ways or
with specific frameworks. This isn't one of them.

Rather, this library provides a simple object model for producing and consuming
Swagger specifications.


## Models

Model types extend Python `dict`, `list`, or `string` to support reading from JSON,
writing to JSON, and validation against (the relevant portion of) the Swagger schema.

As a result, models are interchangeable with their primitive counterparts and can
be used as much (or as little) as desired to enhange readability or perform validation.

Models convert contained primitive types to models when accessed using keys or attributes
(for `dict`-based types) and when using indexing (for `list`-based access). Access to
model internals via iteration bypasses conversion.


## Usage

 1. Either load a schema from json:

        from openapi import load

        with open("/path/to/swagger.json") as fileobj:
            swagger = load(fileobj)

    Or construct one explicitly from the model:

        from openapi.model import Swagger, Info, Operation, PathItem, Paths, Response, Responses

        swagger = Swagger(
            swagger="2.0",
            info=Info(
                title="Example",
                version="1.0.0",
            ),
            basePath="/api",
			paths=Paths({
                "/hello": PathItem(
                    get=Operation(
                        responses=Responses({
                            "200": Response(
                                description="Returns hello",
                            )
                        })
                    ),
                ),
            }),
        )

 2. Access model internals using attributes:

        print swagger.info
        print swagger.basePath

    Pythonic names are automically converted when using attribute access:

        print swagger.base_path

    Naturally, attribute names that are illegel or that shadow existing attributes
    must be accessed using key syntax:

        print swagger.paths["/hello"]["get"].responses["200"].description

 3. Validate the model:

        swagger.validate()

    Internal models can be validated independently:

        swagger.info.validate()

 4. Dump the result to JSON:

        print swagger.dumps()
