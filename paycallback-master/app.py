import streamlit as st
import os
import sqlite3
from typing import Optional
from contextlib import contextmanager

# Konfigurasi halaman
st.set_page_config(
    page_title="Counter App",
    page_icon="🔢",
    layout="centered"
)

# ======================
# Database Configuration
# ======================
# Baca konfigurasi database dari environment variables
MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME", "")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
MYSQL_ADDRESS = os.environ.get("MYSQL_ADDRESS", "")
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "nodejs_demo")

# Tentukan apakah menggunakan MySQL atau SQLite
USE_MYSQL = bool(MYSQL_USERNAME and MYSQL_PASSWORD and MYSQL_ADDRESS)

if USE_MYSQL:
    try:
        import pymysql
        # Parse host dan port dari MYSQL_ADDRESS
        if ":" in MYSQL_ADDRESS:
            MYSQL_HOST, MYSQL_PORT = MYSQL_ADDRESS.split(":")
            MYSQL_PORT = int(MYSQL_PORT)
        else:
            MYSQL_HOST = MYSQL_ADDRESS
            MYSQL_PORT = 3306
    except ImportError:
        st.error("PyMySQL not installed. Falling back to SQLite.")
        USE_MYSQL = False
else:
    # Fallback ke SQLite
    SQLITE_DB = "counter.db"

# ======================
# Database Connection
# ======================
@contextmanager
def get_db_connection():
    """Context manager untuk mendapatkan koneksi database"""
    if USE_MYSQL:
        conn = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USERNAME,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    else:
        conn = sqlite3.connect(SQLITE_DB)
        conn.row_factory = sqlite3.Row
    
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

# ======================
# Database Initialization
# ======================
def init_db():
    """Inisialisasi database dan buat tabel Counter jika belum ada"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        if USE_MYSQL:
            # MySQL syntax
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Counter (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    count INT NOT NULL DEFAULT 1,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """)
        else:
            # SQLite syntax
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Counter (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    count INTEGER NOT NULL DEFAULT 1,
                    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        conn.commit()

# ======================
# Counter Model Methods
# ======================
class Counter:
    """Model untuk tabel Counter"""
    
    @staticmethod
    def create(count: int = 1) -> int:
        """Buat record counter baru"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if USE_MYSQL:
                cursor.execute("INSERT INTO Counter (count) VALUES (%s)", (count,))
            else:
                cursor.execute("INSERT INTO Counter (count) VALUES (?)", (count,))
            
            return cursor.lastrowid
    
    @staticmethod
    def get_by_id(counter_id: int) -> Optional[dict]:
        """Ambil counter berdasarkan ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if USE_MYSQL:
                cursor.execute("SELECT * FROM Counter WHERE id = %s", (counter_id,))
                result = cursor.fetchone()
            else:
                cursor.execute("SELECT * FROM Counter WHERE id = ?", (counter_id,))
                row = cursor.fetchone()
                result = dict(row) if row else None
            
            return result
    
    @staticmethod
    def get_all() -> list:
        """Ambil semua counter"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Counter ORDER BY id")
            
            if USE_MYSQL:
                results = cursor.fetchall()
            else:
                rows = cursor.fetchall()
                results = [dict(row) for row in rows]
            
            return results
    
    @staticmethod
    def increment(counter_id: int) -> Optional[dict]:
        """Increment nilai count sebesar 1"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if USE_MYSQL:
                cursor.execute(
                    "UPDATE Counter SET count = count + 1, updatedAt = CURRENT_TIMESTAMP WHERE id = %s",
                    (counter_id,)
                )
            else:
                cursor.execute(
                    "UPDATE Counter SET count = count + 1, updatedAt = CURRENT_TIMESTAMP WHERE id = ?",
                    (counter_id,)
                )
            
            if cursor.rowcount > 0:
                return Counter.get_by_id(counter_id)
            return None
    
    @staticmethod
    def get_total_count() -> int:
        """Ambil total dari semua count"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(count) as total FROM Counter")
            
            if USE_MYSQL:
                result = cursor.fetchone()
                return result['total'] or 0
            else:
                row = cursor.fetchone()
                return row[0] if row and row[0] else 0
    
    @staticmethod
    def delete_all() -> int:
        """Hapus semua counter"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Counter")
            return cursor.rowcount
    
    @staticmethod
    def delete_by_id(counter_id: int) -> bool:
        """Hapus counter berdasarkan ID"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            if USE_MYSQL:
                cursor.execute("DELETE FROM Counter WHERE id = %s", (counter_id,))
            else:
                cursor.execute("DELETE FROM Counter WHERE id = ?", (counter_id,))
            
            return cursor.rowcount > 0

# ======================
# Streamlit UI
# ======================
def main():
    # Inisialisasi database
    try:
        init_db()
    except Exception as e:
        st.error(f"❌ Database initialization error: {e}")
        return
    
    # Header
    st.title("🔢 Counter App")
    
    # Info database
    db_type = "MySQL" if USE_MYSQL else "SQLite"
    st.caption(f"Using: {db_type}")
    
    st.markdown("---")
    
    # Ambil count saat ini
    try:
        total_count = Counter.get_total_count()
        all_counters = Counter.get_all()
    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
        return
    
    # Display total counter dengan style
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #f0f2f6; border-radius: 10px;'>
            <h1 style='font-size: 72px; margin: 0; color: #1f77b4;'>{total_count}</h1>
            <p style='font-size: 18px; color: #666; margin: 10px 0 0 0;'>Total Count</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tombol kontrol utama
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add New Counter", use_container_width=True, type="primary"):
            try:
                Counter.create(1)
                st.success("✅ Counter created!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear All", use_container_width=True, type="secondary"):
            try:
                deleted = Counter.delete_all()
                st.success(f"✅ Deleted {deleted} counters")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # Display individual counters
    if all_counters:
        st.markdown("---")
        st.subheader(f"📊 Individual Counters ({len(all_counters)})")
        
        for counter in all_counters:
            col1, col2, col3, col4 = st.columns([2, 3, 2, 2])
            
            with col1:
                st.metric("ID", counter['id'])
            
            with col2:
                st.metric("Count", counter['count'])
            
            with col3:
                if st.button(f"➕", key=f"inc_{counter['id']}", use_container_width=True):
                    try:
                        Counter.increment(counter['id'])
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            with col4:
                if st.button(f"🗑️", key=f"del_{counter['id']}", use_container_width=True):
                    try:
                        Counter.delete_by_id(counter['id'])
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
            
            st.markdown("---")
    else:
        st.info("ℹ️ No counters yet. Click 'Add New Counter' to create one.")
    
    # Info tambahan
    with st.expander("ℹ️ Informasi & Dokumentasi"):
        st.markdown("""
        ### 📖 Cara Penggunaan
        
        **Tombol Utama:**
        - **➕ Add New Counter**: Buat counter baru dengan nilai awal 1
        - **🔄 Refresh**: Perbarui tampilan data
        - **🗑️ Clear All**: Hapus semua counter dari database
        
        **Per Counter:**
        - **➕**: Increment counter +1
        - **🗑️**: Hapus counter tertentu
        
        ---
        
        ### 🗄️ Database
        
        Aplikasi ini support 2 tipe database:
        
        **1. SQLite (Default)**
        - Otomatis digunakan jika tidak ada MySQL config
        - File: `counter.db`
        - Cocok untuk development dan testing
        
        **2. MySQL (Production)**
        - Set environment variables berikut:
          - `MYSQL_USERNAME`: Username MySQL
          - `MYSQL_PASSWORD`: Password MySQL  
          - `MYSQL_ADDRESS`: Host:Port (contoh: localhost:3306)
          - `MYSQL_DATABASE`: Nama database (default: nodejs_demo)
        
        ---
        
        ### 🚀 Deployment
        
        **Streamlit Cloud:**
        1. Upload file ke GitHub
        2. Deploy di share.streamlit.io
        3. Tambahkan secrets untuk MySQL (optional)
        
        **Local:**
        ```bash
        pip install streamlit pymysql
        streamlit run app.py
        ```
        """)
    
    # Footer
    st.markdown("---")
    st.caption("Counter App • Powered by Streamlit • Database: " + db_type)

if __name__ == "__main__":
    main()
