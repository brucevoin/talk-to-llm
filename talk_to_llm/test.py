import streamlit as st

# Initialize the button state
button_state = False

# Display the button
if st.button("Start" if not button_state else "Stop"):
    # Toggle the button state
    button_state = not button_state

# Display the current button state
st.write(f"Button state: {'Start' if not button_state else 'Stop'}")