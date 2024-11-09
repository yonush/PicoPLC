import iomapping as IO
import pyRTOS

def task1(self):    
    IO.QX0.value = False
    yield
    
    while True:
        IO.QX0.value = not IO.QX0.value
        yield [pyRTOS.timeout(1.3)]

def task2(self):
    IO.QX1.value = False
    yield
    
    while True:        
        IO.QX1.value = not IO.QX1.value        
        yield [pyRTOS.timeout(1.2)]
    
def task3(self):
    IO.QX2.value = False
    yield
    
    while True:
        IO.QX2.value = not IO.QX2.value
        yield [pyRTOS.timeout(1.15)]

def task4(self):
    IO.QX3.value = False
    yield
    
    while True:
        IO.QX3.value = not IO.QX3.value
        yield [pyRTOS.timeout(1.10)]

def task5(self):
    IO.QX4.value = False
    yield
    
    while True:
        IO.QX4.value = not IO.QX4.value
        yield [pyRTOS.timeout(1.05)]

def task6(self):
    IO.QX5.value = False
    yield
    
    while True:
        IO.QX5.value = not IO.QX5.value
        yield [pyRTOS.timeout(1)]

def task7(self):
    IO.QX6.value = False
    yield
    
    while True:
        IO.QX6.value = not IO.QX6.value
        yield [pyRTOS.timeout(0.95)]

def task8(self):
    IO.QX7.value = False
    yield
    
    while True:
        IO.QX7.value = not IO.QX7.value
        yield [pyRTOS.timeout(0.90)]



pyRTOS.add_task(pyRTOS.Task(task1))
pyRTOS.add_task(pyRTOS.Task(task2))
pyRTOS.add_task(pyRTOS.Task(task3))
pyRTOS.add_task(pyRTOS.Task(task4))
pyRTOS.add_task(pyRTOS.Task(task5))
pyRTOS.add_task(pyRTOS.Task(task6))
pyRTOS.add_task(pyRTOS.Task(task7))
pyRTOS.add_task(pyRTOS.Task(task8))


pyRTOS.start()

