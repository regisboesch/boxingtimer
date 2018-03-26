# First things, first. Import the wxPython package.
import wx
import MySettings

class MyFrameSetting(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Boxygene Settings", size=(500,500))
		self.Centre() 
		self.Show()
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.VERTICAL)

		#Grid Settings
		self.gs = gs = wx.GridSizer(rows=2, cols=2, hgap=5, vgap=5)
		
		#Color Pickers
		self.colour_picker_stop = wx.ColourPickerCtrl(self.panel)
		col_stop = wx.Colour();
		col_stop.Set(settings.config['DEFAULT']['color_stop'])
		self.colour_picker_stop.SetColour(col_stop)

		self.colour_picker_run = wx.ColourPickerCtrl(self.panel)
		col_run = wx.Colour();
		col_run.Set(settings.config['DEFAULT']['color_run'])
		self.colour_picker_run.SetColour(col_run)

		# Adding properties
		self.gs.AddMany( [
			(wx.StaticText(self.panel, -1, "Stop Color"), wx.EXPAND),
			(self.colour_picker_stop, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Run Color"), wx.EXPAND),
			(self.colour_picker_run, wx.EXPAND),
			])

		self.sizer.Add(self.gs,0, wx.ALL|wx.EXPAND, 5)

		#Buttons
		self.saveBtn = wx.Button(self.panel, wx.ID_ANY, "Save")	
		self.Bind(wx.EVT_BUTTON, self.save_settings, self.saveBtn)
		self.sizer.Add(self.saveBtn,0, wx.ALL|wx.EXPAND, 5)

		#Main panel
		self.panel.SetSizer(self.sizer)

	def save_settings(self, evt):
		print self.colour_picker_stop.GetColour().GetAsString()

class MyFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Boxygene Timer")
		self.panel = wx.Panel(self)
		self.Maximize(True)

		#Buttons
		self.startBtn = wx.Button(self.panel, wx.ID_ANY, "Start")
		self.pauseBtn = wx.Button(self.panel, wx.ID_ANY, "Pause")
		self.settingsBtn = wx.Button(self.panel, wx.ID_ANY, "Settings")
		self.Bind(wx.EVT_BUTTON, self.OnPressSettingsButton, self.settingsBtn)

		#Timer

		#Clock
		self.lcdClock = wx.StaticText(self.panel, -1, "00:00", style=wx.ALIGN_CENTER)
		self.fontLcdClock = wx.Font(140, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
		self.lcdClock.SetFont(self.fontLcdClock)

		# Round text
		#Main Sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.lcdClock, 0, wx.ALL|wx.CENTER, 5)

		#ButtonSizer
		self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.button_sizer.Add(self.startBtn, 0, wx.ALL|wx.CENTER, 5)
		self.button_sizer.Add(self.pauseBtn, 0, wx.ALL|wx.CENTER, 5)
		self.button_sizer.Add(self.settingsBtn, 0, wx.ALL|wx.CENTER, 5)
		self.sizer.Add(self.button_sizer, 0, wx.ALL|wx.CENTER, 5)

		self.panel.SetSizer(self.sizer)

	def OnPressSettingsButton(self, evt):
		settings_frame = MyFrameSetting()
		settings_frame.Show()

if __name__ == "__main__":

	# Load Settings
	settings = MySettings.MySettings()
	settings.loadFromFile()

	# Next, create an application object.
	app = wx.App()

	# Show it.
	frame = MyFrame().Show()

	# Start the event loop.
	app.MainLoop()