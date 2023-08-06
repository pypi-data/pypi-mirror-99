jznsearch
===

jznsearch is a small commandline utility that searches entities in provided data sources (organizations.json, users.json and tickets.json). It performs search based on field name and filed value and print results in standard output (including dependant objects if found).

Usage example
====

Let's find all organisations with _id = 102 using files provided in `simple_data` folder

`❯ jznsearch -e organizations -f '_id' -v '102' -d 'sample_data'`

Positive result:

```
--------------------Organizations 102-----------------------------------------------------
_id              - 102
url              - http://initech.zendesk.com/api/v2/organizations/102.json
external_id      - 7cd6b8d4-2999-4ff2-8cfd-44d05b449226
name             - Nutralab
domain_names     - ['trollery.com', 'datagen.com', 'bluegrain.com', 'dadabase.com']
created_at       - 2016-04-07T08:21:44 -10:00
details          - Non profit
shared_tickets   - False
tags             - ['Cherry', 'Collier', 'Fuentes', 'Trevino']
>> User - Roman Meyers (25)
>> User - Jaime Dickerson (33)
>> User - Velasquez Cameron (69)
>> Ticket - A Problem in Syria (25cb699f-a5dd-45d8-9bc1-9c4b7d096946)
>> Ticket - A Problem in Gambia (20615fe1-765b-4ff5-b4f6-ea42dcc8cac3)
>> Ticket - A Problem in Antigua and Barbuda (3ff0599a-fe0f-4f8f-ac31-e2636843bcea)
>> Ticket - A Catastrophe in Bermuda (6fed7d01-15dd-4b59-94f9-1093b4bc0995)
>> Ticket - A Nuisance in Eritrea (df1a642a-e704-4556-af79-98a63b59401d)
>> Ticket - A Problem in Japan (bb8b1829-25d9-4534-83a2-c4e6086d76d4)
>> Ticket - A Drama in Martinique (ea69e0c0-d1b8-462e-a654-b571666e6253)
>> Ticket - A Nuisance in Liberia (a12a5f33-d4a0-4e43-8773-4b22e16fc0c8)
```

Negative result

`❯ jznsearch -e organizations -f '_id' -v '-1' -d 'sample_data'`

```
No organizations found with _id = -1
```

Empty values
===
It is possible to search for empty value, however results will include entities with the missing tag as well

`jznsearch -e organizations -f 'emptyfield' -v '' -d 'tests'`
```
--------------------Organizations 101-----------------------------------------------------
_id              - 101
url              - http://initech.zendesk.com/api/v2/organizations/101.json
external_id      - 9270ed79-35eb-4a38-a46f-35725197ea8d
name             - Enthaze
domain_names     - ['kage.com', 'ecratic.com', 'endipin.com', 'zentix.com']
created_at       - 2016-05-21T11:10:28 -10:00
doesnotexist     - nonono
shared_tickets   - False
emptyfield       - 
tags             - ['Fulton', 'West', 'Rodriguez', 'Farley']
>> User - Loraine Pittman (5)
>> User - Francis Bailey (23)
>> User - Haley Farmer (27)
>> Ticket - A Drama in Georgia (31ec2df9-edaf-496e-b05a-ca6a75ddcc67)
--------------------Organizations 102-----------------------------------------------------
_id              - 102
url              - http://initech.zendesk.com/api/v2/organizations/102.json
external_id      - 7cd6b8d4-2999-4ff2-8cfd-44d05b449226
name             - Nutralab
domain_names     - ['trollery.com', 'datagen.com', 'bluegrain.com', 'dadabase.com']
created_at       - 2016-04-07T08:21:44 -10:00
details          - Non profit
shared_tickets   - False
tags             - ['Cherry', 'Collier', 'Fuentes', 'Trevino']
>> User - Roman Meyers (25)
>> Ticket - A Nuisance in Romania (b2035bdc-2ff4-4d23-9752-c5b67541193e)
```

Available search fields
====

jznsearch can provide a list of all searchable fields

`jznsearch -l -d 'sample_data/'`

```
--------------------Here are searchable fields for Organizations--------------------------
_id
url
external_id
name
....
```


Available parameters
====
```
  -h, --help                            show this help message and exit
  -l, --list                            List searchable fields
  -f FIELD, --field FIELD               Field to search for
  -v VALUE, --value VALUE               Value to search for
  -e {organizations,users,tickets}, --entity {organizations,users,tickets}
                                        Entity to search for
  -d DATA_DIR, --data-dir DATA_DIR      Files location. Current folder if not set
```

Installation
====

`jznsearch` is automatically built using Github Actions and published into PyPI: https://pypi.org/project/jznsearch/

Utility is distributes as pip package. To install it use the following command (you need to have a working Python installation and `pip`)

`pip install jznsearch`

Assumptions and limitations
====

jznsearch is ad-hoc solution to provide operators with basic search capabilities in existing data structures. Current limitations are:
* It doesn't support nested JSONs (arrays are fine, e.g "tags")
* Source files are relatively small and the can fit into memory on a single machine
* Search is performed by substring match, which may be confusing in some cases (`d79-35eb-1a38` and `-1` are a match)


