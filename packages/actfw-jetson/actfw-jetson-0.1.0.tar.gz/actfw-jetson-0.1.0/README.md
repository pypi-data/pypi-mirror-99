# actfw-jetson

actfw's components for Jetson series.
actfw is a framework for Actcast Application written in Python.

## Installation

```console
sudo apt-get update
sudo apt-get install -y python3-pip python3-pil 

# Install GStreamer dependencies (some components in actfw-jetson uses GStreamer in implementation)
sudo apt-get install -y libgstreamer1.0-dev libgirepository1.0-dev ibgstreamer-plugins-base1.0-dev libglib2.0-dev libcairo2-dev

pip3 install actfw-jetson
```

## Document

- [API References](https://idein.github.io/actfw-jetson/latest/)

## Usage

See [actfw-core](https://github.com/Idein/actfw-core) for basic usage.

Since actfw-jetson uses GStreamer to implement some components, an application using actfw-jetson may have to initialize GStreamer library before using actfw-jetson's components.

```python
if __name__ == '__main__':
    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
    Gst.init(None)

    main()
```

actfw-jetson provides:

- `actfw_jetson.Display` : Display using `nvoverlaysink` element in [NVIDIA's Accelerated GStreamer](https://docs.nvidia.com/jetson/l4t/index.html#page/Tegra%20Linux%20Driver%20Package%20Development%20Guide/accelerated_gstreamer.html).

## Example

- `example/hello_jetson` : The simplest application example for Jetson
  - Use HDMI display as 1280x720 area
  - Generate 1280x720 single-colored image
  - Draw "Hello, Actcast!" text
  - Display it as 1280x720 image
  - Notice message for each frame
  - Support application heartbeat
  - Support "Take Photo" command
  - Depends: fonts-dejavu-core

## Development Guide

### Installation of dev requirements

```console
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install
```

### Running tests

```console
poetry run nose2 -v
```

### Running examples

#### hello_jetson

Displays a red rectangle and greeting text on it on HDMI display.

Run on a Jetson Nano connected to HDMI display:

```console
apt-get install fonts-dejavu-core
poetry run python example/hello_jetson
```

#### camera_display

Displays camera input on HDMI display.

Run on a Jetson Nano with CSI camera and HDMI display:

```console
poetry run python example/camera_display
```

### Releasing package & API doc

CI will automatically do.
Follow the following branch/tag rules.

1. Make changes for next version in `master` branch (via pull-requests).
2. Update `version` field in `pyproject.toml` with new version in `master` branch.
3. Create Git tag from `master` branch's HEAD named `release-<New version>`. E.g. `release-1.4.0`.
4. Then CI will build/upload package to PyPI & API doc to GitHub Pages.
