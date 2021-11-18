# -*- coding: utf-8 -*-

from enum import Enum
from typing import Union
from datetime import date, datetime

class CamlFilterDataType(Enum):
    """ Enumeration qui définit les différents type de données. """
    Text = 'Text'
    Int = 'Integer'
    Datetime = 'DateTime'
    Float = 'Number'
    Bool = 'Boolean'    # not used => Integer 0/1

class CamlOperatorType(Enum):
    """ Enumeration qui définit comment on doit filtrer les résultats. """
    BeginsWith = 'BeginsWith'
    """ Chaine de caractères commençant par """
    Contains = 'Contains'
    """ Chaine de caractères contenant"""
    Equal = 'Eq'
    """ Equal"""
    Different = 'Neq'
    """ Différent """
    GreaterOrEqual = 'Geq'
    """ Supérieur ou égal"""
    Greater = 'Gt'
    """ Supérieur """
    InList = 'In'
    """ Contenu dans une liste de valeurs """
    LowerOrEqual = 'Leq'
    """ Inférieur ou égal"""
    Lower = 'Lt'
    """ Inférieur """
    IsNull = 'IsNull'
    """ vide """
    IsNotNull = 'IsNotNull'
    """ non vide """

class CamlBlock():
    """ Définit un bloc de filtres.

    :param tuple args: des blocs ou des filtres à ajouter à ce bloc

    """
    def __init__(self, head:str, tail:str, *args) -> None:
        self.head = head
        self.tail = tail
        self._blocks = []
        if (args is not None):
            self._blocks.extend(args)

    def add(self, block):
        """ Ajoute un bloc ou un filtre à ce bloc.

        :param Union[CamlBlock, CamlFilter] filter_or_block: le bloc ou le filtre à ajouter
        """
        self._blocks.append(block)

    def __str__(self) -> str:
        result = self.head
        for block in self._blocks:
            result += str(block)
        result += self.tail
        return result

class CamlOperator(CamlBlock):
    def __init__(self, operator_type:CamlOperatorType, *args) -> None:
        super().__init__('<{0}>'.format(operator_type.value), '</{0}>'.format(operator_type.value), *args)

class CamlAnd(CamlBlock):
    """ Représente un bloc logique ET. Tous ses blocs ou filtres devront être satisfaits pour que l'élément soit retourné.

    :param tuple args: des blocs ou des filtres à ajouter à ce bloc
    """
    def __init__(self, *args) -> None:
        super().__init__('<And>', '</And>', *args)

class CamlField(CamlBlock):
    def __init__(self, *args) -> None:
        super().__init__('<FieldRef Name="', '" />', *args)

class CamlFilter():
    """ Définit un filtre sur une propriété d'une liste.

    :param CamlOperatorType operator_type: le type de filtre à appliquer
    :param str field_name: le nom de la propriété à filtrer
    :param tuple args: les paramètres de filtre. Généralement, une seule valeur.
    """

    def __init__(self, operator_type:CamlOperatorType, field_name:str, *args) -> None:

        self.field_block = CamlField(field_name)

        if (len(args) == 0):    
            #
            # no arg : isNull, isNotNull operator
            #
            self.value_blocks = None
            self.operator_block = CamlOperator(operator_type, self.field_block)
        elif (len(args) == 1):
            #
            # 1 arg : equal, notEqual, lower, ... operators
            #
            self.value_blocks = CamlValue(args[0])
            self.operator_block = CamlOperator(operator_type, self.field_block, self.value_blocks)
        else:
            #
            # multiples values : inList, includes, notIncludes operators
            #
            self.value_blocks = CamlValues(*[CamlValue(arg) for arg in args])
            self.operator_block = CamlOperator(operator_type, self.field_block, self.value_blocks)

    def __str__(self) -> str:
        return str(self.operator_block)

class CamlOr(CamlBlock):
    """ Représente un bloc logique OU. Un de ses blocs ou filtres devra être satisfait pour que l'élément soit retourné.

    :param tuple args: des blocs ou des filtres à ajouter à ce bloc
    """
    def __init__(self, *args) -> None:
        super().__init__('<Or>', '</Or>', *args)

class CamlValue(CamlBlock):
    def __init__(self, *args) -> None:
        
        value = args[0]
        value_type = None
        if (isinstance(value, str)):
            value_type = CamlFilterDataType.Text.value
        elif (isinstance(value, bool)):
            value = 1 if value else 0
            value_type = CamlFilterDataType.Int.value
        elif (isinstance(value, int)):
            value_type = CamlFilterDataType.Int.value
        elif (isinstance(value, float)):
            value_type = CamlFilterDataType.Float.value
        elif (isinstance(value, date) and not(isinstance(value, datetime))):
            value = value.isoformat()
            value_type = CamlFilterDataType.Datetime.value
        elif (isinstance(value, datetime)):
            value = value.replace(microsecond=0).isoformat()
            value_type = CamlFilterDataType.Datetime.value

        if (value_type == 'DateTime' and len(value) > 10):
            super().__init__('<Value IncludeTimeValue="TRUE" Type="{0}">'.format(value_type), '</Value>', value)
        elif (value_type == 'DateTime'):
            super().__init__('<Value IncludeTimeValue="FALSE" Type="{0}">'.format(value_type), '</Value>', value)
        else:
            super().__init__('<Value Type="{0}">'.format(value_type), '</Value>', value)

class CamlValues(CamlBlock):
    def __init__(self, *args) -> None:
        super().__init__('<Values>', '</Values>', *args)

class CamlWhere(CamlBlock):
    """ Représente la clause WHERE dans sa globalité.

    :param Union[Block, Filter] filter_or_block: un bloc ou un filtre
    """
    def __init__(self, filter_or_block:Union[CamlBlock, CamlFilter]) -> None:
        super().__init__('<Where>', '</Where>', filter_or_block)
        self._order_by_field_name = None
        self._order_by_ascending = None

    def orderBy(self, field_name:str, ascending:bool=True):
        """ Spécifie si un tri doit être appliqué sur les éléments qui vérifient les différents filtres.

        :param str field_name: le nom de la propriété qui servira de filtre
        :param bool ascending: indique si le filtre doit se faire dans l'ordre croissant ou décroissant
        """
        self._order_by_field_name = field_name
        self._order_by_ascending = ascending

        return self

    @property
    def query_text(self) -> str:
        """ Retourne la requête au format CAML à utiliser pour filtrer les éléments d'une liste SharePoint.

        :returns: la requête xml au format CAML
        :rtype: str
        """
        query = super().__str__()
        if (self._order_by_field_name is not None):
            query += '<OrderBy><FieldRef Name="{0}" Ascending="{1}" /></OrderBy>'.format(self._order_by_field_name, str(self._order_by_ascending))
        
        return query
