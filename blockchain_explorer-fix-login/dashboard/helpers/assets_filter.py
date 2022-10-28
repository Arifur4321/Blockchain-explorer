from datetime import datetime

class AssetsFilter:
    def __init__(self, list_assets) -> None:
        self.list_assets = list_assets

    ''' Return asset details with corresponding username '''

    def get_details_from_username(self,username):
        #detail = {'value': 0, 'userName': 'Damiano--19/09/2022 10:24:20', 'idFascicolo': 'kjgsdfkjsafd', 'statoOld': '27', 'statoNew': '98', 'tipo_oprazione': 'Cambio Stato Fascicolo', 'descrizione': 'testin putpose'}
        
        aux = []
        for asset in self.list_assets:
            name_data = asset['details']['userName'].split('--')
            name = name_data[0]
            if username.lower() in name.lower() or username == '':
                aux.append(asset['details'])
        return aux
        
        #return [asset['details'] for asset in self.list_assets if asset['details']['userName'].split('--')[0] == username ]

    ''' Return asset details with compatible start date '''

    def get_details_from_start_date(self, date):
        aux = []
        for asset in self.list_assets:
            name_data = asset['details']['userName'].split('--')
            my_date_raw = name_data[1]
            try:
                my_date_formatted = datetime.strptime(my_date_raw, '%d/%m/%Y %H:%M:%S')

                if my_date_formatted >= date or date == '':

                    aux.append(asset['details'])
            except:
                pass

        return aux

    ''' Return asset details with compatible end date '''
    
    def get_details_from_end_date(self, date):
        aux = []
        for asset in self.list_assets:
            name_data = asset['details']['userName'].split('--')
            my_date_raw = name_data[1]
            try:
                my_date_formatted = datetime.strptime(my_date_raw, '%d/%m/%Y %H:%M:%S')

                if my_date_formatted <= date or date == '':

                    aux.append(asset['details'])
            except:
                pass
        
        return aux

    ''' Return asset details with corresponding operation type '''

    def get_details_from_operation_type(self, operation_type):
        #detail = {'value': 0, 'userName': 'Damiano--19/09/2022 10:24:20', 'idFascicolo': 'kjgsdfkjsafd', 'statoOld': '27', 'statoNew': '98', 'tipo_oprazione': 'Cambio Stato Fascicolo', 'descrizione': 'testin putpose'}
        
        aux = []
        for asset in self.list_assets:
            operation_data = asset['details']['tipo_oprazione']
            if operation_data == operation_type or operation_type == '':
                aux.append(asset['details'])
        return aux

    ''' Combines the results of start date and end date filters '''

    def get_detail_from_filters_with_dates(self, start_date, end_date):
        aux = []

        for asset in self.list_assets:
            if asset['details'] in self.get_details_from_start_date(start_date) and asset['details'] in self.get_details_from_end_date(end_date):
                
                aux.append(asset['details'])

        return aux

    ''' Combines the results of username, start date and end date filters '''

    def get_detail_from_filters_with_username(self, username, start_date, end_date):
        aux = []

        for asset in self.list_assets:
            if asset['details'] in self.get_details_from_username(username) and asset['details'] in self.get_details_from_start_date(start_date) and asset['details'] in self.get_details_from_end_date(end_date):
                
                aux.append(asset['details'])

        return aux
        
    ''' Combines the results of username, operation type, start date and end date filters '''
    def get_detail_from_filters_with_username_and_operation_type(self, username, operation_type, start_date, end_date):
        aux = []

        for asset in self.list_assets:
            if asset['details'] in self.get_details_from_username(username) and asset['details'] in self.get_details_from_operation_type(operation_type) and asset['details'] in self.get_details_from_start_date(start_date) and asset['details'] in self.get_details_from_end_date(end_date):
                
                aux.append(asset['details'])

        return aux