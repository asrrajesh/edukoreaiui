# MySchool Configuration Guide

This document provides a comprehensive guide to configuring the MySchool application.

> **Note:** Database (MongoDB) and Claude OCR configuration now live in the
> sibling `edukoreaiapi` project. This `edukoreaiui` project only needs
> `API_BASE_URL` (and UI/window settings below) — see that project's own
> `.env.example` for the backend settings.

## Overview

The MySchool application uses environment variables stored in a `.env` file for all configuration settings. This approach provides:

- **Single source of truth** - All settings in one `.env` file
- **Secure** - Sensitive data (credentials) never in version control
- **Flexible** - Easy to switch between environments (dev/staging/prod)
- **Standard practice** - Industry-standard 12-factor app configuration
- **No code changes needed** - Update config without touching code

## Configuration Files

### `.env` (Required for runtime)
- Contains all environment variables for the application
- Created from `.env.example` template
- **DO NOT commit to version control** (it's in .gitignore)
- One `.env` file per environment/deployment

### `.env.example` (Template)
- Template showing all available configuration options
- Safe to commit to version control
- Users copy this to `.env` and fill in their values
- Contains comments explaining each setting

### `config/config.py` (Application config loader)
- Loads variables from `.env` file using `python-dotenv`
- Provides sensible defaults if a variable is missing
- No hardcoded values - all from environment
- Safe to commit to version control

## Quick Start

### Local Development

1. A `.env` file is already provided with defaults
2. Just run the application:
   ```bash
   python main.py
   ```

### Production or Custom Setup

1. Copy `.env.example` to create your `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your settings:
   ```bash
   nano .env
   ```

3. Ensure `.env` is NOT in version control (it's in `.gitignore`)

## Configuration Structure

All settings are organized into sections in `.env`:

### Database Configuration
```bash
MONGO_URI=mongodb://localhost:27017/
DB_NAME=myschool
DB_CONNECTION_TIMEOUT=5000
```

### Application Settings
```bash
APP_TITLE=MySchool
APP_VERSION=1.0.0
THEME_COLOR=#3949AB
SECONDARY_COLOR=#5C6BC0
```

### Window Configuration
```bash
WINDOW_WIDTH=400
WINDOW_HEIGHT=780
WINDOW_RESIZABLE=true
BACKGROUND_COLOR=#F5F5F5
```

### Security Settings
```bash
PASSWORD_MIN_LENGTH=8
SESSION_TIMEOUT=0
MAX_LOGIN_ATTEMPTS=5
LOCKOUT_DURATION=15
```

### Validation Patterns
```bash
EMAIL_PATTERN=^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$
MOBILE_PATTERN=^\+?[0-9]{10,15}$
MOBILE_MIN_LENGTH=10
MOBILE_MAX_LENGTH=15
```

### API Endpoints
```bash
API_BASE_URL=http://localhost:8000
PASSWORD_RESET_SERVICE=http://localhost:8000/api/reset-password
EMAIL_SERVICE_ENABLED=false
SMS_SERVICE_ENABLED=false
```

### Feature Flags
```bash
ENABLE_PASSWORD_RESET_EMAIL=false
ENABLE_SMS_NOTIFICATIONS=false
ENABLE_USER_REGISTRATION=true
ENABLE_GUEST_ACCESS=false
ENABLE_SOCIAL_LOGIN=false
```

### Logging Configuration
```bash
LOG_LEVEL=DEBUG
LOG_TO_FILE=false
LOG_TO_CONSOLE=true
LOG_FILE_PATH=logs/myschool.log
```

### Environment Settings
```bash
ENVIRONMENT=development
DEBUG=true
ALLOW_CORS=true
CORS_ORIGINS=http://localhost:*,http://127.0.0.1:*
```

## How to Customize Settings

### Method 1: Edit `.env` directly (Easiest)

```bash
# Open .env file
nano .env

# Change any setting you want
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/myschool
DEBUG=false
LOG_LEVEL=INFO

# Save and restart application
python main.py
```

### Method 2: Using Environment Variables (CI/CD)

Override `.env` settings using system environment variables:

```bash
# Set in shell
export MONGO_URI="mongodb+srv://user:pass@cluster.mongodb.net/myschool"
export DEBUG="false"

# Run application
python main.py
```

### Method 3: Docker Environment

Pass environment variables to Docker:

```bash
docker run -e MONGO_URI="mongodb://mongo:27017/" \
           -e DEBUG="false" \
           myschool:latest
```

## Configuration Examples

### Example 1: Local Development (Default)

Use the provided `.env` file as-is:

```bash
MONGO_URI=mongodb://localhost:27017/
DB_NAME=myschool
DEBUG=true
LOG_LEVEL=DEBUG
ENVIRONMENT=development
```

### Example 2: Production Deployment

Create `.env` for production:

```bash
MONGO_URI=mongodb+srv://produser:prodpass@prod-cluster.mongodb.net/myschool
DB_NAME=myschool_prod
DEBUG=false
LOG_LEVEL=WARNING
LOG_TO_FILE=true
ENVIRONMENT=production
MAX_LOGIN_ATTEMPTS=3
LOCKOUT_DURATION=30
PASSWORD_MIN_LENGTH=12
```

### Example 3: Staging Environment

Create `.env` for staging:

```bash
MONGO_URI=mongodb+srv://staginguser:stagingpass@staging-cluster.mongodb.net/myschool
DB_NAME=myschool_staging
DEBUG=true
LOG_LEVEL=INFO
ENVIRONMENT=staging
ENABLE_PASSWORD_RESET_EMAIL=true
EMAIL_SERVICE_ENABLED=true
```

### Example 4: MongoDB Atlas Cloud

```bash
MONGO_URI=mongodb+srv://username:password@mycluster-abc123.mongodb.net/myschool?retryWrites=true&w=majority
DB_NAME=myschool
DB_CONNECTION_TIMEOUT=10000
```

### Example 5: Docker Compose

```bash
# .env for Docker Compose
MONGO_URI=mongodb://mongo_service:27017/
DB_NAME=myschool
API_BASE_URL=http://api:8000
DEBUG=false
ENVIRONMENT=docker
```

## Environment-Specific Setup

### Development

```bash
# .env.development (or just .env)
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
MONGO_URI=mongodb://localhost:27017/
DB_NAME=myschool_dev
ENABLE_PASSWORD_RESET_EMAIL=false
```

### Staging

```bash
# .env.staging
ENVIRONMENT=staging
DEBUG=true
LOG_LEVEL=INFO
MONGO_URI=mongodb+srv://staging_user:pass@cluster.mongodb.net/myschool_staging
DB_NAME=myschool_staging
ENABLE_PASSWORD_RESET_EMAIL=true
EMAIL_SERVICE_ENABLED=true
```

### Production

```bash
# .env.production (NEVER commit this!)
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=WARNING
LOG_TO_FILE=true
MONGO_URI=mongodb+srv://prod_user:prod_pass@prod-cluster.mongodb.net/myschool_prod
DB_NAME=myschool_prod
ENABLE_PASSWORD_RESET_EMAIL=true
EMAIL_SERVICE_ENABLED=true
SMS_SERVICE_ENABLED=true
MAX_LOGIN_ATTEMPTS=3
LOCKOUT_DURATION=30
PASSWORD_MIN_LENGTH=12
```

## Data Types in .env

Variables in `.env` are read as strings, but `config/config.py` handles type conversion:

- **Strings**: Used as-is
  ```bash
  APP_TITLE=MySchool
  MONGO_URI=mongodb://localhost:27017/
  ```

- **Booleans**: Converted from "true", "false", "1", "0", etc.
  ```bash
  DEBUG=true
  WINDOW_RESIZABLE=false
  ```

- **Numbers**: Converted to int
  ```bash
  WINDOW_WIDTH=400
  PASSWORD_MIN_LENGTH=8
  ```

- **Lists**: Comma-separated values
  ```bash
  CORS_ORIGINS=http://localhost:*,http://127.0.0.1:*
  ```

## Security Best Practices

1. **Never commit `.env`** - It's in `.gitignore` for a reason
2. **Use `.env.example`** - As a template for new environments
3. **Keep credentials secure** - Never share or version control production `.env`
4. **Use strong passwords** - For database and service credentials
5. **Limit file permissions** - Restrict `.env` file access to application user only
   ```bash
   chmod 600 .env
   ```
6. **Use secrets manager** - For production, consider using AWS Secrets Manager, HashiCorp Vault, etc.

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'dotenv'"

**Solution**: Install python-dotenv:
```bash
pip install python-dotenv
# or
pip install -r requirements.txt
```

### Issue: Settings not being loaded from `.env`

**Solution**: 
1. Ensure `.env` is in the project root directory
2. Check that file is named exactly `.env` (no extension)
3. Verify variable names match exactly (case-sensitive)
4. Restart the application after changing `.env`

### Issue: "Cannot connect to database"

**Solution**: Check MONGO_URI in `.env`:
1. Local: `MONGO_URI=mongodb://localhost:27017/`
2. Cloud: `MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/myschool`
3. Ensure MongoDB is running
4. Verify credentials are correct

### Issue: Port already in use

**Solution**: Change ports in `.env` or kill the process using the port

### Issue: Values in `.env` appear to not be updating

**Solution**: The application may be caching. Try:
1. Completely close the application
2. Edit `.env`
3. Restart the application

## How `config/config.py` Works

The config module:

1. Loads `.env` file using `python-dotenv`
2. Reads environment variables using `os.getenv()`
3. Provides default values if variable doesn't exist
4. Converts data types (string → bool/int/list)
5. Exports as module attributes for use in code

Example:
```python
# In config/config.py
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DEBUG = get_env_bool("DEBUG", True)
WINDOW_WIDTH = get_env_int("WINDOW_WIDTH", 400)
```

This means if `MONGO_URI` is not in `.env`, it defaults to `"mongodb://localhost:27017/"`

## Next Steps

- Copy `.env.example` to `.env` for custom setup
- Review the `.env` file and update settings as needed
- See [README.md](README.md) for installation and running instructions
- Refer to individual setting sections above for detailed explanations

For production deployments, follow the security best practices section above.

