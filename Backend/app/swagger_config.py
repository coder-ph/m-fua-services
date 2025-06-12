"""
Swagger configuration for API documentation.
"""

# Swagger template for API documentation
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "M-FUA Services Platform API",
        "description": "API documentation for the M-FUA Services Platform - Connecting service providers with clients",
        "version": "1.0.0",
        "contact": {
            "name": "M-FUA Support",
            "email": "support@m-fua.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "basePath": "/api",
    "schemes": ["http", "https"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "security": [{"Bearer": []}],
    "consumes": ["application/json"],
    "produces": ["application/json"],
    "tags": [
        {
            "name": "Authentication",
            "description": "User authentication and authorization"
        },
        {
            "name": "Users",
            "description": "User management and profiles"
        },
        {
            "name": "Services",
            "description": "Service requests and management"
        },
        {
            "name": "Categories",
            "description": "Service categories and subcategories"
        },
        {
            "name": "Ratings",
            "description": "Ratings and reviews"
        },
        {
            "name": "Notifications",
            "description": "User notifications"
        }
    ],
    "definitions": {
        "User": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "email": {"type": "string", "format": "email", "example": "user@example.com"},
                "first_name": {"type": "string", "example": "John"},
                "last_name": {"type": "string", "example": "Doe"},
                "role": {"type": "string", "enum": ["customer", "provider", "admin"], "example": "customer"},
                "phone": {"type": "string", "example": "+1234567890"},
                "address": {"type": "string", "example": "123 Main St"},
                "city": {"type": "string", "example": "Nairobi"},
                "country": {"type": "string", "example": "Kenya"},
                "company_name": {"type": "string", "example": "ACME Corp"},
                "bio": {"type": "string", "example": "A short bio about the user"},
                "is_active": {"type": "boolean", "example": True},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            }
        },
        "Service": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "title": {"type": "string", "example": "House Cleaning"},
                "description": {"type": "string", "example": "Need cleaning for a 3-bedroom house"},
                "status": {"type": "string", "enum": ["pending", "assigned", "in_progress", "completed", "cancelled", "rejected", "expired"]},
                "budget": {"type": "number", "format": "float", "example": 5000},
                "deadline": {"type": "string", "format": "date-time"},
                "location": {"type": "string", "example": "Nairobi, Kenya"},
                "latitude": {"type": "number", "format": "float", "example": -1.2921},
                "longitude": {"type": "number", "format": "float", "example": 36.8219},
                "client_id": {"type": "integer", "example": 1},
                "provider_id": {"type": "integer", "example": 2},
                "category_id": {"type": "integer", "example": 1},
                "created_at": {"type": "string", "format": "date-time"},
                "updated_at": {"type": "string", "format": "date-time"}
            }
        },
        "Category": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "name": {"type": "string", "example": "Cleaning"},
                "description": {"type": "string", "example": "Home and office cleaning services"},
                "icon": {"type": "string", "example": "cleaning_services"},
                "parent_id": {"type": "integer", "example": None},
                "is_active": {"type": "boolean", "example": True},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "Rating": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "service_id": {"type": "integer", "example": 1},
                "provider_id": {"type": "integer", "example": 2},
                "reviewer_id": {"type": "integer", "example": 1},
                "rating": {"type": "integer", "minimum": 1, "maximum": 5, "example": 5},
                "comment": {"type": "string", "example": "Excellent service!"},
                "is_anonymous": {"type": "boolean", "example": False},
                "created_at": {"type": "string", "format": "date-time"}
            }
        },
        "Notification": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "example": 1},
                "user_id": {"type": "integer", "example": 1},
                "title": {"type": "string", "example": "New Message"},
                "message": {"type": "string", "example": "You have a new message"},
                "type": {"type": "string", "enum": ["info", "success", "warning", "error"], "example": "info"},
                "is_read": {"type": "boolean", "example": False},
                "created_at": {"type": "string", "format": "date-time"},
                "read_at": {"type": "string", "format": "date-time", "nullable": True}
            }
        },
        "Error": {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "Error description"},
                "errors": {"type": "object", "example": {"field": ["Error message"]}}
            }
        },
        "Pagination": {
            "type": "object",
            "properties": {
                "items": {"type": "array"},
                "total": {"type": "integer", "example": 100},
                "pages": {"type": "integer", "example": 10},
                "page": {"type": "integer", "example": 1},
                "per_page": {"type": "integer", "example": 10}
            }
        }
    },
    "responses": {
        "200": {
            "description": "Success"
        },
        "201": {
            "description": "Created"
        },
        "400": {
            "description": "Bad Request",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "401": {
            "description": "Unauthorized",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "403": {
            "description": "Forbidden",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "404": {
            "description": "Not Found",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "422": {
            "description": "Validation Error",
            "schema": {"$ref": "#/definitions/Error"}
        },
        "500": {
            "description": "Internal Server Error",
            "schema": {"$ref": "#/definitions/Error"}
        }
    },
    "parameters": {
        "page": {
            "name": "page",
            "in": "query",
            "type": "integer",
            "description": "Page number",
            "default": 1,
            "required": False
        },
        "per_page": {
            "name": "per_page",
            "in": "query",
            "type": "integer",
            "description": "Items per page",
            "default": 10,
            "required": False
        },
        "sort_by": {
            "name": "sort_by",
            "in": "query",
            "type": "string",
            "description": "Field to sort by",
            "required": False
        },
        "order": {
            "name": "order",
            "in": "query",
            "type": "string",
            "enum": ["asc", "desc"],
            "default": "desc",
            "description": "Sort order",
            "required": False
        }
    }
}
