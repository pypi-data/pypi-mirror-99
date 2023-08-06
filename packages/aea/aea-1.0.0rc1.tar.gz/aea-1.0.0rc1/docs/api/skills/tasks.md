<a name="aea.skills.tasks"></a>
# aea.skills.tasks

This module contains the classes for tasks.

<a name="aea.skills.tasks.Task"></a>
## Task Objects

```python
class Task(WithLogger)
```

This class implements an abstract task.

<a name="aea.skills.tasks.Task.__init__"></a>
#### `__`init`__`

```python
 | __init__(**kwargs: Any) -> None
```

Initialize a task.

<a name="aea.skills.tasks.Task.__call__"></a>
#### `__`call`__`

```python
 | __call__(*args: Any, **kwargs: Any) -> Any
```

Execute the task.

**Arguments**:

- `args`: positional arguments forwarded to the 'execute' method.
- `kwargs`: keyword arguments forwarded to the 'execute' method.
:return the task instance

**Raises**:

- `ValueError`: if the task has already been executed.

<a name="aea.skills.tasks.Task.is_executed"></a>
#### is`_`executed

```python
 | @property
 | is_executed() -> bool
```

Check if the task has already been executed.

<a name="aea.skills.tasks.Task.result"></a>
#### result

```python
 | @property
 | result() -> Any
```

Get the result.

:return the result from the execute method.

**Raises**:

- `ValueError`: if the task has not been executed yet.

<a name="aea.skills.tasks.Task.setup"></a>
#### setup

```python
 | setup() -> None
```

Implement the task setup.

**Returns**:

None

<a name="aea.skills.tasks.Task.execute"></a>
#### execute

```python
 | @abstractmethod
 | execute(*args: Any, **kwargs: Any) -> Any
```

Run the task logic.

**Returns**:

None

<a name="aea.skills.tasks.Task.teardown"></a>
#### teardown

```python
 | teardown() -> None
```

Implement the task teardown.

**Returns**:

None

<a name="aea.skills.tasks.init_worker"></a>
#### init`_`worker

```python
init_worker() -> None
```

Initialize a worker.

Disable the SIGINT handler of process pool is using.
Related to a well-known bug: https://bugs.python.org/issue8296

**Returns**:

None

<a name="aea.skills.tasks.TaskManager"></a>
## TaskManager Objects

```python
class TaskManager(WithLogger)
```

A Task manager.

<a name="aea.skills.tasks.TaskManager.__init__"></a>
#### `__`init`__`

```python
 | __init__(nb_workers: int = 2, is_lazy_pool_start: bool = True, logger: Optional[logging.Logger] = None, pool_mode: str = "multithread") -> None
```

Initialize the task manager.

**Arguments**:

- `nb_workers`: the number of worker processes.
- `is_lazy_pool_start`: option to postpone pool creation till the first enqueue_task called.
- `pool_mode`: str. multithread or multiprocess

<a name="aea.skills.tasks.TaskManager.is_started"></a>
#### is`_`started

```python
 | @property
 | is_started() -> bool
```

Get started status of TaskManager.

**Returns**:

bool

<a name="aea.skills.tasks.TaskManager.nb_workers"></a>
#### nb`_`workers

```python
 | @property
 | nb_workers() -> int
```

Get the number of workers.

**Returns**:

int

<a name="aea.skills.tasks.TaskManager.enqueue_task"></a>
#### enqueue`_`task

```python
 | enqueue_task(func: Callable, args: Sequence = (), kwargs: Optional[Dict[str, Any]] = None) -> int
```

Enqueue a task with the executor.

**Arguments**:

- `func`: the callable instance to be enqueued
- `args`: the positional arguments to be passed to the function.
- `kwargs`: the keyword arguments to be passed to the function.
:return the task id to get the the result.

**Raises**:

- `ValueError`: if the task manager is not running.

<a name="aea.skills.tasks.TaskManager.get_task_result"></a>
#### get`_`task`_`result

```python
 | get_task_result(task_id: int) -> AsyncResult
```

Get the result from a task.

**Returns**:

async result for task_id

<a name="aea.skills.tasks.TaskManager.start"></a>
#### start

```python
 | start() -> None
```

Start the task manager.

**Returns**:

None

<a name="aea.skills.tasks.TaskManager.stop"></a>
#### stop

```python
 | stop() -> None
```

Stop the task manager.

**Returns**:

None

