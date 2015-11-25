# main function to start Zero.
#
#
import sys
import zero

def main():
    z = zero.Zero()
    done = False
    print("running zero")
    while not done:
        z.run()
        done = z.isdone()

if __name__ == "__main__":
    main()
sys.exit()