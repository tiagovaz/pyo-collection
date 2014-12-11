import wx

class MyFrame(wx.Frame):

    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, -1, title=title, size=size)
        self.main_panel = wx.Panel(self)







app = wx.App(False)
frame = MyFrame(None, title="wxpython + pyglet", size=(800, 600))
frame.Show()
app.MainLoop()


