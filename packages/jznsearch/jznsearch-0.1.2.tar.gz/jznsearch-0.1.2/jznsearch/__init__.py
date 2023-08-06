import argparse
import os
import json


class InvalidArgumentException(Exception):
    pass


class Searchable(object):
    @property
    def id_key(self):
        return '_id'

    @property
    def entity_name(self):
        return self.__class__.ENTITY_NAME

    @property
    def printable_name(self):
        return self.__class__.PRINTABLE_NAME

    @property
    def file_name(self):
        return f'{self.entity_name}.json'

    def load_dependencies(self, ids):
        raise RuntimeError('Class Searchable can\'t load dependencies')

    def __init__(self):
        self.data = None
        self.schema = None
        self.data_dir = None

    def load_data(self, data_dir):
        self.data_dir = data_dir
        file_name = os.path.join(data_dir, self.file_name)
        f = open(file_name, 'r')
        try:
            r = json.load(f)
        except Exception as e:
            raise InvalidArgumentException(f'Invalid JSON {file_name} file: {e}')
        finally:
            f.close()
        self.data = r
        self.schema = self.build_schema()

    def find_by_id(self, id):
        for el in self.data:
            if el[self.id_key] == id:
                return el

    def is_field_searchable(self, field_name):
        if field_name in self.schema.keys():
            return True
        return False

    def search(self, field, value):
        result = []
        for el in self.data:
            if value.lower() in str(el.get(field, '')).lower():
                result.append(el[self.id_key])
        return result

    def print_full(self, entities):
        for entity in entities:
            print(f'{self.printable_name} {entity[self.id_key]}'.ljust(70, '-').rjust(90, '-'))
            for k, v in entity.items():
                print('{:<16} - {}'.format(k, v))

    def print_short(self, entities):
        pass

    def build_schema(self):
        fields = {}
        for el in self.data:
            fields.update(el)
        return fields

    def print_searchable_fields(self):
        print()
        print(f'Here are searchable fields for {self.printable_name}'.ljust(70, '-').rjust(90, '-'))
        for el in self.schema.keys():
            print(el)


class Orgs(Searchable):
    ENTITY_NAME = 'organizations'
    PRINTABLE_NAME = 'Organizations'

    def print_short(self, entities):
        for entity in entities:
            if entity is None:
                print(f'>> Organization - <<NONEXISTENT>>')
            else:
                print(f'>> Organization - {entity["name"]} ({entity[self.id_key]})')

    def load_dependencies(self):
        self.users = Users()
        self.users.load_data(self.data_dir)
        self.tickets = Tickets()
        self.tickets.load_data(self.data_dir)

    def print_search_results(self, results):
        for org_id in results:
            org = self.find_by_id(org_id)
            users = self.users.filter_by_org(org_id)
            tickets = self.tickets.filter_by_org(org_id)
            self.print_full([org])
            self.users.print_short(users)
            self.tickets.print_short(tickets)


class Users(Searchable):
    ENTITY_NAME = 'users'
    PRINTABLE_NAME = 'Users'

    def print_short(self, entities):
        for entity in entities:
            if entity is None:
                print(f'>> User - <<NONEXISTENT>>')
            else:
                print(f'>> User - {entity["name"]} ({entity[self.id_key]})')

    def filter_by_org(self, org_id):
        return [x for x in self.data if x.get('organization_id', -1) == org_id]

    def load_dependencies(self):
        self.organizations = Orgs()
        self.organizations.load_data(self.data_dir)
        self.tickets = Tickets()
        self.tickets.load_data(self.data_dir)

    def print_search_results(self, results):
        for user_id in results:
            user = self.find_by_id(user_id)
            org = self.organizations.find_by_id(user.get('organization_id', -1))
            tickets = self.tickets.filter_by_user(user_id)
            self.print_full([user])
            self.organizations.print_short([org])
            self.tickets.print_short(tickets)

class Tickets(Searchable):
    ENTITY_NAME = 'tickets'
    PRINTABLE_NAME = 'Tickets'

    def print_short(self, entities):
        for entity in entities:
            if entity is None:
                print(f'>> Ticket - <<NONEXISTENT>>')
            else:
                print(f'>> Ticket - {entity["subject"]} ({entity[self.id_key]})')

    def filter_by_org(self, org_id):
        return [x for x in self.data if x.get('organization_id', -1) == org_id]

    def filter_by_user(self, user_id):
        return [x for x in self.data if user_id in (x.get('submitter_id', -1), x.get('assignee_id', -1))]

    def load_dependencies(self):
        self.organizations = Orgs()
        self.organizations.load_data(self.data_dir)
        self.users = Users()
        self.users.load_data(self.data_dir)

    def print_search_results(self, results):
        for ticket_id in results:
            ticket = self.find_by_id(ticket_id)
            org = self.organizations.find_by_id(ticket.get('organization_id', -1))
            submitter = self.users.find_by_id(ticket.get('submitter_id', -1))
            assignee = self.users.find_by_id(ticket.get('assignee_id', -1))
            self.print_full([ticket])
            self.organizations.print_short([org])
            print('>>Submitter:')
            self.users.print_short([submitter])
            print('>>Assignee:')
            self.users.print_short([assignee])


VALID_ENTITIES = [Orgs, Users, Tickets]


class SearchRunner(object):
    def parse_args(self, args=None):
        o = argparse.ArgumentParser('Search in JSON files')
        o.add_argument('-l', '--list', action='store_true', help='List searchable fields')
        o.add_argument('-f', '--field', type=str, help='Field to search for')
        o.add_argument('-v', '--value', type=str, help='Value to search for')
        o.add_argument('-e', '--entity', choices=[x.ENTITY_NAME for x in VALID_ENTITIES],
            type=str, help='Entity to search for')
        o.add_argument('-d', '--data-dir', type=str, default='.', help='Files location')

        if args is None:
            self.p = o.parse_args()
        else:
            self.p = o.parse_args(args)

    def validate_args(self):
        if not os.path.exists(self.p.data_dir):
            raise InvalidArgumentException(f'Location {self.p.data_dir} doesn\'t exist')
        if self.p.list:
            return
        if self.p.field is None:
            raise InvalidArgumentException('Search field must be set')
        if self.p.value is None:
            raise InvalidArgumentException('Search value must be set')
        if self.p.entity is None:
            raise InvalidArgumentException('Search entity must be set')

    def find_entity_class(self, entity_name):
        for e in VALID_ENTITIES:
            if e.ENTITY_NAME == entity_name:
                return e
        raise InvalidArgumentException(f'Entity {entity_name} is not known')

    def print_all_searchable_fields(self):
        for entity_class in VALID_ENTITIES:
            e = entity_class()
            e.load_data(self.p.data_dir)
            e.print_searchable_fields()

    def run(self):
        self.parse_args()
        self.validate_args()
        if self.p.list:
            self.print_all_searchable_fields()
            return
        entity_class = self.find_entity_class(self.p.entity)
        self.entity = entity_class()
        self.entity.load_data(self.p.data_dir)
        if not self.entity.is_field_searchable(self.p.field):
            raise InvalidArgumentException(f'Field {self.p.field} is not searchable for {self.entity.printable_name}')
        found = self.entity.search(self.p.field, self.p.value)
        if len(found) == 0:
            print(f'No {self.p.entity} found with {self.p.field} = {self.p.value}')
            return
        self.entity.load_dependencies()
        self.entity.print_search_results(found)


def main():
    try:
        r = SearchRunner()
        r.run()
    except Exception as e:
        print(f'Fatal error: {e}')
