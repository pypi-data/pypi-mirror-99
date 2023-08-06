# <img src="https://uploads-ssl.webflow.com/5ea5d3315186cf5ec60c3ee4/5edf1c94ce4c859f2b188094_logo.svg" alt="Pip.Services Logo" width="200"> <br/> Portable Abstractions and Patterns for Python Changelog

## <a name="3.2.1"></a> 3.2.1 (2021-03-12)

### Bug Fixes
* remove **numpy** dependency

## <a name="3.2.0"></a> 3.2.0 (2021-03-01)

### Features
* **random** added DoubleConverter


### Breaking changes
* Сhanged access to variables from `Class.name` to `Class.get_name()` for:
- Scheme
- ArraySchema
- Mapschema
- ObjectSchema
- PropertySchema
- ValidationException
- ValidationResult

### Bug Fixes
* TypeConverter fixed to_type_code, to_nullable_type, to_type
* Fixed JsonConverter.from_json datetime convert
* Fixed LongConverter.to_nullable_long
* Fixed Map.Converter.to_nullable_map
* Fixed ApplicationException with_details and with_stack_trace methods
* Fixed init PagingParams
* Fixed FixedRateTimer


## <a name="3.1.5-3.1.6"></a> 3.1.5-3.1.6 (2021-02-26)

### Bug Fixes

* Fixed BooleanConverter.to_nullable_boolean
* Fixed TypeMatcher.match_type

## <a name="3.1.3-3.1.4"></a> 3.1.3-3.1.4 (2021-01-16)

### Bug Fixes

* Fixed description.message in ErrorDescriptionFactory
* Fixed RandomDateTime.next_datetime

## <a name="3.1.1-3.1.2"></a> 3.1.1-3.1.2 (2020-12-21)

### Bug Fixes

* Fixed id in IIdentifiable
* Fixed setup.py

## <a name="3.0.0"></a>3.0.0 (2018-10-30)

### New release
* Restructuring package

### Features
* **commands** Command and Eventing patterns
* **config** Configuration framework
* **convert** Portable soft data converters
* **data** Data value objects and random value generators
* **errors** Portable application errors
* **random** Random components
* **refer** Component referencing framework
* **reflect** Portable reflection helpers
* **run** Execution framework
* **validate** Data validators

