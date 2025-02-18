numcake = 2

def make_cupcakes():
    global numcake
    if numcake:
        print(f"Manufacturing {numcake} green cupcakes!")
    else:
        print("Error: No number of cupcakes provided.")

if __name__ == "__main__":
    make_cupcakes()
