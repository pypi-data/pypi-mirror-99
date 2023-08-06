########################################
# Testing file of the Shared_Generator #
########################################

from multiprocessing import Process
import unittest
from threading import Thread
import types

from cm_shared_generator import Shared_Generator


      # ########################## #
######### Class declaration PART #########
      # ########################## #

'''
    Mock of a Shared_Generator to get usefull protected values for tests
'''
class Mock_Shared_Generator(Shared_Generator):

    def get_queue(self):
        return self.QUEUE

    def get_generator_state_value(self):
        return self.GENERATOR_STATE.value


'''
    Simple class point to test if it pass throw the generator
'''
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add_x(self, inc): self.x += inc
    def add_y(self, inc): self.y += inc
    def __eq__(self, other): return self.x == other.x and self.y == other.y



class UT_Shared_Generator(unittest.TestCase):

      # ######################## #
######### Generator tests PART #########
      # ######################## #

    '''
        Function which test a Shared_Generator with the generator passed by parameter
    '''
    def _generator_func_test_(self, generator_func, DEFAULT_GENERATOR_TRAITMENT_FUNCTION=None):

        self.assertEqual(type(generator_func), types.FunctionType)

        # Creation of a normal and a Shared_Generator to compare their execution
        my_generator = generator_func()
        my_shared_generator = Mock_Shared_Generator(generator_func, DEFAULT_GENERATOR_TRAITMENT_FUNCTION=DEFAULT_GENERATOR_TRAITMENT_FUNCTION, MAX_OBJECT_IN_QUEUE=2)

        my_shared_generator.start()
        self.assertEqual(1, my_shared_generator.get_generator_state_value())
       
        my_generator_is_stopped = False
        my_shared_generator_is_stopped = False
        data_generator = 0

        # Test for every generation of each generator that they correspond #
        while True:
            try:
                data_generator = next(my_generator)
            except StopIteration:
                my_generator_is_stopped = True

            try:
                data_shared_generator = my_shared_generator.next()
                while data_shared_generator is None:
                    data_shared_generator = my_shared_generator.next()
            except StopIteration:
                my_shared_generator_is_stopped = True
                self.assertEqual(0, my_shared_generator.get_generator_state_value())

            self.assertEqual(data_generator, data_shared_generator) # Test if the data are the same one between the two generators

            if my_generator_is_stopped:
                try:
                    data_shared_generator = my_shared_generator.next()
                    while data_shared_generator is None:
                        data_shared_generator = my_shared_generator.next()
                except StopIteration:
                    my_shared_generator_is_stopped = True
                    self.assertEqual(0, my_shared_generator.get_generator_state_value())
            self.assertEqual(my_generator_is_stopped, my_shared_generator_is_stopped)

            if my_generator_is_stopped :
                break

        my_shared_generator.stop()

    '''
        Test the Shared_Generator with an Integer generator
    '''
    def test_with_int_generator(self):

        def int_generator(): # Generator int function useful for the test
            i = 0
            while i<10:
                i+=1
                yield i
            return

        self._generator_func_test_(int_generator)

    '''
        Test the Shared_Generator with a String generator
    '''
    def test_with_str_generator(self):

        def str_generator(): # Generator string function useful for the test
            str_base = "abcdefghij"
            str_send = ""
            i=0
            while i<len(str_base):
                str_send+=str_base[i]
                yield str_send
                i+=1
            return

        self._generator_func_test_(str_generator)

    '''
        Test the Shared_Generator with a List generator
    '''
    def test_with_list_generator(self):

        def list_generator(): # Generator list function useful for the test
            list_base = ['a', 3, 'b', 'e', 5, 'd', 'x', 8, 'p']
            list_send = []
            i=0
            while i<len(list_base):
                list_send.append(list_base[i])
                yield list_send
                i+=1
            return

        self._generator_func_test_(list_generator)

    '''
        Test the Shared_Generator with a Dict generator
    '''
    def test_with_dict_generator(self):

        def dict_generator(): # Generator dict function useful for the test
            dict_base = {'a' : 3, 'b' : 'e', 5 : 'd', 'x' : 8, 'p' : 'o'}
            dict_send = {}
            for key in dict_base:
                dict_send[key] = dict_base[key]
                yield dict_send
            return

        self._generator_func_test_(dict_generator)

    '''
        Test the Shared_Generator with a Tuple generator
    '''
    def test_with_tuple_generator(self):

        def tuple_generator(): # Generator tuple function useful for the test
            dict_base = {'a' : 3, 'b' : 'e', 5 : 'd', 'x' : 8, 'p' : 'o'}
            for key in dict_base:
                yield key, dict_base[key]
            return

        self._generator_func_test_(tuple_generator)

    '''
        Test the Shared_Generator with a Class generator
    '''
    def test_with_class_generator(self):

        def class_generator():
            point_send = Point(0, 0)
            i=0
            while i<10:
                point_send.add_x(1)
                point_send.add_y(2)
                yield point_send
                i+=1
            return

        self._generator_func_test_(class_generator, DEFAULT_GENERATOR_TRAITMENT_FUNCTION=Mock_Shared_Generator.DEFAULT_GENERATOR_TRAITMENT_CLASS)


      # ##################### #
######### Multiprocess PART #########
      # ##################### #

    '''
        Test the Shared_Generator with multiprocessing and multithreading
    '''
    def test_multiprocess(self):
        ### Parallel test with threads (Shared_generator read with thread then process) ###
        self._parallel_test_(False, False)
        self._parallel_test_(False, True)
        ### Parallel test with process (Shared_generator read with thread then process) ###
        self._parallel_test_(True, False)
        self._parallel_test_(True, True)

    '''
        Function which represent the work of threads and process
    '''
    def _process_tests_(self, shared_generator, tab):
        val = shared_generator.next()
        while val is None:
            val = shared_generator.next()
        self.assertEqual(val in tab, True)

    '''
        Tests of parallelisation
    '''
    def _parallel_test_(self, PROCESS=False, NEW_PROCESS=False):

        def int_generator(): # Generator int function useful for the test
            i = 0
            while i<10:
                i+=1
                yield i
            return

        my_generator = int_generator()
        listofvalues = []
        while True:
            try:
                listofvalues.append(next(my_generator))
            except StopIteration:
                break

        nb_values_waiting = len(listofvalues)
        self.assertNotEqual(nb_values_waiting, 0)

        my_shared_generator = Mock_Shared_Generator(int_generator, MAX_OBJECT_IN_QUEUE=2)
        my_shared_generator.start(NEW_PROCESS=NEW_PROCESS)

        i = 0
        l_parallel = []
        while i<nb_values_waiting:
            if PROCESS:
                l_parallel.append(Process(target=self._process_tests_, args=(my_shared_generator, listofvalues,)))
            else:
                l_parallel.append(Thread(target=self._process_tests_, args=(my_shared_generator, listofvalues,)))
            l_parallel[i].start()
            i+=1

        for t in l_parallel:
            t.join()

        self.assertEqual(len(l_parallel), nb_values_waiting)

        with self.assertRaises(StopIteration):
            my_shared_generator.next()


      # ###################################### #
######### Stop and Start generator test PART #########
      # ###################################### #

    '''
        Function which will test alternance of start and stop the shared_generator
    '''
    def test_start_stop_continue(self):

        def int_generator(): # Generator int function useful for the test
            yield 1
            yield 2
            yield 3
            yield 4
            return

        my_shared_generator = Mock_Shared_Generator(int_generator, MAX_OBJECT_IN_QUEUE=2)
        self.assertEqual(my_shared_generator.is_alive(), False)

        my_shared_generator.start()
        val = my_shared_generator.next()
        self.assertEqual(val, 1)
        self.assertEqual(my_shared_generator.is_alive(), True)

        my_shared_generator.stop()
        self.assertEqual(my_shared_generator.is_alive(), False)

        i = 2
        while not my_shared_generator.get_queue().empty():
            val = my_shared_generator.next()
            self.assertEqual(val, i)
            i+=1

        with self.assertRaises(StopIteration):
            val = my_shared_generator.next()

        my_shared_generator.start()
        self.assertEqual(my_shared_generator.is_alive(), True)

        val = my_shared_generator.next()
        self.assertEqual(val, i)

        my_shared_generator.stop()

      # ############# #
######### END TESTS #########
      # ############# #