import abc
from typing import Coroutine, Any
import asyncio

"""
Описание задачи:
    Необходимо реализовать планировщик, позволяющий запускать и отслеживать фоновые корутины.
    Планировщик должен обеспечивать:
        - возможность планирования новой задачи
        - отслеживание состояния завершенных задач (сохранение результатов их выполнения)
        - отмену незавершенных задач перед остановкой работы планировщика
        
    Ниже представлен интерфейс, которому должна соответствовать ваша реализация.
    
    Обратите внимание, что перед завершением работы планировщика, все запущенные им корутины должны быть
    корректным образом завершены.
    
    В папке tests вы найдете тесты, с помощью которых мы будем проверять работоспособность вашей реализации
    
"""


class AbstractRegistrator(abc.ABC):
    """
    Сохраняет результаты работы завершенных задач.
    В тестах мы передадим в ваш Watcher нашу реализацию Registrator и проверим корректность сохранения результатов.
    """
    def __init__(self):
        self.values = []
        self.errors = []
    
    @abc.abstractmethod
    def register_value(self, value: Any) -> None:
        # Store values returned from done task
        self.values.append(value)

    @abc.abstractmethod
    def register_error(self, error: BaseException) -> None:
        # Store exceptions returned from done task
        self.errors.append(error)


class AbstractWatcher(abc.ABC):
    """
    Абстрактный интерфейс, которому должна соответсововать ваша реализация Watcher.
    При тестировании мы расчитываем на то, что этот интерфейс будет соблюден.
    """

    def __init__(self, registrator: AbstractRegistrator):
        self.registrator = registrator  # we expect to find registrator here


class StudentWatcher(AbstractWatcher):
    def __init__(self, registrator: AbstractRegistrator):
        super().__init__(registrator)
        self.running_tasks = []

    async def start(self) -> None:
        pass
    
    async def start_task(self) -> None:
        pass
    
    async def stop(self) -> None:
        # Your code goes here
        print('all tasks ', asyncio.all_tasks())
        # Your code goes here
        print('starting all tasks')
        
        for task in self.running_tasks:
            try:
                res = await task
                print('task res', res)
                self.registrator.register_value(res)
            except ValueError as e:
                print('task error', res)
                self.registrator.register_error(e)

        self.running_tasks = []

    def start_and_watch(self, coro: Coroutine) -> None:
        self.running_tasks.append(coro)