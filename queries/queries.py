# INITIAL SETUP

CREATE_ROLES_TABLE = "CREATE TABLE roles (uuid CHAR(36) PRIMARY KEY, roles VARCHAR(100) UNIQUE NOT NULL) ENGINE=InnoDB"
CREATE_USER_TABLE = ("CREATE TABLE users (uuid CHAR(36) PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL, "
                     "password VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                     "is_confirmed BOOLEAN DEFAULT TRUE, is_active BOOLEAN DEFAULT FALSE, "
                     "is_master BOOLEAN DEFAULT FALSE, 2fa_active BOOLEAN DEFAULT FALSE, "
                     "2fa_secret VARCHAR(64), session_id CHAR(36), session_expires_at DATETIME) ENGINE=InnoDB")
CREATE_BLOCKS_TABLE = ("CREATE TABLE blocks (uuid CHAR(36) PRIMARY KEY, block VARCHAR(150) UNIQUE NOT NULL, "
                       "code VARCHAR(5) UNIQUE NOT NULL, language VARCHAR(100) DEFAULT 'English', description TEXT, "
                       "is_active BOOLEAN DEFAULT TRUE, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                       "created_by CHAR(36) NOT NULL, FOREIGN KEY (created_by) REFERENCES users(uuid)) ENGINE=InnoDB")

CREATE_CONFIG_TABLE = ("CREATE TABLE initialconfig (uuid CHAR(36) PRIMARY KEY, secret BOOLEAN DEFAULT FALSE, "
                       "initialdb BOOLEAN DEFAULT FALSE, email BOOLEAN DEFAULT FALSE, masteruser BOOLEAN DEFAULT FALSE, "
                       "deploydb BOOLEAN DEFAULT FALSE) ENGINE=InnoDB ")

INITIAL_QUERIES = [CREATE_ROLES_TABLE, CREATE_USER_TABLE, CREATE_BLOCKS_TABLE, CREATE_CONFIG_TABLE]

# === SESSION ===

UPDATE_SESSION = "UPDATE users SET session_id = %s, session_expires_at = %s WHERE uuid = %s"
CHECK_SESSION = "SELECT session_expires_at, is_master FROM users WHERE uuid = %s AND session_id = %s"
DELETE_SESSION = "UPDATE users SET session_id = NULL, session_expires_at = NULL WHERE uuid = %s"

# === MASTER USER ==

INITIALIZATION_MASTER = ("INSERT INTO users (uuid, email, password, is_confirmed, is_active, is_master, 2fa_active, 2fa_secret) "
                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")

# == CONFIG TABLE ==

INITIAL_CONFIG_TABLE = ("INSERT INTO initialconfig (uuid, secret, initialdb, masteruser) "
                 "VALUES (%s, TRUE, TRUE, TRUE)")
SELECT_CONFIG_UUID = "SELECT uuid FROM initialconfig LIMIT 1"
UPDATE_INITIAL_CONFIG = "UPDATE initialconfig SET email = TRUE WHERE uuid = %s"

# == USERS ==
LAST_2FA = "SELECT uuid, 2fa_secret FROM users ORDER BY created_at DESC LIMIT 1"
USER_IS_ACTIVE = "UPDATE users SET is_active = TRUE WHERE uuid = %s"
