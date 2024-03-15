import pandas as pd
class eso:
    def __init__(self, prices, availability, consumption, subscribers, date):#prices is an excel file
        self.prices=prices                                                   #date in format 'Sun, 03/10'
        self.availability=availability
        self.consumption=consumption
        self.subscribers=subscribers
        

    def send_prices(prices, date):
        

        df = pd.read_excel(prices, sheet_name='Sheet3')
        #df=pd.DataFrame(df)
        #print(df)
        #
        column_list = df[date].tolist()

        
        #df = pd.read_csv('file_name_here.csv')
        print(df)
    def send_grid_status(consumption):
        pass

    def cut_subscriber(subscribers):
        pass

    def retrieve_consumption():
        pass
    

if __name__ == '__main__':
    a=[]
    eso1=eso
    eso1.send_prices("\\upravtok\\Data\\last_week_prices.xlsx", 'Sun, 03/10')