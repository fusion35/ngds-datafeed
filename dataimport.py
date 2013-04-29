from ConfigParser import RawConfigParser
from datetime import datetime
from mongokit.connection import Connection
from ngds.core import model
from xml.etree import ElementTree
import sys
  
def main():    
    if len(sys.argv) > 1: 
        parser = RawConfigParser()        
        parser.read(sys.argv[1])
        global connection
        connection = Connection(parser.get('main', 'mongodb.connection_string')) 
        #ngdsDB = parser.get('main', 'mongodb.db_name')
        xmlFile = open(parser.get('main', 'xml.datasource.location'))
        connection.register(model.MODEL_LIST)
        dbDealers = connection.Dealer.find({},{'code':1, '_id':0})
        dbDealerList =[]        
        for d in dbDealers:dbDealerList.append(d['code'])        
        root = ElementTree.parse(xmlFile).getroot()
        #print getattr(connection, model.DB_NAME)
        feedDealer = FeedDealer(root)
        feedDealer.ensureIntegrity(dbDealerList)
        

class FeedDealer :    
    feedData ={}
    #This an attribute mapping between model and xml        
    attrMapping = {
                   'orgid':'OrgId',
                   'code':'PaCode',
                   'secondary_pa_code':'SecondaryPaCode',                   
                   'name':'Name',
                   'country':'Country',
                   'region':'Region',
                   'latitude':'Latitude',
                   'longitude':'Longitude',
                   'display_phone':'DisplayPhone',
                   'email_internal':'Email',
                   'primary_email':'Email',
                   'fax': 'Fax',                   
                   'phone':'Phone',
                   'subdomain':'Subdomain',
                   'sales_code':'SalesCode',
                   'brands':'Brands',
                   'settings':{
                               'is_GeS_enabled':'is_GeS_enabled',
                               'is_hev':'is_hev',
                               'is_certified_preowned':'is_certified_preowned',
                               'is_rent_a_car':'is_rent_a_car',
                               'is_fordparts_opted':'is_fordparts_opted',
                               'is_PAIS_enrolled':'is_PAIS_enrolled',
                               'is_flood_light_enabled':'is_flood_light_enabled',
                               'is_autocheck_subscribed':'is_autocheck_subscribed',
                               'is_SVT':'is_SVT',
                               'is_internet_certified':'is_internet_certified',
                               'is_blue_oval_certified':'is_blue_oval_certified',
                               'is_lincoln_premier_experience_certified':'is_lincoln_premier_experience_certified',
                               'is_premier':'is_premier'
                              },
                   'primary_address':{
                                      'street1':'Street',
                                      'city':'City',
                                      'state':'State',
                                      'postal_code':'PostalCode',
                                      'label':'Label'
                                      }                  
                  }

    def __init__(self, root=None):        
        if root is not None:
            attrDict = {'settings': 'Settings', 'primary_address':'PrimaryAddress'}
            startDate = datetime.now() 
            print 'Start reading xml file'
            
            for dealer in root.findall('Dealer'):
                dealerData = {}
                for k, v in self.attrMapping.iteritems(): 
                    if k in ['brands', 'settings', 'primary_address']:                        
                        if k == 'brands':
                            dealerData.update({k:[i.attrib['value'] for i in list(dealer.find('Brands'))]})
                        else:
                            attr = attrDict[k]
                            subData={}
                            for k1, v1 in v.iteritems() :
                                subData.update({k1: self._castvalue(k+'.'+k1,dealer.find(attr+'/'+v1).text)})                                
                            dealerData.update({k:subData})
                    else:
                        dealerData.update({k: self._castvalue(k,dealer.find(v).text)})
        
                self.feedData.update({dealerData.get('code'):dealerData})       
            print 'Done reading xml file in '+str(datetime.now()-startDate)
    
    def _castvalue(self, key, textvalue):
        datatype = None
        if '.' in key:
            #Ignore TypeError that will raise in case of primary_address 
            #where structure is not explicit but only type is provided
            #in the DB structure.  
            try:
                datatype = reduce(dict.get, key.split('.'), model.Dealer.structure)
            except(TypeError):
                pass
        else:
            datatype = model.Dealer.structure.get(key)
        if datatype in (float, bool, unicode):
            return (datatype)(textvalue)
        return textvalue
        
                
    def ensureIntegrity(self, dbDealerList):               
        feedDealerList = self.feedData.keys()
        allDealers = set(dbDealerList + feedDealerList)
        commondealers, dbonlydealers, feedonlydealers = set(), set(), set()        
        for aDealer in allDealers :
            if aDealer in dbDealerList and aDealer in feedDealerList :
                commondealers.add(aDealer)
                continue  
            if  aDealer in dbDealerList and aDealer not in feedDealerList :
                dbonlydealers.add(aDealer)
                continue
            if  aDealer in feedDealerList and aDealer not in  dbDealerList:
                feedonlydealers.add(aDealer)            
            
        print 'Common Dealer ',commondealers
        #self._updateDealersInDB(commondealers)
        print 'Feed Dealer ',feedonlydealers
        self._insertDealersInDB(feedonlydealers)
        print 'DB Dealer ',dbonlydealers
        self._markDealerAsExpired(dbonlydealers)
                
    def _updateDealersInDB(self, commondealers):
        #processing Common dealers (updating)
        #TODO: primary address need to updated in a way so 
        #that uuid dosn't get removed
        if len(commondealers) > 0 :
            print 'Starting to process common dealer \n'            
            for aDealer in commondealers :
                fDealer = self.feedData.get(aDealer)                
                dbDealer = connection.Dealer.find_one({'code':aDealer})
                print dbDealer
                updateflag = False
                print 'Processing', dbDealer['code'], '\n'
                for k in self.attrMapping.keys():                      
                    print 'Is',k,'matching :', dbDealer[k] == fDealer[k]                      
                    if fDealer[k] != dbDealer[k]:                       
                        print dbDealer[k], 'updated with ', fDealer[k]
                        updateflag = True 
                        dbDealer[k] = fDealer[k]
                print dbDealer
                if updateflag:
                    dbDealer['dealer_type'] = 'dataUpdatedDealer'
                    dbDealer.save()
                    print 'Changes Saved for',dbDealer['code'],'\n'
                    
    def _insertDealersInDB(self, feedonlydealers):
        DEFAULT_DEALERSHIP_INFO = {
                                   'display_dealer_phone': True,
                                   'display_style': model.VERTICAL_LIST,
                                   'department_contact': [], 
                                   'pcs_additional': {}
                                   }
        if len(feedonlydealers) > 0:
            print 'starting to process feed dealer \n'
            for aDealer in feedonlydealers :
                fDealer = self.feedData.get(aDealer)
                dealer = connection.Dealer()
                dealer = fDealer
                dealer['dealership_info'] = DEFAULT_DEALERSHIP_INFO
                dealer['dealer_type'] = 'displacedDealer'
                dealer.save()
                print dealer
    
    def _markDealerAsExpired(self, dbonlydealers):        
        if len(dbonlydealers) > 0:
            print 'starting to process DB dealer \n'
            for aDealer in dbonlydealers :
                fDealer = self.feedData.get(aDealer)
                dealer = connection.Dealer()
                dealer = fDealer
                dealer['dealership_info'] = DEFAULT_DEALERSHIP_INFO
                dealer['dealer_type'] = 'displacedDealer'
                dealer.save()
                print dealer
        
               
if __name__ == '__main__':
    main()
