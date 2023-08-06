# Chocs [![PyPI version](https://badge.fury.io/py/chocs.svg)](https://pypi.org/project/chocs/) ![Release](https://github.com/kodemore/chocs/workflows/Release/badge.svg) ![Linting and Tests](https://github.com/kodemore/chocs/workflows/Linting%20and%20Tests/badge.svg) [![codecov](https://codecov.io/gh/kodemore/chocs/branch/master/graph/badge.svg)](https://codecov.io/gh/kodemore/chocs) [![Maintainability](https://api.codeclimate.com/v1/badges/9e3c979283b2361a9174/maintainability)](https://codeclimate.com/github/kodemore/chocs/maintainability)
Chocs is a modern HTTP framework for building AWS HTTP API/REST API and WSGI compatible applications. 
Chocs aims to be small, expressive, and robust. 
It provides an elegant API for writing fault-proof, extensible microservices.  

## Features

 - AWS Serverless integration
 - Open api integration  
 - Elegant and easy API
 - No additional bloat like built-in template engines, session handlers, etc.
 - Compatible with all WSGI servers
 - Loosely coupled components which can be used separately
 - Multipart body parsing
 - Graceful error handling
 - HTTP middleware support
 - Fast routing

## Installation
```
pip install chocs
```

or with poetry

```
poetry add chocs
```

## Quick start

```python
import chocs

http = chocs.Application()

@http.get("/hello/{name}")
def hello(request: chocs.HttpRequest) -> chocs.HttpResponse:
    return chocs.HttpResponse(f"Hello {request.path_parameters.get('name')}!")

chocs.serve(http)
```

> Keep in mind that the `chocs.serve()` function is using the `bjoern` package, so make sure you included it in your project
> dependencies before using it. You are able to use any WSGI compatible server.

# Documentation
For usage and detailed documentation please visit our [wiki page](https://github.com/kodemore/chocs/wiki)
