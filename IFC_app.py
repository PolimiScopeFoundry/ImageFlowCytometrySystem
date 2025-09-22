"""
Created on Sept 20 18:07:04 2025

@authors: Andrea Bassi, Politecnico di Milano
"""

from ScopeFoundry import BaseMicroscopeApp


def add_path(path):
    import sys
    import os
    # add path to ospath list, assuming that the path is in a sybling folder
    from os.path import dirname
    sys.path.append(os.path.abspath(os.path.join(dirname(dirname(__file__)),path)))


class camera_app(BaseMicroscopeApp):
    
    name = 'camera_app'
    
    def setup(self):
        
        #Add hardware components
        print("Adding Hardware Components")
        add_path('IDS_ScopeFoundry')
        from camera_hw import IdsHW
        self.add_hardware(IdsHW(self))
        
        # Add measurement components
        print("Create Measurement objects")
        from IFC_measurement import IfcMeasure
        self.add_measurement(IfcMeasure(self))


if __name__ == '__main__':
    import sys
    import os
    
    app = camera_app(sys.argv)
    
    path = os.path.dirname(os.path.realpath(__file__))
    new_path = os.path.join(path, 'Settings', 'Settings.ini')
    print(new_path)

    # app.settings_load_ini(new_path)
    
    #connect all the hardwares
    for hc_name, hc in app.hardware.items():
       hc.settings['connected'] = True


    sys.exit(app.exec_())