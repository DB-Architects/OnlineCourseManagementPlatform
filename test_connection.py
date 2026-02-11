import psycopg2
from psycopg2.extras import RealDictCursor

# Try different connection methods
configs = [
    {
        'name': 'Unix Socket (Recommended)',
        'config': {
            'user': '23CS30052',
            'password': '23CS30052',
            'database': '23CS30052',
            'host': '/var/run/postgresql',  # Unix socket
        }
    },
    {
        'name': 'IPv4 localhost',
        'config': {
            'host': '127.0.0.1',
            'user': '23CS30052',
            'password': '23CS30052',
            'database': '23CS30052',
            'port': 5432
        }
    },
    {
        'name': 'No host specified',
        'config': {
            'user': '23CS30052',
            'password': '23CS30052',
            'database': '23CS30052',
        }
    }
]

print("Testing different connection methods...\n")

working_config = None

for method in configs:
    print(f"Trying: {method['name']}...")
    try:
        conn = psycopg2.connect(**method['config'])
        print(f"✓ SUCCESS with {method['name']}!\n")
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Test query
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        tables = cursor.fetchall()
        print(f"✓ Found {len(tables)} tables:")
        for table in tables:
            print(f"  - {table['table_name']}")
        
        # Check Users
        cursor.execute("SELECT COUNT(*) as count FROM Users;")
        user_count = cursor.fetchone()
        print(f"\n✓ Users table has {user_count['count']} users")
        
        # Show users
        cursor.execute("SELECT user_id, name, email, role_type FROM Users;")
        users = cursor.fetchall()
        print("\nUsers in database:")
        for user in users:
            print(f"  ID: {user['user_id']}, Name: {user['name']}, Email: {user['email']}, Role: {user['role_type']}")
        
        cursor.close()
        conn.close()
        
        working_config = method['config']
        print(f"\n{'='*60}")
        print("WORKING CONFIGURATION:")
        print(f"{'='*60}")
        for key, value in method['config'].items():
            print(f"{key}: {value}")
        print(f"{'='*60}\n")
        break
        
    except Exception as e:
        print(f"✗ Failed: {e}\n")

if not working_config:
    print("❌ None of the connection methods worked!")
    print("\nTry running: psql -U 23CS30052 -d 23CS30052")
    print("If that works, the issue is with Python connection settings.")
else:
    print("✅ Use the working configuration above in your app_server.py")
