import streamlit as st
import subprocess

# Title
st.title("Cupcake Maker")

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
    if st.button("Disconnect from Cupcake Maker", key="disconnect_btn"):
        subprocess.run(["python", "stop.py"])  # Run stop script
        st.session_state["connected"] = False
        st.session_state["show_options"] = False
        st.session_state["disable_inputs"] = False
        st.warning("Disconnected!")
else:
    if st.button("Connect to Cupcake Maker", key="connect_btn"):
        subprocess.run(["python", "start.py"])  # Run start script
        st.session_state["connected"] = True
        st.session_state["show_options"] = True
        st.success("Connected!")

# Show options only if connected
if st.session_state["show_options"]:
    
    # Flavor selection (Disabled when process starts)
    flavor = st.selectbox("Select Cupcake Flavor", ["Pink", "Blue", "Green"], disabled=st.session_state["disable_inputs"])
    
    # Quantity input (Disabled when process starts)
    quantity = st.number_input("Enter Quantity", min_value=1, step=1, disabled=st.session_state["disable_inputs"])
    
    # Start Button
    if st.button("Start Making Cupcakes", key="start_btn", disabled=st.session_state["disable_inputs"]):
        if quantity:
            st.session_state["disable_inputs"] = True  # Disable input fields and button
            
            script_map = {"Pink": "pink.py", "Blue": "blue.py", "Green": "green.py"}
            script_path = script_map[flavor]
            
            # Read and modify the script
            with open(script_path, "r") as file:
                lines = file.readlines()
            
            # Update the `numcake` value
            for i in range(len(lines)):
                if lines[i].startswith("numcake"):
                    lines[i] = f"numcake = {quantity}\n"
            
            # Write back the modified script
            with open(script_path, "w") as file:
                file.writelines(lines)
            
            st.session_state["log"].append(f"Updated {script_path} with numcake = {quantity}")
            
            # Execute the script
            result = subprocess.run(["python", script_path], capture_output=True, text=True)
            
            # Show status updates
            st.session_state["log"].extend(result.stdout.split("\n"))
            
    # Display log
    log_area = st.empty()
    log_area.text("\n".join(st.session_state["log"]))
