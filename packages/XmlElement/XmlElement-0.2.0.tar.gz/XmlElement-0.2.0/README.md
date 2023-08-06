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

### Creating XmlElements

```python
from XmlElement import XmlElement as X

# Build a XML by nesting XmlElements:

xml = X('RootElement', s=[                             # root element without attributes
    X('Child1', {'testattr': 'Example attribute'}, [   # sub element with an attribute
        X('Child2', t='Example text value')            # sub-sub element with text value
    ])
])


# Alternative: Build a XML from a POJO-like object:

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






