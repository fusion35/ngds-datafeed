# -*- coding: utf-8 -*-
from bson.objectid import ObjectId
from constants import languages, countries
from mongokit import Document, IS
#from ngds import settings
#from ngds.core.auth import authrules
import StringIO
#import api
import datetime
import logging
import shutil
import uuid

SOCIAL_MEDIA_URLS = {
    "twitter": "http://www.twitter.com/",
    "facebook": "http://www.facebook.com/",
    "youtube": "http://www.youtube.com/"
}
try:
    import PIL

    if PIL.Image == None:
        raise ImportError
except ImportError:
    try:
        import Image
        import ImageOps

        class PIL(object):
            Image = Image
            ImageOp = ImageOps

    except ImportError:
        PIL = None

LOG = logging.getLogger(__name__)

DB_NAME = 'ngds'
#if 'mongodb.db_name' in settings.config:
#    DB_NAME = settings.config['mongodb.db_name']

#: Countries, use ISO 3166 Country codes (http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
#: .. deprecated:: 3-1-2013
#: use constants.countries
US = countries.US
CA = countries.INFO[countries.CA]['name']

#: Brands
FORD = u"Ford"
LINCOLN = u"Lincoln"

BRANDS = [FORD, LINCOLN]
MAKE_TYPE = IS(FORD, LINCOLN)

ALL = {"id": '', "display_name": {"en": "All", "es": "All", "fr": "All"}}

CARS = {"id": u"car", "display_name": {
    "en": "Cars", "es": "Cars", "fr": "Cars"}}
SUVS = {"id": u"suv", "display_name": {
    "en": "SUVs", "es": "SUVs", "fr": "SUVs"}}
TRUCKS = {"id": u"truck", "display_name": {
    "en": "Trucks", "es": "Trucks", "fr": "Trucks"}}
COMMERCIAL_TRUCKS = {"id": u"commercial-truck", "display_name": {
    "en": "Commercial Trucks", "es": "Commercial Trucks", "fr": "Commercial Trucks"}}
CROSSOVERS = {"id": u"crossover", "display_name": {
    "en": "Crossovers", "es": "Crossovers", "fr": "Crossovers"}}
HYBRIDS = {"id": u"hybrid", "display_name": {
    "en": "Hybrids", "es": "Hybrids", "fr": "Hybrids"}}

NGP_NGDS_VEHICLE_TYPE_MAPPING = {
    # Mapping of the vehicle type representation on NGP with NGDS
    'car': CARS,
    'suv': SUVS,
    'truck': TRUCKS,
    'commercial-truck': COMMERCIAL_TRUCKS,
    'crossover': CROSSOVERS,
    'hybrid': HYBRIDS
}

ALL_VEHICLE_TYPE_IDS = [CARS["id"], CROSSOVERS[
    "id"], SUVS["id"], TRUCKS["id"], COMMERCIAL_TRUCKS["id"]]
ALL_VEHICLE_TYPES = [CARS, CROSSOVERS, SUVS,
                     TRUCKS, COMMERCIAL_TRUCKS]  # we dont support hybrids
VEHICLE_TYPE = IS(CARS, SUVS, TRUCKS, COMMERCIAL_TRUCKS,
                  CROSSOVERS)  # we dont support hybrids

### Dealer Types
STANDARD = {"id": "S", "display_name": {
    "en": "Standard", "es": "Standard", "fr": "Standard"}}
QCOMMERCIAL = {"id": "Q", "display_name": {
    "en": "Q-Commercial", "es": "Q-Commercial", "fr": "Q-Commercial"}}
CCOMMERCIAL = {"id": "C", "display_name": {
    "en": "C-Commercial", "es": "C-Commercial", "fr": "C-Commercial"}}
UCOMMERCIAL = {"id": "U", "display_name": {
    "en": "U-Commercial", "es": "U-Commercial", "fr": "U-Commercial"}}

ALL_DEALER_TYPES = [STANDARD, QCOMMERCIAL, CCOMMERCIAL, UCOMMERCIAL]
DEALER_TYPE = IS(STANDARD, QCOMMERCIAL, CCOMMERCIAL, UCOMMERCIAL)

### INVENTORY DEFAULT SETTINGS
TILE_VIEW = {'id': 'tile', 'display_name': {
    'en': 'Tile View', 'fr': 'Tile View', 'es': 'Tile View'}}
LIST_VIEW = {'id': 'list', 'display_name': {
    'en': 'List View', 'fr': 'List View', 'es': 'List View'}}
VIEWS_TYPE = IS(TILE_VIEW, LIST_VIEW)

SORT_PRICE_LOW_TO_HIGH = {
    'id': 'price_asc',
    'display_name': {
        US: {
            'en': 'Price: Low To High',
            'fr': 'Price: Low To High',
            'es': 'Price: Low To High'
        },
        CA: {
            'en': 'Price: Low To High',
            'fr': 'Price: Low To High',
            'es': 'Price: Low To High'
        }
    },
}

SORT_PRICE_HIGH_TO_LOW = {
    'id': 'price_desc',
    'display_name': {
        US: {
            'en': 'Price: High To Low',
            'fr': 'Price: High to Low',
            'es': 'Price: High To Low'
        },
        CA: {
            'en': 'Price: High To Low',
            'fr': 'Price: High to Low',
            'es': 'Price: High To Low'
        }
    }
}

SORT_YEAR_LOW_TO_HIGH = {
    'id': 'year_asc',
    'display_name': {
        US: {
            'en': 'Year: Low To High',
            'fr': 'Year: Low To High',
            'es': 'Year: Low To High'
        },
        CA: {
            'en': 'Year: Low To High',
            'fr': 'Year: Low To High',
            'es': 'Year: Low To High'
        }
    }
}

SORT_YEAR_HIGH_TO_LOW = {
    'id': 'year_desc',
    'display_name': {
        US: {
            'en': 'Year: High To Low',
            'fr': 'Year: High to Low',
            'es': 'Year: High To Low'
        },
        CA: {
            'en': 'Year: High To Low',
            'fr': 'Year: High to Low',
            'es': 'Year: High To Low'
        }
    }
}

SORT_MILEAGE_LOW_TO_HIGH = {
    'id': 'mileage_asc',
    'display_name': {
        US: {
            'en': 'Mileage: Low To High',
            'fr': 'Mileage: Low To High',
            'es': 'Mileage: Low To High'
        },
        CA: {
            'en': 'Odometer: Low To High',
            'fr': 'Odometer: Low To High',
            'es': 'Odometer: Low To High'
        }
    }
}

SORT_MILEAGE_HIGH_TO_LOW = {
    'id': 'mileage_desc',
    'display_name': {
        US: {
            'en': 'Mileage: High To Low',
            'fr': 'Mileage: High To Low',
            'es': 'Mileage: High To Low'
        },
        CA: {
            'en': 'Odometer: High To Low',
            'fr': 'Odometer: High To Low',
            'es': 'Odometer: High To Low'
        }
    }
}

USED_INVENTORY_SORT_TYPE = IS(SORT_PRICE_LOW_TO_HIGH, SORT_PRICE_HIGH_TO_LOW,
                              SORT_YEAR_LOW_TO_HIGH, SORT_YEAR_HIGH_TO_LOW, SORT_MILEAGE_LOW_TO_HIGH, SORT_MILEAGE_HIGH_TO_LOW)
NEW_INVENTORY_SORT_TYPE = IS(SORT_PRICE_LOW_TO_HIGH, SORT_PRICE_HIGH_TO_LOW)

SORT_TYPE_MAPPING = {
    "price_asc": SORT_PRICE_LOW_TO_HIGH,
    "price_desc": SORT_PRICE_HIGH_TO_LOW,
    "mileage_asc": SORT_MILEAGE_LOW_TO_HIGH,
    "mileage_desc": SORT_MILEAGE_HIGH_TO_LOW,
    "year_asc": SORT_YEAR_LOW_TO_HIGH,
    "year_desc": SORT_YEAR_HIGH_TO_LOW
}

AZ_PLAN = {"id": "az_plan", "display_name": {
    "en": "A/Z Plan", "es": "A/Z Plan", "fr": "A/Z Plan"}}
X_PLAN = {"id": "x_plan", "display_name": {
    "en": "X Plan", "es": "X Plan", "fr": "X Plan"}}
AXZ_PLAN_TYPE = IS(AZ_PLAN, X_PLAN)

# user roles

SITE_ROLES = [] #IS(authrules.SITE_VIEWER, authrules.SITE_MANAGER,
#                authrules.CALL_CENTER_REPRESENTATIVE,
#                authrules.PREMIER_DEALER_REPRESENTATIVE,
#                authrules.SYSTEM_ADMINISTRATOR)
### Themes
THEMES = [
    {
        'themeid': 'default',
        'themename': {
            'en': u'Blue Theme',
            'fr': u'thème bleu',
            'es': u'Tema azul'
        }
    }, {
        'themeid': 'three',
        'themename': {
            'en': u'Aqua Theme',
            'fr': u'Thème Aqua',
            'es': u'Tema Aqua'
        }
    }, {
        'themeid': 'four',
        'themename': {
            'en': u'Blue-Green Theme',
            'fr': u'Thème bleu-vert',
            'es': u'Tema azul-verde'
        }
    }
]

# Image library related constants
STAFF = {'id': 'staff', 'display_name': {'en': 'Staff', 'es': '', 'fr': ''}}
INFORMATIONAL = {'id': 'informational', 'display_name': {
    'en': 'Informational', 'es': '', 'fr': ''}}
HEROSHOT = {'id': 'heroshot', 'display_name': {
    'en': 'Heroshot', 'es': '', 'fr': ''}}
LOGO = {'id': 'logo', 'display_name': {'en': 'Logo', 'es': '', 'fr': ''}}
BANNER = {'id': 'banner', 'display_name': {'en': 'Banner', 'es': '', 'fr': ''}}
CUSTOM = {'id': 'custom', 'display_name': {'en': 'Custom', 'es': '', 'fr': ''}}
INTERIORPROMOTILE = {'id': 'interior_promotile', 'display_name': {
    'en': 'Interior Promotile', 'es': '', 'fr': ''}}
IMAGE_CATEGORIES = [STAFF, INFORMATIONAL,
                    HEROSHOT, LOGO, BANNER, CUSTOM, INTERIORPROMOTILE]
IMAGE_CATEGORIES_MAPPING = {
    'staff': STAFF,
    'informational': INFORMATIONAL,
    'heroshot': HEROSHOT,
    'logo': LOGO,
    'banner': BANNER,
    'custom': CUSTOM,
    'interior_promotile': INTERIORPROMOTILE
}
CATEGORY_SIZE_MAPPING = {
    'staff': [90, 90],
    'informational': [732, 732],
    'heroshot': [900, 300],
    'logo': [130, 90],
    'banner': [980, 130],
    'custom': [975, 975],
    'interior_promotile': [150, 177]
}

# Lang Code
#: .. deprecated:: 3-1-2013
#: use constants.languages
ENGLISH = languages.EN
#: .. deprecated:: 3-1-2013
#: use constants.languages
FRENCH = languages.FR
#: .. deprecated:: 3-1-2013
#: use constants.languages
SPANISH = languages.ES

# supported languages for Dealers
US_LANGUAGES = [languages.ENGLISH, languages.SPANISH]
FOC_LANGUAGES = [languages.ENGLISH, languages.FRENCH]

### Languages
LANGUAGES = languages.INFO

DAYS = IS(u"Mon", u"Tue", u"Wed", u"Thu", u"Fri", u"Sat", u"Sun")
TIME = IS(u"12.00 AM", u"12.30 AM", u"1.00 AM", u"1.30 AM", u"2.00 AM",
          u"2.30 AM", u"3.00 AM", u"3.30 AM", u"4.00 AM", u"4.30 AM",
          u"5.00 AM", u"5.30 AM", u"6.00 AM", u"6.30 AM", u"7.00 AM",
          u"7.30 AM", u"8.00 AM", u"8.30 AM", u"9.00 AM", u"9.30 AM",
          u"10.00 AM", u"10.30 AM", u"11.00 AM", u"11.30 AM", u"12.00 PM",
          u"12.30 PM", u"1.00 PM", u"1.30 PM", u"2.00 PM", u"2.30 PM",
          u"3.00 PM", u"3.30 PM", u"4.00 PM", u"4.30 PM", u"5.00 PM",
          u"5.30 PM", u"6.00 PM", u"6.30 PM", u"7.00 PM", u"7.30 PM",
          u"8.00 PM", u"8.30 PM", u"9.00 PM", u"9.30 PM", u"10.00 PM",
          u"11.30 PM")

# DealerShip Info Phone number component
HORIZONTAL_LIST = {'id': 'horizontal', 'display_name': {
    'en': 'Horizontal', 'fr': 'Horizontal', 'es': 'Horizontal'}}
VERTICAL_LIST = {'id': 'vertical', 'display_name': {
    'en': 'Vertical', 'fr': 'Vertical', 'es': 'Vertical'}}
DEALERSHIP_CONTACT_DISPLAY = IS(HORIZONTAL_LIST, VERTICAL_LIST)

# Minishowroom related constants
NEWEST_TO_OLDEST = {'id': 'newest_to_oldest', 'display_name': {
    'en': 'Newest to Oldest', 'fr': '', 'es': ''}}
OLDEST_TO_NEWEST = {'id': 'oldest_to_newest', 'display_name': {
    'en': 'Oldest to Newest', 'fr': '', 'es': ''}}
LOWEST_FIRST = {'id': 'lowest_first', 'display_name': {
    'en': 'Lowest First', 'fr': '', 'es': ''}}
HIGHEST_FIRST = {'id': 'highest_first', 'display_name': {
    'en': 'Highest First', 'fr': '', 'es': ''}}
VEHICLE_TYPE_ORDER = {'id': 'vechicle_type', 'display_name': {
    'en': 'Order by Vehicle Type', 'fr': '', 'es': ''}}
LAUNCH_DATE_ORDER = {'id': 'launch_date', 'display_name': {
    'en': 'Order by Vehicle Launch Date', 'fr': '', 'es': ''}}
DATE_ORDER_TYPE = IS(NEWEST_TO_OLDEST, OLDEST_TO_NEWEST)
PRICE_ORDER_TYPE = IS(LOWEST_FIRST, HIGHEST_FIRST)
ORDER_BY_TYPE = IS(VEHICLE_TYPE_ORDER, LAUNCH_DATE_ORDER)

ONLINE = {'id': 'online', 'display_name': {
    'en': 'Online', 'fr': '', 'es': ''}}
NATIONAL = {'id': 'national', 'display_name': {
    'en': 'National', 'fr': '', 'es': ''}}
COUPONS_TYPE = IS(ONLINE, NATIONAL)

LAYOUT_SHOP = {"id": u"shop", "display_name": {"en": "Shop", "es":
                                               "", "fr": ""}, "image": "/static/img/edit/layout/shop_tn.png"}
LAYOUT_WELCOME = {"id": u"welcome", "display_name": {
    "en": "Welcome", "es": "", "fr": ""}, "image": "/static/img/edit/layout/welcome_tn.png"}
LAYOUT_LINKS = {"id": u"links", "display_name": {
    "en": "Links", "es": "", "fr": ""}, "image": "/static/img/edit/layout/links_tn.png"}
LAYOUT_HERO = {"id": u"hero", "display_name": {"en": "Hero", "es":
                                               "", "fr": ""}, "image": "/static/img/edit/layout/hero_tn.png"}

HOMEPAGE_LAYOUT_TYPES = [
    LAYOUT_SHOP, LAYOUT_WELCOME, LAYOUT_LINKS, LAYOUT_HERO]

PREOWNED_INVENTORY = {
    'make': [u'Ford', u'Lincoln', u'Mercury'],
    'years': range(datetime.date.today().year,
                   datetime.date.today().year - 10, -1),
    'vehicle_types': [u'Car', u'SUV', u'Truck', u'Van & Minivan'],
    'mileages': ['0 - 10,000', '10,001 - 20,000', '20,001 - 30,000',
                 '30,001 - 40,000', '40,001 - 150,000'],
    'prices': ['$0 - $4,999', '$5,000 - $9,999', '$10,000 - $14,999',
               '$15,000 - $19,999', '$20,000 - $24,999', '$25,000 - $29,999',
               '$30,000 - $39,999', '$40,000 - $150,000']
}

DEALER_SCRIPT_HEAD = {'id': 'head', 'display_name': 'End of Head Tag'}
DEALER_SCRIPT_BODY = {'id': 'body', 'display_name':  'End of Body Tag'}

DEALER_SCRIPT_POSITION = IS(DEALER_SCRIPT_HEAD, DEALER_SCRIPT_BODY)

# Assets Manager related constants
FMC = {'id': u'fmc', 'display_name': {
    'en': u'FMC', 'fr': u'FMC', 'es': u'FMC'}}
FOC = {'id': u'foc', 'display_name': {'en': u'Ford of Canada',
                                      'fr': u'Ford of Canada', 'es': u'Ford of Canada'}}
OPERATING_UNITS = IS(FMC, FOC)
OPERATING_UNITS_MAPPING = {'fmc': FMC, 'foc': FOC}
ADMIN_AND_DEALERSITES = {'id': 'admin_and_dealersites', 'display_name': {
    'en': 'Admin, DealerSites', 'fr': 'Admin, DealerSites', 'es': 'Admin, DealerSites'}}
ADMIN_ONLY = {'id': 'admin_only', 'display_name': {
    'en': 'Admin Only', 'fr': 'Admin Only', 'es': 'Admin Only'}}
USAGE_TYPES = IS(ADMIN_AND_DEALERSITES, ADMIN_ONLY)
USAGE_TYPES_MAPPING = {'admin_and_dealersites':
                       ADMIN_AND_DEALERSITES, 'admin_only': ADMIN_ONLY}

PUBLISHED_DISCLOSURE = {'id': 'published', 'display_name':
                       {'en': 'Published Disclosures', 'fr': 'Published Disclosures',
                        'es': 'Published Disclosures'}}
UNPUBLISHED_DISCLOSURE = {'id': 'unpublished', 'display_name':
                         {'en': 'Un-published Disclosures', 'fr': 'Un-published Disclosures',
                          'es': 'Un-published Disclosures'}}
EXPIRED_DISCLOSURE = {'id': 'expired', 'display_name':
                     {'en': 'Expired Disclosures', 'fr': 'Expired Disclosures',
                      'es': 'Expired Disclosures'}}
DISCLOSURE_STATUS = IS(
    PUBLISHED_DISCLOSURE, UNPUBLISHED_DISCLOSURE, EXPIRED_DISCLOSURE)

FMC_REGION = {'id': 'fmc', 'display_name': 'Regions for FMC'}
FOC_REGION = {'id': 'foc', 'display_name': 'Regions for FOC'}

# Campaigns Constants
REGIONAL = {
    # u'name': IS(u'Regional'),
    u'region': IS(u'Regions for FMC', u'Regions for Ford of Canada'),
    u'regions': [basestring]
}
IMAGE_INFO = {
    # For link_to has been made dictionary because it can change per region
    # For default case basestring would be Dealer.NULL_CODE
    # else it would be region code if required
    u'link_to': {
        basestring: {
            'type': IS(u'URL', u'Site Page', None),
            'value': basestring
        }
    },
    u'image_id': basestring
}

CAMPAIGN_IMAGE = {
    u'en': IMAGE_INFO,
    u'fr': IMAGE_INFO
}

DATA_CHANGE_TYPE = {'id': u"data", 'display_name': 'Data'}
SITE_CHANGE_TYPE = {'id': u"site", 'display_name': 'DealerSite'}
NAVIGATION_CHANGE_TYPE = {'id': u"navigation", 'display_name': 'Navigation'}
CHANGE_TYPES = IS(SITE_CHANGE_TYPE, DATA_CHANGE_TYPE, NAVIGATION_CHANGE_TYPE)


class BaseDocument(Document):
    use_schemaless = True

    def change_history_info_dict(self, user_id, change_type, description):

        return {
            'user_id': user_id,
            'change_id': str(uuid.uuid4()),
            'change_type': change_type,
            'description': description,
        }

    def __add_change_history__(self, dealer_code, change_details):

#        change_hist = self.db.ChangeHistory.find_and_modify(
#            query={'dealer_code': dealer_code},
#            update={ '$push': { 'change_description':  change_details} },
#            upsert=True
#        )
        insertion_date = datetime.datetime.now().strftime("%Y-%m-%d")
        change_history = self.db.ChangeHistory.find_one({
            'dealer_code': dealer_code}
        )
        change_desc = list()

        if change_history:
            if insertion_date in change_history['change_description']:
                change_desc = change_history[
                    'change_description'][insertion_date]
        else:
            change_history = self.db.ChangeHistory()
            change_history['dealer_code'] = dealer_code

        change_desc.append(change_details)
        change_history['change_description'][insertion_date] = change_desc

        change_history.save()

    def save(self, dealer_code=None, change_details=None, *args, **kwargs):
        """

        """
        super(BaseDocument, self).save(*args, **kwargs)
        try:
            if change_details and dealer_code:
                self.__add_change_history__(dealer_code, change_details)
        except Exception, ex:
            LOG.exception(
                "Error while adding change description : " +
                change_details['description'] + " : " +
                str(change_details['user_id']))
            pass
    # Add for delete
    pass

LocalizedString = {"en": basestring, "fr": basestring, "es": basestring}
# Image = {"url" : basestring}
Applicability = {"brands": [basestring], "countries": [basestring], "languages": [
    basestring], "start_date": datetime.datetime, "end_date": datetime.datetime}

HoursOfOperation = {
    "start_day": DAYS,
    "end_day": DAYS,
    "is_open": bool,
    "start_time": TIME,
    "end_time": TIME
}

Address = {
    "label": LocalizedString,
    "street1": unicode,
    "street2": unicode,
    "city": unicode,
    "state": unicode,
    "country": basestring,
    "postal_code": basestring
}


Staff = {
    "uid": basestring,
    "name": unicode,
    "email": unicode,
    "phone": basestring,
    "description": LocalizedString,
    "title": unicode,
    "fax": basestring,
    "image": basestring,
}


NavItem = {
    "name": LocalizedString,  # corresponds to the page name
    "url": unicode,  # corresponds to the page path
    "is_admin_locked": bool,
    "is_visible": bool,
    "is_editable": bool,
    "icon_url": basestring,
    "icon_sprite": basestring,
    "ui_column_index": int  # corresponds to the columnIndex to which the main category of navigation items belong
}


class UserRole(BaseDocument):
    __collection__ = 'userrole'
    __database__ = DB_NAME

    def add_user_role(self, userid, role, site=None):
        if userid is None or role is None:
            raise Exception('userid and role are mandatory')

        userrole = self.db.UserRole()
        userrole['userid'] = userid
        userrole['role'] = role
        userrole['site'] = site
        userrole.save()
        return userrole

    structure = {
        'userid': basestring,
        'role': SITE_ROLES,
        'site': basestring,  # pacode of dealersite allowed to manage by this user
    }


class Domain(BaseDocument):
    __collection__ = 'domain'
    __database__ = DB_NAME

    def add_domain(self, domain_name, belongs_to, is_redirect=False, redirect_to=None):
        if domain_name is None or belongs_to is None:
            raise Exception("Missing domain or owner")

        domain = self.db.Domain()
        domain['domain'] = domain_name
        domain['belongs_to'] = belongs_to
        domain['is_redirect'] = is_redirect
        domain['redirect_to'] = redirect_to

        domain.save()
        return domain

    structure = {
        'domain': basestring,
        'is_redirect': bool,
        'redirect_to': basestring,
        'belongs_to': basestring  # dealer pa code
    }


class ImageLibrary(BaseDocument):
    __collection__ = 'image_library'
    __database__ = DB_NAME

    IMAGE_MIMES = {
        'PNG': 'image/png',
        'JPEG': 'image/jpeg',
        'GIF': 'image/gif',
        #'pdf': 'application/pdf',  # TODO: add support
        'svg': 'image/svg+xml',  # TODO: add support
        #'html': 'text/html',  # TODO: add support
        #'htm': 'text/html',  # TODO: add support
    }

    IMAGE_TYPES = {
        '*': 'All Types',
        'image/*': 'Images',
        'application/octet-stream': 'Downloadable'
    }

    THUMBNAIL_SIZE = (90, 90)
    THUMBNAIL_FORMAT = 'PNG'

    structure = {
        'alt': LocalizedString,
        'name': LocalizedString,
        'brand': [IS(FORD, LINCOLN)],
        'category': IS(IMAGE_CATEGORIES[0], IMAGE_CATEGORIES[1],
                       IMAGE_CATEGORIES[2], IMAGE_CATEGORIES[3],
                       IMAGE_CATEGORIES[4], IMAGE_CATEGORIES[5],
                       IMAGE_CATEGORIES[6]),
        'owner': basestring,
        'mime': {basestring: basestring},
        'size': {basestring: (int, int)},
        # Extra fields added for asset manager functionality
        'applicable_languages': [IS(languages.EN, languages.ES, languages.FR)],
        'usage': USAGE_TYPES,
        'operating_units': OPERATING_UNITS,
        'uploaded_date': datetime.datetime,
        'm_size': float
    }

    gridfs = {
        'containers': [
            'images'
        ]
    }

    def from_filename(self, filename, **kwargs):
        """
        Load an image into mongodb from a file on disk.
        """
        # At least according to the docs this should automatically close the
        # file incase of an exception
        fd = open(filename)

        try:
            image = self.from_file(fd, **kwargs)
        finally:
            fd.close()

        return image

    def from_field_storage(self, field_storage, **kwargs):
        """
        Load an image into mongodb from a cgi.FieldStorage object.
        """

        try:
            return self.from_file(field_storage.file, mime=field_storage.type, **kwargs)
        except:
            return self.from_file(None, mime=None, **kwargs)

    def from_file(self, fd, alt='', owner='', brand=FORD, name='', category='', mime='application/octet-stream', **kwargs):
        """
        Load an image into mongodb from a file-like object. The other from_*
        methods depend on this one to do the heavy lifting.
        """

        if 'edit_image_id' in kwargs and kwargs['edit_image_id']:
            image = '' #= api.get_image_from_library(kwargs['edit_image_id'])
        else:
            image = self.db.ImageLibrary()
            image['owner'] = owner
            image['brand'] = brand if isinstance(
                brand, list) else [unicode(brand)]
            image['category'] = IMAGE_CATEGORIES_MAPPING[category]
            image['mime']['source'] = mime
            image['mime']['thumb'] = None
            image['size']['source'] = (0, 0)
            image['size']['thumb'] = (0, 0)
            image['operating_units'] = OPERATING_UNITS_MAPPING[kwargs[
                'operating_units']] if 'operating_units' in kwargs else None
            image['usage'] = USAGE_TYPES_MAPPING[kwargs[
                'usage']] if 'usage' in kwargs else None
            image['uploaded_date'] = datetime.datetime.now()
        image['alt'] = alt
        image['name'] = name
        image['applicable_languages'] = kwargs[
            'languages'] if 'languages' in kwargs else []
        image.save()

        # For edit scenario with only image content edit(new image not being
        # uploaded)
        if not fd:
            return image

        # use PIL to get the metadata on the file
        fd.seek(0)
        try:
            source_image = PIL.Image.open(fd)
        except IOError:
            # If there is any IOError at this point, its probably from PIL.
            source_image = None
        else:
            if source_image.format in self.IMAGE_MIMES:
                image['mime']['source'] = self.IMAGE_MIMES[source_image.format]

            # Fit the size of image( if both height and width are more than the expected size)
            # Largest side is reduced to fit within the expected
            # dimensions(maintaing aspect ratio)
            width, height = source_image.size
            expected_image_size = CATEGORY_SIZE_MAPPING[
                image['category']['id']]
            if expected_image_size[0] < width and expected_image_size[1] < height:
                response = self.resize_image(expected_image_size, source_image)
                fd = response['fd']
                source_image.size = response['size']
            image['size']['source'] = source_image.size

        image['m_size'] = float(fd.tell())  # read memory taken by file
        # copy the source file into the container
        fd.seek(0)
        source_fd = image.fs.images.new_file('source')
        try:
            shutil.copyfileobj(fd, source_fd)
        finally:
            source_fd.close()

        # If we know we can use the source image, generate the thumbnail and
        # save it to the container.
        if source_image:
            thumb_fd = image.fs.images.new_file('thumb')
            image['mime']['thumb'] = self.IMAGE_MIMES[self.THUMBNAIL_FORMAT]
            image['size']['thumb'] = self.THUMBNAIL_SIZE
            try:
                source_image.thumbnail(
                    self.THUMBNAIL_SIZE, PIL.Image.ANTIALIAS)
                source_image.save(thumb_fd, self.THUMBNAIL_FORMAT)
            finally:
                thumb_fd.close()

        image.save()

        return image

    def resize_image(self, expected_image_size, source_image):
        """resizes the images
            #Fit the size of image( if both height and width are more than
                the expected size)
            #Largest side is reduced to fit within the expected dimensions
                (maintaing aspect ratio)
        """
        width, height = source_image.size
        image_format = source_image.format
        ratio = max(expected_image_size[0] / float(width),
                    expected_image_size[1] / float(height))
        source_image = source_image.resize((int(width * ratio),
                                            int(height * ratio)), PIL.Image.ANTIALIAS)
        fd = StringIO.StringIO()
        source_image.save(fd, image_format)
        return {'fd': fd, 'size': source_image.size}

Department = {
    "name": LocalizedString,
    "primary_contact": Staff,
    "is_default_department": bool,
    "is_visible": bool,
    "internal_email": unicode,
    "displayed_email": unicode,
    "phone": basestring,
    "fax": basestring,
    "hours": [HoursOfOperation],
    "address": [unicode],
    "sort_order": int
}

DealershipInfo = {
    "display_style": DEALERSHIP_CONTACT_DISPLAY,
    "display_dealer_phone": bool,  # true if dealer default phone('display_phone' field - Shown for 'Call Us Now')
    "department_contact": [unicode],  # this will store the uuid for departments whose contact would be shown
    "pcs_additional": {
        "banner_font_color": basestring,
        "display_contact_info": bool,
        "display_dealership_name": bool,
        "logo": basestring,
    },
    "banner": basestring
}


class Dealer(BaseDocument):
    __collection__ = 'dealer'
    __database__ = DB_NAME

    NULL_CODE = '00000'

    structure = {
        "subdomain": unicode,
        "code": basestring,
        "orgid": basestring,
        "enrollment_date": datetime.datetime,
        "expiry_date": datetime.datetime,
        "live_date": datetime.datetime,
        "name": unicode,
        "region": unicode,
        "country": IS(US, CA),
        "brands": [basestring],
        "phone": basestring,
        "email_internal": unicode,
        "primary_email": unicode,
        "fax": basestring,
        "primary_address": dict,  # These dict will have a uuid key mapped to Addresses, primary address also need to have a uuid as other address which will maintain uniformity in usage
        "dealer_status": basestring,
        "addresses": dict,
        "staff": [Staff],
        "latitude": float,
        "longitude": float,
        "primary_contact": Staff,
        "call_tracking_number": basestring,
        "sales_code": basestring,
        "display_phone": basestring,
        "dealer_type": DEALER_TYPE,
        "secondary_pa_code": basestring,
        "departments": dict,  # These dict will have a uuid key mapped to Department
        "dealership_info": DealershipInfo,
        "coupons": [COUPONS_TYPE],

        # Consider breaking it up further e.g. settings.autocheck.enabled,
        # settings.autocheck.visible etc.
        "settings": {
            "is_blue_oval_certified": bool,
            "is_lincoln_premier_experience_certified": bool,
            "is_internet_certified": bool,
            "is_certified_preowned": bool,
            "is_GeS_enabled": bool,
            "is_rent_a_car": bool,
            "is_hev": bool,
            "is_SVT": bool,
            "is_fleet_dealer": bool,
            "is_flood_light_enabled": bool,
            "is_autocheck_subscribed": bool,
            "is_PAIS_enrolled": bool,
            "is_fordparts_enrolled": bool,
            "is_fordparts_opted": bool,
            "is_premier": bool,
        }
    }

PageLayout = {
    "name": basestring,  # name for the layout, to be shown on edit layout
    "is_default": bool,
    "metadata": dict
}


class PageType(BaseDocument):
    __collection__ = 'pagetype'
    __database__ = DB_NAME

    structure = {
        "name": basestring,  # name for the pagetype
        "page_type_image": basestring,  # static image to be shown on the add/edit dialogs to help user choose a pagetype
        "layouts": [PageLayout]  # each pagetype has 1 or more applicable layouts
    }


PageVariation = {
    "name": unicode,  # this is what gets shown on the add/edit page dialogs
    "is_active": bool,  # DO NOT RELY ON THIS VALUE, the active variation is tracked by the page. Formerly decided which variation gets shown on the dealer site.
    "provided": bool,  # TODO: need to track if this variation is provided by an admin
    "type": basestring,  # PageType.name - a page type is associated with a variation and not a page
    "layout": basestring  # PageLayout.name
}

Page = {
    "path": unicode,
    "name": LocalizedString,
    "owner": basestring,  # the pa code of the dealer who owns the page
    "settings": {
        "locked": bool,  # Admin can lock a page so that dealer can't edit its properties via DMT
        "visible": bool  # Dealer can make a page visible or invisible on his dealer site. An invisible page cannot be accessed even via directly hitting the URL
    },
    "variations": [PageVariation],  # each page has a list of variations
    "active_variation": int,
    "title": LocalizedString,  # this gets shown on the page as a content, should be a localized string
    "content": dict,  # to be replaced with the partials
    "applicability": Applicability
}

Minishowroom = {
    "brand_ordering": [basestring],
    "vehicle_type_ordering": [VEHICLE_TYPE],
    "date_ordering": DATE_ORDER_TYPE,
    "price_ordering": PRICE_ORDER_TYPE,
    "orderby_type": ORDER_BY_TYPE
}

SlideshowSettings = {
    "uid": basestring,
    'image': {
        'en': basestring,
        'es': basestring,
        'fr': basestring
    },
    'type': IS(u'heroshot', u'campaign'),
    'landing_url': basestring,
    'metadata': basestring
}


class DealerSite(BaseDocument):
    __collection__ = 'dealer_site'
    __database__ = DB_NAME

    structure = {
        "theme": basestring,  # see Themes.themeid
        "pages": dict,  # a dictionary that maps page path to Page structure defined above
        "navigation": {
            "header": [[NavItem]],  # header is a list of lists
            "more": {
                "show_menu": bool,
                "navitems": [[NavItem]]
            }  # more is also a list of lists
        },
        "owner": basestring,  # dealer.pacode
        "language": {  # site language settings
            "default": unicode,
            "enabled": [unicode],
            "enable_google_translate": bool
        },
        "dmt_language": {  # dealer maintenance tool language settings
            "default": unicode
            #  ,"enabled": [unicode]
        },
        "social_media": [  # dealer social media site settings
        {"twitter": {"enabled": bool, "url": basestring}},
        {"facebook": {"enabled": bool, "url": basestring}},
        {"youtube": {"enabled": bool, "url": basestring}}
        ],
        "privacy_policy": {
        "enabled": bool,
        "policy_text": LocalizedString
        },
        "dealer_disclaimer": {
        "enabled": bool,
        "disclaimer_text": LocalizedString
        },
        "showroom_defaults": {
            "year": basestring,
            "make": MAKE_TYPE,
            "model": basestring,
            "show_commercial_trucks": bool
        },
        "used_inventory_settings": {
            "is_autocheck_enabled": bool,
            "view": VIEWS_TYPE,
            "sort_by": USED_INVENTORY_SORT_TYPE,
            "dcpais": {  # PAIS dealer settings
                "lead_form_button_text": LocalizedString
            },
            "canada_additional": {
                "lead_form_button_text": LocalizedString
            }
        },
        "new_inventory_settings": {
            FORD: {
                "sort_by": NEW_INVENTORY_SORT_TYPE,
                "view": VIEWS_TYPE,
                "show_commercial_trucks": bool,
                "inv_default": {
                    "vehicle_type": VEHICLE_TYPE,
                    "year": basestring,
                    "model": unicode
                }
            },
            LINCOLN: {
                "sort_by": NEW_INVENTORY_SORT_TYPE,
                "view": VIEWS_TYPE,
                "inv_default": {
#                    "vehicle_type": VEHICLE_TYPE,
                    "year": basestring,
                    "model": unicode
                }
            },
            "dcpais": {
                "is_dealer_pricing_enabled": bool,
                "is_inline_incentives_enabled": bool,
                "is_axz_pricing_enabled": bool,
                "axz_plan_type": AXZ_PLAN_TYPE,
                "lead_form_button_text": LocalizedString
            },
            "canada_additional": {
                "is_dealer_pricing_enabled": bool,
                "is_inline_incentives_enabled": bool,
                "lead_form_button_text": LocalizedString
            }
        },
        'minishowroom': Minishowroom,
        'slideshow_settings': [SlideshowSettings],
        'dealer_script': {
            'script_text': basestring,
            'script_position': DEALER_SCRIPT_POSITION._operands.append(u'')
        },
        'homepage_welcome_text': {
            'heading': LocalizedString,
            'content': LocalizedString
        },
        'analytics_id': basestring
    }

    # TODO: Add a better mechanism for default site values
    def create_site(self, owner, theme, navigation, language,
                    social_icons=None, privacy_policy=None, dealer_disclaimer=None,
                    showroom_defaults=None, new_inventory_settings=None,
                    used_inventory_settings=None, dmt_language=None,
                    dealer_script=None, slideshow_settings=None, analytics_id=None):
        site = self.db.DealerSite()
        site['_id'] = 'site%s' % owner
        site['owner'] = owner
        site['theme'] = theme
        site['navigation'] = navigation
        site['language'] = language
        site['dmt_language'] = dmt_language or {"default": language['default']}

        if slideshow_settings is not None:
            site['slideshow_settings'] = slideshow_settings

        if showroom_defaults is not None:
            site['showroom_defaults'] = showroom_defaults

        if new_inventory_settings is not None:
            site['new_inventory_settings'] = new_inventory_settings

        if social_icons is None:
            social_icons = [  # dealer social media default settings for a new dealerSite
                {"twitter": {"enabled": False, "url": ''}},
                {"facebook": {"enabled": False, "url": ''}},
                {"youtube": {"enabled": False, "url": ''}}
            ]  # Instead of a default param,added the setting here for readability

        site['social_media'] = social_icons

        if social_icons is not None:
            site['social_media'] = social_icons

        if privacy_policy is not None:
            site['privacy_policy'] = privacy_policy

        if dealer_disclaimer is not None:
            site['dealer_disclaimer'] = dealer_disclaimer

        if used_inventory_settings is not None:
            site['used_inventory_settings'] = used_inventory_settings

        if dealer_script is not None:
            site['dealer_script'] = dealer_script

        if analytics_id is not None:
            site['analytics_id'] = analytics_id
        site.save()
        return site

    def add_page(self, page):
        path = page['path']
        self['pages'][path] = page
        self.save()

        return self['pages'][path]

    def move_page(self, old_path, new_path):
        if new_path not in self['pages']:
            page = self['pages'][old_path]
            self['pages'][new_path] = page
            del self['pages'][old_path]
        else:
            raise KeyError  # TODO: Find a better exception to throw

    def add_page_variation(self, path, variation):
        self['pages'][path]['variations'].append(variation)

    def update_page(self, path, new_page):
        page = self['pages'][new_page['path']]
        page.update(new_page)

        self['pages'][path] = page

        if path != new_page['path']:
            self.move_page(path, new_page['path'])

        self.save()

    def update_page_variation(self, path, variation_id, new_variation):
        self['pages'][path]['variations'][variation_id].update(new_variation)
        self.save()

    def get_social_media(self, dealer):
        """
        Returns the status of the social media icons on the page header.
        """
        # Could be made cacheable
        enabled = dealer['country'] == CA and FORD in dealer['brands']

        social_media = self['social_media'] if 'social_media' in self else []
        is_edit = False
        icons = []

        for x in social_media:
            key, value = x.popitem()

            # Determines whether icons present and the mode
            if 'enabled' in value \
                    and value['enabled'] \
                    and key in SOCIAL_MEDIA_URLS:

                # Generate ordered tuple for icons
                icons.append((key, SOCIAL_MEDIA_URLS[key], value['url']))
                is_edit = True

        return {
            'isEnabled': enabled,
            'isEdit': is_edit,
            'icons': icons
        }


#===============================================================================
#    Partials code to be integrated later
#    def add_page(self, path, parts):
#        keys = path.split('/')[1:]
#        values = self['funny_pages']
#
#        for key in keys:
#            if key not in values:
#                values[key] = PartialContext()
#
#            values = values[key]
#
#        values.page_content = parts
#
#        return self
#
#    def add_page_from_json(self, path, json):
#        return self.add_page(path, PagePartial(json))
#=========================================================================


class Disclosures(BaseDocument):
    __collection__ = 'disclosures'
    __database__ = DB_NAME

    def get_top_disclosure_position(self):
        """

        :return:
        """
        last_doc = self.db.Disclosures.find_one(sort=[('relative_order', -1)])

        if last_doc and 'relative_order' in last_doc:
            return int(last_doc['relative_order'])
        return 0

    def add_disclosure(self, operating_unit=FMC, brands=None, state=None,
                       zips=None, status=UNPUBLISHED_DISCLOSURE, start_date=None, end_date=None,
                       pages=None, disclosure_text=None):

        """

        :param operating_unit:
        :param brands:
        :param state:
        :param zips:
        :param start_date:
        :param end_date:
        :param pages:
        :param disclosure_text:
        """
        disclosures = self.db.Disclosures()

        disclosure_text = disclosure_text or {'en': '', 'es': '', 'fr': ''}
        zip_codes = zips or []
        state = state or []
        start_date = start_date or datetime.datetime.now()
        end_date = end_date or (start_date + datetime.timedelta(days=180))
        pages = pages or {
            'admin_pages': [], 'dealer_pages': []
        }

        disclosures['operating_unit'] = operating_unit
        disclosures['brands'] = brands or [FORD]
        disclosures['state'] = state
        disclosures['postal_code'] = zip_codes
        disclosures['status'] = status
        disclosures['start_date'] = start_date
        disclosures['end_date'] = end_date
        disclosures['pages'] = pages
        disclosures['disclosure_text'] = disclosure_text
        disclosures['relative_order'] = self.get_top_disclosure_position() + 1

        disclosures.save()

    structure = {
        'operating_unit': OPERATING_UNITS,
        'brands': BRANDS,
        'state': [basestring],  # list of subnational codes
        'postal_code': [basestring],
        'status': DISCLOSURE_STATUS,
        'start_date': datetime.datetime,
        'end_date': datetime.datetime,
        'pages': dict,  # List of page paths
        'disclosure_text': LocalizedString,
        'relative_order': int  # higher value ones to the top. Desc ordering
    }

# Admin Message
GLOBAL_SCOPE = {'id': 'global', 'display_name': 'Global', 'value': {}}
REGIONAL_SCOPE = {
    'id': 'regional', 'display_name': 'Regional', 'value': {
    'region': IS(FMC_REGION, FOC_REGION), 'regions': [basestring]
    }}
OPERATING_UNIT_SCOPE = {'id': 'operation', 'display_name': 'Operating Unit',
                        'value': {'operating_unit': OPERATING_UNITS,
                                  'brands': BRANDS}}
DEALER_SCOPE = {'id': 'dealer', 'display_name': 'Dealer', 'value': {
                'pacode': [basestring]
                }}

MESSAGES_SCOPE = IS(
    GLOBAL_SCOPE, REGIONAL_SCOPE, OPERATING_UNIT_SCOPE, DEALER_SCOPE)

INVALID_CONTENT_MESSAGE_TYPE = u'invalidcontent'
DEALER_MESSAGES_TYPE = u'dealermessage'


class AdminMessages(BaseDocument):
    __collection__ = 'admin_messages'
    __database__ = DB_NAME

    def add_or_update_message(self, message_id=None, scope=None, title=None,
                              image=None, message_text=None, scope_details=None,
                              published_date=None, message_type=DEALER_MESSAGES_TYPE):

        if message_id:
            message = self.db.AdminMessages.find_one(
                {'_id': ObjectId(message_id)}
            )
            read_by = message['read_by']
        else:
            message = self.db.AdminMessages()
            read_by = list()

        scope = scope or unicode(GLOBAL_SCOPE['id'])
        title = title or {'en': '', 'es': '', 'fr': ''}
        image = image or {'en': '', 'es': '', 'fr': ''}
        message_text = message_text or {'en': '', 'es': '', 'fr': ''}
        scope_details = scope_details or GLOBAL_SCOPE
        published_date = published_date or datetime.datetime.now()

        if str(scope) == scope_details['id']:
            message['scope'] = scope
            message['title'] = title
            message['image'] = image
            message['message_text'] = message_text
            message['scope_details'] = scope_details
            message['published_date'] = published_date
            message['message_type'] = message_type
            message['read_by'] = read_by

            message.save()
        else:
            raise Exception("Scope should match with ScopeDetails Id")

    structure = {
        'scope': IS(unicode(GLOBAL_SCOPE['id']), unicode(REGIONAL_SCOPE['id']),
                    unicode(
                    OPERATING_UNIT_SCOPE['id']), unicode(DEALER_SCOPE['id'])),
        'title': LocalizedString,
        'image': LocalizedString,
        'message_text': LocalizedString,
        'scope_details': MESSAGES_SCOPE,
        'published_date': datetime.datetime,
        'message_type': IS(DEALER_MESSAGES_TYPE, INVALID_CONTENT_MESSAGE_TYPE),
        'read_by': [basestring]  # List of pacodes who've read this message
    }


class Campaigns(BaseDocument):
    __collection__ = 'campaigns'
    __database__ = DB_NAME

    structure = {
        'name': basestring,
        'open_in_new_window': bool,
        'scope': IS(u'operating_unit', u'regional'),  # As REGIONAL and OPERATING_UNITS already have IS operator, nested IS can't be there, so IS(REGIONAL, OPERATING_UNITS) wasn't possible
        'regional': REGIONAL,
        'operating_unit': OPERATING_UNITS,
        'start_date': datetime.datetime,
        'end_date': datetime.datetime,
        'brands': [IS(FORD, LINCOLN)],
        'homepage_heroshot_image': CAMPAIGN_IMAGE,
        'interior_promotiles': [CAMPAIGN_IMAGE],
        'disclosure_text': LocalizedString,
        'status': IS(u'Published', u'Draft'),

        'published_date': datetime.datetime,
        'update_date': datetime.datetime
    }

    def create_or_update(self, id=None, **kwargs):
        """Create or update a campaign
        **Parameters:**
            :id: campaign id
        """
        if id:
            campaign = self.db.Campaigns.find_one({'_id': ObjectId(id)})
        else:
            campaign = self.db.Campaigns()
            campaign['status'] = u'Draft'
    
        campaign.update(**kwargs)
        campaign['start_date'] = datetime.datetime.combine(
            campaign['start_date'], datetime.time(0, 0))
        campaign['end_date'] = datetime.datetime.combine(
            campaign['end_date'], datetime.time(0, 0))
        campaign['update_date'] = datetime.datetime.now()
        campaign.save()
        
    def publish_campaign(self, id):
        campaign = '' #api.get_campaign(id)
        campaign['status'] = u'Published'
        campaign.save()

# dealer_code -> { 'date' -> [ {ChangeDescription} ] }
ChangeDescription = {
    basestring: [{
        'user_id': basestring,
        'change_id': basestring,
        'change_type': CHANGE_TYPES,
        'description': basestring,
    }]
}


class ChangeHistory(BaseDocument):
    __collection__ = 'change_history'
    __database__ = DB_NAME

    structure = {
        'dealer_code': basestring,
        'change_description': ChangeDescription
    }


class Lead(BaseDocument):
    __collection__ = 'lead_info'
    __database__ = DB_NAME

    structure = {
        "data": {unicode: unicode},
        "dealer_code": basestring,
        "lead_type": basestring,
        "title": basestring,
        "first_name": basestring,
        "last_name": basestring,
        "language": basestring,
        "street": basestring,
        "city": basestring,
        "postal_code": basestring,
        "country": basestring,
        "state": basestring,
        "phone_number": basestring,
        "email": basestring,
        "evening_phone": basestring,
        "day_phone_ext": basestring,
        "comments": basestring,
        "status": basestring,
        "make": basestring,
        "model": basestring,
        "year": basestring,
        "lead_source": basestring,
        "page_name": basestring,
        "name_plate": basestring,
        "transmission": basestring,
        "trim_name": basestring,
        "exterior": basestring,
        "lead_id": basestring,
        "system_comments": basestring,
        "purchase_timeframe": basestring,
        "payment_method": basestring,
        "preferred_contact_method": basestring,
        "preferred_contact_time": basestring,
        "send_offers_mail": bool,
        "preferred_contact_am_pm": basestring,
        "provider_service": basestring,
        "VIN": basestring,
        "first_pref_date": basestring,
        "first_pref_time": basestring,
        "first_pref_month": basestring,
        "lang": basestring,
        "interior": basestring,
        "dlr_inv_url": basestring,
        "mnf_stage": basestring,
        "to_email_address": basestring,
        "is_invalid_lead": bool,
        "mileage": basestring,
        "symptoms_or_comments": basestring,
        "service_parts_req": basestring,
        "preferred_rental_vehicle": basestring,
        "first_pref_service_appt_date": basestring,
        "first_pref_service_appt_month": basestring,
        "first_pref_service_appt_time": basestring,
        "other_option_service_appt_date": basestring,
        "other_option_service_appt_month": basestring,
        "other_option_service_appt_time": basestring,
        "request_type": basestring,
        "pickup_date": basestring,
        "pickup_time": basestring,
        "dropoff_date": basestring,
        "dropoff_time": basestring,
        "dealer_region_id": basestring,
        "dealer_id": basestring,
        "requested_vehicle_id": basestring,
    }


class TradeInLead(BaseDocument):
    __collection__ = "tradein_lead"
    __database__ = DB_NAME

    structure = {
        "lead_type": unicode,
        "lead_source": unicode,
        "lead_id": unicode,
        "first_name": unicode,
        "last_name": unicode,
        "address": unicode,
        "city": unicode,
        "state": unicode,
        "zip": unicode,
        "phone_number": unicode,
        "email": unicode,
        "year": unicode,
        "make": unicode,
        "model": unicode,
        "mileage": unicode,
        "ext_color": unicode,
        "trim_series": unicode,
        "style": unicode,
        "transmission": unicode,
        "air_conditioning": unicode,
        "power_windows": unicode,
        "power_lock": unicode,
        "power_seats": unicode,
        "cruise_control": unicode,
        "navigation_system": unicode,
        "sunroof": unicode,
        "dvd_player": unicode,
        "satellite_radio": unicode,
        "cdplayer_changer": unicode,
        "am_fm_sterio": unicode,
        "cassette": unicode,
        "leather_interior": unicode,
        "alloy_wheels": unicode,
        "spoiler": unicode,
        "ext_body_rating": unicode,
        "engine_rating": unicode,
        "tires_rating": unicode,
        "interior_rating": unicode,
        "buy_vehicle_new": unicode,
        "paint_work": unicode,
        "existing_damage": unicode,
        "damage_degree": unicode,
        "options_accessories": unicode,
        "accidents": unicode,
        "cost_repair": unicode,
        "dealer": unicode,
        "is_invalid_lead": bool
    }

MODEL_LIST = [Dealer, DealerSite, PageType, Lead, ImageLibrary, TradeInLead,
              Domain, Disclosures, Campaigns, AdminMessages, UserRole,
              ChangeHistory]
