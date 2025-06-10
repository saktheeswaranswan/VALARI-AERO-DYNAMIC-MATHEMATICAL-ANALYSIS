# Example plugin for Graph for creating slope fields.
# The plugin will create an action and add it to the main menu. When executed, the action will show a dialog where you can enter dy/dx in terms of x and y, and parameters of the slopefield plot
# When the dialog is closed it will create the Slopefield as a parametric function and add it to the function list.
# In addition the plugin hooks into Edit command and shows the same dialog when a Slopefield previously created by the plugin is edited.
# Credit given to Ivan Johansen, benice (C. J. Chen) benice-equation.blogspot.com, Erin Soderberg, and Marco Rainaldi
import Graph
import vcl
import Gui
class SlopefieldDialog(Gui.SimpleDialog):
    def __init__(self, SlopefieldItem=None):
        Gui.SimpleDialog.__init__(self)
        self.SlopefieldItem = SlopefieldItem
        self.Caption = "Insert slope field"
        self.Height = 320
        self.Width = 340
        SlopefieldData = SlopefieldItem.PluginData["SlopefieldExample"] if SlopefieldItem else ("","","","","","","")

        self.label1 = vcl.TLabel(None, Parent = self.Panel, Caption = "dy/dx:", Top = 12, Left = 8)
        self.label2 = vcl.TLabel(None, Parent = self.Panel, Caption = "Slope Field Window Settings:", Top = 35, Left = 8)
        self.label3 = vcl.TLabel(None, Parent = self.Panel, Caption = "x-min:", Top = 55, Left = 8)
        self.label4 = vcl.TLabel(None, Parent = self.Panel, Caption = "x-max:", Top = 55, Left = 100)
        self.label5 = vcl.TLabel(None, Parent = self.Panel, Caption = "y-min:", Top = 85, Left = 8)
        self.label6 = vcl.TLabel(None, Parent = self.Panel, Caption = "y-max:", Top = 85, Left = 100)    
        self.label7 = vcl.TLabel(None, Parent = self.Panel, Caption = "# of equal subdivisions X:", Top = 120, Left = 8)
        self.label8 = vcl.TLabel(None, Parent = self.Panel, Caption = "# of equal subdivisions Y:", Top = 150, Left = 8)
        self.label9 = vcl.TLabel(None, Parent = self.Panel, Caption = "Segment Width:", Top = 180, Left = 8)
        self.label10 = vcl.TLabel(None, Parent = self.Panel, Caption = "Color:", Top = 210, Left = 8)
        self.edit1 = vcl.TEdit(None, Parent = self.Panel, Top = 8, Left = 50, Width = 250, Text = SlopefieldData[0])
        self.edit2 = vcl.TEdit(None, Parent = self.Panel, Top = 51, Left = 50, Width = 40, Text = SlopefieldData[1])
        self.edit3 = vcl.TEdit(None, Parent = self.Panel, Top = 51, Left = 150, Width = 40, Text = SlopefieldData[2])
        self.edit4 = vcl.TEdit(None, Parent = self.Panel, Top = 81, Left = 50, Width = 40, Text = SlopefieldData[3])
        self.edit5 = vcl.TEdit(None, Parent = self.Panel, Top = 81, Left = 150, Width = 40, Text = SlopefieldData[4])
        self.edit6 = vcl.TEdit(None, Parent = self.Panel, Top = 116, Left = 150, Width = 40, Text = SlopefieldData[5])
        self.edit7 = vcl.TEdit(None, Parent = self.Panel, Top = 146, Left = 150, Width = 40, Text = SlopefieldData[6])
        self.edit8 = vcl.TEdit(None, Parent = self.Panel, Top = 176, Left = 150, Width = 40, Text = str(SlopefieldItem.Size) if SlopefieldItem else "2")
        self.colorbox = vcl.TExtColorBox(None, Parent = self.Panel, Top = 206, Left = 90, Width = 100, Selected = SlopefieldItem.Color if SlopefieldItem else 0x000000)

    def OnOk(self, sender):
        SlopefieldData = (self.edit1.Text, self.edit2.Text, self.edit3.Text, self.edit4.Text, self.edit5.Text, self.edit6.Text, self.edit7.Text)
        Graph.Constants ["f"] = (SlopefieldData[0], "x", "y")
        Graph.Constants ["a"] = (SlopefieldData[1])
        Graph.Constants ["b"] = (SlopefieldData[2])
        Graph.Constants ["c"] = (SlopefieldData[3])
        Graph.Constants ["d"] = (SlopefieldData[4])
        Graph.Constants ["m"] = (SlopefieldData[5])
        Graph.Constants ["n"] = (SlopefieldData[6])
        Graph.Constants ["h"] = ("(d-c)/n")
        Graph.Constants ["s"] = ("(b-a)/m")
        Graph.Constants ["k"] = ("0.4*min(s,h)")
        Graph.Constants ["step"] = ("10000*(m+1)*(n+1)")
        Graph.Constants ["g1"] = ("x + k*(2t - 1)/sqrt(1 + f(x,y)^2)", "x", "y", "t")
        Graph.Constants ["g2"] = ("y + k*(2t - 1)*f(x,y)/sqrt(1 + f(x,y)^2)", "x", "y", "t")
        Func = Graph.TParFunc("g1(a + s*floor(mod(t,m+1)), c + h*floor(t/(m+1)), mod(t,1))", "g2(a + s*floor(mod(t,m+1)), c + h*floor(t/(m+1)), mod(t,1))")
        Func.PluginData["SlopefieldExample"] = SlopefieldData
        Func.LegendText = "Slopefield: dy/dx={0}".format(*SlopefieldData)
        Func.Color = self.colorbox.Selected
        Func.Size = int(self.edit8.Text)
        Func.From = 0
        Func.To = ((float(SlopefieldData[5])+1)*(float(SlopefieldData[6])+1))
        Func.DrawType = Graph.dtDots
        Func.Steps = (100*((float(SlopefieldData[5])+1)*(float(SlopefieldData[6])+1)))

        if self.SlopefieldItem:
            Graph.FunctionList[Graph.FunctionList.index(self.SlopefieldItem)] = Func
        else:
            Graph.FunctionList.append(Func)
        Graph.Update()
        self.Close()

def execute_action(action):
    d = SlopefieldDialog()
    d.ShowModal()

def OnEdit(Item):
    if "SlopefieldExample" in Item.PluginData:
        d = SlopefieldDialog(Item)
        d.ShowModal()
        return True

Action = Graph.CreateAction(Caption="Insert Slopefield...", OnExecute=execute_action, Hint="Create Slopefield from dy/dx.", ShortCut="Ctrl+Shift+S")
Graph.AddActionToMainMenu(Action)
Graph.OnEdit.append(OnEdit)