'''
Created on Nov 7, 2011

@author: Dusan
'''
import time
from pysimplesoap.client import SoapClient
from pysimplesoap.simplexml import SimpleXMLElement
from datetime import datetime
import atomia_entities

class AtomiaActions(object):
    
    def __init__(self, username, password, api_url = None, token_created = None, token_expires = None, soap_header = None, body_xmlns = None):

        if token_created is None:
            self.created = datetime.fromtimestamp(time.mktime(time.gmtime())).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            self.created = token_created
        
        if token_expires is None:
            self.expires = datetime.fromtimestamp(time.mktime(time.gmtime()) + 300).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            sefl.expires = token_expires 
        
        self.username = username
        self.password = password
        self.api_url = api_url
        
        if soap_header is None:

            self.header = """<soap:Header xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" 
                            xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
                <wsse:Security soap:mustUnderstand="1">
                    <wsu:Timestamp wsu:Id="_0">
                        <wsu:Created>%(Created)s</wsu:Created>
                        <wsu:Expires>%(Expires)s</wsu:Expires>
                    </wsu:Timestamp>
                    <wsse:UsernameToken wsu:Id="uuid-8a45f51b-fe46-4715-bdae-e596c36ad6be-1">
                      <wsse:Username>%(Username)s</wsse:Username>
                      <wsse:Password
                        Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">
                         %(Password)s
                      </wsse:Password>
                   </wsse:UsernameToken>
                </wsse:Security>
            </soap:Header>"""
            
            self.header = self.header % dict(Created=self.created, Expires=self.expires, Username = self.username, Password = self.password)
        else:
            self.header = soap_header
            
        if body_xmlns is None:
            self.body_xmlns = 'xmlns:prov="http://atomia.com/atomia/provisioning/" xmlns:atom="http://schemas.datacontract.org/2004/07/Atomia.Provisioning.Base" xmlns:arr="http://schemas.microsoft.com/2003/10/Serialization/Arrays"'
        else:
            self.body_xmlns = body_xmlns
            
        self.client = SoapClient(wsdl=self.api_url if self.api_url is not None else "https://provisioning.int.atomia.com/CoreAPIBasicAuth.svc?wsdl", header=self.header, body_xmlns= self.body_xmlns, namespace="http://atomia.com/atomia/provisioning/", trace=False)
    
    def add_account(self, account):
        
        return self.client.AddAccount(account = account)
        
    def create_service(self, service_name, parent_service, account_number):

        return self.client.CreateService(
                                    serviceName = service_name,
                                    parentService = parent_service,
                                    accountName = account_number)
        
    def add_service(self, service, parent_service, account_number, resource_request_descriptions = None):

        return self.client.AddService(
                                    service = service,
                                    parentService = parent_service,
                                    accountName = account_number,
                                    resourceRequestDescriptions = resource_request_descriptions)
        
    def delete_service(self, service, account_number):

        return self.client.DeleteService(
                                    service = service,
                                    accountName = account_number)
        
        
    def modify_service (self, service, account_number):

        return self.client.ModifyService(
                                    service = service,
                                    accountName = account_number)

        
    def find_services_by_path_with_paging(self, search_criteria_list, account_number, search_properties = None,  sort_by_prop_name = '', sort_asc = 'true', page_number ='0', page_size = '100'):

        return self.client.FindServicesByPathWithPaging(searchCriteriaList = search_criteria_list,
                                                 properties = search_properties,
                                                 account = account_number,
                                                 sortByPropName = sort_by_prop_name,
                                                 sortAsc = sort_asc,
                                                 pageNumber = page_number,
                                                 pageSize = page_size)
        
    def get_service_by_id(self, account_number, service_id):
        return self.client.GetServiceById(accountId = account_number,
                                          serviceID = service_id)
        
    def list_existing_service(self, parent_service, account_number, get_logical_children = 'true', sort_asc = 'true', page_number ='0', page_size = '100'):
        return self.client.ListExistingServices(parentService = parent_service,
                                                getLogicalChildren = get_logical_children,
                                                accountId = account_number,
                                                sortAsc = sort_asc,
                                                pageNumber = page_number,
                                                pageSize = page_size)