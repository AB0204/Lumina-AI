# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in Lumina AI, please report it responsibly:

1. **Do NOT open a public issue**
2. **Email**: abhibhardwaj427@gmail.com
3. **Include**: Description, steps to reproduce, potential impact

## Security Measures

- All API endpoints use input validation via Pydantic
- CORS is configured to restrict cross-origin requests
- Docker containers run as non-root users
- No secrets are stored in source code
- Redis connections are internal-only (not exposed publicly)
- Environment variables are used for all sensitive configuration
