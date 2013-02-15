import wx

class rammi(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,'Bangsimon',size=(300,200))
        panel = wx.Panel(self)

        button=wx.Button(panel,label="exit",pos=(150,120),size=(50,30))
        self.Bind(wx.EVT_BUTTON, self.closebutton, button)
        button2=wx.Button(panel,label="Open",pos=(100,120),size=(50,30))

        wx.StaticText(panel, -1, "Enter ticker of company/indice you wish to examin:",(20,20))

        
        basicText = wx.TextCtrl(panel, -1, "", size=(175, -1),pos=(65,70))
        
    def closebutton(self,event):
        self.Close(True)
   


if __name__=='__main__':
    app=wx.PySimpleApp()
    frame=rammi(parent=None,id=-1)             
    frame.Show()
    app.MainLoop()
