#to start:
#import rob
#ap = rob.WorkingSpace(rob.Pipette(63,"http://10.0.3.1","P200", tip = "tip200",to=1,verbose=True ))
#Assay=rob.Assay(ap)
#Assay.checkVol(check=True)
#Assay.run(<column_wp96>)

import dill as pickle

class Assay:
    
    def __init__(self,ap):
        self.ap = ap
        self.ap.setBinName("buffer/DMSO" , [[ "eppi20", 0,0]])
        self.ap.setBinName("enzyme" ,[[ "eppi20", 0,1]])
        self.ap.setBinName("inhibitor" , [["eppi20", 0,2]])
        self.ap.setBinName("substrate" ,[[ "eppi20", 0,3]])
        self.ap.setBinName("dilution" , [["eppi15", 0,0]])
        self.ap.setVol("buffer/DMSO",1000)
        self.ap.setVol("enzyme",800)
        self.ap.setVol("inhibitor",200)
        self.ap.setVol("substrate",1000)
        
    def run(self, wp96_row , speed_x = None , speed_y = None , speed_z = None,verbose = None):
        self.ap.setBinName("replicate1" , [["wp96", wp96_row,0]])
        self.ap.setBinName("replicate2" , [["wp96", wp96_row+1,0]])
        self.ap.setBinName("replicate3" , [["wp96", wp96_row+2,0]])
        self.ap.setBinName("inh+sub" , [["wp96", wp96_row+3,0]])
        self.ap.pipette.init( speed_x= speed_x, speed_y = speed_y , speed_z = speed_z, dip_in=250)
        self.ap.getTip("tipbin","tip", 0,0,speed=120)
        self.pause()
        self.ap.fill("buffer/DMSO", 200 , "buffer/DMSO", 1,1, medium="Water", count=1)
        self.ap.fill("buffer/DMSO", 100 , "dilution", 1,8, vol_max = 100 , medium="Water", count=0)
        self.ap.fill("inhibitor", 100 , "dilution" , 1,7, dil = True , medium="Water" , count=3, vol_wet=150)
        self.ap.getTip("tipbin","tip", 0,1,speed=120)
        self.pause()
        self.ap.fill("substrate", 200 , "substrate", 1,1, medium="Water", count=1)
        self.ap.fill("substrate", 120 , "inh+sub", 1,8, vol_max = 120 , medium="Water", count=0)
        self.ap.fill("dilution", 60 , "inh+sub" , 1,-8, NtoN = True , medium="Water" , count=1)
        self.ap.getTip("tipbin","tip", 0,2,speed=120)
        self.pause()
        self.ap.fill("enzyme", 200 , "enzyme", 1,1, medium="Water", count=1)
        self.ap.fill("enzyme", 30 , "replicate1", 1,8, vol_max = 30 , medium="Water", count=0)
        self.ap.fill("enzyme", 30 , "replicate2", 1,8, vol_max = 30 , medium="Water", count=0)
        self.ap.fill("enzyme", 30 , "replicate3", 1,8, vol_max = 30 , medium="Water", count=0)
        self.ap.reset()
#########################################################
#              Standard methods for class               #
#########################################################
    
    def checkVol(self, bin=None , vol = None , check = None):
        if check:  self.ap.init(speed_x = 150 , speed_y = 150 , speed_z = 150)
        if bin == None :
            for n in self.ap.bin_names:
                print( self.ap.setVol(n, None , check))
        else:
            return self.ap.setVol(bin, vol , check)
    
    def save(self, path):
        self.ap.save(path +"_ap")
        pickle.dump(self, open( path + ".p" , "wb"))
    
    def reset(self ):
        self.ap.reset()
    def pause(self):
        while True :
            result = input( "C(ontinue) / A(bort)?:")
            if result == "C" or result== "c": return
            elif result =="A" or result=="a": 
                self.reset()
                raise Exception ("User abort")

def loadProg (path):
    prog = pickle.load(open( path+'.p','rb'))
    prog.ap = pickle.load(open( path+'_ap.p','rb'))
    prog.ap.rack_list = pickle.load(open( path+'_ap_racks.p','rb'))
    prog.ap.bin_names = pickle.load(open( path+'_ap_bnames.p','rb'))
    prog.ap.rack_names = pickle.load(open(path+'_ap_rnames.p','rb'))
    return prog