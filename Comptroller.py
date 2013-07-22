'''
Comptroller API Library
'''

import requests

class Budget:
    def __init__(self,ID,key):
        '''
        Create Budget Object: object = Comptroller.Budget('ID' ,'key')
        '''
        self.ID = ID
        self.key = key
        self.type = 'Budget'

        self.headers = {'app_id': self.ID,'app_key' : self.key }
        self.url = 'https://api.cityofnewyork.us/comptroller/v1/api'

        self.format_dict = {'max_records':'max' , 'record_from':'max',
                            'year':'exact' , 'budget_code':'exact' ,
                            'agency_code':'max' , 'department_code':'max' ,
                            'expense_category':'max' , 'adopted':'max' ,
                            'modified':'max' , 'pre_encumbered':'max',
                            'encumbered':'max' , 'accrued_expense':'max',
                            'cash_expense':'max', 'post_adjustment':'max'
                            }

        self.predef_dict = {'max_records': 4 , 'record_from': 15,
                            'year': 4 , 'budget_code': 4 ,
                            'agency_code': 3 , 'department_code': 3 ,
                            'expense_category': 3 , 'adopted': 18 ,
                            'modified': 18 , 'pre_encumbered': 18,
                            'encumbered': 18 , 'accrued_expense': 18,
                            'cash_expense': 18, 'post_adjustment': 18
                            }

        self.valGlobRange = {'year':'value' , 'budget_code':'value',
                           'agency_code':'value','department_code':'value',
                           'expense_category':'value' , 'adopted':'range',
                           'modified':'range' , 'pre_encumbered':'range',
                           'encumbered':'range', 'accrued_expense':'range',
                           'cash_expense':'range', 'post_adjustment':'range',
                           'max_records':'global' , 'record_from':'global'
                            }
        self.criterias,self.global_criterias,self.response_columns = {},{},{}

    def getKey(self):
        print self.key
        return self.key
    
    def setKey(self,newKey):
        print 'New Key:',newKey
        self.key = newKey

    def getID(self):
        print self.ID
        return self.ID
    
    def setID(self,newID)
        print 'New ID:',newID
        self.ID = newID
    
    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        Values: object.add_criteria(crit_name,value))
        Ranges: object.add_criteria(crit_name,startDate,endDate)


        Values:
        max_records , record_from , year , budget_code, 
        agency_code , department_code , expense_category, 

        Ranges:
        adopted , modified , pre_encumbered , encumbered,
        accrued_expense , cash_expense , post_adjustment
        '''
        try:
            criteria_type = self.valGlobRange[name]
            if criteria_type == 'value':
                self.create_value_criteria(name,valGlobDate)
            elif criteria_type == 'range':
                self.create_range_criteria(name,valGlobDate,endDate)
            elif criteria_type == 'global':
                self.create_global_criteria(name,valGlobDate)
                
        except KeyError:
            print 'Invalid Criteria Name Entered:',name

    def create_global_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.global_criterias.update({name:'<'+name+'>'+value+'</'+name+'>'})
            
    def create_value_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.criterias.update({name:("<criteria><name>" + name +
                                        "</name><type>value</type><value>"
                                         + value + "</value></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again:'

    def create_range_criteria(self,name,start,end):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        validateStart = self.validation(validation_type,validation_value,start)
        validateEnd =   self.validation(validation_type,validation_value,end)
        if validateStart == True and validateEnd == True:
            self.criterias.update({name:("<criteria><name>" + name + "</name><type>range</type><start>"
                                         + str(start) + "</start><end>"+ str(end) + "</end></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again:',start+' ',end

    def validation(self,val_type, validation_value, value):
        if val_type == 'exact':
            if len(str(value)) == validation_value:
                return True
        if val_type == 'max':
            if len(str(value)) <= validation_value:
                return True
        if val_type == 'date':
            check = value.split('-')
            if len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2:
                return True

        return False

    def add_response_column(self,name):
        '''
        object.create_response_column('name')

        Creates a Response Column to filter search results

        Response Columns:        
        agency , department , expense_category, 
        budget_code , budget_name , pre_encumbered, 
        accrued_expense , year , post_adjustment,
        modified , adopted , encumbered , cash_expense
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')

        Deletes a response column that was created for a specific object
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')

        Deletes a criteria that was created for a specific object
        '''
        try:
            if name == 'max_records' or name == 'record_from':
                del self.global_criterias[name]
            else:
                del self.criterias[name]
        except KeyError:
            print 'Criteria doesn\'t exist'
        

    def getBudget(self):
        '''
        Call to Budget API: object.getBudget()

        Returns the results as XML text
        '''
        budgetString = ('<request><type_of_data>Budget</type_of_data>')
        #Adding global criteria filters
        for key in self.global_criterias.keys():
            budgetString += self.global_criterias[key]

        #Adding optional criteria filters
        budgetString += '<search_criteria>'
        if len(self.criterias) != 0:
            for key in self.criterias.keys():
                budgetString += self.criterias[key]

        #Adding response columns
        budgetString += "</search_criteria><response_columns>"
        if len(self.response_columns) != 0:
            for key in self.response_columns.keys():
                budgetString += self.response_columns[key]
        budgetString += "</response_columns></request>"
        
        #print budgetString
        self.budgetRequest = requests.post(self.url, data=budgetString,headers=self.headers)
        print 'Status Code:', self.budgetRequest.status_code
        #print 'Sample Info:', self.budgetRequest.text[0:500]
        return self.budgetRequest.text
            
            
class Contracts:
    def __init__(self,ID,key):
        self.ID = ID
        self.key = key

        self.headers = {'app_id': self.ID,'app_key' : self.key }
        self.url = 'https://api.cityofnewyork.us/comptroller/v1/api'

        self.format_dict = {'fiscal_year': 'max' , 'calendar_year':'max',
                            'status':'list' , 'category':'list' ,
                            'vendor_code':'max', 'contract_type':'max',
                            'agency_code':'max' , 'contract_id':'max',
                            'award_method':'max' , 'current_amount':'max',
                            'start_date':'date' , 'end_date':'date',
                            'registration_date':'date' , 'received_date':'date',
                            'max_records':'max' , 'record_from':'max'
                            }

        self.predef_dict = {'fiscal_year': 4 , 'calendar_year': 4,
                            'status' : ['active','pending','registered'],
                            'category':['expense','revenue'],
                            'vendor_code': 4, 'contract_type': 2,
                            'agency_code': 4, 'contract_id': 32,
                            'award_method': 3, 'current_amount': 18,
                            'start_date': 'YYYY-MM-DD', 'end_date': 'YYYY-MM-DD',
                            'registration_date': 'YYYY-MM-DD',
                            'received_date': 'YYYY-MM-DD',
                            'max_records': 4 , 'record_from':15
                            }

        self.valGlobRange = {'fiscal_year':'value' , 'calendar_year':'value',
                             'status':'value' , 'category':'value',
                             'vendor_code':'range' , 'contract_type':'value',
                             'agency_code':'value' , 'contract_id':'value',
                             'award_method':'value', 'current_amount':'range',
                             'start_date':'range' , 'end_date':'range',
                             'registration_date':'range' , 'received_date':'range',
                             'max_records':'global' , 'record_from':'global'
                             }

        self.criterias,self.global_criterias,self.response_columns = {},{},{}

    def getKey(self):
        print self.key
        return self.key
    
    def setKey(self,newKey):
        print 'New Key:',newKey
        self.key = newKey

    def getID(self):
        print self.ID
        return self.ID
    
    def setID(self,newID)
        print 'New ID:',newID
        self.ID = newID

    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        Values: object.add_criteria(crit_name,value))
        Ranges: object.add_criteria(crit_name,startDate,endDate)

        Required Values:
        status(Value options: active, pending or registered)
        category(Value options: expense OR revenue)
        

        Values:
        max_records , record_from , fiscal_year OR calendar_year,
        vendor_code , contract_type , agency_code , contract_id,
        award_method 
        
        Ranges:
        current_amount , start_date , end_date,
        registration_date , received_date
        '''
        try:
            criteria_type = self.valGlobRange[name]
            if criteria_type == 'value':
                self.create_value_criteria(name,valGlobDate)
            elif criteria_type == 'range':
                self.create_range_criteria(name,valGlobDate,endDate)
            elif criteria_type == 'global':
                self.create_global_criteria(name,valGlobDate)
                
        except KeyError:
            print 'Invalid Criteria Name Entered:',name

    def create_global_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.global_criterias.update({name:'<'+name+'>'+str(value)+'</'+name+'>'})
            
    def create_value_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.criterias.update({name:("<criteria><name>" + name +
                                        "</name><type>value</type><value>"
                                         + value + "</value></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again'

    def create_range_criteria(self,name,start,end):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        validateStart = self.validation(validation_type,validation_value,start)
        validateEnd =   self.validation(validation_type,validation_value,end)
        if validateStart == True and validateEnd == True:
            self.criterias.update({name:("<criteria><name>" + name + "</name><type>range</type><start>"
                                         + str(start) + "</start><end>"+ str(end) + "</end></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again:',start+' ',end

    def validation(self,val_type, validation_value, value):
        if val_type == 'exact':
            if len(str(value)) == validation_value:
                return True
        if val_type == 'max':
            if len(str(value)) <= validation_value:
                return True
        if val_type == 'date':
            check = value.split('-')
            if len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2:
                return True
        if val_type == 'list':
            for i in range(len(validation_value)):
                if value == validation_value[i]:
                    return True

        return False

    def add_response_column(self,name):
        '''
        object.create_response_column('name')

        Creates a Response Column to filter search results

        Response Columns:

        -----All Statuses & Categories:-----
        contract_id , purpose , version ,
        parent_contract , original_amount,
        current amount, apt_pin , vendor,
        agency , contract_type , award_method,
        start_date , end_date , pin,
        contract_industry , document_code

        -----Status:Active & Registered - Category:Expense:-----
        expense_category , spend_to_date
        registration_date

        -----Status:Active & Registered - Category: Revenue:-----
        year

        -----Status:Pending - Category: Expense & Revenue:-----
        original_modified

        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')

        Delete a response column filter for a specific object
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')

        Delete a criteria filter for a specific object
        '''
        try:
            if name == 'max_records' or name == 'record_from':
                del self.global_criterias[name]
            else:
                del self.criterias[name]
        except KeyError:
            print 'Criteria doesn\'t exist'
        

    def getContracts(self):
        '''
        Call to Contracts API: object.getBudget()

        Get Contracts information for a specific object

        Returns text in XML format
        '''
        cString = ('<request><type_of_data>Contracts</type_of_data>')
        #Adding global criteria filters
        for key in self.global_criterias.keys():
            cString += self.global_criterias[key]

        #Adding optional criteria filters
        cString += '<search_criteria>'
        if len(self.criterias) != 0:
            for key in self.criterias.keys():
                cString += self.criterias[key]

        #Adding response columns
        cString += "</search_criteria><response_columns>"
        if len(self.response_columns) != 0:
            for key in self.response_columns.keys():
                cString += self.response_columns[key]
        cString += "</response_columns></request>"
        
        #print cString
        self.contractsRequest = requests.post(self.url, data=cString,headers=self.headers)
        print 'Status Code:', self.contractsRequest.status_code
        #print 'Sample Info:', self.contractsRequest.text[0:500]
        return self.contractsRequest.text
            

        
        
class Payroll:
    def __init__(self,ID,key):
        self.ID = ID
        self.key = key
        
        self.headers = {'app_id': self.ID,'app_key' : self.key }
        self.url = 'https://api.cityofnewyork.us/comptroller/v1/api'

        self.format_dict = {'fiscal_year':'max', 'calendar_year': 'max',
                            'agency_code':'max', 'pay_frequency':'list',
                            'title':'list','pay_date':'date',
                            'amount': 'max' , 'amount_type': 'list',
                            'gross_pay':'max' , 'base_pay':'max',
                            'other_payments':'max', 'overtime_payments':'max',
                            'gross_pay_ytd':'max',
                            'max_records':'max' , 'record_from':'max'}

        self.predef_dict = {'fiscal_year': 4 , 'calendar_year': 4,
                            'agency_code': 4 ,
                            'pay_frequency':['BI-WEEKLY','MONTHLY','SUPPLEMENTAL'],
                            'title':['civil service title 1','civil service title 2',
                                     'civil service title 3'],
                            'pay_date':'YYYY-MM-DD', 'amount': 18,
                            'amount_type':['ANNUAL','RATE','ALL'], #All is default
                            'gross_pay':18 , 'base_pay':18 , 'other_payments':18,
                            'overtime_payments':18 , 'gross_pay_ytd':18,
                            'max_records': 4 , 'record_from':15
                            }

        self.valGlobRange = {'max_records':'global' , 'record_from':'global',
                             'fiscal_year':'value' , 'calendar_year':'value',
                             'agency_code':'value' , 'pay_frequency':'value',
                             'title':'value' , 'pay_date':'range',
                             'amount':'range' , 'amount_type':'value',
                             'gross_pay':'range' , 'base_pay':'range',
                             'other_payments':'range', 'overtime_payments':'range',
                             'gross_pay_ytd':'range'
                             }

        self.criterias,self.global_criterias,self.response_columns = {},{},{}

        #Setting default 
        self.criterias.update({'amount_type':'<criteria><name>amount_type</name><type>value</type>'+
                               '<value>ALL</value></criteria>'})

    def getKey(self):
        print self.key
        return self.key
    
    def setKey(self,newKey):
        print 'New Key:',newKey
        self.key = newKey

    def getID(self):
        print self.ID
        return self.ID
    
    def setID(self,newID)
        print 'New ID:',newID
        self.ID = newID
        
    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        Values: object.add_criteria(crit_name,value))
        Ranges: object.add_criteria(crit_name,startDate,endDate)


        Values:
        max_records , record_from , fiscal_year OR calendar year,
        agency_code , pay_frequency* , title*,
        pay_date , amount AND amount_type

        Ranges:
        gross_pay, base_pay, other_payments,
        overtime_payments , gross_pay_ytd
        '''
        try:
            criteria_type = self.valGlobRange[name]
            if criteria_type == 'value':
                self.create_value_criteria(name,valGlobDate)
            elif criteria_type == 'range':
                self.create_range_criteria(name,valGlobDate,endDate)
            elif criteria_type == 'global':
                self.create_global_criteria(name,valGlobDate)
                
        except KeyError:
            print 'Invalid Criteria Name Entered'

    def create_global_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.global_criterias.update({name:'<'+name+'>'+str(value)+'</'+name+'>'})
            
    def create_value_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.criterias.update({name:("<criteria><name>" + name +
                                        "</name><type>value</type><value>"
                                         + str(value) + "</value></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again'

    def create_range_criteria(self,name,start,end):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        validateStart = self.validation(validation_type,validation_value,start)
        validateEnd =   self.validation(validation_type,validation_value,end)
        if validateStart == True and validateEnd == True:
            self.criterias.update({name:("<criteria><name>" + name + "</name><type>range</type><start>"
                                         + str(start) + "</start><end>"+ str(end) + "</end></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again:',start+' ',end

    def validation(self,val_type, validation_value, value):
        if val_type == 'exact':
            if len(str(value)) == validation_value:
                return True
        if val_type == 'max':
            if len(str(value)) <= validation_value:
                return True
        if val_type == 'date':
            check = value.split('-')
            if len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2:
                return True
        if val_type == 'list':
            for i in range(len(validation_value)):
                if value == validation_value[i]:
                    return True

        return False

    def add_response_column(self,name):
        '''
        object.create_response_column('name')

        Response Columns:
        agency , fiscal_year , pay_frequency,
        hourly_rate, gross_pay, title,
        pay_date , base_pay, other_payments,
        overtime_payments, gross_pay_ytd,
        calendar_year, annual_salary
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')

        Delete a response column filter for a specific object
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')

        Delete a criteria filter for a specific object
        '''
        try:
            if name == 'max_records' or name == 'record_from':
                del self.global_criterias[name]
            else:
                del self.criterias[name]
        except KeyError:
            print 'Criteria doesn\'t exist'
        

    def getPayroll(self):
        '''
        Call to Payroll API: object.getPayroll()

        Get Payroll information

        Returns text in XML format
        '''
        payrollString = ('<request><type_of_data>Payroll</type_of_data>')
        #Adding global criteria filters
        for key in self.global_criterias.keys():
            payrollString += self.global_criterias[key]

        #Adding optional criteria filters
        payrollString += '<search_criteria>'
        if len(self.criterias) != 0:
            for key in self.criterias.keys():
                payrollString += self.criterias[key]

        #Adding response columns
        payrollString += "</search_criteria><response_columns>"
        if len(self.response_columns) != 0:
            for key in self.response_columns.keys():
                payrollString += self.response_columns[key]
        payrollString += "</response_columns></request>"
        
        #print payrollString
        self.payrollRequest = requests.post(self.url, data=payrollString,headers=self.headers)
        print 'Status Code:', self.payrollRequest.status_code
        #print 'Sample Info:', self.payrollRequest.text[0:500]
        return self.payrollRequest.text
            


class Revenue:
    def __init__(self,ID,key):
        self.ID = ID
        self.key = key
        self.headers = {'app_id': self.ID,'app_key' : self.key }
        self.url = 'https://api.cityofnewyork.us/comptroller/v1/api'

        self.format_dict = {'budget_fiscal_year':'exact' , 'fiscal_year':'max',
                            'agency_code':'max' , 'revenue_class':'max',
                            'fund_class':'max','funding_class':'max',
                            'revenue_category':'max' , 'revenue_source':'max',
                            'adopted':'max' , 'modified':'max',
                            'recognized':'max',
                            'max_records':'max' , 'record_from':'max'}

        self.predef_dict = {'budget_fiscal_year': 4 , 'fiscal_year': 4,
                            'agency_code': 3 , 'revenue_class': 3,
                            'fund_class': 4,'funding_class': 4,
                            'revenue_category': 2 , 'revenue_source': 5,
                            'adopted': 18 , 'modified': 18,
                            'recognized': 18,
                            'max_records': 4 , 'record_from':15}

        self.valGlobRange = {'max_records':'global' , 'record_from':'global',
                             'budget_fiscal_year':'value' , 'fiscal_year':'value',
                             'agency_code':'value','revenue_class':'value',
                             'fund_class':'value','funding_class':'value',
                             'revenue_category':'value', 'revenue_source':'value',
                             'adopted':'range' , 'modified':'range',
                             'recognized':'range'
                            }

        self.criterias,self.global_criterias,self.response_columns = {},{},{}

    def getKey(self):
        print self.key
        return self.key
    
    def setKey(self,newKey):
        print 'New Key:',newKey
        self.key = newKey

    def getID(self):
        print self.ID
        return self.ID
    
    def setID(self,newID)
        print 'New ID:',newID
        self.ID = newID
        
    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        Values: object.add_criteria(crit_name,value))
        Ranges: object.add_criteria(crit_name,startDate,endDate)


        Values:
        max_records , record_from , budget_fiscal_year,
        fiscal_year, agency_code, revenue_class,
        fund_class, funding_class, revenue_category,
        revenue_source
        
        Ranges:
        adopted, modified, recognized
        '''
        try:
            criteria_type = self.valGlobRange[name]
            if criteria_type == 'value':
                self.create_value_criteria(name,valGlobDate)
            elif criteria_type == 'range':
                self.create_range_criteria(name,valGlobDate,endDate)
            elif criteria_type == 'global':
                self.create_global_criteria(name,valGlobDate)
                
        except KeyError:
            print 'Invalid Criteria Name Entered'

    def create_global_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.global_criterias.update({name:'<'+name+'>'+str(value)+'</'+name+'>'})
            
    def create_value_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.criterias.update({name:("<criteria><name>" + name +
                                        "</name><type>value</type><value>"
                                         + str(value) + "</value></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again'

    def create_range_criteria(self,name,start,end):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]
        
        validateStart = self.validation(validation_type,validation_value,start)
        validateEnd =   self.validation(validation_type,validation_value,end)
        if validateStart == True and validateEnd == True:
            self.criterias.update({name:("<criteria><name>" + name + "</name><type>range</type><start>"
                                         + str(start) + "</start><end>"+ str(end) + "</end></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again:',start+' ',end

    def validation(self,val_type, validation_value, value):
        if val_type == 'exact':
            if len(str(value)) == validation_value:
                return True
        if val_type == 'max':
            if len(str(value)) <= validation_value:
                return True
        if val_type == 'date':
            check = value.split('-')
            if len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2:
                return True
        if val_type == 'list':
            for i in range(len(validation_value)):
                if value == validation_value[i]:
                    return True

        return False

    def add_response_column(self,name):
        '''
        object.create_response_column('name')

        Response Columns:
        agency, fiscal_year, revenue_category,
        revenue_source, adopted, recognized,
        budget_fiscal_year, funding_class, revenue_class,
        fund_class, modified, closing_classification_name
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')

        Delete a response column filter for a specific object
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')

        Delete a criteria filter for a specific object
        '''
        try:
            if name == 'max_records' or name == 'record_from':
                del self.global_criterias[name]
            else:
                del self.criterias[name]
        except KeyError:
            print 'Criteria doesn\'t exist'
        

    def getRevenue(self):
        '''
        Call to Revenue API: object.getRevenue()

        Get Revenue information

        Returns text in XML format
        '''
        revenueString = ('<request><type_of_data>Revenue</type_of_data>')
        #Adding global criteria filters
        for key in self.global_criterias.keys():
            revenueString += self.global_criterias[key]

        #Adding optional criteria filters
        revenueString += '<search_criteria>'
        if len(self.criterias) != 0:
            for key in self.criterias.keys():
                revenueString += self.criterias[key]

        #Adding response columns
        revenueString += "</search_criteria><response_columns>"
        if len(self.response_columns) != 0:
            for key in self.response_columns.keys():
                revenueString += self.response_columns[key]
        revenueString += "</response_columns></request>"
        
        #print revenueString
        self.revenueRequest = requests.post(self.url, data=revenueString,headers=self.headers)
        print 'Status Code:', self.revenueRequest.status_code
        #print 'Sample Info:', self.revenueRequest.text[0:500]
        return self.revenueRequest.text
            

class Spending:
    def __init__(self,ID,key):
        self.ID = ID
        self.key = key

        self.headers = {'app_id': self.ID,'app_key' : self.key }
        self.url = 'https://api.cityofnewyork.us/comptroller/v1/api'
        

        self.format_dict = {'fiscal_year' : 'exact' , 'calendar_year' : 'exact' ,
                            'payee_code' : 'max'    , 'document_id' : 'max',
                            'agency_code' : 'max'   , 'issue_date' : 'date',
                            'department_code' : 'max' , 'check_amount' : 'max',
                            'expense_category' : 'max' , 'contract_id' : 'max',
                            'capital_project_code' : 'max' , 'spending_category' : 'max',
                            'max_records':'max' , 'record_from':'max'
                           }

        self.predef_dict = {'fiscal_year' : 4 , 'calendar_year' : 4 ,
                           'payee_code' : 20    , 'document_id' : 20,
                           'agency_code' : 4   , 'issue_date' : 'YYYY-MM-DD',
                           'department_code' : 9 , 'check_amount' : 22,
                           'expense_category' : 4 , 'contract_id' : 32,
                           'capital_project_code' : 15 , 'spending_category' : 2,
                           'max_records': 4 , 'record_from':15}

        self.valGlobRange = {'max_records':'global' , 'record_from':'global',
                             'fiscal_year':'value' , 'calendar_year':'value',
                             'payee_code':'value' , 'document_id':'value',
                             'agency_code':'value' , 'issue_date':'range',
                             'department_code':'value' , 'check_amount':'range',
                             'expense_category':'value' , 'contract_id':'value',
                             'capital_project_code':'value' ,'spending_category':'value'
                            }

        self.criterias,self.global_criterias,self.response_columns = {},{},{}

    def getKey(self):
        print self.key
        return self.key
    
    def setKey(self,newKey):
        print 'New Key:',newKey
        self.key = newKey

    def getID(self):
        print self.ID
        return self.ID
    
    def setID(self,newID)
        print 'New ID:',newID
        self.ID = newID
        
    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        Values: object.add_criteria(crit_name,value))
        Ranges: object.add_criteria(crit_name,startDate,endDate)


        Values:
        max_records , record_from,
        fiscal_year OR calendar_year OR issue_date(Range),
        payee_code, document_id, agency_code,
        department_code, contract_id,
        capital_project_code, spending_category

        Ranges:
        check_amount,
        issue_date(choose this or fiscal_year/calendar_year)
        '''
        try:
            criteria_type = self.valGlobRange[name]
            if criteria_type == 'value':
                self.create_value_criteria(name,valGlobDate)
            elif criteria_type == 'range':
                self.create_range_criteria(name,valGlobDate,endDate)
            elif criteria_type == 'global':
                self.create_global_criteria(name,valGlobDate)
                
        except KeyError:
            print 'Invalid Criteria Name Entered'

    def create_global_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.global_criterias.update({name:'<'+name+'>'+str(value)+'</'+name+'>'})
            
    def create_value_criteria(self,name,value):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        if self.validation(validation_type,validation_value,value) == True:
            self.criterias.update({name:("<criteria><name>" + name +
                                        "</name><type>value</type><value>"
                                         + str(value) + "</value></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again'

    def create_range_criteria(self,name,start,end):
        validation_type = self.format_dict[name]
        validation_value = self.predef_dict[name]

        validateStart = self.validation(validation_type,validation_value,start)
        validateEnd =   self.validation(validation_type,validation_value,end)
        if validateStart == True and validateEnd == True:
            self.criterias.update({name:("<criteria><name>" + name + "</name><type>range</type><start>"
                                         + str(start) + "</start><end>"+ str(end) + "</end></criteria>")})
        else:
            print 'Invalid Criteria. Please check your information again:',start+' ',end

    def validation(self,val_type, validation_value, value):
        if val_type == 'exact':
            if len(str(value)) == validation_value:
                return True
        if val_type == 'max':
            if len(str(value)) <= validation_value:
                return True
        if val_type == 'date':
            check = value.split('-')
            if len(check[0]) == 4 and len(check[1]) == 2 and len(check[2]) == 2:
                return True
        if val_type == 'list':
            for i in range(len(validation_value)):
                if value == validation_value[i]:
                    return True

        return False

    def add_response_column(self,name):
        '''
        object.create_response_column('name')

        Response columns:
        agency, fiscal_year, spending_category,
        document_id, payee_name, check_amount,
        department, expense_category,
        calendar_year, contract_id, purpose,
        issue_date, capital_project
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')

        Delete an already created response column filter for a specific object
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')

        Delete an already created criteria filter for a specific object
        '''
        try:
            if name == 'max_records' or name == 'record_from':
                del self.global_criterias[name]
            else:
                del self.criterias[name]
        except KeyError:
            print 'Criteria doesn\'t exist'
        

    def getSpending(self):
        '''
        Call to Spending API: object.getSpending()

        Get Spending information

        Returns text in XML format
        
        '''
        spendingString = ('<request><type_of_data>Spending</type_of_data>')
        #Adding global criteria filters
        for key in self.global_criterias.keys():
            spendingString += self.global_criterias[key]

        #Adding optional criteria filters
        spendingString += '<search_criteria>'
        if len(self.criterias) != 0:
            for key in self.criterias.keys():
                spendingString += self.criterias[key]

        #Adding response columns
        spendingString += "</search_criteria><response_columns>"
        if len(self.response_columns) != 0:
            for key in self.response_columns.keys():
                spendingString += self.response_columns[key]
        spendingString += "</response_columns></request>"
        
        #print spendingString
        self.spendingRequest = requests.post(self.url, data=spendingString,headers=self.headers)
        print 'Status Code:', self.spendingRequest.status_code
        #print 'Sample Info:', self.spendingRequest.text[0:500]
        return self.spendingRequest.text
