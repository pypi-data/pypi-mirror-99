# Welcome to OpenRPA

_Pixel based RPA automation library_

OpenRPA is a Robot Framework library that can automate desktop
tasks with state of the art AI. OpenRPA is totally free for use in
commercial and non-commercial applications. Development is sponsored 
by Robocorp with a long term agreement.

OpenRPA development started in 2019 and now - 2 years later - we are
publishing the results by making all components available as a seamless
automation library.

Current components:

- Text detection
- Text recognition
- Image detection
- Controller primitives for mouse and keyboard

Integration roadmap

- Locator query language and NLP
- Extracting and classification of user interface elements

Library is available for

- Windows
- MacOS
- Linux

### Keywords

```
Click Word  pattern
Click Image  filename
```

### Examples of Locator Query Language (LQL)

```
Type Text  Customer id  12345
Mouse Left Click  Description  To Right
Mouse Left Click  money.png  Close to Submit
```

## Installation

```
channels:
  - conda-forge
  - pytorch
  - fcakyon
dependencies:
  - python=3.7.5
  - python-mss=6.1.0
  - numpy=1.20.1
  - craft-text-detector=0.3.3
  - tesseract=4.1.1
  - pytesseract=0.3.7
  - opencv=4.5.1
  - regex=2020.11.13
  - pynput=1.7.1
  - pyobjc-core=6.2.2
```