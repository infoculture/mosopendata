#!/usr/bin/env python
# coding: utf8
"""
Importer data from Data.mos.ru to hub.opengovdata.ru
"""
import ckanclient
import csv

API_KEY_FILENAME = "apikey.txt"
API_URL = "http://hub.opengovdata.ru/api"
DATASETS_FILENAME = 'datasets.csv'
BASE_URL = 'http://data.mos.ru'
DIRECT_DOWNLOAD_URLPAT = "http://data.mos.ru/datasets/download/%s"


class DataImporter:
    """Data importer class for data.mos.ru"""
    def __init__(self):
        self.apikey = open("apikey.txt").read()
        self.ckan = ckanclient.CkanClient(base_location=API_URL, api_key=self.apikey)
        self.package_list = self.ckan.package_register_get()
        pass

    def import_moscow(self):
        """Processes all data from datasets.csv and creates package"""
        reader = csv.DictReader(open(DATASETS_FILENAME, 'r'), delimiter="\t")
        package_names = []
        for package in reader:
            package['id'] = package['id']
            package_names.append(self.register(package))
        self.update_group('moscow', package_names)
        pass

    def register(self, package):
        """Register or update dataset
        :param package:
        """
        key = 'datamosru_' + package['id'].replace('.', '_')
        try:
            r = self.ckan.package_entity_get(key)
            status = 0
        except ckanclient.CkanApiNotFoundError, e:
            status = 404
        tags = [u'Москва', u'официально', package['theme'].lower(), u'datamosru']
        resources = [{'name': package['name'], 'format': '', 'url':  package['url'],
                      'description': u'Страница на сайте data.mos.ru'},
                     {'name': package['name'], 'format': 'CSV', 'url': DIRECT_DOWNLOAD_URLPAT % package['id'],
                      'description': u'Данные в формате CSV на data.mos.ru'}]
        # Add direct url to the CSV file and url to HTML

        the_package = { 'name' : key, 'title' : package['name'], 'url' :  package['url'],
                           'notes' : u'Данные города Москвы.\n\n'.encode('utf8') + package['name'],
                           'tags' : tags,
                           'state' : 'active',
                           'resources': resources,
                           'group' : 'moscow',
                           'author' : 'Ivan Begtin',
                           'author_email' : 'ibegtin@infoculture.ru',
                           'maintainer' : 'Ivan Begtin',
                           'maintainer_email' : 'ibegtin@infoculture.ru',
                           'extras':
                               {'govbody' : package['source']}
                        }
        if status != 404:
            self.ckan.package_entity_delete(r['name'])

        if True:
            try:
                self.ckan.package_register_post(the_package)
                rname = 'thedata/%s.csv' %(package['id'])
                self.ckan.upload_file(rname)
                self.ckan.add_package_resource(the_package['name'], rname, resource_type="data", name=package['name'], description=u"Данные в формате CSV")
            except Exception, e:
                print key
                print package['url']
                return key
                pass
            print "Imported", key
        else:
            package_entity = self.ckan.last_message
            if type(package_entity) == type(''): return None
            package_entity.update(the_package)
            for k in ['id', 'ratings_average', 'relationships', 'ckan_url', 'ratings_count']:
                del package_entity[k]
            self.ckan.package_entity_put(package_entity)
            print "Updated", key
#            print self.ckan.last_message
        return key

    def update_group(self, group_name, package_names, group_title="", description=""):
            #        print key
            try:
                group = self.ckan.group_entity_get(group_name)
                status = 0
            except ckanclient.CkanApiNotFoundError, e:
                status = 404
            if status == 404:
                group_entity = {'name' : group_name, 'title' : group_title, 'description' : description }
                self.ckan.group_register_post(group_entity)
            group = self.ckan.group_entity_get(group_name)
            for name in package_names:
                if name not in group['packages']:
                    group['packages'].append(name)
            self.ckan.group_entity_put(group)


if __name__ == "__main__":
    imp = DataImporter()
    imp.import_moscow()