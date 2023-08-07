.. _using-sharedbuffers:

Using sharedbuffers
===================

This library implements shared-memory typed buffers that can be read and manipulated (and we'll eventually
support writes too) efficiently without serialization or deserialization.

The main supported implementation of obtaining shared memory is by memory-mapping files, but the library also supports
mapping buffers (anonymous mmap objects) as well, albeit they're harder to share among processes.

Supported primivite types:

    * int (up to 64 bit precision)
    * str (bytes)
    * unicode
    * frozenset
    * tuple / list
    * dict
    * buffer
    * date
    * datetime
    * numpy arrays
    * decimal

Primitive types can be cloned into their actual builtin objects (As specified by the mapped types), which is fast,
but potentially memory-intensive. In addition, they can be proxied, in which case they will be built directly
on top of the memory mapping, without the need for constructing the actual object. Proxied objects aim at supporting
the same interface as the builtin containers.

Objects can be registered with schema serializers and thus composite types can be mapped as well. For this to function
properly, objects need a class attribute specifying the attributes it holds and the type of the attributes. When an
attribute doesn't have a clearly defined type, it can be wrapped in a RTTI-containing container by specifying it as
type `object`.

For example:

.. code:: python

    class SomeStruct(object):
        __slot_types__ = {
            'a' : int,
            'b' : float,
            's' : str,
            'u' : unicode,
            'fset' : frozenset,
            'l' : list,
            'o' : object,
        }
        __slots__ = __slot_types__.keys()

Adding `__slot_types__`, however, isn't enough to make the object mappable. A schema definition needs to be created,
which can be used to map files or buffers and obtain proxies to the information within:

.. code:: python

    class SomeStruct(object):
        __slot_types__ = {
            'a' : int,
            'b' : float,
            's' : str,
            'u' : unicode,
            'fset' : frozenset,
            'l' : list,
            'o' : object,
        }
        __slots__ = __slot_types__.keys()
        __schema__ = mapped_struct.Schema.from_typed_slots(__slot_types__)

Using the schema is thus straightforward:

.. code:: python

    s = SomeStruct()
    s.a = 3
    s.s = 'blah'
    s.fset = frozenset([1,3])
    s.o = 3
    s.__schema__.pack(s) # returns a bytearray

    buf = bytearray(1000)

    # writes in offset 10 of buf, returns the size of the written object
    s.__schema__.pack_into(s, buf, 10)

    # returns a proxy for the object just packed into buf, does not deserialize
    p = s.__schema__.unpack_from(s, buf, 10)

    print p.a
    print p.s
    print p.fset

.. _composite-types:

Declaring compound types
------------------------

Typed objects can be nested, but for that a typecode must be assigned to each type in order for `RTTI` to properly
identify the custom types:

.. code:: python

    SomeStruct.__mapped_type__ = mapped_struct.mapped_object.register_schema(
        SomeStruct, SomeStruct.__schema__, 'S')

From then on, `SomeStruct` can be used as any other type when declaring field types.

.. _container-structures:

Container structures
--------------------

High-level typed container_ classes can be created by inheriting the proper base class.

The API for these high-level container objects is aimed at collections that don't really fit in RAM in their
pure-python form, so they must be built using an iterator over the items (ideally a generator that doesn't
put the whole collection in memory at once), and then mapped from the resulting file or buffer.

Currently, there are three kind of mappings supported: string-to-object, uint-to-object and a generic object-to-object.
The first two are provided for efficiency's sake; use the generic one when the others won't do.

.. code:: python

    class StructArray(mapped_struct.MappedArrayProxyBase):
        schema = SomeStruct.__schema__
    class StructNameMapping(mapped_struct.MappedMappingProxyBase):
        IdMapper = mapped_struct.StringIdMapper
        ValueArray = StructArray
    class StructIdMapping(mapped_struct.MappedMappingProxyBase):
        IdMapper = mapped_struct.NumericIdMapper
        ValueArray = StructArray
    class StructObjectMapping(mapped_struct.MappedMappingProxyBase):
        IdMapper = mapped_struct.ObjectIdMapper
        ValueArray = StructArray

An example:

.. code:: python

    with tempfile.NamedTemporaryFile() as destfile:
        arr = StructArray.build([SomeStruct(), SomeStruct()], destfile=destfile)
        print arr[0]

    with tempfile.NamedTemporaryFile() as destfile:
        arr = StructNameMapping.build(dict(a=SomeStruct(), b=SomeStruct()).iteritems(), destfile=destfile)
        print arr['a']

    with tempfile.NamedTemporaryFile() as destfile:
        arr = StructIdMapping.build({1:SomeStruct(), 3:SomeStruct()}.iteritems(), destfile=destfile)
        print arr[3]

.. _idmap-usage:

When using nested hierarchies, it's possible to unify references to the same object by specifying an `idmap` dict.
However, since the idmap will map objects by their `id()`, objects must be kept alive by holding references to
them while they're still referenced in the idmap, so its usage is non-trivial. An example technique:

.. code:: python

    def all_structs(idmap):
        iter_all = iter(some_generator)
        while True:
            idmap.clear()

            sstructs = list(itertools.islice(iter_all, 10000))
            if not sstructs:
                break

            for ss in sstructs :
                # mapping from "s" attribute to struct
                yield (ss.s, ss)
            del sstructs

    idmap = {}
    name_mapping = StructNameMapping.build(all_structs(idmap),
        destfile = destfile, idmap = idmap)

The above code syncs the lifetime of objects and their idmap entries to avoid mapping issues. If the invariant
isn't maintained (objects referenced in the idmap are alive and holding a unique `id()` value), the result will be
silent corruption of the resulting mapping due to object identity mixups.

There are variants of the mapping proxy classes and their associated id mapper classes that implement multi-maps.
That is, mappings that, when fed with multiple values for a key, will return a list of values for that key rather
than a single key. Their in-memory representation is identical, but their querying API returns all matching values
rather than the first one, so multi-maps and simple mappings are binary compatible.

Multi-maps with string keys can also be approximate, meaning the original keys will be discarded and the mapping will
only work with hashes, making the map much faster and more compact, at the expense of some inaccuracy where the
returned values could have extra values corresponding to other keys whose hash collide with the one being requested.

Running tests
-------------

Running tests can be done locally or on docker, using the script `run-tests.sh`:

.. code:: shell

  $> virtualenv venv
  $> . venv/bin/activate
  $> sh ./run-tests.sh


Alternatively, running it on docker can be done with the following command:

.. code:: shell

  $> docker run -v ${PWD}:/opt/sharedbuffers -w /opt/sharedbuffers python:2.7 /bin/sh run-tests.sh

.. _container: https://en.wikipedia.org/wiki/Container_(abstract_data_type)
