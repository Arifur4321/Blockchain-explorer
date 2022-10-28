from datetime import datetime

class BlocksFilter:
    def __init__(self, list_blocks) -> None:
        self.list_blocks = list_blocks

    ''' Return block details with corresponding block height '''

    def get_block_from_height(self, height):        
        aux = []

        for block in self.list_blocks:
            block_height = block[0]['height']
            if int(height) == int(block_height) or height == '':
                aux.append(block[0])

        return aux
        
    ''' Return block details with compatible start date '''

    def get_block_from_start_date(self, date):
        aux = []

        for block in self.list_blocks:

            my_date = datetime.fromtimestamp(block[0]['time'])

            if my_date >= date or date == '':

                aux.append(block[0])

        return aux

    ''' Return block details with compatible end date '''

    def get_block_from_end_date(self, date):
        aux = []

        for block in self.list_blocks:

            my_date = datetime.fromtimestamp(block[0]['time'])

            if my_date <= date or date == '':

                aux.append(block[0])
        
        return aux

    ''' Combines the results of start date and end date filters '''

    def get_block_from_filters_with_dates(self, start_date, end_date):
        aux = []

        for block in self.list_blocks:
            if block[0] in self.get_block_from_start_date(start_date) and block[0] in self.get_block_from_end_date(end_date):
                
                aux.append(block[0])

        return aux

    ''' Combines the results of height, start date and end date filters '''

    def get_block_from_filters_with_height(self, height, start_date, end_date):
        aux = []

        for block in self.list_blocks:
            if block[0] in self.get_block_from_height(height) and block[0] in self.get_block_from_start_date(start_date) and block[0] in self.get_block_from_end_date(end_date):
                
                aux.append(block[0])

        return aux