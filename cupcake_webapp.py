import streamlit as st
import subprocess

# Title
st.title("Cupcake Maker Automation 🍰")

# Initialize session state for connection, UI visibility, and input state
if "connected" not in st.session_state:
    st.session_state["connected"] = False
if "show_options" not in st.session_state:
    st.session_state["show_options"] = False
if "disable_inputs" not in st.session_state:
    st.session_state["disable_inputs"] = False
if "log" not in st.session_state:
    st.session_state["log"] = []

# Connect/Disconnect Button
if st.session_state["connected"]:
    if st.button("Disconnect from Cupcake Maker"):
        subprocess.run(["python", "stop.py"])  # Run stop script
        st.session_state["connected"] = False
        st.session_state["show_options"] = False
        st.session_state["disable_inputs"] = False
        st.session_state["log"].append("Disconnected!")
    else:
        st.info("Click 'Disconnect' to turn off the cupcake maker.")
else:
    if st.button("Connect to Cupcake Maker"):
        subprocess.run(["python", "start.py"])  # Run start script
        st.session_state["connected"] = True
        st.session_state["show_options"] = True
        st.session_state["log"].append("Connected!")
    else:
        st.warning("Click 'Connect' to turn on the cupcake maker.")

# Show options only if connected
if st.session_state["show_options"]:
    
    # Flavor selection (Disabled when process starts)
    flavor = st.selectbox(
        "Select Cupcake Flavor", 
        ["Pink", "Blue", "Green"], 
        disabled=st.session_state["disable_inputs"]
    )
    
  
    quantity = st.number_input("Enter Quantity", min_value=1, step=1, format="%d")

if st.button("Start Making Cupcakes"):
    # Convert to int in case
    quantity_int = int(quantity)

    # Now pass integer to update_and_run.py
    result = subprocess.run(
        ["python", "update_and_run.py", flavor.lower(), str(quantity_int)],
        capture_output=True,
        text=True
    )
    st.text_area("Cupcake Log:", result.stdout)

    # Start Button
    if st.button("Start Making Cupcakes", disabled=st.session_state["disable_inputs"]):
        if quantity > 0:
            # Disable input fields and button
            st.session_state["disable_inputs"] = True

            # Run the update_and_run.py script
            result = subprocess.run(
                ["python", "update_and_run.py", flavor.lower(), str(quantity)],
                capture_output=True, 
                text=True
            )

            # The flavor script's output (including the line from update_and_run.py that says "Updated X script with numcake = Y")
            output_lines = result.stdout.strip().split("\n")
            st.session_state["log"].extend(output_lines)

# Display log
st.text_area("Activity Log:", "\n".join(st.session_state["log"]), height=300)
