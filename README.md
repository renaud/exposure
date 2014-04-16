Exposure
========

Easily expose your python objects as a read-only REST service

### simple example

    import exposure
    ex = exposure.Exposure()
    mydict = {'banana': 'yellow', 'mango': 'yellow', 'apple': 'red'}
    ex.add(mydict, 'fruits')
    ex.start()

The objects are now accessible at:

* http://localhost:8888/ lists all available objects
* http://localhost:8888/ex/fruits returns the whold dictionary
* http://localhost:8888/ex/fruits/banana returns the corresponding key

See example.py for more advanced use
