# XmlElement

A simpler XML writer.

## Installation

`pip install XmlElement`

## Test

```
>>> from XmlElement import XmlElement as X
>>> xml = X.from_string('<test><x/></test>')
>>> xml
XmlElement(test)
```

## Usage

### Build a XML by nesting XmlElements

```python
from XmlElement import XmlElement as X

xml = X('RootElement', s=[                             # root element without attributes
    X('Child1', {'testattr': 'Example attribute'}, [   # sub element with an attribute
        X('Child2', t='Example text value')            # sub-sub element with text value
    ])
])
```

### Alternative: Build a XML from a POJO-like object:

```python
from XmlElement import XmlElement as X

xml2 = X.from_object(
    node_name='RootElement',                           # root element without attributes
    data={                                             # no @-elements: root has -> no attributes
        'Child1': {                                    # sub element with an attribute @testattr
            '@testattr': 'Example attribute',
            'Child2': 'Example text value'             # sub-sub element with text value
        }
    }
)

print(str(xml) == str(xml2))                           # True
```

### Accessing values by dot operator

```python
print(xml)
print(xml.Child1[0].attributes['testattr']) # Example attribute
print(xml.Child1[0].Child2[0].text)         # Example text value
```

### Accessing values dict-like (to avoid static type checker warnings)

```python
print(xml)
print(xml['Child1'][0].attributes['testattr']) # Example attribute
print(xml['Child1'][0]['Child2'][0].text)      # Example text value
```

### Converting XmlElement to POJO-like object

```python
from XmlElement import XmlElement as X

xml = X('RootElement', s=[                # root element without attributes
    X('Child1', {'testattr': 'true'}, [   # sub element with a boolean attribute
        X('Child2', t='1234'),            # sub-sub element with int-like value
        X('Child3', t='-1234.56')         # sub-sub element with float-like value
    ])
])

print(xml)                    # <RootElement><Child1 testattr="true"><Child2>1234</Child2><Child3>-1234.56</Child3></Child1></RootElement>

print(xml.to_dict())          # {'Child1': {'@testattr': True, 'Child2': 1234, 'Child3': -1234.56}}

print(xml.to_dict(            # {'Child1': {'@testattr': 'true', 'Child2': '1234', 'Child3': '-1234.56'}}
    recognize_numbers=False, 
    recognize_bool=False)
)
```
Subnodes of equal names under a node will result in a list. 
However, this cannot recognize if a single element should be list in another context.



