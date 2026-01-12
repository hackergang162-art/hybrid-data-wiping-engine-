#!/usr/bin/env python3
"""
Database Migration Script for SecureWipe Platform
Handles migration from old database structure to new enhanced system
"""

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

class DatabaseMigrator:
    def __init__(self, db_path='instance/secure_wipe.db'):
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Connect to database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def backup_database(self):
        """Create backup of current database"""
        import shutil
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"instance/secure_wipe_backup_{timestamp}.db"
        
        try:
            shutil.copy2(self.db_path, backup_file)
            print(f"✓ Database backed up to: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"✗ Backup failed: {e}")
            return None
    
    def migrate_wipe_records(self):
        """Migrate existing wipe records to new structure"""
        cursor = self.conn.cursor()
        
        try:
            # Check if old table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='wipe_record'
            """)
            
            if not cursor.fetchone():
                print("ℹ No legacy WipeRecord table found, skipping migration")
                return True
            
            # Get all existing wipe records
            cursor.execute("SELECT * FROM wipe_record")
            records = cursor.fetchall()
            
            print(f"ℹ Found {len(records)} legacy wipe records")
            
            # Migrate each record
            migrated = 0
            for record in records:
                try:
                    cursor.execute("""
                        INSERT INTO wipe_history 
                        (user_id, filename, file_size, wipe_level, 
                         wipe_method, passes, status, timestamp, duration)
                        VALUES (1, ?, ?, ?, ?, 1, ?, ?, 0)
                    """, (
                        record['device_name'],
                        0,  # file_size
                        'military',
                        record.get('wipe_method', 'DoD 5220.22-M'),
                        record['status'],
                        datetime.fromisoformat(record['started_at'])
                    ))
                    migrated += 1
                except Exception as e:
                    print(f"✗ Error migrating record {record['id']}: {e}")
            
            self.conn.commit()
            print(f"✓ Successfully migrated {migrated} wipe records")
            return True
            
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            self.conn.rollback()
            return False
    
    def create_admin_user(self):
        """Create admin user if not exists"""
        from werkzeug.security import generate_password_hash
        
        cursor = self.conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM user WHERE username='admin'")
            if cursor.fetchone():
                print("ℹ Admin user already exists")
                return True
            
            admin_password = generate_password_hash('admin123')
            
            cursor.execute("""
                INSERT INTO user 
                (username, email, password_hash, is_admin, phone)
                VALUES (?, ?, ?, ?, ?)
            """, ('admin', 'diziavatar@gmail.com', admin_password, True, '+1234567890'))
            
            self.conn.commit()
            print("✓ Admin user created (username: admin, password: admin123)")
            return True
            
        except Exception as e:
            print(f"✗ Error creating admin user: {e}")
            self.conn.rollback()
            return False
    
    def initialize_new_schema(self):
        """Initialize new database schema"""
        cursor = self.conn.cursor()
        
        try:
            # Create user table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(256) NOT NULL,
                    is_admin BOOLEAN DEFAULT 0,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    phone VARCHAR(20),
                    notifications_enabled BOOLEAN DEFAULT 1
                )
            """)
            
            # Create wipe_history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS wipe_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    filename VARCHAR(255),
                    file_size INTEGER,
                    wipe_level VARCHAR(50),
                    wipe_method VARCHAR(100),
                    passes INTEGER,
                    status VARCHAR(50) DEFAULT 'completed',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    duration FLOAT,
                    data_type VARCHAR(50),
                    certificate_hash VARCHAR(128),
                    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
                )
            """)
            
            # Create payment table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payment (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    amount FLOAT NOT NULL,
                    currency VARCHAR(10) DEFAULT 'USD',
                    payment_method VARCHAR(50),
                    transaction_id VARCHAR(100) UNIQUE,
                    status VARCHAR(50) DEFAULT 'pending',
                    wipe_type VARCHAR(50),
                    file_count INTEGER DEFAULT 1,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
                )
            """)
            
            self.conn.commit()
            print("✓ New schema created successfully")
            return True
            
        except Exception as e:
            print(f"✗ Error creating schema: {e}")
            self.conn.rollback()
            return False
    
    def verify_migration(self):
        """Verify migration was successful"""
        cursor = self.conn.cursor()
        
        try:
            # Check user table
            cursor.execute("SELECT COUNT(*) as count FROM user")
            user_count = cursor.fetchone()['count']
            print(f"✓ Users: {user_count}")
            
            # Check payment table
            cursor.execute("SELECT COUNT(*) as count FROM payment")
            payment_count = cursor.fetchone()['count']
            print(f"✓ Payments: {payment_count}")
            
            # Check wipe_history table
            cursor.execute("SELECT COUNT(*) as count FROM wipe_history")
            wipe_count = cursor.fetchone()['count']
            print(f"✓ Wipes: {wipe_count}")
            
            return True
            
        except Exception as e:
            print(f"✗ Verification failed: {e}")
            return False
    
    def run_migration(self):
        """Run complete migration"""
        print("=" * 60)
        print("SecureWipe Database Migration")
        print("=" * 60)
        
        try:
            # Connect to database
            self.connect()
            print("✓ Connected to database")
            
            # Backup database
            if not self.backup_database():
                print("✗ Backup failed. Aborting migration.")
                return False
            
            # Create new schema
            if not self.initialize_new_schema():
                print("✗ Schema creation failed")
                return False
            
            # Create admin user
            if not self.create_admin_user():
                print("✗ Admin user creation failed")
                return False
            
            # Migrate existing data
            if not self.migrate_wipe_records():
                print("✗ Data migration failed")
                return False
            
            # Verify migration
            print("\n" + "=" * 60)
            print("Migration Summary")
            print("=" * 60)
            if not self.verify_migration():
                print("✗ Verification failed")
                return False
            
            print("\n" + "=" * 60)
            print("✓ Migration completed successfully!")
            print("=" * 60)
            print("\nDefault Admin Account:")
            print("  Username: admin")
            print("  Password: admin123")
            print("  Email: diziavatar@gmail.com")
            print("\n⚠️  IMPORTANT: Change the admin password in production!")
            
            return True
            
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            return False
        
        finally:
            self.disconnect()

def main():
    """Main entry point"""
    migrator = DatabaseMigrator()
    
    # Check if database exists
    if not Path('instance/secure_wipe.db').exists():
        print("✗ Database not found at instance/secure_wipe.db")
        print("   Run 'python app.py' to create the database first")
        sys.exit(1)
    
    # Ask for confirmation
    print("\n⚠️  WARNING: This will modify your database!")
    response = input("Continue with migration? (yes/no): ").strip().lower()
    
    if response != 'yes':
        print("Migration cancelled.")
        sys.exit(0)
    
    # Run migration
    success = migrator.run_migration()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
