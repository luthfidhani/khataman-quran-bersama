# Backend untuk Aplikasi Khataman Al-Quran

## Brief Description

Backend for the Khataman Al-Quran Application is an API designed to manage Quran recitation activities. This API allows efficient and structured management of members, periods, and Quran recitation checklists. With this API, users can add members, create recitation periods, and manage the reading progress of each member flexibly.

## Technologies Used
- FastAPI - As the framework for building the API.
- Python - The main programming language used.
- PostgreSQL - The database used for storing data.

## Installation Guide

To install and run this project, simply execute the following command in the terminal:

```
./auto/start
```

This command will run the pre-configured Docker for this project.

## Endpoints

### Get Member Names

Endpoint: `/member`

Method: **GET**

**Response:**

```json
[
    {
        "name": "User 1",
        "id": "edbd85"
    },
    {
        "name": "User 2",
        "id": "1d0e5c"
    }
]
```

### Add Member

Endpoint: `/member/create`

Method: **POST**

**Request:**

```json
{
    "name": "Luthfi Afrizal Ardhani"
}
```

**Response:**

```json
{
    "status": "success"
}
```

### Delete Member

Endpoint: `/member`

Method: **DELETE**

**Request:**

```json
{
    "id": "80f0ff"
}
```

**Response:**

```json
{
    "status": "success"
}
```

### Update Member

Endpoint: `/member`

Method: **PUT**

**Request:**

```json
{
    "id": "80f0ff",
    "update": {
        "name": "Captain Luth"
    }
}
```

**Response:**

```json
{
    "status": "success"
}
```

### Get All Periods

Endpoint: `/period`

Method: **GET**

**Response:**

```json
[
    { "name": "week 1", "id": "c44ba6" },
    { "name": "week 2", "id": "114898" }
]
```

### Get Period Details

Endpoint: `/period/{period_id/current}`

Method: **GET**

**Response:**

```json
{
    "data": [
        [
            {
                "name": "User 1",
                "id": "edbd85"
            },
            {
                "juz": [
                    {
                        "number": 1,
                        "status": false
                    },
                    {
                        "number": 2,
                        "status": false
                    }
                ]
            }
        ],
        [
            {
                "name": "User 2",
                "id": "1d0e5c"
            },
            {
                "juz": [
                    {
                        "number": 7,
                        "status": false
                    },
                    {
                        "number": 8,
                        "status": false
                    }
                ]
            }
        ]
    ],
    "can_update": true,
    "can_lock": false,
    "is_done": false,
    "period": "114898"
}
```

### Edit Checklist

Endpoint: `/period/{period_id}`

Method: **PUT**

**Request:**

```json
{
    "data": [
        [
            {
                "name": "Member 1",
                "id": "1"
            },
            {
                "juz": [
                    {
                        "number": 26,
                        "status": true
                    },
                    {
                        "number": 27,
                        "status": true
                    }
                ]
            }
        ],
        [
            {
                "name": "hesoyam aezakmi",
                "id": "2"
            },
            {
                "juz": [
                    {
                        "number": 1,
                        "status": true
                    },
                    {
                        "number": 2,
                        "status": true
                    }
                ]
            }
        ]
    ]
}
```

**Response:**

```json
{
    "status": "success"
}
```

### Lock Checklist

Endpoint: `/period/{period_id}/lock`

Method: **GET**

**Response:**

```json
{
    "data": [
        [
            {
                "name": "User 1",
                "id": "edbd85"
            },
            {
                "juz": [
                    {
                        "number": 1,
                        "status": false
                    },
                    {
                        "number": 2,
                        "status": false
                    }
                ]
            }
        ],
        [
            {
                "name": "User 2",
                "id": "1d0e5c"
            },
            {
                "juz": [
                    {
                        "number": 7,
                        "status": false
                    },
                    {
                        "number": 8,
                        "status": false
                    }
                ]
            }
        ]
    ],
    "can_update": false,
    "can_lock": false,
    "is_done": true,
    "period": "c44ba6"
}
```

### Create Period

Endpoint: `/period`

Method: **POST**

**Request:**

```json
{
    "name": "week 2",
    "data": [
        {
            "id": "edbd85",
            "juz": [1, 2, 3, 4, 5, 6]
        },
        {
            "id": "1d0e5c",
            "juz": [7, 8, 9, 10, 11, 12]
        }
    ]
}
```

**Response:**

```json
{
    "status": "success"
}
```

