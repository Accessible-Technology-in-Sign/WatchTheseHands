from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from config import DBLogin

class DashboardDB:
    def __init__(self):
        self.engine = None
        self.session = None
        self.connect()
    
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            connection_string = f'mysql+pymysql://{DBLogin.USER}:{DBLogin.PSWD}@localhost/labels'
            
            self.engine = create_engine(connection_string, echo=False)
            
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            print("Dashboard connected to MySQL database 'labels'")
            
        except SQLAlchemyError as e:
            print(f"Failed to connect to database: {e}")
            raise e
    
    def execute_query(self, query, params=None):
        """Execute a raw SQL query and return results"""
        try:
            result = self.session.execute(text(query), params or {})
            return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Query execution failed: {e}")
            return None
    
    def get_all_signs(self):
        """Get all unique signs from annotations"""
        query = "SELECT DISTINCT sign FROM annots ORDER BY sign"
        result = self.execute_query(query)
        if result:
            return [row[0] for row in result]
        return []
    
    def get_all_users(self):
        """Get all users from the users table"""
        query = "SELECT username FROM users ORDER BY username"
        result = self.execute_query(query)
        if result:
            return [row[0] for row in result]
        return []
    
    def get_labels_by_sign(self, sign=None):
        """Get label distribution for a specific sign or all signs"""
        if sign and sign != "All Signs":
            query = """
            SELECT label, COUNT(*) as count 
            FROM annots 
            WHERE sign = :sign 
            GROUP BY label 
            ORDER BY count DESC
            """
            params = {"sign": sign}
        else:
            query = """
            SELECT label, COUNT(*) as count 
            FROM annots 
            GROUP BY label 
            ORDER BY count DESC
            """
            params = {}
        
        result = self.execute_query(query, params)
        if result:
            return {row[0]: row[1] for row in result}
        return {}
    
    def get_labels_by_user(self, user=None):
        """Get label distribution for a specific user or all users"""
        if user and user != "All Users":
            query = """
            SELECT label, COUNT(*) as count 
            FROM annots 
            WHERE user = :user 
            GROUP BY label 
            ORDER BY count DESC
            """
            params = {"user": user}
        else:
            query = """
            SELECT label, COUNT(*) as count 
            FROM annots 
            GROUP BY label 
            ORDER BY count DESC
            """
            params = {}
        
        result = self.execute_query(query, params)
        if result:
            return {row[0]: row[1] for row in result}
        return {}
    
    def get_sign_stats(self, sign=None):
        """Get statistics for a specific sign"""
        if sign and sign != "All Signs":
            query = """
            SELECT 
                COUNT(*) as total_annotations,
                COUNT(DISTINCT user) as unique_users,
                COUNT(DISTINCT video_path) as unique_videos
            FROM annots 
            WHERE sign = :sign
            """
            params = {"sign": sign}
        else:
            query = """
            SELECT 
                COUNT(*) as total_annotations,
                COUNT(DISTINCT user) as unique_users,
                COUNT(DISTINCT video_path) as unique_videos
            FROM annots
            """
            params = {}
        
        result = self.execute_query(query, params)
        if result:
            row = result[0]
            return {
                'total_annotations': row[0],
                'unique_users': row[1],
                'unique_videos': row[2]
            }
        return {}
    
    def get_user_stats(self, user=None):
        """Get statistics for a specific user"""
        if user and user != "All Users":
            query = """
            SELECT 
                COUNT(*) as total_annotations,
                COUNT(DISTINCT sign) as unique_signs,
                COUNT(DISTINCT video_path) as unique_videos
            FROM annots 
            WHERE user = :user
            """
            params = {"user": user}
        else:
            query = """
            SELECT 
                COUNT(*) as total_annotations,
                COUNT(DISTINCT sign) as unique_signs,
                COUNT(DISTINCT video_path) as unique_videos
            FROM annots
            """
            params = {}
        
        result = self.execute_query(query, params)
        if result:
            row = result[0]
            return {
                'total_annotations': row[0],
                'unique_signs': row[1],
                'unique_videos': row[2]
            }
        return {}
    
    def close(self):
        """Close database connection"""
        if self.session:
            self.session.close()
        if self.engine:
            self.engine.dispose()

db = DashboardDB()
