import jumpcoin
import pyglet
if __name__ == "__main__":
    dime = jumpcoin.JumpCoin(
            "Dime",
            "/dev/ttyUSB0",
            9600,
            0x50,
            "kaching.wav",
            )
    pyglet.app.run()
    print("Done initializing coins in main.py")
