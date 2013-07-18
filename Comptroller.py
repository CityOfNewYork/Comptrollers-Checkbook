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
        

    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        object.add_criteria(criteria_name,value/startDate,endDate(OPTIONAL))
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
            print 'Invalid Criteria. Please check your information again:',name

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
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')
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

    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        object.add_criteria(criteria_name,value/startDate,endDate(OPTIONAL))
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
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')
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
                               
                                    
    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        object.add_criteria(criteria_name,value/startDate,endDate(OPTIONAL))
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
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')
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

    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        object.add_criteria(criteria_name,value/startDate,endDate(OPTIONAL))
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
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')
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

    def add_criteria(self,name,valGlobDate,endDate=''):
        '''
        object.add_criteria(criteria_name,value/startDate,endDate(OPTIONAL))
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
        '''
        self.response_columns.update({name:name})

    def del_reponse_column(self,name):
        '''
        object.del_response_column('name')
        '''
        try:
            del self.response_columns[name]
        except KeyError:
            print 'Response Column doesn\'t exist'
            

    def delete_criteria(self,name):
        '''
        object.del_criteria('name')
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
