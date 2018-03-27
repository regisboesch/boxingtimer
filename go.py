# First things, first. Import the wxPython package.
import wx
import MySettings
from enum import Enum

class TimerState(Enum):
	STOP = 1
	RUN = 2
	PAUSE = 3
	ALMOST_END = 4
	END_ROUND = 5

class MyFrameSetting(wx.Frame):

	def __init__(self, ground_frame):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Boxygene Settings", size=(500,800))
		self.Centre() 
		self.Show()
		self.panel = wx.Panel(self)
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.ground_frame = ground_frame

		#Grid Settings
		self.gs = gs = wx.GridSizer(rows=8, cols=2, hgap=5, vgap=5)
		
		#Color Pickers
		self.colour_picker_stop = wx.ColourPickerCtrl(self.panel)
		col_stop = wx.Colour();
		col_stop.Set(settings.config['DEFAULT']['color_stop'])
		self.colour_picker_stop.SetColour(col_stop)

		self.colour_picker_run = wx.ColourPickerCtrl(self.panel)
		col_run = wx.Colour();
		col_run.Set(settings.config['DEFAULT']['color_run'])
		self.colour_picker_run.SetColour(col_run)

		self.colour_picker_pause = wx.ColourPickerCtrl(self.panel)
		col_pause = wx.Colour();
		col_pause.Set(settings.config['DEFAULT']['color_pause'])
		self.colour_picker_pause.SetColour(col_pause)

		self.colour_picker_almostdone = wx.ColourPickerCtrl(self.panel)
		col_almost_done = wx.Colour();
		col_almost_done.Set(settings.config['DEFAULT']['color_almost_end'])
		self.colour_picker_almostdone.SetColour(col_almost_done)

		#Number of rounds
		self.number_of_rounds_SpinCtrl = wx.SpinCtrl(self.panel, min=1, max=50)
		self.number_of_rounds_SpinCtrl.SetValue(int(settings.config['DEFAULT']['number_of_rounds']))

		#Time round in seconds
		self.time_rounds_second_SpinCtrl = wx.SpinCtrl(self.panel, min=30, max=600)
		self.time_rounds_second_SpinCtrl.SetValue(int(settings.config['DEFAULT']['timer_in_seconds']))

		#Pause between rounds in seconds
		self.time_between_rounds_second_SpinCtrl = wx.SpinCtrl(self.panel, min=1, max=600)
		self.time_between_rounds_second_SpinCtrl.SetValue(int(settings.config['DEFAULT']['pause_each_round_in_seconds']))

		#Notification round almost done in seconds
		self.time_notification_alost_done_rounds_second_SpinCtrl = wx.SpinCtrl(self.panel, min=1, max=60)
		self.time_notification_alost_done_rounds_second_SpinCtrl.SetValue(int(settings.config['DEFAULT']['notification_before_end_of_ring_in_seconds']))

		#Logo
		self.logo = wx.FileCtrl(self.panel, size=(500,300))
		self.logo.SetPath(settings.config['DEFAULT']['logo'])

		# Adding properties to grid
		self.gs.AddMany( [
			(wx.StaticText(self.panel, -1, "Number of rounds"), wx.EXPAND),
			(self.number_of_rounds_SpinCtrl, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Time of the round in seconds"), wx.EXPAND),
			(self.time_rounds_second_SpinCtrl, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Time between rounds in seconds"), wx.EXPAND),
			(self.time_between_rounds_second_SpinCtrl, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Notification before end of the round in seconds"), wx.EXPAND),
			(self.time_notification_alost_done_rounds_second_SpinCtrl, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Stop Color"), wx.EXPAND),
			(self.colour_picker_stop, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Run Color"), wx.EXPAND),
			(self.colour_picker_run, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Pause Color"), wx.EXPAND),
			(self.colour_picker_pause, wx.EXPAND),
			(wx.StaticText(self.panel, -1, "Almost Done Color"), wx.EXPAND),
			(self.colour_picker_almostdone, wx.EXPAND),
			])

		self.sizer.Add(self.gs,0, wx.ALL|wx.EXPAND, 5)

		self.sizer.Add(wx.StaticText(self.panel, -1, "Logo"),0, wx.ALL|wx.EXPAND, 5)
		self.sizer.Add(self.logo, 0, wx.ALL|wx.EXPAND, 25)

		#Save Button
		self.saveBtn = wx.Button(self.panel, wx.ID_ANY, "Save")	
		self.Bind(wx.EVT_BUTTON, self.save_settings, self.saveBtn)
		self.sizer.Add(self.saveBtn,0, wx.ALL|wx.EXPAND, 5)

		#Main panel
		self.panel.SetSizer(self.sizer)

	def save_settings(self, evt):

		#Saving to preferences
		settings.config['DEFAULT']['color_stop'] = self.colour_picker_stop.GetColour().GetAsString()
		settings.config['DEFAULT']['color_run'] = self.colour_picker_run.GetColour().GetAsString()
		settings.config['DEFAULT']['color_pause'] = self.colour_picker_pause.GetColour().GetAsString()
		settings.config['DEFAULT']['color_almost_end'] = self.colour_picker_almostdone.GetColour().GetAsString()
		settings.config['DEFAULT']['number_of_rounds'] = str(self.number_of_rounds_SpinCtrl.GetValue())
		settings.config['DEFAULT']['timer_in_seconds'] = str(self.time_rounds_second_SpinCtrl.GetValue())
		settings.config['DEFAULT']['pause_each_round_in_seconds'] = str(self.time_between_rounds_second_SpinCtrl.GetValue())
		settings.config['DEFAULT']['notification_before_end_of_ring_in_seconds'] = str(self.time_notification_alost_done_rounds_second_SpinCtrl.GetValue())
		settings.config['DEFAULT']['logo'] = str(self.logo.GetPath())
		settings.saveToFile()

		#Reloading Display
		self.ground_frame.update_display_after_settings()

class MyFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, "Boxygene Timer")
		self.panel = wx.Panel(self)
		self.Maximize(True)

		#Buttons
		self.startBtn = wx.Button(self.panel, wx.ID_ANY, "Start")
		self.Bind(wx.EVT_BUTTON, self.OnPressStartStopButton, self.startBtn)
		self.pauseBtn = wx.Button(self.panel, wx.ID_ANY, "Pause")
		self.Bind(wx.EVT_BUTTON, self.OnPressPauseButton, self.pauseBtn)
		self.settingsBtn = wx.Button(self.panel, wx.ID_ANY, "Settings")
		self.Bind(wx.EVT_BUTTON, self.OnPressSettingsButton, self.settingsBtn)

		#Timer
		self.timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_update_timer, self.timer)

		#Clock
		self.lcdClock = wx.StaticText(self.panel, -1, "00:00", style=wx.ALIGN_CENTER)
		self.fontLcdClock = wx.Font(440, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
		self.lcdClock.SetFont(self.fontLcdClock)

		#Number of round
		self.numberRound = wx.StaticText(self.panel, -1, "00:00", style=wx.ALIGN_CENTER)
		self.fontNumberRound = wx.Font(140, wx.DECORATIVE,  wx.NORMAL, wx.NORMAL)
		self.numberRound.SetFont(self.fontNumberRound)

		#Logo
		self.logo =wx.StaticBitmap(self.panel)

		# Round text
		#Main Sizer
		self.sizer = wx.BoxSizer(wx.VERTICAL)
		self.sizer.Add(self.logo, 0, wx.ALL|wx.CENTER, 5)
		self.sizer.Add(self.lcdClock, 0, wx.ALL|wx.CENTER, 5)
		self.sizer.Add(self.numberRound, 0, wx.ALL|wx.CENTER, 5)

		#ButtonSizer
		self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.button_sizer.Add(self.startBtn, 0, wx.ALL|wx.CENTER, 5)
		self.button_sizer.Add(self.pauseBtn, 0, wx.ALL|wx.CENTER, 5)
		self.button_sizer.Add(self.settingsBtn, 0, wx.ALL|wx.CENTER, 5)
		self.sizer.Add(self.button_sizer, 0, wx.ALL|wx.CENTER, 5)

		self.panel.SetSizer(self.sizer)

		#Update Display settings
		self.update_display_after_settings()

		#Timer variable
		self.current_round_number = 1
		self.current_round_timer_in_seconds = 0
		self.timer_state = TimerState.STOP
		self.timer_start_time_this_round = 0

	def update_display_after_settings(self):

		#Logo image
		self.logo.SetBitmap(wx.Bitmap(settings.config['DEFAULT']['logo'], wx.BITMAP_TYPE_ANY))

		#Reset everything
		self.reset()

	def update_background_color(self, colour):
		self.panel.SetBackgroundColour(colour)

	def reset(self):

		#Background panel
		col_stop = wx.Colour();
		col_stop.Set(settings.config['DEFAULT']['color_stop'])
		self.update_background_color(col_stop)

		#Button
		self.startBtn.SetLabel("Start")
		self.pauseBtn.SetLabel("Pause")

		#Timer Value
		self.timer.Stop()
		self.timer_state = TimerState.STOP
		self.current_round_number = 1
		self.current_round_timer_in_seconds = int(settings.config['DEFAULT']['timer_in_seconds'])

		#Countdown label
		self.update_countdown_label(self.current_round_timer_in_seconds)

		#Number of round
		self.update_number_of_round(self.current_round_number, int(settings.config['DEFAULT']['number_of_rounds']))

	def update_number_of_round(self, current_round_number, total_round_number):
		roundformat = '{:02d}/{:02d}'.format(current_round_number, total_round_number)
		self.numberRound.SetLabel(roundformat)

	def update_countdown_label(self, seconds_left_in_second):
		mins, secs = divmod(seconds_left_in_second, 60)
		timeformat = '{:02d}:{:02d}'.format(mins, secs)
		self.lcdClock.SetLabel(timeformat)

	def OnPressSettingsButton(self, evt):
		settings_frame = MyFrameSetting(self)
		settings_frame.Show()

	def OnPressStartStopButton(self, evt):
		if self.timer_state == TimerState.STOP :
			#Start Timer
			self.timer.Start(1000)

			#Set start time
			self.current_round_timer_in_seconds = int(settings.config['DEFAULT']['timer_in_seconds'])

			#Changing color background
			col_stop = wx.Colour();
			col_stop.Set(settings.config['DEFAULT']['color_run'])
			self.update_background_color(col_stop)

			#Update Label
			self.startBtn.SetLabel("Stop")
			self.timer_state = TimerState.RUN

			#Disable other button ??
		else :
			#Stop Timer
			self.timer.Stop()

			self.timer_state = TimerState.STOP

			#Changing background

			#Update label
			self.startBtn.SetLabel("Start")

			#Reset
			self.reset()

	#Save old_status too when Pausing
	def OnPressPauseButton(self, evt):

		if self.timer_state == TimerState.PAUSE :
			self.timer_state = self.timer_state_old
			self.pauseBtn.SetLabel("Pause")
		else :
			self.timer_state_old = self.timer_state
			self.timer_state = TimerState.PAUSE
			self.pauseBtn.SetLabel("Resume")

	def on_update_timer(self, event) :
		
		#WHen on RUN round
		if (self.timer_state==TimerState.RUN) or (self.timer_state==TimerState.ALMOST_END) :
			self.current_round_timer_in_seconds = self.current_round_timer_in_seconds-1

			#Checking before almost end of round
			if (self.current_round_timer_in_seconds <= int(settings.config['DEFAULT']['notification_before_end_of_ring_in_seconds'])) and (self.timer_state==TimerState.RUN):
				self.timer_state=TimerState.ALMOST_END
				col = wx.Colour();
				col.Set(settings.config['DEFAULT']['color_almost_end'])
				self.update_background_color(col)

			if self.current_round_timer_in_seconds <= 0 and self.timer_state == TimerState.ALMOST_END:
				self.timer_state=TimerState.END_ROUND
				col = wx.Colour();
				col.Set(settings.config['DEFAULT']['color_pause'])
				self.update_background_color(col)
				self.current_round_timer_in_seconds = int(settings.config['DEFAULT']['pause_each_round_in_seconds'])

		#When on Pause round
		if self.timer_state==TimerState.END_ROUND :
			self.current_round_timer_in_seconds = self.current_round_timer_in_seconds-1

			if self.current_round_timer_in_seconds <= 0 :
				self.current_round_number = self.current_round_number +1

				if self.current_round_number > int(settings.config['DEFAULT']['number_of_rounds']) :
					self.reset()
				else :
					self.current_round_timer_in_seconds = int(settings.config['DEFAULT']['timer_in_seconds'])
					self.timer_state=TimerState.RUN
					col = wx.Colour();
					col.Set(settings.config['DEFAULT']['color_run'])
					self.update_background_color(col)

		print "Updating timer state %s : time elapsed %d [s] form round %d" % (self.timer_state.name, self.current_round_timer_in_seconds, self.current_round_number)

		#Updating timer labels
		self.update_number_of_round(self.current_round_number, int(settings.config['DEFAULT']['number_of_rounds']))
		self.update_countdown_label(self.current_round_timer_in_seconds)

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