# Orionpy

The OrionPy API allows to manage and administrate Orion without having to use the arcOpole Builder console.

- [Orionpy](#orionpy)
- [Installation requirements](#installation-requirements)
  * [Which python modules are required for this project ?](#which-python-modules-are-required-for-this-project-)
  * [Installation](#installation)
- [Usage](#usage)
  * [Jupyter example](#jupyter-example)
  * [Connection to Orion](#connection-to-orion)
  * [Get access to the data](#get-access-to-the-data)
  * [Working with filters](#working-with-filters)
  * [Groups management](#groups-management)
  * [Resource handling](#resource-handling)
  * [Changing rights](#changing-rights)
  * [Handling Cadastre resource](#handling-cadastre-resource)
  * [CSV Handling](#csv-handling)
  * [Handling Stats resource](#handling-stats-resource)
  * [Handling projects and geonotes](#handling-projects-and-geonotes)
  * [Working with the ArcGIS API for Python.](#working-with-the-arcgis-api-for-python)
- [Go further](#go-further)

# Installation requirements

First of all, you need to have [Python](https://www.python.org/) installed, with a version >= 3.6.

It is then required to install [pip](https://pip.pypa.io/en/stable/installing/).  
For information, pip is already installed if you are using Python 2 >=2.7.9 or Python 3 >=3.4 downloaded from https://www.python.org/.
It is also already installed if you are working in a Virtual Environment created by virtualenv or pyvenv.

Just make sure to upgrade pip.

## Which python modules are required for this project ?

The packages that will be installed in the following steps are :
* requests
* urllib3

## Installation

Since **OrionPy** is available on https://pypi.org/project/orionpy/, it must be installed using :
```bash
pip install orionpy
```

# Usage
The following section describes the main functions available in the API.

## Jupyter example
There is a full and executable example of OrionPy's usage in the file _Demonstration.ipynb_.

This file can be found in the project's [homepage](https://gitlab.com/esrifrance-public/orionpy/orionpy))
 and opened using [Jupyter](http://jupyter.org/).

For more information on Jupyter, how to install it and use it, check the following links:
* http://jupyter.org/
* https://developers.arcgis.com/python/guide/using-the-jupyter-notebook-environment/
* https://developers.arcgis.com/python/guide/install-and-set-up/#Test-your-install-with-jupyter-notebook

> Of course, you can also test the API without Jupyter.
Just note that the examples in this README might not work being "copy-and-pasted" in a Python file.

Other examples of code using the API can be found in the _main.py_ file.

## Connection to Orion
Orion is our main class.
It is by using its instance that the user has access to all data and operations available.

This Orion class generates a token authorizing the user connection to the Orion server.

Here is an example connecting to [https://front.arcopole.fr](https://front.arcopole.fr) :
```python
from orionpy.orioncore.Orion import Orion

username = ""  # Enter here the login for the arcOpole Builder console.
password = ""  # If empty, will be asked - securely - later.
url_machine = "https://front.arcopole.fr"  # External url of the WebAdaptor.
portal = "portal"  # Entry point to the WebAdaptor of the Portal for ArcGIS. (optional. default = "portal")
orion = Orion(username, password, url_machine, portal)
```
> In the case where there is a problem with SSL verification, the parameter **verify_cert** can be set as follow :
```python
orion = Orion(username, password, url_machine, portal, verify_cert=False)
```
> It is recommended to leave password as an empty string.
>   If left empty, a message will be displayed, asking to type down the username's password.

## Get access to the data
Once the connection is done, it is possible to get access to the data.

Two methods are used for this.
One to get all the elements and another to get one element using its name/id.
WARNING : {**_elements_**} must be replaced by one of the following : **groups**, **filters**, **services**.

[//]: # (TODO : /!\ get toujours avec le nom. Nouveau nom de méthode pour les services?)

```python
# Get the list of elements
elements_list = orion.{elements}.all()
# print this list
for element in elements_list:
    print(element)

# Get a particular element and print it
element = orion.{elements}.get(element_name)
print(element)
```

For instance, to get (and print) the group "Groupe 2" :
```python
group = orion.groups.get("Groupe 2")
print(group)
```

## Working with filters
To apply accurate and specific rights, data filters are essentials.

Currently, two types of data filters exist : FDU filters and SQL filters.

[//]: # (TODO : Quick description of each filter type)

Get the list of all the filters defined or of a particular filter:
```python
filters = orion.filters.all()
filter = orion.filters.get(filter_name)
```
Create a new FDU filter :
```python
# Create a FDU filter on one field :
orion.filters.add_FDU_filter(filter_name, fields = [field],
                             filtering_values = ['val1', 'val2', ...])
# Create a FDU filter on several fields :
orion.filters.add_FDU_filter(filter_name, fields = [field1, field2],
                             filtering_values = [['val11', 'val21'],
                                                 ['val12', 'val22']])
```
Create a new SQL filter :
```python
# Example creation of a SQL filter
orion.filters.add_SQL_filter(filter_name, where_clause = "NOMCOMM='NICE'")
```

Removing an existing filter :
```python
orion.filters.remove_filter(filter_name)
```

### FDU filter
If the filter is of FDU type, some more operations are available such as :
```python
# Print all fdu filters :
for fdu_f in orion.filters.all_fdu():
    print(fdu_f)
# Get fields concerned by the filter
fields = fdu_filter.get_fields()

# Get all labels corresponding to the defined filtering values
labels = fdu_filter.get_labels()

# Know if a given label is defined :
fdu_filter.is_label_defined(label)
```

### Update a filter's value

From orion.filters, it is possible to update a given filter's values.

#### Update SQL Filter

*where_clause* parameter is a string that contains the filter's condition :

_"territoire in ('1')"_

```python
# Updates the where clause on a SQL filter.
orion.filters.update_sql_filter_value(filter_name, where_clause)
```

#### Update FDU Filter

To update FDU filter, need to use an array in *filtering_values* like :

_["Filter value 1","Filter value 2"]_

```python
# Replace all FDU values by the new input filtering values
orion.filters.replace_fdu_values(filter_name, filtering_values)

# Adds new filtering values to a FDU
orion.filters.add_values_to_fdu(filter_name, filtering_values)

# Removes filtering values from a FDU
orion.filters.remove_values_from_fdu(filter_name, filtering_values)
```

_**NB** : filtering_values is formatted the same way as in `orion.filters.add_FDU_filter`._

## Groups management
In arcOpole Builder, rights are mainly applied on groups. A group is composed of several users.
Get the list of all groups / a particular group:
```python
groups = orion.groups.all()
group = orion.groups.get(group_name)
group = orion.groups.get_with_id(group_id)
```
Update/Add a FDU's filtering values for this group :
```python
fdu_filter = orion.filters.get(filter_name)

filter_values = ['val1', 'val2']
group.set_filter_values(fdu_filter, filter_values)

# 2nd solution if want to set all filtering values
group.set_filter_values(fdu_filter, add_all_values=True)

# Other solution if doesn't use labels but field_values :
field_values = ['field_val1', 'field_val2', 'field_val3']
field = "" # Field corresponding to field values
group.set_filter_field_values(fdu_filter, field_values, field)
```
Update/Add several FDU's filtering values for this group :
```python
filter1_name = "" # Filter name
filter2_name = "" # Filter name
filter1 = orion.filters.get(filter1_name)
filter2 = orion.filters.get(filter2_name)

filters_values = {filter1: ['val1', 'val2'], filter2: ['val3', 'val4']}
group.set_several_filter_values(filters_values)
```
Check if a group already have defined filtering values on a given filter:
```python
if group.has_defined_filter_values(fdu_filter):
    print('This group has defined filtering values')
```
Redefine all FDU's filtering values for this group :
```python
group.reset_all_filters_values(filters_values)
```

### Users management
In arcOpole Builder, stats are applied on users. 

Get the list of all users / a particular user:
```python
users = orion.users.all()
user = orion.users.get(user_name)
user = orion.users.get_with_id(user_id)
```

## Resource handling
Types of resource handled in this API :
* services
    * layers
        * fields
    * tables
        * fields

### Services
Get the list of all ArcGIS services :
```python
services = orion.services.all()
```

To get 1 particular ArcGIS service, it is required to use its REST relative Url, which is formatted as :
**FOLDER/SERVICE_SERVICETYPE**.

For instance :
```python
service = orion.services.get("Cannes/EspacesVerts_FeatureServer")

# Get all services' REST urls
urls = orion.services.urls()
```
Get only the services managed by arcOpole Builder (or 1 service in this list) :
```python
services = orion.services.all_managed()
service = orion.services.get_in_managed(service_rest_url)
```
Enable or Disable service management:
```python
service.enable()
service.disable()
```

It is also possible to know if a given service is a cadastre resource.
If that is the case, the usual right-handling methods won't be available for this service.
```python
if service.is_cadastre_resource():
    print("The service is a cadastre resource")
```

### Layers
Get all layers or 1 layer from a specific service.
> In a same service, two layers can have the same name.
Therefore, it is more recommended to use the `get_with_id` method.

```python
layers = service.layers.all()
layer = service.layers.get_with_id(layer_id)

# Not recommended for layers.
layer = service.layers.get(layer_name)
```
Get a layer's id :
```python
layer_id = service.layers.get_id(layer_name)
```

#### Group of layers
As a "subtype" of layer, it is also possible to find groups of layers.
In OrionPy, they are handled in the class `Layer` using several methods.

```python
# If the layer is a group of layers...
if layer.is_group():
    print('Layer is a group of layers')

    if layer.has_sub_layers():
        # The following methods get a list with IDs of layers in this group
        sub_layers_ids = layer.get_sub_layers_ids()
        print('Layers contained in this group have ids : ', sub_layers_ids)
else:
    print('Layer is not a group of layer')
    if layer.has_parent_layer():  # If the layer is in a group of layers
        print("layer's parent id is :", layer.get_parent_layer_id())
```

### Tables
Access to tables (all of them or a specific one) :
```python
tables = service.tables.all()
table = service.tables.get(table_name)
```

### Fields
It is possible to get access to fields using a layer or a table.

Get all / 1 field(s) for a specific layer or a specific table :
```python
fields = layer_or_table.fields.all()
field = layer_or_table.fields.get(field_name)
```
Get a field's name :
```python
name = field.get_name()
```

## Changing rights

Once you've had your resource (service, layer, table or field), it is possible to apply the following operations :

### Print a right summary :
Print a summary of the rights defined on a resource, also the filters applied and if the right is inherited or not.
```python
service.print_rights(group)
```
### Inheritance handling
Enable/disable right inheritance for a resource and a particular group :
```python
service.enable_inheritance(group)
service.disable_inheritance(group)

if service.has_inherited_right(group):
    print('Resource right is inherited for this group')
```

### Clear all rights

From aOB 1.3.4, it is possible to clear all rights on a given resources and its sub-resources.
Basically, it does the same as manually enabling inheritance for all profiles on a resource and its sub-resources.

```python
service.clear_all_rights()
```

### Handling right level
Update right-level for a group on a resource :
```python
from orionpy.orioncore.resources.Resource import RightLevel

right_level = RightLevel.[ACCESS|READ|WRITE]  # Pick one of the three rights you want to apply

service.update_right(group, right_level)
```
Note that it is not possible to update right if (between else), the right is inherited or the service is not enabled.

If you know what you are doing, you can also use the `force_rights` command.
This method will automatically disable inheritance and enable service management before updating rights.
```python
service.force_right(group, right_level)
```

### Apply a filter
The arcOpole Builder console handles the application of a FDU filter on three types of resources :
* Service,
* Table,
* Layer.

As an example, here is how to (de)activate a FDU filter on a service for a group
```python
# Get the data required
fdu_filter = orion.filters.get(filter_name)
group = orion.groups.get(group_name)
service = orion.services.get(service_name)

# Activate and/or deactivate a fdu
service.activate_fdu_filter(group, fdu_filter)
service.deactivate_fdu_filter(group, fdu_filter)
```

It is also possible to (de)activate a SQL filter on layer or table :
```python
# Get the data required
sql_filter = orion.filters.get(filter_name)
group = orion.groups.get(group_name)
service = orion.services.get(service_name)
layer = service.layers.get(layer_name)

# Activate and/or deactivate a sql filter
layer.activate_sql_filter(group, sql_filter)
layer.deactivate_sql_filter(group, sql_filter)
```

## Handling Cadastre resource

You can get the cadastre resource with
```python
# Get the data required
cadastre_resource = orion.businesses.get_cadastre_resource()
```

### Get the filter associated with a Cadastre resource
After the cadastre resource is recovered, you can access to the associated filter's id using the `associated_filter_id` property.

If you want to update this filter's filtering value, you must get the corresponding filter.
It is necessary for others methods such as `update_right` (if update to **NOMINATIF_ACCESS**), `activate_filter` and `deactivate_filter`.

To access this filter directly from the Cadastre resource, you must first set it.
It will then be possible to access it using the `associated_filter` property.
```python
# Get the filter associated with the resource's :
filter = orion.filters.get_with_id(cadastre_resource.associated_filter_id)

cadastre_resource.init_filter_access(filter)

#... It is now possible to call methods directly on :
cadastre_resource.associated_filter
```

### Using filter with Cadastre resource

Any FDU filter method can be used with `associated_filter`.
Moreover, you can call specific method with the Cadastre resource.

_Reminder : you **must** call the `init_filter_access` method before calling these_

Also note that `deactivate_filter` will not work if the group has a NOMINATIF_ACCESS

```python

cadastre_resource.activate_filter(group)
cadastre_resource.deactivate_filter(group)
```

### Managing Cadastre resource

On the cadastre resource, three rights are available and can be updated using `update_right` method.
The right levels available are :
* `RightLevel.ACCESS`
* `RightLevel.PUBLIC_ACCESS`
* `RightLevel.NOMINATIF_ACCESS`

_Note : When switching to `RightLevel.NOMINATIF_ACCESS` for a group, the filter must be activated for this group.
If `init_filter_access` was called before, `update_right` will automatically apply the filter_

```python
# (... get a group to update right for ...)

# update the rights
cadastre_resource.update_right(group, RightLevel.***) # replace *** by one of the 3 rights applicable

# print the rights defined for the group on the cadastre_resource
cadastre_resource.print_rights(group)
```

## CSV Handling
It is also possible to generate a CSV containing a summary on the current system rights.

Several CSV classes exists. Each of them with two methods.
The `generate` method generating a CSV with information.
And the `read_and_apply` method reading a CSV file generated and applying modification to the server.

### Handling filtering values with a CSV
This is done creating a `CSVFilteringValues` class.

```python
from orionpy.orioncsv.csvfilteringvalues import CSVFilteringValues

# Creates the class to create/handle a csv for filtering values.
csv_handler = CSVFilteringValues(orion)

csv_path = "my_csv.csv"  # Enter here a csv filename
csv_handler.generate(csv_path)

### Now you can open the csv file analyze its content and modify it...

# To apply modifications written in CSV file :
csv_handler.read_and_apply(csv_path)
```

Sample of the CSV generated :

| Filter | Label | Group1 | Group2 | ... |
| --- | --- | :---: | :---: | --- |
| filter1 | label1 | 1 | 0 | ... |
| filter1 | label2 | 0 | 0 | ... |
| filter2 | label1 | 1 | 1 | ... |
| ... | ... | ... | ... | ... |

* 0 means that the filtering value is not activated for this group,
* 1 means that it is.

### Handling rights on a resource with a CSV
This is done creating a `CSVRightsManagement` class.

It will create a summary of rights on a Service and all of its component (layers, fields, tables).

```python
from orionpy.orioncsv.csvrightsmanagement import CSVRightsManagement

# Creates the class to create/handle a csv for filtering values.
csv_handler = CSVRightsManagement(orion)

csv_path = ""  # TODO : Enter here a csv filename
service_url = ""  # TODO : Enter here a valid service's rest url
service = orion.services.get(service_url)
group_name = "" # TODO enter here a group name
group_list = [orion.groups.get(group_name)]

# NB : The following line might not work directly, please refer
csv_handler.generate(csv_path, service, group_list = group_list)

### Now you can open the csv file analyze its content and modify it...

# To apply modifications written in CSV file :
csv_handler.read_and_apply(csv_path)
```

If the `group_list` argument isn't set, the `generate` method will get the groups shared with the Service given to generate a summary of rights for all these groups.
> In order to use this functionnality of getting the groups shared, your orion instance must be of OrionGIS type. (refer to section "Working with the ArcGIS API for Python")

```python
csv_handler.generate(csv_path, service)
```

Sample of the CSV generated :

| Type | Relative url | Label | Group1 | Group2 | ... |
| --- | --- | --- | --- | --- | --- |
| SERVICE | Serv1_MapServer | Serv1_MapServer | read | access | ... |
| LAYER | Serv1_MapServer/0 | layer1 | inherited (read) | write | ... |
| FIELD | Serv1_MapServer/0/field1 | field1 | access | inherited (write) | ... |
| FIELD | Serv1_MapServer/0/field2| field2 | inherited (read) | access | ... |
| SERVICE | Serv2_FeatureServer | Serv2_FeatureServer | inherited (read)| write | ... |
| ... | ... | ... | ... | ... | ... |

### Importing rights from a JSON file

This can be made using the `CSVFilteringCadastre` class.

First, the class must be initialized with a connection to Orion :

```python
from src.orioncsv.csvfilteringcadastre import CSVFilteringCadastre

csv_filtering_cadastre = CSVFilteringCadastre(orion)
```

Then, a CSV file must be generated from the json file, containing data :

```python
csv_path = ""  # TODO : Enter here the csv path
json_path = "" # TODO : Enter here the json file's path
csv_filtering_cadastre.generate(csv_path, json_path)
```

Once the CSV is generated by analyzing the json, the rights can be imported :

```python
csv_filtering_cadastre.read_and_apply(csv_path)
```


## Handling Stats resource

Stats resource allows to group users in specific organisationnal units. Organizational units represent the administrative division of your organization. One user can only associate with one organisationnal unit. 

You can get the stats resource with
```python
# Get the data required
stats_resource = orion.businesses.get_stats_resource("hosted")
```

`storage_id` is an optional parameter to found a specific storage in stats resource. Actually `hosted` is the only available type of storage. 
This method return the specific `StorageResource` object. If not found `get_stats_resource` return None.

Stats resource works with the units organisationnal.  with a specific FDU in arcOpole Builder. After creation, apply one value of this FDU on user

### FDU for stats

In arcOpole Builder, organisationnal units are modelized by the FDU. So you need to create new FDU with all division of your organisation. 

It is possible to use FDU with OrionPy or in aob-admin application.

For more information on FDU in OrionPy, please refere on FDU creation describe above.

```python
# Create FDU
orion.filters.add_FDU_filter(filter_stats_name, fields = fields,
                             filtering_values = values)
```

> Example for filtering_values : ['Secteur1', 'Secteur2', ...]

### (Dis)associate FDU with storage resource

To associate FDU with storage resource use `update_filter` method.

To disassociate it, use `disassociate_filter` method.

```python
# Associate filter to storage resource
storage_resource.update_filter(fdu_filter.get_id())

# Disassociate the filter from the storage resource
storage_resource.disassociate_filter()
```

### Add filter value to user

After create specific stats FDU, associate FDU to storage resource, the last step is to add filter value for users. In stats module, one user only can associate one filter value.

```python
# Add filter value to a specific user
filter_values = ['Secteur1']
user.set_filter_values(fdu_filter, filter_values)
```

### Handling organisationnal units with a CSV
This is done creating a `CSVOrganisationUnit` class.

It will create a summary of users and there associated organisationnal units.

```python
from orionpy.orioncsv.csvorganisationunit import CSVOrganisationUnit

# Creates the class to create/handle a csv for filtering values.
csv_handler = CSVOrganisationUnit(orion)

csv_path = ""  # TODO : Enter here a csv filename

# To generate a csv file that will list the users and their associated organizational unit 
csv_handler.generate(csv_path)

### Now you can open the csv file analyze its content and modify it...

# To apply modifications written in CSV file :
csv_handler.read_and_apply(csv_path)
```

Sample for CSV 

| UserName | Organization
| --- | ---
| admin_aob | Secteur1
| user1 | Secteur2
| editor1 | Secteur3
| ... | ...
||

> Before using this functionality, please ensure that a filter is associated with the storage resource (refer to section "Associate FDU with storage resource")

## Handling projects and geonotes

You can access projects or geonotes and use methods on these items :

```python
orion.{items}.{method(...)}

# for projects
orion.projects.{method(...)}

# for geonotes
orion.geonotes.{method(...)}

```

Here are the methods you can use to:

* search for items

```python
# get the result of the method search (as a list of items) and print it

search = orion.{items}.search(q="", start=-1, num=100, all=False)
# values in search are the default values
# q is the query
# start correspond to the number of the first result
# num correspond to the number of results
# define all as True to search also on elasticsearch

print(search)
```

* get the DATA of an item from an item id, also called 'itemId'

```python
# get the result of the method data (json) and print it

data = orion.{items}.data('itemId')

#you can get the data and export it in a new or existing json file using this method:
data = orion.{items}.data_export('itemId', 'path_of_the_exported_file.json')
#the path of the file must contain '.json' at the end

#you can also use the id of the first item returned in the previous method :
data = orion.{items}.data(search[0].get_id())
print(data)
```

* add an item in aOB

```python
# return the result of the query, here in add_item

add_item = orion.{items}.add_item("owner", "title", text, snippet=None)
# owner is the user that create the item
# title is the title of the item you want to add
# text is the json data to add
# text can be for example 'text = orion.{items}.data('itemId')'
# snippet is the description, set by default on None.

#you can also import data from an existing json file
add_item = orion.{items}.add_item_from_file("title", 'path_of_json_file.json', snippet=None)

#you can print the return of the method, which is the result of the query send to the server
print(add_item)
```

* update an item in aOB

```python
# return the result of the query, here in add_item

update_item = orion.{items}.update_item("itemId", "title", text, snippet=None)
# itemId is the id of the item to update
# title is the new title of the item you want to update
# text is the json data to update
# text can be for example 'text = orion.{items}.data('itemId')'
# snippet is the description, set by default on None.

#you can also update an item with an existing json file
update_item = orion.{items}.update_item_from_file("itemId", "title", "path_of_json_file.json", snippet=None)

#you can print the return of the method, which is the result of the query send to the server
print(update_item)
```

* reassign the owner of an item

```python
# return the result of the query, here in add_item

reassign_item = orion.{items}.reassign("itemId", "targetUsername")
# itemId is the id of the item to reassign
# targetUsername is the new username

#you can print the return of the method, which is the result of the query send to the server
print(reassign_item)
```

* delete an item

```python
# return the result of the query, here in add_item

delete = orion.{items}.delete("itemId")
# itemId is the id of the item to reassign

#you can print the return of the method, which is the result of the query send to the server
print(delete)
```


## Working with the ArcGIS API for Python.
In some cases, OrionPy can work with the ArcGIS API for Python.
It is first required to install the API following its [documentation](https://developers.arcgis.com/python/).

Then, you can access its methods creating the class :
```python
from orionpy.oriongis.oriongis import OrionGIS

# NB : parameter are the same as the Orion class
orion_gis = OrionGIS(username, password, url_machine, portal)
```

### Access a Esri API method
```python
orion_gis.gis.[....]
```

### Handling sharing on a service.
Adding the Esri's API into OrionPy allowed to add the posibility of handling a service sharing.

doesn't only allow to call methods from the API.
It gives the opportunity to create methods mixing calls to OrionPy and to the Esri API.

```python
service_url = ""
service = orion_gis.services.get(service_url)
group_name = ""
group = orion_gis.groups.get(group_name)

# Share a service with a group
orion_gis.services_gis_mgr.share(service, group.get_id())

# Unshare a service with a group
orion_gis.services_gis_mgr.unshare(service, group.get_id())

# Check if a service is share with a group :
if orion_gis.service_gis_mgr.is_shared_with(service, group.get_id()):
    print('Service shared with group')
else:
    print('Service not shared with group')

# Get ID's of the groups with which a given service is shared
orion_gis.services_gis_mgr.get_groups_id_shared(service)
```


# Go further

Access to the full code documentation of the API is possible by opening
the file *index.html* on your web browser in the folder :
**docs/build/html**.

> This folder can be found in the project's [homepage](https://gitlab.com/esrifrance-public/orionpy/orionpy)).

Gitlab deposit is at https://gitlab.com/esrifrance-public/orionpy/orionpy
