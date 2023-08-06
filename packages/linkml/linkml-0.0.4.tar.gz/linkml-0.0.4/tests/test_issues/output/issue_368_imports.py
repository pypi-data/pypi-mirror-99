# Auto generated from issue_368_imports.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-03-24 16:47
# Schema: mixs
#
# id: https://microbiomedata/schema/mixs
# description:
# license:

import dataclasses
import sys
import re
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml.utils.slot import Slot
from linkml.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
if sys.version_info < (3, 7, 6):
    from linkml.utils.dataclass_extensions_375 import dataclasses_init_fn_with_kwargs
else:
    from linkml.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml.utils.formatutils import camelcase, underscore, sfx
from linkml.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml.utils.curienamespace import CurieNamespace


metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
DEFAULT_ = CurieNamespace('', 'https://microbiomedata/schema/mixs/')


# Types

# Class references



class ParentClass(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/mixs/ParentClass")
    class_class_curie: ClassVar[str] = None
    class_name: ClassVar[str] = "parent_class"
    class_model_uri: ClassVar[URIRef] = URIRef("https://microbiomedata/schema/mixs/ParentClass")


# Enumerations
class SampleEnum(EnumDefinitionImpl):

    pva = PermissibleValue(text="pva",
                             description="PVA description")
    pvb = PermissibleValue(text="pvb",
                             description="PVB description")

    _defn = EnumDefinition(
        name="SampleEnum",
    )

# Slots
class slots:
    pass

