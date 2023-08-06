#############################################
# 			Shared_Generator CLASS 			#
#####				#####				#####
# Share a python generator between threads	#
# and process. 								#
#############################################

import copy
from multiprocessing import Process, Queue, Semaphore, Value
import os
from threading import Thread
import types

	  # ########################## #
######### Class declaration PART #########
	  # ########################## #

class Shared_Generator():

	DEFAULT_TIMEOUT = 1		# Default timeout of the Semaphore waiting by the producer
	DEFAULT_NUMBER_PUT_RETRY = 9 	# Default number of retry to acquire SEMAPHORE_PUT

	'''
		Goal : Share a python generator between threads
		Params :
			REQUIRED :
				arg_generator -> The generator to shared
			OPTIONAL :
				DEFAULT_GENERATOR_TRAITMENT_FUNCTION (Default : None) -> Function to treat default type of value from the generator.
					Possible value : 	- Shared_Generator.DEFAULT_GENERATOR_TRAITMENT_CLASS (Create a deep copy of the class before the insertion into the Queue).
										- Your own function !
				FORCE (Default : False) -> If True, the generator will be defined even his type is not a proper generator.
				NUMBER_PUT_RETRY (Default : None) -> Number of retry to acquire the semaphore which define if the generator process can continue to fill the Generator list before quitting timeout.
				MAX_OBJECT_IN_QUEUE (Default : Nb of logical processors) :	Defined the maximum of elements in the queue at the same time. ( > 0 )
				TIMEOUT (Default : Shared_Generator.DEFAULT_TIMEOUT) : Defined the timeout of Semaphores (The Shared_Generator will be stopped after (1+NUMBER_PUT_RETRY)*TIMEOUT if no process has taken a value from the generator.
	'''
	def __init__(self, arg_generator, DEFAULT_GENERATOR_TRAITMENT_FUNCTION=None, FORCE=False, NUMBER_PUT_RETRY=None, MAX_OBJECT_IN_QUEUE=len(os.sched_getaffinity(0)), TIMEOUT=0):

		if TIMEOUT is None or TIMEOUT > 0:
			self.TIMEOUT = TIMEOUT
		else :
			self.TIMEOUT = Shared_Generator.DEFAULT_TIMEOUT

		### GENERATOR VARIABLES ###
		# self.DEFAULT_GENERATOR_TRAITMENT_FUNCTION -> Function to use when the type is not known
		# self.GENERATOR -> The generator to share
		# self.MAX_OBJECT_IN_QUEUE -> Maximum number of objects took into the queue in the same time
		# self.NUMBER_PUT_RETRY -> Number of retry to acquire SEMAPHORE_PUT
		# self.QUEUE -> The queue which will contain every elements
		###

		if isinstance(arg_generator, types.FunctionType):
			arg_generator = arg_generator()
		if isinstance(arg_generator, types.GeneratorType):
			self.GENERATOR=arg_generator
		else:
			if not FORCE:
				raise TypeError(f"arg_generator must be a generator !")
			else:
				self.GENERATOR=arg_generator

		if MAX_OBJECT_IN_QUEUE > 0:
			self.MAX_OBJECT_IN_QUEUE = MAX_OBJECT_IN_QUEUE
			self.QUEUE = Queue(MAX_OBJECT_IN_QUEUE)
		else:
			raise ValueError(f"MAX_OBJECT_IN_QUEUE = {MAX_OBJECT_IN_QUEUE} (Must be > 0)")

		self.DEFAULT_GENERATOR_TRAITMENT_FUNCTION = DEFAULT_GENERATOR_TRAITMENT_FUNCTION
		if self.DEFAULT_GENERATOR_TRAITMENT_FUNCTION is not None and not isinstance(self.DEFAULT_GENERATOR_TRAITMENT_FUNCTION, types.FunctionType):
			self.DEFAULT_GENERATOR_TRAITMENT_FUNCTION = None

		if NUMBER_PUT_RETRY is None or not isinstance(NUMBER_PUT_RETRY, int):
			self.NUMBER_PUT_RETRY = Shared_Generator.DEFAULT_NUMBER_PUT_RETRY
		else:
			self.NUMBER_PUT_RETRY = NUMBER_PUT_RETRY

		### STATE VARIABLES ###
		# self.SEMAPHORE_PUT -> Semaphore which define if the generator reader is autorized to take new value in Queue
		# self.SEMAPHORE_READ -> Semaphore which define if a process is autorized to get value from Queue
		# self.GENERATOR_STATE -> Shared integer which define if the Generator is started or not (0 = Stopped)
		###

		self.SEMAPHORE_PUT = Semaphore(self.MAX_OBJECT_IN_QUEUE)
		self.SEMAPHORE_READ = Semaphore(0)

		self.GENERATOR_STATE = Value('i', 0)	# 0 : Stopped, 1 : Running
		

	  # ################## #
######### Principal PART #########
	  # ################## #

	'''
		Start the generator process/thread which will kill himself when the StopIteration will be reach OR the timeout of a Semaphore is reach OR stop function is call
		Params :
			OPTIONAL:
				NEW_PROCESS (Default : False) -> Define if the generator reader need to be launch in a new process or a new thread (True = Process, False = Thread)
	'''
	def start(self, NEW_PROCESS=False):
		if self.GENERATOR_STATE.value == 0 :
			try:
				self.GENERATOR_STATE.value = 1
				if NEW_PROCESS:
					Process(target=self._read_generator_process_, args=(self.GENERATOR,)).start()
				else:
					Thread(target=self._read_generator_process_, args=(self.GENERATOR,)).start()
			except Exception as e:
				self.GENERATOR_STATE.value = 0
				raise e

		else :
			print("[!] The shared generator is always running !")
			return False
		return True


	'''
		Stop the generator
	'''
	def stop(self):
		self.GENERATOR_STATE.value = 0


	'''
		Get the next value of the generator
	'''
	def next(self):
		if not self.is_alive() and self.QUEUE.empty():
			raise StopIteration

		if not self.SEMAPHORE_READ.acquire(timeout=self.TIMEOUT):
			if not self.is_alive() and self.QUEUE.empty():
				raise StopIteration
			else:
				return None

		data = self.QUEUE.get()

		self.SEMAPHORE_PUT.release()

		return data

	'''
		Test if the generator is started or not (True = Started)
	'''
	def is_alive(self):
		return self.GENERATOR_STATE.value != 0


	  # ################ #
######### Process PART #########
	  # ################ #

	'''
		Function of a thread/process to read the generator and take value in Queue
	'''
	def _read_generator_process_(self, arg_generator):

		while True:

			if not self.SEMAPHORE_PUT.acquire(timeout=self.TIMEOUT):
				i = 0
				state = False
				while i < self.NUMBER_PUT_RETRY and not state:
					if self.GENERATOR_STATE.value == 0:
						break
					state = self.SEMAPHORE_PUT.acquire(timeout=self.TIMEOUT)
					i+=1
				if not state:
					break
			if self.GENERATOR_STATE.value == 0:
				break

			try:
				val = next(arg_generator)
			except StopIteration:
				break

			type_val = type(val)
			if type_val is str:
				val = str(val)
			elif type_val is int:
				val = int(val)
			elif isinstance(val, list):
				val = list(val)
			elif isinstance(val, dict):
				val = dict(val)
			elif isinstance(val, tuple):
				val = tuple(val)
			elif self.DEFAULT_GENERATOR_TRAITMENT_FUNCTION is not None:
				val = self.DEFAULT_GENERATOR_TRAITMENT_FUNCTION(val)
			self.QUEUE.put(val)
			self.SEMAPHORE_READ.release()

		self.GENERATOR_STATE.value = 0


	  # ############################################## #
######### DEFAULT_GENERATOR_TRAITMENT_FUNCTIONs PART #########
	  # ############################################## #

	'''
		Default function for a class traitment (OPTIONAL utilisation)
	'''
	@staticmethod
	def DEFAULT_GENERATOR_TRAITMENT_CLASS(arg_value):
		return copy.deepcopy(arg_value)


	  # ############# #
######### END CLASS #########
	  # ############# #