# einsteinify
A pip moudle that transforms every C #include absolute path to a given directory to a relative path to the .c or .h file

## Install

You can install einsteinify with pip:

```sh
$ pip install einsteinify
```

## Project purpose

It may happen that you have a folder with `.c` and `.h` files where some the `#include "*.h"` are **global paths** to respect to the root folder. This module makes them **relative paths** to the root folder.

## Usage

```python
from einsteinify import einsteinify

PATH = 'path/to/root/folder'

einsteinify(PATH)
```

## Result

Suppose that you have a directory like this:

```
root
 ├── main.h
 ├── other.h
 ├─> services
 │   └── services.h
 └─> utils
     └── utils.h
```

Where initially:

**main.h**

```c
#include "root/other.h"
#include "root/services/services.h"
```

**other.h**

```c
#include "root/utils/utils.h"
```

**utils.h**

```c
#include "root/other.h"
#include "root/services/services.h"
```

After running **einsteinify** the includes would be:

**main.h**

```c
#include "./other.h"
#include "./services/services.h"
```

**other.h**

```c
#include "./utils/utils.h"
```

**utils.h**

```c
#include "./other.h"
#include "../services.h"
```
