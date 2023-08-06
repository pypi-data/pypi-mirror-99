import neopixel, machine, network, urequests, gc, math
from time import sleep_ms

def Dashboard(length = 10):
    # Define length and initiate NeoPixel object
    np = neopixel.NeoPixel(machine.Pin(4), length)

    # Startup animation
    for i in range(length):
        np[i] = (64, 64, 64)
        np.write()
        sleep_ms(10)
    sleep_ms(800)
    for i in range(length):
        np[i] = (0,0,0)
    np.write()

    return np

def colorFill(neoObj,startPosition,length,rgb):
    for i in range(startPosition,startPosition+length):
        neoObj[i] = rgb
    neoObj.write()

def clear(neoObj,startPosition,length):
    for i in range(startPosition,startPosition+length):
        neoObj[i] = (0,0,0)  
    neoObj.write()

def translate(val, in_min, in_max, out_min, out_max):
    return (val-in_min) * (out_max-out_min) / (in_max-in_min) + out_min

### There is a new class for every possible function that a set of LED's can have. This allows for an easy
### way to add more items to the dashboard whenever necessary/wanted. 

class wifi:

    def __init__(self,neoObj,ssid,password,startPosition = 0):
        # Define object vars
        self.startPosition = startPosition
        self.np = neoObj
        self.length = 1

        # Connect to the wifi
        self.station = network.WLAN(network.STA_IF)
        self.station.active(True)
        self.station.connect(ssid,password)
        print("\nConnecting...")
        self.np[self.startPosition] = (16,8,0)
        self.np.write()

        i = 0
        while self.station.isconnected() == False & i < 50:
            sleep_ms(100)
            i = i +1

        if self.station.isconnected() == True:
            print("Connected!")
            self.np[self.startPosition] = (0,16,0)
        else:
            print("Connection failed")
            self.np[self.startPosition] = (16,0,0)


    def update(self):
        if self.station.isconnected() == True:
            self.np[self.startPosition] = (0,16,0)
        else:
            self.np[self.startPosition] = (16,0,0)

class temperature:

    def __init__(self,neoObj,startPosition,city,apiid):
        # Define object vars
        self.startPosition = startPosition
        self.np = neoObj
        self.length = 5
        self.city = city
        self.apiid = apiid

    def update(self):

        # OpenWeather API info
        self.call = "http://api.openweathermap.org/data/2.5/weather?q="+self.city+"&appid="+self.apiid
        r = urequests.get(self.call).json()
        self.temp_F = (r['main']['temp']-273.15)*(9/5)+32
        del r
        
        # update pixels
        if self.temp_F > 32:
            colorFill(self.np,self.startPosition,self.length,(10,5,0))
            brightNum = int((self.temp_F-32)/10)
            colorFill(self.np,self.startPosition,brightNum,(128,64,0))

        else:
            colorFill(self.np,self.startPosition,self.length,(0,5,10))
            brightNum = int((32-self.temp_F)/10)
            colorFill(self.np,self.startPosition,brightNum,(0,64,128))

class humidity:

    def __init__(self,neoObj,startPosition,city,apiid):
        self.startPosition = startPosition
        self.np = neoObj
        self.length = 5
        self.city = city
        self.apiid = apiid



    def update(self):
        # OpenWeather API info
        self.call = "http://api.openweathermap.org/data/2.5/forecast?q="+self.city+"&cnt=1&appid="+self.apiid
        r = urequests.get(self.call).json()
        self.hum = r['list'][0]['main']['humidity']
        self.prec = r['list'][0]['pop']
        del r

        # fill the leds according to the given data
        colorFill(self.np,self.startPosition,self.length,(0,10,4))
        brightNum = int(self.hum/20)
        brightness = translate(self.prec,0.,1.,.2,1.)
        colorFill(self.np,self.startPosition,brightNum,(0,int(brightness*255),int(brightness*110)))

class stock:

    def __init__(self,neoObj,startPosition,symbol,apiid):
        self.np = neoObj
        self.startPosition = startPosition
        self.length = 5
        self.symbol = symbol
        self.apiid = apiid

    def update(self):
        self.call = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+self.symbol+'&apikey='+self.apiid
        gc.collect()
        r = urequests.get(self.call).json()
        dayOpen = float(r['Global Quote']['02. open'])
        current = float(r['Global Quote']['05. price'])
        dayPercent = ((current-dayOpen)/dayOpen)*100.
        del(r)

        # LED's are filled based on a logarithmic scale:
        # 0.1%-1.0% = 1 bright LED, 1.0%-10% = 2 bright LED's...
        try:
            brightNum = int(math.log(math.fabs(dayPercent),10)+2)
        except:
            brightNum = 0

        if dayPercent > 0:
            baseColor = (0,12,0)
        elif dayPercent < 0:
            baseColor = (12,0,0)
        else:
            baseColor = (8,8,8)

        colorFill(self.np,self.startPosition,self.length,baseColor)
        colorFill(self.np,self.startPosition,brightNum,tuple(i*10 for i in baseColor))

