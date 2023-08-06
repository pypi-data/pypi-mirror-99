import collections
import logging
import warnings
from typing import Dict, Callable, List, Optional

import rdflib
# Get the rdflib-jsonld capability initialized
# Note: this is for side effect. The parser is not used.
# The side effect is that the JSON-LD parser is registered in RDFlib.
from rdflib_jsonld import parser as jsonld_parser

from . import *
from .object import BUILDER_REGISTER

_default_bindings = {
    'sbol': SBOL3_NS,
    'prov': PROV_NS,
    'om': OM_NS,
    # Should others like SO, SBO, and CHEBI be added?
}


class Document:

    @staticmethod
    def register_builder(type_uri: str,
                         builder: Callable[[str, str], SBOLObject]) -> None:
        """A builder function will be called with an identity and a
        keyword argument type_uri.

        builder(identity_uri: str, type_uri: str = None) -> SBOLObject
        """
        Document._uri_type_map[type_uri] = builder

    # Map type URIs to a builder function to construct entities from
    # RDF triples.
    _uri_type_map: Dict[str, Callable[[str, str], Identified]] = BUILDER_REGISTER

    def __init__(self):
        self.logger = logging.getLogger(SBOL_LOGGER_NAME)
        self.objects: List[Identified] = []
        # Orphans are non-TopLevel objects that are not otherwise linked
        # into the object hierarchy.
        self.orphans: List[Identified] = []
        self._namespaces: Dict[str, str] = _default_bindings.copy()
        # Non-SBOL triples. These are triples that are not recognized as
        # SBOL. They are stored in _other_rdf for round-tripping purposes.
        self._other_rdf = rdflib.Graph()

    def _build_extension_object(self, identity: str, sbol_type: str,
                                types: List[str]) -> Optional[Identified]:
        custom_types = {
            SBOL_IDENTIFIED: CustomIdentified,
            SBOL_TOP_LEVEL: CustomTopLevel
        }
        if sbol_type not in custom_types:
            msg = f'{identity} has SBOL type {sbol_type} which is not one of'
            msg += f' {custom_types.keys()}. (See Section 6.11)'
            raise SBOLError(msg)
        # Look for a builder associated with one of the rdf:types.
        # If none of the rdf:types have a builder, use the sbol_type's builder
        builder = None
        build_type = None
        for type_uri in types:
            try:
                builder = self._uri_type_map[type_uri]
                build_type = type_uri
                break
            except KeyError:
                logging.warning(f'No builder found for {type_uri}')
        if builder is None:
            builder = custom_types[sbol_type]
            build_type = types[0]
        return builder(identity=identity, type_uri=build_type)

    def _build_object(self, identity: str, types: List[str]) -> Optional[Identified]:
        # Given an identity and a list of RDF types, build an object if possible.
        # If there is 1 SBOL type and we don't know it, raise an exception
        # If there are multiple types and 1 is TopLevel or Identified, then
        #    it is an extension. Use the other types to try to build it. If
        #    no other type is known, build a generic TopLevel or Identified.
        sbol_types = [t for t in types if t.startswith(SBOL3_NS)]
        if len(sbol_types) == 0:
            # If there are no SBOL types in the list. Ignore this entity.
            # Its triples will be stored in self._other_rdf later in the
            # load process.
            return None
        if len(sbol_types) > 1:
            # If there are multiple SBOL types in the list, raise an error.
            # SBOL 3.0.1 Section 5.4: "an object MUST have no more than one
            # rdfType property in the 'http://sbols.org/v3#' namespace"
            msg = f'{identity} has more than one rdfType property in the'
            msg += f' {SBOL3_NS} namespace.'
            raise SBOLError(msg)
        extension_types = {
            SBOL_IDENTIFIED: CustomIdentified,
            SBOL_TOP_LEVEL: CustomTopLevel
        }
        sbol_type = sbol_types[0]
        if sbol_type in extension_types:
            # Build an extension object
            types.remove(sbol_type)
            return self._build_extension_object(identity, sbol_type, types)
        else:
            try:
                builder = self._uri_type_map[sbol_type]
            except KeyError:
                logging.warning(f'No builder found for {sbol_type}')
                raise SBOLError(f'Unknown type {sbol_type}')
            obj = builder(identity=identity, type_uri=sbol_type)
            return obj

    def _parse_objects(self, graph: rdflib.Graph) -> Dict[str, SBOLObject]:
        # First extract the identities and their types. Each identity
        # can have either one or two rdf:type properties. If one,
        # create the entity. If two, it is a custom type (see section
        # 6.11 of the spec) and we instantiate it specially.
        #
        identity_types: Dict[str, List[str]] = collections.defaultdict(list)
        for s, p, o in graph.triples((None, rdflib.RDF.type, None)):
            str_o = str(o)
            str_s = str(s)
            identity_types[str_s].append(str_o)
        # Now iterate over the identity->type dict creating the objects.
        result = {}
        for identity, types in identity_types.items():
            obj = self._build_object(identity, types)
            if obj:
                obj.document = self
                result[obj.identity] = obj
        return result

    @staticmethod
    def _parse_attributes(objects, graph):
        for s, p, o in graph.triples((None, None, None)):
            str_s = str(s)
            str_p = str(p)
            try:
                obj = objects[str_s]
            except KeyError:
                # Object is not an SBOL object, skip it
                continue
            if str_p in obj._owned_objects:
                other_identity = str(o)
                other = objects[other_identity]
                obj._owned_objects[str_p].append(other)
            elif str_p == RDF_TYPE:
                # Handle rdf:type specially because the main type(s)
                # will already be in the list from the build_object
                # phase and those entries need to be maintained and
                # we don't want duplicates
                if o not in obj._properties[str_p]:
                    obj._properties[str_p].append(o)
            else:
                obj._properties[str_p].append(o)

    @staticmethod
    def _clean_up_singletons(objects: Dict[str, SBOLObject]):
        """Clean up singleton properties after reading an SBOL file.

        When an SBOL file is read, values are appended to the property
        stores without knowledge of which stores are singletons and
        which stores are lists. This method cleans up singleton properties
        by ensuring that each has exactly one value.
        """
        # This is necessary due to defaulting of properties when using
        # the builder. Some objects have required properties, which the
        # builder sets. In the case of singleton values, that can result
        # in multiple values in a singleton property. Only the first value
        # is used, so the value read from file is ignored.
        for _, obj in objects.items():
            for name, attr in obj.__dict__.items():
                if isinstance(attr, SingletonProperty):
                    prop_uri = attr.property_uri
                    store = attr._storage()
                    if len(store[prop_uri]) > 1:
                        store[prop_uri] = store[prop_uri][-1:]

    def clear(self) -> None:
        self.objects.clear()
        self._namespaces = _default_bindings.copy()

    def _parse_graph(self, graph) -> None:
        objects = self._parse_objects(graph)
        self._parse_attributes(objects, graph)
        self._clean_up_singletons(objects)
        # Validate all the objects
        # TODO: Where does this belong? Is this automatic?
        #       Or should a user invoke validate?
        # for obj in objects.values():
        #     obj.validate()
        # Store the TopLevel objects in the Document
        self.objects = [obj for uri, obj in objects.items()
                        if isinstance(obj, TopLevel)]
        # Gather Orphans for future writing.
        # These are expected to be non-TopLevel annotation objects whose owners
        # have no custom implementation (i.e. no builder registered). These objects
        # will be written out as part of Document.write_string()
        self.orphans = []
        for uri, obj in objects.items():
            if obj in self.objects:
                continue
            found = self.find(uri)
            if found:
                continue
            self.orphans.append(obj)
        # Store the namespaces in the Document for later use
        for prefix, uri in graph.namespaces():
            self.bind(prefix, uri)
        # Remove the triples for every object we have loaded, leaving
        # the non-RDF triples for round tripping
        # See https://github.com/SynBioDex/pySBOL3/issues/96
        for uri in objects:
            graph.remove((rdflib.URIRef(uri), None, None))
        # Now tuck away the graph for use in Document.write_string()
        self._other_rdf = graph

    def _guess_format(self, fpath: str):
        return rdflib.util.guess_format(fpath)

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read(self, location: str, file_format: str = None) -> None:
        if file_format is None:
            file_format = self._guess_format(location)
        if file_format is None:
            raise ValueError('Unable to determine file format')
        if file_format == SORTED_NTRIPLES:
            file_format = NTRIPLES
        graph = rdflib.Graph()
        graph.load(location, format=file_format)
        return self._parse_graph(graph)

    # Formats: 'n3', 'nt', 'turtle', 'xml'
    def read_string(self, data: str, file_format: str) -> None:
        # TODO: clear the document, this isn't append
        if file_format == SORTED_NTRIPLES:
            file_format = NTRIPLES
        graph = rdflib.Graph()
        graph.parse(data=data, format=file_format)
        return self._parse_graph(graph)

    def add(self, obj: TopLevel) -> None:
        """Add objects to the document.
        """
        if not isinstance(obj, TopLevel):
            message = f'Expected TopLevel instance, {type(obj).__name__} found'
            raise TypeError(message)
        found_obj = self.find(obj.identity)
        if found_obj is not None:
            message = f'An entity with identity "{obj.identity}"'
            message += ' already exists in document'
            raise ValueError(message)
        self.objects.append(obj)

        # Assign this document to the object tree rooted
        # in the TopLevel being added
        def assign_document(x: Identified):
            x.document = self
        obj.accept(assign_document)

    def _find_in_objects(self, search_string: str) -> Optional[Identified]:
        # TODO: implement recursive search
        for obj in self.objects:
            # TODO: needs an object.find(search_string) method on ... Identified?
            result = obj.find(search_string)
            if result is not None:
                return result
        return None

    def find(self, search_string: str) -> Optional[Identified]:
        """Find an object by identity URI or by display_id.

        :param search_string: Either an identity URI or a display_id
        :type search_string: str
        :returns: The named object or ``None`` if no object was found

        """
        for obj in self.objects:
            if obj.identity == search_string:
                return obj
            if obj.display_id and obj.display_id == search_string:
                return obj
        return self._find_in_objects(search_string)

    def write_string(self, file_format: str) -> str:
        graph = self.graph()
        if file_format == SORTED_NTRIPLES:
            # have RDFlib give us the ntriples as a string
            nt_text = graph.serialize(format='nt')
            # split it into lines
            lines = nt_text.splitlines(keepends=True)
            # sort those lines
            lines.sort()
            # write out the lines
            # RDFlib gives us bytes, so open file in binary mode
            result = b''.join(lines)
        elif file_format == JSONLD:
            context = {f'@{prefix}': uri for prefix, uri in self._namespaces.items()}
            context['@vocab'] = 'https://sbolstandard.org/examples/'
            result = graph.serialize(format=file_format, context=context)
        else:
            result = graph.serialize(format=file_format)
        return result.decode()

    def write(self, fpath: str, file_format: str = None) -> None:
        """Write the document to file.

        If file_format is None the desired format is guessed from the
        extension of fpath. If file_format cannot be guessed a ValueError
        is raised.
        """
        if file_format is None:
            file_format = self._guess_format(fpath)
        if file_format is None:
            raise ValueError('Unable to determine file format')
        with open(fpath, 'w') as outfile:
            outfile.write(self.write_string(file_format))

    def graph(self) -> rdflib.Graph:
        """Convert document to an RDF Graph.

        The returned graph is a snapshot of the document and will
        not be updated by subsequent changes to the document.
        """
        graph = rdflib.Graph()
        for prefix, uri in self._namespaces.items():
            graph.bind(prefix, uri)
        for orphan in self.orphans:
            orphan.serialize(graph)
        for obj in self.objects:
            obj.serialize(graph)
        # Add the non-SBOL RDF triples into the generated graph
        graph += self._other_rdf
        return graph

    def bind(self, prefix: str, uri: str) -> None:
        """Bind a prefix to an RDF namespace in the written RDF document.

        These prefixes make the written RDF easier for humans to read.
        These prefixes do not change the semantic meaning of the RDF
        document in any way.
        """
        # Remove any prefix referencing the given URI
        if uri in self._namespaces.values():
            for k, v in list(self._namespaces.items()):
                if v == uri:
                    del self._namespaces[k]
        self._namespaces[prefix] = uri

    def addNamespace(self, namespace: str, prefix: str) -> None:
        """Document.addNamespace is deprecated. Replace with Document.bind.

        Document.addNamespace existed in pySBOL2 and was commonly used.

        Document.addNamespace(namespace, prefix) should now be
        Document.bind(prefix, namespace). Note the change of argument
        order.
        """
        warnings.warn('Use Document.bind() instead', DeprecationWarning)
        self.bind(prefix, namespace)

    def validate(self, report: ValidationReport = None) -> ValidationReport:
        """Validate all objects in this document."""
        if report is None:
            report = ValidationReport()
        for obj in self.objects:
            obj.validate(report)
        return report

    def find_all(self, predicate: Callable[[Identified], bool]) -> List[Identified]:
        """Executes a predicate on every object in the document tree,
        gathering the list of objects to which the predicate returns true.
        """
        result: List[Identified] = []

        def wrapped_filter(visited: Identified):
            if predicate(visited):
                result.append(visited)
        self.accept(wrapped_filter)
        return result

    # TODO: Implement the visitor pattern allowing the user to specify
    #       a function to direct the search, instead of only doing
    #       depth-first search. For example, visit objects in provenance
    #       order using Identified.derived_from.
    # def accept_with_strategy(self, visitor: Callable, *, strategy: Callable = None):
    #     # Use the strategy to compute the set of objects to visit
    #     if strategy is None:
    #         visit_list = self.objects
    #     else:
    #         visit_list = self.find_all(strategy)
    #     while visit_list:
    #         for obj in visit_list:
    #             obj.accept(visitor)
    #         # Compute the next set of objects to visit
    #         if strategy is None:
    #             visit_list = []
    #         else:
    #             visit_list = self.find_all(strategy)

    def accept(self, visitor: Callable[[Identified], None]):
        """Implement the visitor pattern by invoking `visitor` on all
        top-level objects in the document. Those objects, in turn, will
        invoke `visitor` on all of their child objects.
        """
        for obj in self.objects:
            obj.accept(visitor)

    def builder(self, type_uri: str) -> Callable[[str, str], Identified]:
        """Lookup up the builder callable for the given type_uri.

        The builder must have been previously registered under this
        type_uri via Document.register_builder().

        :raises: ValueError if the type_uri does not have an associated
                 builder.
        """
        try:
            return self._uri_type_map[type_uri]
        except KeyError:
            raise ValueError(f'No builder for {type_uri}')
