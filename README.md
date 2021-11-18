# A simple Caml Query Builder - Python

[CAML](https://docs.microsoft.com/en-us/sharepoint/dev/schema/query-schema) is a query language for filter SharePoint lists.
This library expose some classes for build the 'query' part of the query for the most common usages.


## Usage exemples

### Filter an integer field

```python
m_filter = CamlFilter(CamlOperatorType.Equal, 'Somme', 2)
query_text = CamlWhere(m_filter).query_text
```
```xml
<Where>
    <Eq>
        <FieldRef Name="Somme" />
        <Value Type="Integer">2</Value>
    </Eq>
</Where>
```

### Filter a date field

```python
date_filter = CamlFilter(CamlOperatorType.Equal, 'Created', date(2021,11,17))
query_text = CamlWhere(date_filter).query_text
```
```xml
<Where>
    <Eq>
        <FieldRef Name="Created" />
        <Value IncludeTimeValue="FALSE" Type="DateTime">2021-11-17</Value>
    </Eq>
</Where>
```

### Filter a datetime field

```python
date_filter = CamlFilter(CamlOperatorType.GreaterOrEqual, 'Created', datetime(2021,11,17,20,43,33))
query_text = CamlWhere(date_filter).query_text
```
```xml
<Where>
    <Eq>
        <FieldRef Name="Created" />
        <Value IncludeTimeValue="TRUE" Type="DateTime">2021-11-17T20:43:33</Value>
    </Eq>
</Where>
```

### Filter an interger field with multiple values

```python
somme_filter = CamlFilter(CamlOperatorType.InList, 'Somme', 10, 11, 12)
query_text = CamlWhere(somme_filter).query_text
```
```xml
<Where>
    <In>
        <FieldRef Name="Somme" />
        <Values>
            <Value Type="Integer">10</Value>
            <Value Type="Integer">11</Value>
            <Value Type="Integer">12</Value>
        </Values>
    </In>
</Where>
```

### Filter a text field with order_by clause

```python
title_filter = CamlFilter(CamlOperatorType.Contains, 'Title', 'book')
query_text = CamlWhere(title_filter).orderBy('Created').query_text
```
```xml
<Where>
    <Contains>
        <FieldRef Name="Title" />
        <Value Type="Text">book</Value>
    </Contains>
</Where>
<OrderBy>
    <FieldRef Name="Created" Ascending="True" />
</OrderBy>
```

### Multiple filters with 'and' and 'or' conditions

```python
filter_1 = CamlFilter(CamlOperatorType.Different, 'Title', 'My book')
filter_2 = CamlFilter(CamlOperatorType.LowerOrEqual, 'Price', 200)
filter_3 = CamlFilter(CamlOperatorType.BeginsWith, 'Author', 'Georges')
query_text = CamlWhere(CamlAnd(filter_2, CamlOr(filter_1, filter_3))).query_text
```
```xml
<Where>
    <And>
        <Leq>
            <FieldRef Name="Price" />
            <Value Type="Integer">200</Value>
        </Leq>
        <Or>
            <Neq>
                <FieldRef Name="Title" />
                <Value Type="Text">My book</Value>
            </Neq>
            <BeginsWith>
                <FieldRef Name="Author" />
                <Value Type="Text">Georges</Value>
            </BeginsWith>
        </Or>
    </And>
</Where>
```