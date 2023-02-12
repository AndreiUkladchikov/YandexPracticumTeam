test_topic_name = "test_topic"

test_data = {
    "user_id": "user",
    "film_id": "1dcfed00-a0a1-4042-9811-66d7eb5d94bb",
    "timestamp": 4675967,
}

test_invalid_user_id = {
    "user_id": ["Hello", "world"],
    "film_id": "1dcfed00-a0a1-4042-9811-66d7eb5d94bb",
    "timestamp": 4675967,
}

test_invalid_timestamp = {
    "user_id": "user",
    "film_id": "1dcfed00-a0a1-4042-9811-66d7eb5d94bb",
    "timestamp": "Tiny",
}
