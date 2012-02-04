import wx

class PanelCtrl:
    """ A group of objects for a control panel pane

        This is just a wrapper object the objects inside of a control panel.
        Therefore its parent object should be a wx.Panel.

        It has a label for the control (static text), a slider, and an editable
        text box (text control).  Each of the three controls are in a
        horizontal sizer.

        Members:

        label       - The label of the control (value of text)
        val         - The value of the control
        val_min     - The minimum value allowed for control
        val_max     - The maximum value allowed for control
        val_chg     - The change in value between ticks of slider
        val_def     - The default value of the control
        ntks        - The number of ticks in the slider
        edit        - The text control box
        text        - The label text for the control
        sldr        - The slider object for the control
        sizer       - The sizer object that holds the other members
    """

    def __init__(self, parent, label, val_min, val_max, chg,val_def):

        # Set initial values
        self.val = float(val_def)
        self.label = label
        self.val_min = float(val_min)
        self.val_max = float(val_max)
        self.chg = float(chg)
        self.val_def = float(val_def)

        # An blank object for spacing
        space = wx.StaticText(parent, -1, "")

        # Create the controls
        ntks = int((self.val_max - self.val_min)/self.chg)
        deftks = int((self.val_def - self.val_min)/self.chg)
        self.edit = wx.TextCtrl(parent, -1, str(self.val_def),
                                style=wx.TE_CENTER)
        self.text = wx.StaticText(parent, -1, label)
        self.sldr = wx.Slider(parent, -1, deftks, 0, ntks,
                              style=wx.SL_AUTOTICKS)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.text, 3, wx.ALIGN_CENTER)
        self.sizer.Add(space, 1, wx.ALIGN_CENTER)
        self.sizer.Add(self.sldr, 3, wx.ALIGN_CENTER)
        self.sizer.Add(space, 1, wx.ALIGN_CENTER)
        self.sizer.Add(self.edit, 3, wx.ALIGN_CENTER)

        # Make is so when the slider changes, the edit text changes
        parent.Bind(wx.EVT_SLIDER, self.__UpdateText__, self.sldr)

        # Change the value of the slider to the value of the edit when the edit
        # is changed
        parent.Bind(wx.EVT_TEXT, self.__UpdateSlider__, self.edit)


    def __UpdateText__(self, evt):
        """ Updates the displayed text in the textfield

            When the slider is adjusted, this event is called and the value
            displayed in the text box is updated.
        """
        self.val = self.sldr.GetValue()*self.chg + self.val_min
        self.edit.SetValue(str(self.val))

    def __UpdateSlider__(self, evt):
        """ Validates and updates the slider position based upon changes in the
            text box.

            If the value inside the textbox is not valid, then the background is
            set to pink.
        """
    
        # Check to see if the value is okay
        try:
            val = self.edit.GetValue()
            val = float(val)
            if (val >= self.val_min) & (val <= self.val_max):
                self.val = val
                self.sldr.SetValue((self.val - self.val_min)/self.chg)
                self.edit.SetBackgroundColour(
                    wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
                self.edit.Refresh()
            else:
                print val
                raise
        except:
            self.edit.SetBackgroundColour("pink")
            self.edit.SetFocus()
            self.edit.Refresh()

    
    def GetValue(self):
        return self.val
