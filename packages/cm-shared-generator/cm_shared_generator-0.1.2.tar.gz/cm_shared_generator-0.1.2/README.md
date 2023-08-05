# Python library : cm_shared_generator

### Resume

In python, it exist a generator type which can be really useful.

The `cm_shared_generator` library provide a Shared_Generator which share generator between thread and process safely.

### Install

#### Pre-required

###### Global requirements

- Python 3 (`sudo apt update && sudo apt install python3 -y`)

###### Install requirements

- Setuptools (`sudo apt update && sudo apt install python3-pip -y && pip3 install setuptools`)

###### Installation

```shell
python3 setup.py install
```

### Utilization

The utilization of the Shared_Generator is quite simple. Its prototype is like :

```python
Shared_Generator(self, arg_generator, DEFAULT_GENERATOR_TRAITMENT_FUNCTION=None, MAX_OBJECT_IN_QUEUE=len(os.sched_getaffinity(0)), TIMEOUT=None)
```

Its parameters are defined as :

- <u>Required</u> :
  - `arg_generator` -> The generator to shared
- <u>Optional</u> :
  - `DEFAULT_GENERATOR_TRAITMENT_FUNCTION`  (Default : None) -> Function to treat default type of value from the generator.
    Possible value : 
    - `Shared_Generator.DEFAULT_GENERATOR_TRAITMENT_CLASS` (Create a deep copy of the class before the insertion into the Queue).
    - Your own function !
  - `MAX_OBJECT_IN_QUEUE` (Default : Nb of logical processors) :	Defined the maximum of elements in the queue at the same time. ( > 0 )
  - `TIMEOUT` (Default : `Shared_Generator.DEFAULT_TIMEOUT`) : Defined the timeout of Semaphores.

###### Example :

```python
from cm_shared_generator import Shared_Generator

# Simple integer generator
def int_generator():
    i = 0
    while i<10:
        i+=1
        yield i
    return

my_shared_generator = Shared_Generator(int_generator, MAX_OBJECT_IN_QUEUE=2) # Creation of the generator with a Maximum lenght queue of 2

my_shared_generator.start(NEW_PROCESS=True) # Launch the generator in a new process

val = my_shared_generator.next() # Get the next value of the generator

my_shared_generator.stop() # Stop the generator
```

For more examples, check unit tests in [tests directory](./tests).