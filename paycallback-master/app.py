import streamlit as st
from db import init, Counter

# Konfigurasi halaman
st.set_page_config(
    page_title="Counter App",
    page_icon="🔢",
    layout="centered"
)

# ======================
# Streamlit UI
# ======================
def main():
    # Inisialisasi database
    try:
        init()
    except Exception as e:
        st.error(f"Database initialization error: {e}")
        return
    
    # Header
    st.title("🔢 Counter App")
    st.markdown("---")
    
    # Ambil count saat ini
    try:
        total_count = Counter.get_total_count()
        all_counters = Counter.get_all()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
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
                st.success("Counter created!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    with col3:
        if st.button("🗑️ Clear All", use_container_width=True, type="secondary"):
            try:
                deleted = Counter.delete_all()
                st.success(f"Deleted {deleted} counters")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
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
                        st.error(f"Error: {e}")
            
            with col4:
                if st.button(f"🗑️", key=f"del_{counter['id']}", use_container_width=True):
                    try:
                        Counter.delete_by_id(counter['id'])
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")
            
            st.markdown("---")
    else:
        st.info("No counters yet. Click 'Add New Counter' to create one.")
    
    # Info tambahan
    with st.expander("ℹ️ Informasi"):
        st.markdown("""
        **Cara Penggunaan:**
        - **Add New Counter**: Buat counter baru dengan nilai awal 1
        - **Refresh**: Perbarui tampilan
        - **Clear All**: Hapus semua counter
        - **➕ (pada counter)**: Increment counter +1
        - **🗑️ (pada counter)**: Hapus counter tertentu
        
        Data disimpan di database (MySQL atau SQLite).
        
        **Environment Variables untuk MySQL:**
        - `MYSQL_USERNAME`: Username MySQL
        - `MYSQL_PASSWORD`: Password MySQL
        - `MYSQL_ADDRESS`: Host:Port MySQL (contoh: localhost:3306)
        - `MYSQL_DATABASE`: Nama database (default: nodejs_demo)
        
        Jika tidak ada env variables, akan menggunakan SQLite.
        """)
    
    # Footer
    st.markdown("---")
    st.caption("Counter App • Powered by Streamlit")

if __name__ == "__main__":
    main()