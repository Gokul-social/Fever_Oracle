"""
Security utilities for Fever Oracle backend
"""
from functools import wraps
from flask import request, jsonify
import re

def sanitize_input(text):
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(text, str):
        return text
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', text)
    return text.strip()

def validate_json_content_type(f):
    """Decorator to ensure request has JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method in ['POST', 'PUT', 'PATCH']:
            if not request.is_json:
                return jsonify({"error": "Content-Type must be application/json"}), 400
        return f(*args, **kwargs)
    return decorated_function

def add_security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

