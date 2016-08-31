
# Interface between zipf and the generator
models is an object with the following sample structure:
```
{
 'model': <model name>,
 'fields': [
 	   {
	   'null': True,
	   'mult': 1,
	   'type': 'String',
	   'name': 'title'
	   },
	   {'null': True,
	   'mult': 1,
	   'type': 'String',
	   'name': 'author'}
	 ]
```


# List of Standard Data types
 - Boolean
 - Integer
 - Decimal
 - Float
 - String
 - Text
 - File
 - Image 
 - Video
 - Audio
 - Date
 - TimeInstant()
 - Duration
 - IP
 - URL
 - Email
 - Phone(Country)
 - Address(Country)
 - Country


# List of UI options for fiels
 - helpText
 - editable
 - label