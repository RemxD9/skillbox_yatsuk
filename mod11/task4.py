import logging
import threading
import time
import queue
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Producer(threading.Thread):
    def __init__(self, priority_queue: queue.PriorityQueue, num_tasks):
        super().__init__()
        self.priority_queue = priority_queue
        self.num_tasks = num_tasks

    def run(self):
        logger.info("Producer: Running")
        for i in range(self.num_tasks):
            task = Task(random.randint(0, 10), f"Task {i}")
            self.priority_queue.put(task)
            logger.info(f"Producer: Added task {task}")
        logger.info("Producer: Done")


class Consumer(threading.Thread):
    def __init__(self, priority_queue: queue.PriorityQueue):
        super().__init__()
        self.priority_queue = priority_queue

    def run(self):
        logger.info("Consumer: Running")
        while True:
            task = self.priority_queue.get()
            if task is None:
                break
            logger.info(f"Running {task}. sleep({task.priority / 10})")
            time.sleep(task.priority / 10)
            self.priority_queue.task_done()
        logger.info("Consumer: Done")


class Task:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

    def __lt__(self, other):
        return self.priority > other.priority

    def __repr__(self):
        return f"Task(priority={self.priority}, name={self.name})"


def main():
    priority_queue = queue.PriorityQueue()
    num_tasks = 10

    producer = Producer(priority_queue, num_tasks)
    consumer = Consumer(priority_queue)

    producer.start()
    consumer.start()

    producer.join()
    priority_queue.join()

    priority_queue.put(None)
    consumer.join()


if __name__ == "__main__":
    main()
