# Breaking Version Changes

## 5.0.0

* AlertHandler.send() and get_or_add_alert_id() were refactored:
    * `source` is now a keyword argument, with default value `""`
    * most arguments are forced to keyword arguments

## 4.0.0

* the Category Enum was renamed to AccessCategory
* all member variables of Category/AccessCategory are lowercased
* the Medium Enum was renamed to MediumType
* all member variables of Medium/MediumType are lowercased
* the default database folder changed to a mounted volume

## 3.0.0

* the registration of bases for the database changed from `register_bases([...])` to `run_env_py([...])`

## 2.0.0

* Pydantic models are now defined in a model folder