import sys
import subprocess

def update_flavor_script(flavor, numcake):
    script_map = {
        "pink": "pink.py",
        "blue": "blue.py",
        "green": "green.py"
    }

    if flavor not in script_map:
        print("Invalid flavor selection!")
        return

    script_path = script_map[flavor]

    # Read and modify the script
    with open(script_path, "r") as file:
        lines = file.readlines()

    # Update the `numcake` value
    for i in range(len(lines)):
        if lines[i].startswith("numcake"):
            lines[i] = f"numcake = {numcake}\n"

    # Write back the modified script
    with open(script_path, "w") as file:
        file.writelines(lines)

    print(f"Updated {script_path} with numcake = {numcake}")

    # Execute the script automatically
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_and_run.py <flavor> <numcake>")
        sys.exit(1)

    flavor = sys.argv[1].lower()
    numcake = sys.argv[2]

    try:
        numcake = int(numcake)
        update_flavor_script(flavor, numcake)
    except ValueError:
        print("Please enter a valid integer for the number of cupcakes!")
