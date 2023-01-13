# QObservable

Easily add multithreading to your Python Qt app or plugin with an easy to use 
observable pattern.

## Work In Progress

Basic functionality is working, more advanced features are in progress:

- [x] QObservable executes in thread
- [ ] Ability to easily cancel running observable threads
- [ ] Pipe Operators for modifying observables
- [ ] Join Operators for combining arbitrary observables

## Basic Example

```python
from typing import Dict
import requests
from q_observable import QObservable, QSubscriberInterface

class Tool(QObject):
    
    def execute_async_op(self) -> None:
        def _subscriber_closure(subscriber: QSubscriberInterface) -> None:
            # this closure is executed in a thread
            try:
                response = requests.get(self._build_query())
                subscriber.next(response.json())
            except Exception as e:
                subscriber.error(e)
            subscriber.complete()  # not required if at end

        # these are executed in the main thread
        def on_next(response: Dict) -> None:
            print(f"Response: {response}")
        def on_error(err: Exception) -> None:
            print(f"Error: {err}")
        def on_compete() -> None:
            print("Done!")
    
        self._subscription = QObservable[Dict](_subscriber_closure).subscribe(
            # these are all optional
            next_fn=on_next,
            error_fn=on_error,
            complete_fn=on_compete,
        )
    
    def teardown(self) -> None:
        # stop listening but running threads keep running
        self._subscription.unsubscribe()
        self._subscription = None
```

Working Qt Application examples can be found in the [examples](./examples) directory.