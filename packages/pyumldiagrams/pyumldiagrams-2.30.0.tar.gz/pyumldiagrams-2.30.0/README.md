[![Build Status](https://travis-ci.com/hasii2011/pyumldiagrams.svg?branch=master)](https://travis-ci.com/hasii2011/pyumldiagrams)
[![PyPI version](https://badge.fury.io/py/pyumldiagrams.svg)](https://badge.fury.io/py/pyumldiagrams)

The documentation is [here](https://hasii2011.github.io/pyumldiagrams/pyumldiagrams/index.html).



## Sample PDF Generation Snippets



### Create a basic class

```python
diagram: PdfDiagram = PdfDiagram(fileName='basicClass.pdf', dpi=75)
classDef: ClassDefinition = ClassDefinition(name='BasicClass', size=Size(width=100, height=100))

diagram.drawClass(classDef)
diagram.write()
```



### Create a class with a method

```python
diagram: PdfDiagram = PdfDiagram(fileName=f'Test-BasicMethod.pdf', dpi=75)

position: Position = Position(107, 30)
size:         Size          = Size(width=266, height=100)

car: ClassDefinition = ClassDefinition(name='Car', position=position, size=size)

initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

initParam: ParameterDefinition = ParameterDefinition(name='make', parameterType='str', defaultValue='')
initMethodDef.parameters = [initParam]
car.methods = [initMethodDef]

diagram.drawClass(car)

diagram.write()

```

### Create a class with some fields

```python
        fileName: str        = f'Test-BasicFields.pdf'
        diagram:  PdfDiagram = PdfDiagram(fileName=fileName, dpi=75)

        fieldsTestClass: ClassDefinition = ClassDefinition(name='FieldsTestClass', position=Position(226, 102), size=Size(height=156, width=230))

        fieldsTestClass.fields = self._buildFields()

        initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

        fieldsTestClass.methods = [initMethodDef]

        diagram.drawClass(classDefinition=fieldsTestClass)

        diagram.write()
```


### Create inheritance diagram



```python
diagram: PdfDiagram = PdfDiagram(fileName='MinimalInheritance.pdf', dpi=75)

cat:   ClassDefinition = ClassDefinition(name='Gato', position=Position(536, 19), size=Size(height=74, width=113))
opie: ClassDefinition = ClassDefinition(name='Opie', position=Position(495, 208), size=Size(width=216, height=87))

diagram.drawClass(classDefinition=cat)
diagram.drawClass(classDefinition=opie)

linePositions: LinePositions = [Position(600, 208), Position(600, 93)]
opieToCat: UmlLineDefinition = UmlLineDefinition(lineType=LineType.Inheritance, linePositions=linePositions)

diagram.drawUmlLine(lineDefinition=opieToCat)
diagram.write()
```





## Sample Image Snippets

### Create a basic .png class

```python
diagram:   ImageDiagram       = ImageDiagram(fileName='BasicClass.png')
classDef: ClassDefinition = ClassDefinition(name=TestDiagramParent.BASE_TEST_CLASS_NAME,
                                                										 size=Size(width=266, height=100),
                                                										 position=Position(x=107, y=30)
                                               											)

diagram.drawClass(classDef)
diagram.write()
```

### Create a basic .png class with fields

```python
fileName:               str                           = 'Test-WithFields.png'
diagram:                 ImageDiagram        = ImageDiagram(fileName=fileName)
fieldsTestClass: ClassDefinition = ClassDefinition(name='FieldsTestClass', 
                                                                           								position=Position(226, 102), 
                                                       													size=Size(height=156, width=230))

fieldsTestClass.fields = self._buildFields()

initMethodDef: MethodDefinition = MethodDefinition(name='__init__', visibility=DefinitionType.Public)

fieldsTestClass.methods = [initMethodDef]

diagram.drawClass(classDefinition=fieldsTestClass)

diagram.write()
```