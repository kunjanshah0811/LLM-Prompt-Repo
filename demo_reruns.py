"""
Simple demo to understand Streamlit re-runs
Run this with: streamlit run demo_reruns.py
"""

import streamlit as st
import time
from datetime import datetime

st.title("🔄 Streamlit Re-run Demonstration")

# ============================================
# COUNTER - Shows how many times script runs
# ============================================
if 'run_count' not in st.session_state:
    st.session_state.run_count = 0
    
st.session_state.run_count += 1

st.markdown(f"""
### 📊 Script Execution Counter: `{st.session_state.run_count}`

**What this number means:** Every time this number increases, the **ENTIRE Python script** 
just executed from top to bottom!
""")

st.markdown("---")

# ============================================
# EXPERIMENT 1: Show the re-run
# ============================================
st.header("Experiment 1: Click and Watch")

st.markdown("""
**Instructions:** 
1. Watch the counter above
2. Click any button below
3. See the counter increase → that's a full script re-run!
""")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Button A"):
        st.success("You clicked A!")

with col2:
    if st.button("Button B"):
        st.success("You clicked B!")
        
with col3:
    if st.button("Button C"):
        st.success("You clicked C!")

st.markdown("**Every button click = Full script re-run!**")

st.markdown("---")

# ============================================
# EXPERIMENT 2: Terminal Output
# ============================================
st.header("Experiment 2: Check Your Terminal")

st.markdown("""
**Instructions:**
1. Look at the terminal/console where you ran `streamlit run demo_reruns.py`
2. Click the buttons below
3. Watch the terminal for messages
""")

# This prints to terminal EVERY TIME the script runs
print(f"⏰ [TERMINAL] Script executed at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")

if st.button("Click me and check terminal"):
    print("🔴 [TERMINAL] Button was clicked!")
    st.info("Check your terminal - you'll see timestamp and button message")

st.markdown("**Notice:** The timestamp prints on EVERY interaction, not just button clicks!")

st.markdown("---")

# ============================================
# EXPERIMENT 3: Variable Reset Problem
# ============================================
st.header("Experiment 3: Why Normal Variables Don't Work")

st.markdown("""
**The Problem:** Normal Python variables reset to their initial value on every re-run!
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ Normal Variable")
    
    # This ALWAYS starts at 0 because script re-runs!
    normal_counter = 0
    
    if st.button("Increment Normal"):
        normal_counter += 1
        print(f"🔴 [TERMINAL] Normal counter incremented to: {normal_counter}")
    
    st.error(f"Normal counter: {normal_counter}")
    st.caption("Always shows 0! It resets on every re-run.")

with col2:
    st.subheader("✅ Session State")
    
    # This persists across re-runs!
    if 'session_counter' not in st.session_state:
        st.session_state.session_counter = 0
    
    if st.button("Increment Session State"):
        st.session_state.session_counter += 1
        print(f"🟢 [TERMINAL] Session counter incremented to: {st.session_state.session_counter}")
    
    st.success(f"Session counter: {st.session_state.session_counter}")
    st.caption("Persists! Stored in session state.")

st.markdown("---")

# ============================================
# EXPERIMENT 4: Expensive Operations
# ============================================
st.header("Experiment 4: Caching for Performance")

st.markdown("""
**The Problem:** Without caching, expensive operations run on EVERY re-run!
""")

# Simulated expensive operation WITHOUT caching
def expensive_operation_no_cache():
    print("🔴 [TERMINAL] Running EXPENSIVE operation (no cache)...")
    time.sleep(1)  # Simulate slow operation
    return f"Result computed at {datetime.now().strftime('%H:%M:%S')}"

# Same operation WITH caching
@st.cache_data
def expensive_operation_with_cache():
    print("🟢 [TERMINAL] Running EXPENSIVE operation (cached)...")
    time.sleep(1)  # Simulate slow operation
    return f"Result computed at {datetime.now().strftime('%H:%M:%S')}"

col1, col2 = st.columns(2)

with col1:
    st.subheader("❌ No Cache")
    if st.button("Run Without Cache"):
        with st.spinner("Computing..."):
            result = expensive_operation_no_cache()
        st.warning(f"Result: {result}")
        st.caption("Takes 1 second EVERY time")

with col2:
    st.subheader("✅ With Cache")
    if st.button("Run With Cache"):
        with st.spinner("Computing..."):
            result = expensive_operation_with_cache()
        st.success(f"Result: {result}")
        st.caption("1 second first time, instant after!")

st.markdown("""
**Try this:**
1. Click "Run Without Cache" multiple times → Always takes 1 second
2. Click "Run With Cache" multiple times → Only first time takes 1 second
3. Check terminal to see when each actually runs!
""")

st.markdown("---")

# ============================================
# Summary
# ============================================
st.header("📝 Key Takeaways")

st.markdown("""
1. **Every interaction = Full script re-run** (by design)
2. **Normal variables reset** on every re-run
3. **Use `st.session_state`** to persist simple values
4. **Use `@st.cache_data`** to cache expensive computations
5. **Use `@st.cache_resource`** to cache connections/objects
6. **Check your terminal** to see what's actually running!

### How to Monitor Re-runs:

✅ Watch the script counter (top of page)  
✅ Add `print()` statements and check terminal  
✅ Use Streamlit's built-in profiler (hamburger menu)  
✅ Monitor database query logs  
""")

st.markdown("---")

# Footer with timestamp
st.caption(f"Current time: {datetime.now().strftime('%H:%M:%S.%f')[:-3]} | Script runs: {st.session_state.run_count}")