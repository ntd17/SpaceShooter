# Space Shooter

Space Shooter is a 2D arcade-style shooting game built with Pygame. The player controls a spaceship at the bottom of the screen, shooting enemies that spawn from the top. The goal is to score as many points as possible by destroying enemies while avoiding losing all lives.

## Features

- Player movement using arrow keys (left and right)
- Shooting bullets to destroy enemies
- Enemies spawn continuously and move downward
- Collision detection between bullets and enemies
- Sound effects for shooting, explosions, and player death
- Background music during gameplay
- Game over screen with final score and option to restart

## Installation and Running

### Desktop

1. Ensure you have Python 3 installed.
2. Install Pygame (version 2.1.0 recommended):

```bash
pip install pygame==2.1.0
```

3. Run the game:

```bash
python app/main.py
```

### Android

The game can be built and packaged for Android using Buildozer.

1. Install Buildozer and dependencies (see [Buildozer documentation](https://buildozer.readthedocs.io/en/latest/)).
2. Build the APK:

```bash
buildozer android debug
```

3. Deploy to your device:

```bash
buildozer android deploy run
```

Alternatively, you can use the provided Docker container to build the Android package:

1. Build the Docker image:

```bash
docker build -t spaceshooter-build .
```

2. Run the container and build inside it:

```bash
docker run --rm -v $(pwd):/app spaceshooter-build buildozer android debug
```

## Controls

- Left Arrow: Move spaceship left
- Right Arrow: Move spaceship right
- Space: Shoot bullet
- R: Restart game after game over

## Assets

The game uses the following assets located in the `app/imgs` and `app/sounds` directories:

- Player, enemy, bullet, and background images
- Sound effects for shooting, explosions, and death
- Background music

## License and Credits

This project is open source. Feel free to use and modify it.

---

Enjoy playing Space Shooter!
