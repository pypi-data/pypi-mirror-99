# SolarY
Welcome to SolarY, a small Open-Source Python library for asteroids, comets, meteoroids, meteors, cosmic dust and other minor bodies in the Solar System. This library is currently active and new modules are being developed and added frequently. Please check the library's main folder *solary/* for all available functions and sub-modules that are briefly described in the following.

To install the package simply run:

```
pip install solary
```

---

## asteroid
This sub-module contains asteroid relevant information like:
- Computation of the size of an asteroid depending on its albedo

## general
General applicable functions and classes for:
- Computation of the Tisserand Parameter of an object w.r.t. a larger object
- Computation of an object's Sphere of Influence
- Conversion of the apparent magnitude to irradiance
- Computation of an object's apparent magnitude
- Miscellaneous vector manipulation and computation functions

## instruments
A module to compute e.g., telescope properties and their corresponding observational performance:
- Camera
    - CCD
- Telescope:
    - Reflector

## neo
In this sub-module Near-Earth Object relevant functions can be found for e.g.:
- Downloading recent NEO data and creating a local SQLite database
- Downloading recent NEO simulation data and creating a local SQLite database

---

## Further contributions and the project's future
The functionality of the library is currently rather basic and more will be added frequently. New sub-modules will also include functionalities for *comets*, *meteors*, as well as *cosmic dust*. Spacecraft mission data (e.g., from Cassini's Cosmic Dust Analyzer or the Rosetta mission) shall be included, too to grant an easy access for all passionate citizen scientists and others.

---

## Collaboration & Questions
If you have any questions (e.g., how to use the package etc.) or if you would like to contribute something, feel free to contact me via [Twitter](https://twitter.com/MrAstroThomas) or [Reddit](https://www.reddit.com/user/MrAstroThomas).

The Dockerfile <i>Dockerfile_VSRemoteContainers</i> is a developer environment / setup that can be used to develop on SolarY. The IDE VS Code has an extension called <i>Remote-Containers</i> that supports one to create reproducible and system-independent environments (based on the Container ecosystem). To work with this work install:

- [Docker](https://www.docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com/)
    - Extension: [Remote-Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

The provided <i>.devcontainer/devcontainer.json</i> and <i>.vscode/settings.json</i> will then setup further extensions and settings within the container like e.g., the testing environment.