import asyncio
import json
from uuid import uuid4
import re

uuid_regex = re.compile("^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")


# def _safe_func_or_corout(func,*args):
#     """Call a function/coroutine safely inside/outside asyncio event loop
#     """
#     try:
#         loop = asyncio.get_event_loop()
#     except RuntimeError:
#         # Not in an event loop
#         if asyncio.iscoroutinefunction(func):
#             return asyncio.run(func(*args))
#         else:
#             return func(*args)
#     else:
#         # In an event loop
#         if asyncio.iscoroutinefunction(func):
#             loop.create_task(func(*args))
#         else:
#             loop.call_soon(func, *args)


def _safe_func_or_corout(func,*args):
    """Call a function/coroutine safely inside/outside asyncio event loop
    """
    if not asyncio.iscoroutinefunction(func):
        return func(*args)
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        return asyncio.run(func(*args))
    else:
        loop.create_task(func(*args))

def _is_beneath(a, b):
    """Is 'a' beneath 'b'?

    Args:
        a : string (path)
        b : string (path)

    Returns:
        bool: True if a is beneath (or equal to) b
    """

    # Everything is beneath the top ("")
    if (b==""):
        return True

    # If paths are both blank, they are equal
    if (b=="" and a==""):
        return True

    A = a.split(".")
    B = b.split(".")

    # A is not beneath B if any part is not the same
    while (len(A) > 0 and len(B) > 0):
        if (A.pop(0) != B.pop(0)):
            return False

    # A is not beneath B if B is longer
    if (len(B) > 0):
        return False

    return True



class EntangldError(Exception):
    """Entangld exception"""
    pass


class Entangld_Message:
    """Entangld message object.

    Args:
        data (dict): message data
        data.type (string): the type of entangld message
        [data.path] (string): the path against which the message is applied
        [data.uuid] (string): the uuid of the get/value or subscribe/event
        [data.value] (any|None): a data packet associated with the message
    """

    def __init__(self, data):

        self.type = data['type']

        try:
            self.path = data['path']
        except KeyError:
            self.path = None

        try:
            self.value = data['value']
        except KeyError:
            self.value = None

        try:
            self.uuid = data['uuid']
        except KeyError:
            self.uuid = None


    def __repr__(self):
        return "<Entangld_Message '{}' path '{}' (uuid: {})>".format(self.type,self.path,self.uuid)

    def __iter__(self):
        yield ('type', self.type)
        yield ('path', self.path)
        yield ('uuid', self.uuid)

        if type(self.value) is list:
            data = []
            for item in self.value:
                try:
                    json.dumps(item)
                    data.append(item)
                except TypeError:
                    data.append({})

            yield ('value', data)
        elif type(self.value) is dict:
            data = {}
            for key, item in self.value.items():
                try:
                    json.dumps(item)
                    data[key] = item
                except TypeError:
                    data[key] = {}

            yield ('value', data)
        else:
            yield ('value', self.value)

    @classmethod
    def get(cls,tree,get_params=None):
        """Construct a (remote) 'get' message

        Args:
            tree (string): the path of the get relative to the remote datastore
            [get_params=None] (any|None): parameters to pass to a function 'get'

        Returns:
            Entangld_Message: the 'get' message
        """
        return cls(dict(
            type = "get",
            path = tree,
            value = get_params,
            uuid = str(uuid4())
        ))

    @classmethod
    def value(cls,get_msg, value):
        """Construct a (remote) 'value' message

        Args:
            get_msg (Entangld_Message): the 'get' message to response to
            value (any|None): the data response to the 'get'

        Returns:
            Entangld_Message: the 'value' message
        """
        return cls(dict(
            type = "value",
            path = get_msg.path,
            value = value,
            uuid = get_msg.uuid
        ))

    @classmethod
    def setpush(cls,obj):
        """Construct a (remote) 'set'/'push' message

        Args:
            obj (dict): the parameter object
            obj.type (string): the type (must be 'set' or 'push')
            obj.path (string): the path against which the 'set'/'push' is applied
            obj.value (any|None): the value of the 'set'/'push'

        Returns:
            Entangld_Message: the 'set'/'push' message
        """
        if (not obj['type'] in ['set','push']):
            raise Exception("Invalid type ({}) for setpush".format(obj["type"]))
        return cls(obj)

    @classmethod
    def subscribe(cls, tree, uuid):
        """Construct a (remote) 'subscribe' message

        Args:
            tree (string): the path of the subscribe (relative to the remote store)
            uuid (sting): the uuid of the subscription

        Returns:
            Entangld_Message: the 'subscribe' message
        """
        return cls(dict(
            type = "subscribe",
            path = tree,
            uuid = uuid
        ))

    @classmethod
    def event(cls, path, value, uuid):
        """Construct a (remote) 'event' message

        Args:
            path (string): the path against which the event is occurring (relative to this datastore)
            uuid (string): the uuid of the subscription

        Returns:
            Entangld_Message: the 'event' message
        """
        return cls(dict(
            type = "event",
            path = path,
            value = value,
            uuid = uuid
        ))


    @classmethod
    def unsubscribe(cls, uuid):
        """Construct a (remote) 'unsubscribe' message

        Args:
            uuid (sting): the uuid of the subscription to unwatch

        Returns:
            Entangld_Message: the 'unsubscribe' message
        """
        return cls(dict(
            type = "unsubscribe",
            uuid = uuid
        ))

class Subscription:
    """A datastore Subscription object

    Args:
        obj (dict): the parameter object for construction
        obj.path (string): the path (relative to this store) of the subscription
        obj.uuid (string): the uuid of the subscription
        obj.callback (function): the callback function to be applied to matching
                                  event messages, signature 'callback(path, value)'
        [obj.downstream] (Entangld): the downstream datastore of the subscription
                                      (if applicable)
        [obj.upstream] (Entangld): the upstream datastore of the subscription
                                     (if applicable)
    """
    def __init__(self,obj):

        self.path = obj["path"]
        self.uuid = obj["uuid"]
        self._callback = obj["callback"]

        try:
            self.downstream = obj["downstream"]
        except:
            self.downstream = None

        try:
            self.upstream = obj["upstream"]
        except:
            self.upstream = None

    def __repr__(self):
        pt = ""
        if self.is_pass_through:
            pt = "Pass Through"
        hd = ""
        if self.has_downstream:
            hd = "Has Downstream"
        return "<Subscription against '{}' (uuid: {}) | {}>".format(self.path,self.uuid,", ".join([pt,hd]))

    def callback(self,path,value):
        """Make a subscription callback in the async loop

        Args:
            path (string): the path of the event (relative to this datastore)
            value (any|None): the value returned by the event
        """
        _safe_func_or_corout(self._callback,path,value)
        # if(asyncio.iscoroutinefunction(self._callback)):
        #     asyncio.run(self._callback(path, value))
        # else:
        #     self._callback(path, value)

    @property
    def is_pass_through(self):
        """Is this subscription a 'pass through' type?

        Pass throughs exist only to support daisy-chain subscriptions across
        multiple datastores, and are not really relevant to the operation of
        this particular datastore. Usually, the user shouldn't directly
        interact with pass through subscriptions.
        """
        return not (self.upstream is None)

    @property
    def has_downstream(self):
        """Does this subscription have a downstream datastore?

        This means that this subscription is not associated with the datastore
        where the path points to, and so it will be listening for event messages
        from other datastores.
        """
        return not (self.downstream is None)

    def matches_message(self, msg):
        """Does this subscription match a provided 'event'/'unsubscribe' message?

        Args:
            msg (Entangld_Message): the 'event'/'unsubscribe' message to check against

        Returns:
            bool: True if the message matches this subscription
        """
        return self.matches_uuid(msg.uuid)

    def matches_uuid(self,uuid):
        """Does this subscription match a provided subscription uuid?

        Args:
            uuid (string): the uuid of the subscription to check against

        Returns:
            bool: True if the message matches this uuid
        """
        return self.uuid == uuid

    def matches_path(self,path):
        """Does this subscription match a provided path?

        Args:
            path (string): the path (relative to this datastore) to check against

        Returns:
            bool - True if the message matches this path
        """
        return self.path == path

    def is_beneath(self,path):
        """Is this subscription beneath (or equal to) a provided path?

        I.e. provided path is 'system.voltage' and subscription is on 'system.voltage.unit'
        returns True.

        Args:
            path (string): the path to check against

        Returns:
            bool: True if the subscription is below the provided path
        """
        return _is_beneath(self.path, path)

    def is_above(self,path):
        """Is this subscription above (or equal to) a provided path?

        I.e. provided path is 'system.voltage.unit' and subscription is on 'system.voltage'
        returns True.

        Args:
            path (string): the path to check against

        Returns:
            bool: True if the subscription is above the provided path
        """
        return _is_beneath(path, self.path)



class Entangld:
    """Synchronized event store"""
    def __init__(self):
        self.stores = {}
        self.namespaces = {}
        self.local_data = {}
        self.requests = {}
        self.subscriptions = []
        self.__transmit_callback = None

    @staticmethod
    def extract_from_path(data, path):
        """Given a dictionary, extracts a child object using a string path.

        Args:
            data (dict): object to extract data from.
            path (string): path to find beneath data.

        Returns:
            tuple - tuple containing (result, remaining_path)
        """
        if not path:
            return (data, '')

        keys = path.split('.')
        while len(keys) > 0:
            key = keys.pop(0)
            try:
                data = data[key]
            except KeyError:
                return (None, '')

            if callable(data):
                return (data, '.'.join(keys))

        return (data, '')

    def namespace(self, obj):
        """Get namespace for a store.

        Args:
            obj (dict): object to get namespace of.

        Returns:
            string: namespace for the given context object.
        """
        return self.namespaces[obj]

    def attach(self, namespace, obj):
        """Attach a namespace and a store

        Args:
            namespace (string): a namespace for this store.
            obj (dict): context object associated with store.

        Raises:
            ValueError: namespace or obj is null/empty.
            EntangldError: tried to attach to a namespace twice.
        """
        if not namespace:
            raise ValueError('you cannot attach to a null or empty namespace')

        if not obj:
            raise ValueError('you cannot attach a null or empty object')

        if namespace in self.stores:
            raise EntangldError('you already attached to that namespace')

        # Register the store and namespace
        self.stores[namespace] = obj
        self.namespaces[obj] = namespace

        # Create an empty local node so the attach point is visible
        self.__set_local(namespace, {})

        # Find and update any subscriptions that fall beneath the new namespace
        func = lambda sub: sub.path.startswith(namespace)
        subs = list(filter(func, self.subscriptions))

        # Clean up old entries
        self.__unsubscribe(subs)

        # Re-subscribe
        for sub in subs:
            self.__subscribe(sub.path, sub.callback, sub.upstream, sub.uuid)

    def detach(self, namespace, obj):
        """Detach a namespace/object pair

        Args:
            namespace (string): the namespace
            obj (dict): the context object

        Raises:
            ValueError: only one parameter was passed
        """
        if not namespace and not obj:
            raise ValueError('must specify either obj or namespace')

        if not obj:
            obj = self.stores[namespace]

        if not namespace:
            namespace = self.namespac/es[obj]

        self.__set_local(namespace, None)

        del self.stores[namespace]
        del self.namespaces[obj]

    def transmit(self, func):
        """Attach a function to handle message transmission.

        Specify a callback to be used when transmitting data to another
        store. Callback will be passed (msg, obj) where msg is an object of
        type Entangld_Message and obj is the context object that should receive() it.

        Args:
            func (function): callback function.

        Raises:
            TypeError: func is not callable.
        """
        if not callable(func):
            raise TypeError('transmit function is not callable')

        self.__transmit_callback = func

    async def receive(self, msg, obj):
        """Call this function with data transmitted from a remote store.

        Args:
            msg (Entangld_Message): the entangld message that was received.
            obj (dict): the store context object where the message originated.

        Raises:
            EntangldError: unknown message type or invalid store
        """

        if(msg.type == 'set'):
            self.set(msg.path, msg.value)

        elif(msg.type == 'push'):
            self.push(msg.path, msg.value)

        elif(msg.type == 'get'):
            value = await self.get(msg.path, msg.value)
            response = Entangld_Message.value(msg, value)
            self.__transmit(response, obj)

        elif(msg.type == 'value'):
            future = self.requests[msg.uuid]
            future.set_result(msg.value)

        elif(msg.type == 'event'):
            if not obj:
                raise EntangldError('receive() called without obj')

            path = self.namespaces[obj] + '.' + msg.path

            count = 0
            for sub in self.subscriptions:
                if sub.matches_message(msg):
                    sub.callback(path,msg.value)
                    count += 1

            # No one is listening.
            # This may happen if an event triggers during unsubscribe.
            if count == 0:
                response = Entangld_Message.unsubscribe(msg.uuid)
                self.__transmit(response, obj)

        elif(msg.type == 'subscribe'):
            def callback(path, value):
                response = Entangld_Message.event(path,value,msg.uuid)
                self.__transmit(response, obj)

            self.__subscribe(msg.path, callback, obj, msg.uuid)

        elif(msg.type == 'unsubscribe'):
            self.__unsubscribe([sub for sub in self.subscriptions if sub.matches_message(msg)])

        else:
            raise EntangldError(f'Received unknown message: {str(msg)}')


    def receive_sync(self, msg, obj):
        """Synchronous version of .receive"""
        _safe_func_or_corout(self.receive, msg, obj)
        # loop = asyncio.get_event_loop()
        # loop.create_task(self.receive(msg, obj))

    async def push(self, path, value):
        """Push an object into a list in the store.

        Args:
            path (string): the path to set.
            value (any|None): the object to store at the path.

        Raises:
            EntangldError: object at path cannot be pushed to.
        """
        await self.set(path, value, 'push')

    def push_sync(self, path, value):
        """Synchronous version of .push"""
        _safe_func_or_corout(self.push, path, value)
        # asyncio.run(self.push(path, value))

    def set(self, path, value, op='set'):
        """Set an object into the store.

        Args:
            path (string): the path to set.
            value (any|None): the object or function to store at path.
            [op='set'] (string): type of operation. Defaults to 'set'.

        Raises:
            TypeError: path is not a string.
            EntangldError: unable to set object.
        """
        if not isinstance(path, str):
            raise TypeError('path must be a string')

        obj, namespace, tree = self.__get_remote_object(path)

        if obj is None:
            for namespace in self.stores:
                if namespace.startswith(path):
                    raise EntangldError(f'unable to overwrite remote store')

            self.__set_local(path, value, op)

            for sub in self.subscriptions:
                if sub.is_above(path):
                    sub.callback(path,value)


        else:
            msg = Entangld_Message.setpush(dict(
                type = op,
                path = tree,
                value = value
            ))
            self.__transmit(msg, obj)

    async def get(self, path='', params=None):
        """Get an object from the store.

        Args:
            [path=''] (string): the path to query.
            [params=None] (any|None): parameters to pass to fucntion 'get'

        Raises:
            TypeError: if path is not a string

        Returns:
            any: the value of the get
        """
        if not isinstance(path, str):
            raise TypeError('path must be a string')

        obj, _, tree = self.__get_remote_object(path)

        if obj is None:
            return await self.__get_local(path, params)
        else:
            return await self.__get_remote(tree, obj, params)

    def get_sync(self, path='', params=None):
        """Synchrones version of .get"""
        return _safe_func_or_corout(self.get, path, params)
        # return asyncio.run(self.get(path, params))

    def subscribe(self, path, func):
        """Subscribe to change events for a path.

        If objects at or below this path change, you will get a callback.

        Subscriptions to keys within attach()ed stores are remote subscriptions.
        If several stores are attached in some kind of arrangement, a given key
        may actually traverse multiple stores!  Since each store only knows its
        immediate neighbors - and has no introspection into those neighbors - each
        store is only able to keeps track of the neighbor on each side with
        respect to a particular path and has no knowledge of the eventual
        endpoints.  This means that subscribing across several datstores is accomplished
        by daisy-chaining 2-way subscriptions across each datastore interface.

        For example, let's suppose capital letters represent Entangld stores and
        lowercase letters are actual objects.  Then  the path "A.B.c.d.E.F.g.h"
        will represent a subscription that traverses four Entangld stores.
        From the point of view of a store in the middle - say, E - the "upstream"
        is B and the "downstream" is F.

        Each store involved keeps track of any subscriptions with which it is
        involved.  It tracks the upstream and downstream, and the uuid of the
        subscription.  The uuid is the same across all stores for a given
        subscription.  For a particular store, the upstream is null if it is the
        original link in the chain (called the 'head'), and the downstream is
        null if this store owns the endpoint value (called the 'tail'). Any
        subscription which is not the head of a chain is called a 'pass through'
        subscription, because it exist only to pass 'event' messages back up the
        chain to the head (where the user-provided callback function exists).
        subscriptions can be checked to see if they are 'pass through' type via
        the getter 'sub.is_pass_through'.

        Args:
            path (string): path to watch.
            func (function): callback function of the form (path, value)

        Returns:
            uuid: the uuid of the subscription
        """
        return self.__subscribe(path, func)

    def subscribed_to(self, path):
        """Check for existing subscriptions.

        Args:
            path (string): the subscription to check for.

        Returns:
            int: count of subscriptions matching path.
        """
        for sub in self.subscriptions:
            if sub.matches_path(path):
                return True

        return False

    def owned_subscriptions(path=""):
        """Get list of subscriptions (not included pass throughs)

        Can also provide a 'path' for which this method will search below.

        Args:
            [path=""] (string): a path to search below
        """
        return [sub for sub in self.subscriptions if sub.is_beneath(path)]

    def unsubscribe(self, path_or_uuid):
        """Unsubscribe to change events for a given path.

        Args:
            path_or_uuid (string): path or uuid to unwatch.

        Raises:
            EntangldError: no match found.

        Returns:
            int: number of subscriptions removed.
        """

        if uuid_regex.match(path_or_uuid):
            match = [
                sub for sub in self.subscriptions\
                if sub.matches_uuid(path_or_uuid) and not sub.is_pass_through
            ]
        else:
            match = [
                sub for sub in self.subscriptions\
                if sub.matches_path(path_or_uuid) and not sub.is_pass_through
            ]

        if len(match) == 0:
            raise EntangldError(f'unsubscribe found no matches for path {path}')

        self.__unsubscribe(match)

        return len(match)

    def unsubscribe_tree(self, path):
        """Remove any subscriptions beneath a path.

        Args:
            path (string): path to unwatch.

        Raises:
            EntangldError: subscription belongs to an attached store.
        """

        match = [
            sub for sub in self.subscriptions\
            if sub.is_beneath(path) and not sub.is_pass_through
        ]

        self.__unsubscribe(match)

        for sub in self.subscriptions:
            if sub.is_beneath(path):
                raise EntangldError('Unable to fully unsubscribe tree')

    def __transmit(self, msg, obj):
        """Send a message to another datastore

        Args:
            msg (Entangld_Message): the message to be sent
            obj (any|None): the context object which will .receive this message
        """
        _safe_func_or_corout(self.__transmit_callback, msg, obj)
        # # loop = asyncio.get_event_loop()
        # if(asyncio.iscoroutinefunction(self.__transmit_callback)):
        #     asyncio.run(self.__transmit_callback(msg, obj))
        #     # loop.create_task(self.__transmit_callback(msg, obj))
        # else:
        #     # loop.call_soon(self.__transmit_callback, msg, obj)
        #     self.__transmit_callback(msg, obj)

    def __get_remote_object(self, path):
        """If path contains a remote store return it as well at the relative
        path to the remote store.

        Example: let A,B be stores. If A.attach("some.path.to.B", B) then
        __get_remote_object("some.path.to.B.data") will return
        (B, "some.path.to.B", "data") and __get_remote_object("nonexistent.path")
        will return (None, None, path).

        Args:
            path (string): the path to investigate.

        Returns:
            tuple: tuple whose elements are (obj, namespace, relative_path).
        """
        for namespace, obj in self.stores.items():
            if path == namespace:
                return (obj, namespace, '')

            if path.startswith(namespace):
                return (obj, namespace, path.split('.', 1)[1])

        return (None, None, path)

    def __subscribe(self, path, func, upstream=None, uuid=None):
        """Create a subscription while specifying the upstream and uuid.

        Args:
            path (string): path to watch.
            func (function): callback function of the form (path, value).
            [upstream=None] (Entangld): Upstream store. Defaults to None.
            [uuid=None] (string): UUID for the subscription. Defaults to new uuid4().

        Raises:
            TypeError: if path is not a string

        Returns:
            uuid: the uuid of the subscription
        """
        if not isinstance(path, str):
            raise TypeError('Path must be a string')

        # prep uuid
        if uuid is None:
            _uuid = str(uuid4())
        else:
            _uuid = uuid

        obj, namespace, tree = self.__get_remote_object(path)

        new_sub = Subscription(dict(
            path = path,
            downstream = obj,
            upstream = upstream,
            uuid = _uuid,
            callback = func
        ))
        self.subscriptions.append(new_sub)

        if new_sub.has_downstream:
            msg = Entangld_Message.subscribe(tree, _uuid)
            self.__transmit(msg, obj)

        return _uuid

    def __unsubscribe(self, subscriptions):
        """Unsubscribe to change events.

        Args:
            subscriptions (Subscription[]): list of subscriptions to remove.
        """
        # Get a list of UUIDs to remove
        uuids = [sub.uuid for sub in subscriptions]

        # Remove the subscriptions
        self.subscriptions = [sub for sub in self.subscriptions if not (sub.uuid in uuids)]

        # Notify downstream of any deleted subscriptions that are remote
        for sub in subscriptions:
            if not sub.has_downstream:
                continue

            msg = Entangld_Message.unsubscribe(sub.uuid)
            self.__transmit(msg, sub.downstream)

    def __set_local(self, path, value, op='set'):
        """Sets object into local store.

        Args:
            path (string): the path at which to store the object.
            value (any|None): the data to store.
            [op="set"] (string): operation type. Defaults to 'set'.

        Raises:
            TypeError: path not a string, or root store not a dict.
            EntangldError: object does not support push.
        """
        if not isinstance(path, str):
            raise TypeError('Path must be a string')

        # Empty path means set root
        if not path:
            if not isinstance(value, dict):
                raise TypeError('Root store must be a dict')

            self.local_data = value
            return

        elements = path.split('.')
        last = elements.pop()
        pointer = self.local_data

        for element in elements:
            try:
                pointer = pointer[element]
            except KeyError:
                pointer[element] = {}
                pointer = pointer[element]

        # Handle unset
        if value is None:
            del pointer[last]
            return

        if op == 'push':
            try:
                pointer[last].append(value)
            except AttributeError:
                raise EntangldError('You cannot push to that object')
        else:
            try:
                pointer[last] = value
            except TypeError:
                pass

    async def __get_local(self, path, params=None):
        """Await data from local store

        Args:
            path (string): path to request
            [params=None] (any|None): Parameteres to pass to function 'get'. Defaults to None.

        Returns:
            any: data returned from the get
        """
        data, path = self.extract_from_path(self.local_data, path)
        if(asyncio.iscoroutinefunction(data)):
            # Create coroutine
            if params is None:
                coroutine = data()
            else:
                coroutine = data(params)

            # Wait for result
            loop = asyncio.get_event_loop()
            task = loop.create_task(coroutine)
            data = await task

        elif callable(data):
            if params is None:
                data = data()
            else:
                data = data(params)

        # Attempt to navigate any remaining path
        data, path = self.extract_from_path(data, path)

        return data

    async def __get_remote(self, tree, obj, params=None):
        """Await data from a remote store.

        Args:
            tree (string): path to request (relative to the remote datastore)
            obj ((Entangld|*)): remote store context.
            [param=None] (any|None): parameters to pass to function get.

        Returns:
            any: returned data.
        """
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        msg = Entangld_Message.get(tree, params)
        self.requests[msg.uuid] = future

        self.__transmit(msg, obj)
        await future

        return future.result()


async def test():
    # Basic use
    store = Entangld()

    # Simple set/get
    store.set('number.six', 6)
    value = await store.get('number.six')
    assert(value == 6)

    # Functions as values
    store.set('number.seven', lambda: 7)
    value = await store.get('number.seven')
    assert(value == 7)

    # Futures from functions
    async def eight():
        await asyncio.sleep(1)
        return 8

    store.set('number.eight', eight)
    value = await store.get('number.eight')
    assert(value == 8)

    # Dereference beneath functions
    store.set('eenie.meenie', lambda: {'miney': 'moe'})
    value = await store.get('eenie.meenie.miney')
    assert(value == 'moe')

    # Paired data stores
    parent = Entangld()
    child = Entangld()

    parent.attach('child', child)

    async def parent_transmit(msg, store):
        await child.receive(msg, parent)

    async def child_transmit(msg, store):
        await parent.receive(msg, child)

    parent.transmit(parent_transmit)
    child.transmit(child_transmit)

    child.set('system.voltage', 33)
    value = await parent.get('child.system.voltage')
    assert(value == 33)

    # Getter functions as RPC
    child.set('double.me', lambda x: x * 2)
    value = await parent.get('child.double.me', 2)
    assert(value == 4)

    # Pub/sub (remote events)
    def callback(path, value):
        assert(path == 'child.system.voltage')
        assert(value == 21)

    parent.subscribe('child.system.voltage', callback)
    child.set('system.voltage', 21)

    parent.unsubscribe('child.system.voltage')
    child.set('system.voltage', 0)

if __name__ == "__main__":
    asyncio.run(test())
