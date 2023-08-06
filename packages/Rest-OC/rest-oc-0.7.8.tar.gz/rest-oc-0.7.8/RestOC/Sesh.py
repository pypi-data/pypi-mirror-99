# coding=utf8
""" Sesh Module

Handles internal sessions shared across microservices
"""

__author__ = "Chris Nasr"
__copyright__ = "FUEL for the FIRE"
__version__ = "1.0.0"
__created__ = "2018-11-11"

# Python imports
import uuid

# Pip imports
from redis import StrictRedis

# Framework imports
from . import JSON, StrHelper

# Open redis connection
_moRedis = None
_muiExpire = 86400

def create(id = None, expires=None):
	"""Create

	Returns a brand new session using the ID given, if no ID is passed, one is
	generated

	Arguments:
		id (str): The ID to use for the session
		expires (uint): A specific expiry in seconds to override the global one
						for this session

	Returns:
		Session
	"""

	# Init the data
	dData = {}

	# If we have an expires time
	if expires:
		dData['__expire'] = expires

	# Create a new Session using a UUID as the id
	return _Session(id and id or uuid.uuid4().hex, dData)

def init(conf, expire=86400):
	"""Init

	Initialises the module

	Arguments:
		conf (dict): The necessary Redis config
		expire (uint): Length in seconds for the session to remain active

	Returns:
		None
	"""

	# Pull in the module variable
	global _moRedis, _muiExpire

	# Create the Redis connection
	_moRedis = StrictRedis(**conf)

	# Store the expire time
	_muiExpire = expire

def load(id):
	"""Load

	Loads an existing session from the cache

	Arguments:
		id (str): The unique id of an existing session

	Returns:
		Session
	"""

	# Fetch from Redis
	s = _moRedis.get(id)

	# If there's no session or it expired
	if s == None: return None

	# Make sure we have a string, not a set of bytes
	try: s = s.decode()
	except (UnicodeDecodeError, AttributeError): pass

	# Create a new instance with the decoded data
	return _Session(id, JSON.decode(s))

class _Session(object):
	"""Session

	A wrapper for the session data
	"""

	def __init__(self, id, data={}):
		"""Constructor

		Intialises the instance, which is just setting up the dict

		Arguments:
			id (str): The ID of the session
			data (dict): The data in the session

		Returns:
			Session
		"""
		self.__id = id
		self.__dStore = data

	def __contains__(self, key):
		"""__contains__

		True if the key exists in the session

		Arguments:
			key (str): The field to check for

		Returns:
			bool
		"""
		return key in self.__dStore

	def __delitem__(self, key):
		"""__delete__

		Removes a key from a session

		Arguments:
			key (str): The key to remove

		Returns:
			None
		"""
		del self.__dStore[key]

	def __getitem__(self, key):
		"""__getitem__

		Returns the given key

		Arguments:
			key (str): The key to return

		Returns:
			mixed
		"""
		return self.__dStore[key]

	def __iter__(self):
		"""__iter__

		Returns an iterator for the internal dict

		Returns:
			iterator
		"""
		return iter(self.__dStore)

	def __len__(self):
		"""__len__

		Return the length of the internal dict

		Returns:
			uint
		"""
		return len(self.__dStore)

	def __setitem__(self, key, value):
		"""__setitem__

		Sets the given key

		Arguments:
			key (str): The key to set
			value (mixed): The value for the key

		Returns:
			None
		"""
		self.__dStore[key] = value

	def __str__(self):
		"""__str__

		Returns a string representation of the internal dict

		Returns:
			str
		"""
		return str(self.__dStore)

	def close(self):
		"""Close

		Deletes the session from the cache

		Returns:
			None
		"""
		_moRedis.delete(self.__id)

	def extend(self):
		"""Extend

		Keep the session alive by extending it's expire time by the internally
		set expirty, or else by the global one set for the module

		Returns:
			None
		"""

		# Use internal time if we have one, else use the global
		iExpire = '__expire' in self.__dStore and \
					self.__dStore['__expire'] or \
					_muiExpire

		# Extend the session in Redis
		_moRedis.expire(self.__id, iExpire)

	def id(self):
		"""ID

		Returns the ID of the session

		Returns:
			str
		"""
		return self.__id

	def save(self):
		"""Save

		Saves the current session data in the cache

		Returns:
			None
		"""

		# Use internal time if we have one, else use the global
		iExpire = '__expire' in self.__dStore and self.__dStore['__expire'] or _muiExpire

		# Set the session in Redis
		_moRedis.setex(self.__id, _muiExpire, JSON.encode(self.__dStore))
