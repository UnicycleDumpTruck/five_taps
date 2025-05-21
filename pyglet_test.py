import pyglet
import time

# Load sound files
sound1 = pyglet.media.load('kaching.wav')
sound2 = pyglet.media.load('kaching.wav')

# Create players
player1 = pyglet.media.Player()
player2 = pyglet.media.Player()

# Queue sounds in players
player1.queue(sound1)
player2.queue(sound2)

# Play both players simultaneously
player1.play()
time.sleep(0.5)
player2.play()

# Keep the program running to allow audio to play
pyglet.app.run()
