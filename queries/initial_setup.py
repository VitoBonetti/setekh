queries = [
    """CREATE TABLE roles (
        uuid CHAR(36) PRIMARY KEY,
        roles VARCHAR(100) UNIQUE NOT NULL
    ) ENGINE=InnoDB""",

    """CREATE TABLE users (
        uuid CHAR(36) PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        is_confirmed BOOLEAN DEFAULT TRUE,
        is_active BOOLEAN DEFAULT FALSE,
        2fa_active BOOLEAN DEFAULT FALSE,
        2fa_secret VARCHAR(64),
        session_id CHAR(36),
        session_expires_at DATETIME
    ) ENGINE=InnoDB""",

    """CREATE TABLE blocks (
        uuid CHAR(36) PRIMARY KEY,
        block VARCHAR(150) UNIQUE NOT NULL,
        code VARCHAR(5) UNIQUE NOT NULL,
        language VARCHAR(100) DEFAULT 'English',
        description TEXT,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_by CHAR(36) NOT NULL,
        FOREIGN KEY (created_by) REFERENCES users(uuid)
    ) ENGINE=InnoDB"""
]
