class AnalystPanel(wx.Panel):

    stockObj = None
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1,style=wx.NO_FULL_REPAINT_ON_RESIZE)
        
        # First button
        b = wx.Button(self, -1, "Get data", pos=(20, 20))
        self.Bind(wx.EVT_BUTTON, self.OnClickGetData, b)
        
        b.SetDefault()
        b.SetSize(b.GetBestSize())
        b.SetToolTipString("Retrieves stock data.")
        
        # Second button
        b = wx.Button(self, -1, "Plot", pos=(20, 80))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, b)
        b.SetToolTipString("Plots stock data.")

        self.static_text1 = wx.StaticText(self, -1,"Data is from date: ",pos=(20, 120))
        self.static_text2 = wx.StaticText(self, -1,"Data is to date: ",pos=(20, 140))
        self.static_text3 = wx.StaticText(self, -1,"Company Ticker",pos=(120,20))

        # Text control
        self.text_ctrl1 = wx.TextCtrl(self, -1, DEFAULT_TICKER, pos=(250,20), size=(125,-1))

        self.text_ctrl1.SetToolTipString("Ticker of company")
        
    def OnClickGetData(self, event):
        # Stock info is kept as stockInfo object
        try:
            self.stockObj = stockInfo(self.text_ctrl1.GetValue())
            self.static_text1.SetLabel("Data is from date: " + str(self.stockObj.fromDate))
            self.static_text2.SetLabel("Data is to date: " + str(self.stockObj.toDate))
        except:
            self.stockObj = stockInfo(DEFAULT_TICKER)
            # Reset text control
            self.text_ctrl1.SetValue(DEFAULT_TICKER)
            self.static_text1.SetLabel("Data is from date: ")
            self.static_text2.SetLabel("Data is to date: ")

        # Create artificial stock data

    def OnClickPlot(self, event):
        if self.stockObj is not None:
            plotFrame = wx.Frame(None, title="Plot",size=(200,200))
            plotp = PlotPanel(plotFrame,self.stockObj)
        
            plotFrame.Show()

        

class PlotPanel(wx.Panel):
    stockObj = None
    ATTR= "Adj Close"
    fromDate = None
    toDate = None
    
    def __init__(self, parent, stockObj):
        wx.Panel.__init__(self, parent, -1,style=wx.NO_FULL_REPAINT_ON_RESIZE)
        self.stockObj = stockObj

        
        # select Attribute
        attr = ['Adj Close', 'Open', 'High', 'Low', 'Close', 'Volume', 'Avg. Price']
        self.combo= wx.ComboBox(self,choices=attr, value="Adj Close",pos=(120,20))
        self.Bind(wx.EVT_COMBOBOX, self.OnCombo, self.combo)

        """#Virkar ekki 
        self.fromDatePicker = wx.DatePickerCtrl(self,dt = self.dateToWxDateTime(stockObj.fromDate),pos = ( 20,120))
        self.toDatePicker = wx.DatePickerCtrl(self,dt = self.dateToWxDateTime(stockObj.toDate), pos = (20, 140))
        
        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, self.fromDatePicker)
        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, self.toDatePicker)
        """ 
        # Plot button
        b = wx.Button(self, -1, "Plot", pos=(20, 20))

        self.Bind(wx.EVT_BUTTON, self.OnClickPlot, b)
        b.SetToolTipString("Plots stock data.")
        

    def OnCombo(self, event):
        self.ATTR = self.combo.GetValue()

    def OnClickPlot(self, event):
        stockPlot(self.stockObj,self.ATTR, self.fromDate, self.toDate)


    def dateToWxDateTime(self,date):
        pass
        
    def WxDateTimeToDate(self,datetime):
        pass
