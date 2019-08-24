import wx


class ventanaPixeles(wx.Frame):

    def __init__(self, parent, title):
        super(ventanaPixeles, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()

    def InitUI(self):

        self.panel = wx.Panel(self)
        self.PhotoMaxSize = 240
        self.sizer = wx.GridBagSizer(6, 6)

        # AGREGA BOTON PARA ABRIR LA IMAGEN (SU EVENTO ESTÁ MAS ABAJO)
        self.photoTxt = wx.TextCtrl(self.panel, size=(200, -1))
        imageButton = wx.Button(self.panel, label='Abrir imagen',
        size=(140, 80))
        imageButton.Bind(wx.EVT_BUTTON, self.onBrowse)
        self.sizer.Add(imageButton, pos=(0, 0), span=(0, 2),
        flag=wx.TOP | wx.LEFT | wx.RIGHT, border=25)

        # TEXTO Y EL CUADRADO (panel) QUE CAMBIA DE COLOR
        st1 = wx.StaticText(self.panel, label='Color: ')
        self.sizer.Add(st1, pos=(1, 0), flag=wx.TOP | wx.LEFT, border=25)
        self.colorPanel = wx.Panel(self.panel, size=(60, 60),
        style=wx.BORDER_SUNKEN)
        self.sizer.Add(self.colorPanel, pos=(1, 1),
          flag=wx.TOP | wx.LEFT, border=10)

        # TEXTOS QUE INDICAN VALOR RGB
        self.st2 = wx.StaticText(self.panel, label='Valores Color')
        self.sizer.Add(self.st2, pos=(2, 0), flag=wx.LEFT, border=25)
        self.st3 = wx.StaticText(self.panel, label='.')
        self.sizer.Add(self.st3, pos=(3, 0),
        flag=wx.LEFT | wx.BOTTOM, border=25)

        # LUGAR DONDE DEBERIA IR LA IMAGEN
        img = wx.Image(240, 240)
        self.imgCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
             wx.Bitmap(img), size=(240, 240))
        self.imgCtrl.Bind(wx.EVT_MOTION, self.mouseOnPicture)
        self.sizer.Add(self.imgCtrl, pos=(0, 2), span=(4, 2),
        flag=wx.TOP | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=25)

        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)

    def onBrowse(self, event):
        """
        Browse for file
        """
        wildcard = "JPEG files (*.jpg)|*.jpg"
        dialog = wx.FileDialog(None, "Choose a file", wildcard=wildcard,
                                style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.photoTxt.SetValue(dialog.GetPath())
        dialog.Destroy()
        self.onView()

    def onView(self):
        filepath = self.photoTxt.GetValue()
        self.img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)

        # ESCALA LA IMAGEN MANTENIENDO SUS PROPORCIONES
        W = self.img.GetWidth()
        H = self.img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        self.img = self.img.Scale(NewW, NewH)

        self.imgCtrl.SetBitmap(wx.Bitmap(self.img))
        self.panel.Refresh()

    def mouseOnPicture(self, event):
        x, y = event.GetPosition()

        # pone los valores RGB en texto
        self.st3.SetLabel("R: " + str(self.img.GetRed(x, y)) + ", G: " +
        str(self.img.GetGreen(x, y)) + ", B: " + str(self.img.GetBlue(x, y)))

        # pinta un cuadrado (panel) con el valor rgb
        self.colorPanel.SetBackgroundColour(wx.Colour(self.img.GetRed(x, y),
        self.img.GetGreen(x, y), self.img.GetBlue(x, y)))
        self.colorPanel.Refresh()


def main():
    app = wx.App()
    vp = ventanaPixeles(None, title='Pixeles')
    vp.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

