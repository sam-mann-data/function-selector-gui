numcake = 20

def make_cupcakes():
    global numcake
    if numcake:
        print(f"Manufacturing {numcake} blue cupcakes!")
    else:
        print("Error: No number of cupcakes provided.")

if __name__ == "__main__":
    make_cupcakes()
