
## ----------------- Writing transducer locations to rt ------------------ ##

import numpy as np; import transducer_placment; import matplotlib.pyplot as plt; import phase_algorithms; import math; import algorithms; import time; import GUI_test
import sys
from PyQt5 import QtWidgets

trans_to_delete = []  # List of unwanted transducers leave blank to keep all
rt = transducer_placment.big_daddy()
rt = transducer_placment.delete_transducers(rt,trans_to_delete)
ntrans = len(rt);
global phase_index

# -------------------------------------------------------------------------- #p


choose = input("Please choose haptic as (h) or pattern as (p) or moving as (m) or GUI controled movment as (GUI): ")


## --------------------------- Haptic feedback --------------------------- ##
    
if choose == ("h"):
    print ("Haptic mode selected")
    phase_index = np.zeros((ntrans),dtype=int)
    phi_focus = phase_algorithms.phase_find( rt, 0, 0, 0.08 ) #  (x , y , z) (z = up)
    for transducer in range(0,ntrans):
        phase_index[transducer] = int(2500-phi_focus[transducer]/((2*math.pi)/1250))
        
    from connect import Controller 
    with Controller() as ctl:
        
        while True:          # Turns the pattern off and on as fast as possible
            
            for i in range(ctl.outputs):
                ctl.setOffset(i,phase_index[i])
            ctl.loadOffsets()
    
            for i in range(ctl.outputs):
                ctl.disableOutput(i)
# -------------------------------------------------------------------------- #
    


## -------------------------- Focused traps ------------------------------- ##  

elif choose == ("p"):
    print ("Pattern mode selected")
    phi_focus = phase_algorithms.phase_find(rt,0,0,0.018) # phi is the initial phase of each transducer to focus on a point
    phi = phase_algorithms.add_twin_signature(rt,phi_focus)
    phase_index = np.zeros((ntrans),dtype=int)
    #phi_focus = algorithms.read_from_excel_phases() # Takes phases from an excel spreadsheet of phases from 0 to 2pi, any over 2pi just loops
    for transducer in range(0,ntrans):
        phase_index[transducer] = int(2500-phi[transducer]/((2*math.pi)/1250))    
    
    
    from connect import Controller 
    with Controller() as ctl:
        ctl.setOutputDACPower(255)
        ctl.setOutputDACDivisor(50)
        for i in range(ctl.outputs):
            ctl.setOffset(i,phase_index[i])
        ctl.loadOffsets()
    
# -------------------------------------------------------------------------- #



## -------------------------- Moving traps ------------------------------- ##

elif choose == ("m"):
    print ("Move mode selected")
    
    circle_co_ords = algorithms.circle_co_ords(50, 0.005)
    #line_coordinates = np.linspace(0,2,100)
    
    
    phi_focus = np.zeros([ntrans,len(circle_co_ords[0])])
    phi =  np.zeros([ntrans,len(circle_co_ords[0])])
    phase_index = np.zeros(([ntrans,len(circle_co_ords[0])]),dtype=int)
    

    for point in range (0,len(circle_co_ords[0])):
        
        phi_focus_all = phase_algorithms.phase_find(rt,circle_co_ords[0][point],0.015,circle_co_ords[1][point]) # phi is the initial phase of each transducer to focus on a point
        for transducer in range(0,ntrans):
            phi_focus[transducer][point] = phi_focus_all[transducer]
    
        phi_all = phase_algorithms.add_twin_signature(rt,phi_focus_all)
        for transducer in range(0,ntrans):
            phi[transducer][point] = phi_all[transducer]
        
        for transducer in range(0,ntrans):
            phase_index[transducer][point] = int(2500-phi_focus[transducer][point]/((2*math.pi)/1250))    
        
    
    from connect import Controller  
    with Controller() as ctl:

        print("You have 25 seconds to trap the particle")
        a = 1
        print(circle_co_ords[0][0],circle_co_ords[1][0])
        while a==1: 
            for fuzz in range(6000):
                for i in range(ctl.outputs):
                    ctl.setOffset(i,phase_index[i][0])
                ctl.loadOffsets()
            a = 0
    
        print("Moving")
        while True: 
            for point in range (0,len(circle_co_ords[0])):
                for i in range(ctl.outputs):
                    ctl.setOffset(i,phase_index[i][point])
                ctl.loadOffsets()
                
# -------------------------------------------------------------------------- #


    
## ------------------------- Moving traps GUI ----------------------------- ##

elif choose == ("GUI"):
    print ("GUI mode selected")
    
    # Initial position in m (x , y , z) (z = up)
    global x,y,z
    x = 0    
    y = 0
    z = 0.02
    rt = transducer_placment.big_daddy()
    ntrans = len(rt);
    phase_index = np.zeros((ntrans),dtype=int)
    
    class Window_update_trap(QtWidgets.QWidget):
    
        def __init__(self):
            
            super().__init__()
            
            self.init_ui()
        
        def init_ui(self):
            
            
            self.forward = QtWidgets.QPushButton('Forward')
            self.backward = QtWidgets.QPushButton('Backwards')
            self.right = QtWidgets.QPushButton('Right')
            self.left = QtWidgets.QPushButton('Left')
            self.up = QtWidgets.QPushButton('Up')
            self.down = QtWidgets.QPushButton('Down')
            self.fuzz = QtWidgets.QPushButton('FUZZ')
            self.reset = QtWidgets.QPushButton('Reset to [0, 0.02, 0]')
            
            self.label1 = QtWidgets.QLabel('Movement Controls')
            self.label2 = QtWidgets.QLabel('Extra Controls')
    
    
            h_box_label = QtWidgets.QHBoxLayout()
            h_box_label.addStretch()
            h_box_label.addWidget(self.label1)
            h_box_label.addStretch() 
            
            h_box_labe2 = QtWidgets.QHBoxLayout()
            h_box_labe2.addStretch()
            h_box_labe2.addWidget(self.label2)
            h_box_labe2.addStretch() 
            
            h_box = QtWidgets.QHBoxLayout()
            h_box.addWidget(self.down)
            h_box.addWidget(self.forward)
            h_box.addWidget(self.up) 
        
            h_box2 = QtWidgets.QHBoxLayout()
            h_box2.addWidget(self.left)
            h_box2.addWidget(self.backward)
            h_box2.addWidget(self.right) 
            
            h_box3 = QtWidgets.QHBoxLayout()
            h_box3.addWidget(self.fuzz)
            h_box3.addWidget(self.reset)
        
            v_box = QtWidgets.QVBoxLayout()
            v_box.addLayout(h_box_label)
            v_box.addLayout(h_box)
            v_box.addLayout(h_box2)
            v_box.addLayout(h_box_labe2)
            v_box.addLayout(h_box3)
            
            self.setLayout(v_box)
            self.setWindowTitle('Particle Mover!')
            
            self.forward.clicked.connect(self.forward_click)
            self.backward.clicked.connect(self.backward_click)
            self.left.clicked.connect(self.left_click)
            self.right.clicked.connect(self.right_click)
            self.up.clicked.connect(self.up_click)
            self.down.clicked.connect(self.down_click)
            self.fuzz.clicked.connect(self.fuzz_click)
            self.reset.clicked.connect(self.reset_click)
            
            self.show()
    
        def calculate_and_move_trap(self):
            import math; import phase_algorithms; import numpy as np; import transducer_placment
            global phase_index
            
            phi_focus = phase_algorithms.phase_find(rt,x,y,z)
            phi = phase_algorithms.add_twin_signature(rt,phi_focus, 90)
            for transducer in range(0,ntrans):
                phase_index[transducer] = int(2500-phi[transducer]/((2*math.pi)/1250)) 
            print(" ")
            print("Moved!")
            print("Phase index is ", phase_index)
            print("New Position: ","x = " "%.3f" % x, "y = " "%.3f" % y, "z = " "%.3f" % z) #tester
            
            from connect import Controller
            with Controller() as ctl:
                ctl.setOutputDACPower(256)
                ctl.setOutputDACDivisor(100)
                for i in range(ctl.outputs):
                    ctl.setOffset(i,phase_index[i])
                ctl.loadOffsets()


        def calculate_and_move_trap_no_print(self):
            
            from connect import Controller
            with Controller() as ctl:
                ctl.setOutputDACPower(256)
                ctl.setOutputDACDivisor(100)
                for i in range(ctl.outputs):
                    ctl.setOffset(i,phase_index[i])
                ctl.setOutputDACFreq(200)
                ctl.loadOffsets()

            
        def forward_click(self):
            global x               
            x += 0.001
            self.calculate_and_move_trap()
            print('x changed to = ', "%.3f" % x)
        
        def backward_click(self):
            global x 
            x -= 0.001
            self.calculate_and_move_trap()
            print('x changed to = ', "%.3f" % x)
            
        def left_click(self):
            global z 
            z += 0.001
            self.calculate_and_move_trap()
            print('z changed to = ', "%.3f" % z)
            
        def right_click(self):
            global z 
            z -= 0.001
            self.calculate_and_move_trap()
            print('z changed to = ', "%.3f" % z)
            
        def up_click(self):
            global y 
            y += 0.001
            self.calculate_and_move_trap()
            print('y changed to = ', "%.3f" % y)
            
        def down_click(self):
            global y 
            y -= 0.001
            self.calculate_and_move_trap()
            print('y changed to = ', "%.3f" % y)
            
        def fuzz_click(self):
            print(' ')
            print('Fuzzing for 30 seconds')
            self.calculate_and_move_trap_no_print()
            print(' ')
            print('Finished Fuzzing')
            
        def reset_click(self):
            global x,y,z
            x = 0; y = 0; z = 0.02;
            print(' ')
            print('Reset to [0, 0, 0.02]')
    
    app = QtWidgets.QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    a_window = Window_update_trap()
    sys.exit(app.exec_())
    
# -------------------------------------------------------------------------- #


else:
    print("Come on, pick one of the correct letters!")
    




















    
    
    
    
    
    
    
    
    