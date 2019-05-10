import dill as pickle

class Peptide:
    def __init__(self, resin , loading , seq , eq = None , volfactor = None ,verbose = None, sim = None):
        self.mw = { 'A' : [311.33,0],
                'C' : [585.70,0],
                'D' : [411.50,0],
                'E' : [425.48,0],
                'F' : [387.43,0],
                'G' : [297.31,0],
                'H' : [619.71,0],
                'I' : [353.42,0],
                'K' : [468.54,0],
                'L' : [353.41,0],
                'M' : [371.45,0],
                'N' : [596.69,0],
                'P' : [337.37,0],
                'Q' : [610.72,0],
                'R' : [648.78,0],
                'S' : [383.45,0],
                'T' : [397.48,0],
                'V' : [339.39,0],
                'W' : [526.59,0],
                'Y' : [459.55,0],
                'Bz' : [122.12,0],
                'FAM' : [376.12,0]}
        sim = False if sim == None else sim
        verbose = False if verbose == None else verbose
        self.seq = seq
        findus = __import__ ('findus')
        self.pip = findus.Pipette(83,"http://10.0.3.1", "P1000" , tip = "tip1000",to=1,verbose= verbose, sim = sim )
        self.ap = findus.WorkingSpace(self.pip)
        self.peptizer = findus.Peptidizer("http://10.0.3.99", rpm = 320 , verbose = verbose , sim = sim )
    #syringe
        syringe = None
        syringe = findus.Rack(52)
        syringe.setXY([37500,64200])
        syringe.setupRack(0 , 1 , 1 , bin_type="syringe10")
        self.ap.addRack("syringe" , syringe)
        self.ap.setBinName("syr_1", [["syringe" , 0,0]])
    #amino acid
        self.ap.setBinName("A",[["eppi15", 0,0]])
        self.ap.rack("eppi15").setType( [0,0], "eppi20")
        self.ap.setBinName("C",[["eppi15", 0,1]])
        self.ap.rack("eppi15").setType( [0,1], "eppi20")
        self.ap.setBinName("D",[["eppi15", 0,2]])
        self.ap.rack("eppi15").setType( [0,2], "eppi20")
        self.ap.setBinName("E",[["eppi15", 0,3]])
        self.ap.rack("eppi15").setType( [0,3], "eppi20")
        self.ap.setBinName("F",[["eppi15", 0,4]])
        self.ap.rack("eppi15").setType( [0,4], "eppi20")
        self.ap.setBinName("G",[["eppi15", 0,5]])
        self.ap.rack("eppi15").setType( [0,5], "eppi20")
        self.ap.setBinName("H",[["eppi15", 0,6]])
        self.ap.rack("eppi15").setType( [0,6], "eppi20")
        self.ap.setBinName("I",[["eppi15", 0,7]])
        self.ap.rack("eppi15").setType( [0,8], "eppi20")
        self.ap.setBinName("K",[["eppi15", 0,8]])
        self.ap.rack("eppi15").setType( [0,8], "eppi20")
        self.ap.setBinName("L",[["eppi15", 0,9]])
        self.ap.rack("eppi15").setType( [0,9], "eppi20")
        self.ap.setBinName("M",[["eppi20", 0,0]])
        # in WorkingSpace rack eppi20 are default type eppi15
        self.ap.rack("eppi20").setType( [0,0], "eppi20")
        self.ap.setBinName("N",[["eppi20", 0,1]])
        self.ap.rack("eppi20").setType( [0,1], "eppi20")
        self.ap.setBinName("P",[["eppi20", 0,2]])
        self.ap.rack("eppi20").setType( [0,2], "eppi20")
        self.ap.setBinName("Q",[["eppi20", 0,3]])
        self.ap.rack("eppi20").setType( [0,3], "eppi20")
        self.ap.setBinName("R",[["eppi20", 0,4]])
        self.ap.rack("eppi20").setType( [0,4], "eppi20")
        self.ap.setBinName("S",[["eppi20", 0,5]])
        self.ap.rack("eppi20").setType( [0,5], "eppi20")
        self.ap.setBinName("T",[["eppi20", 0,6]])
        self.ap.rack("eppi20").setType( [0,6], "eppi20")
        self.ap.setBinName("V",[["eppi20", 0,7]])
        self.ap.rack("eppi20").setType( [0,7], "eppi20")
        self.ap.setBinName("W",[["eppi20", 0,8]])
        self.ap.rack("eppi20").setType( [0,8], "eppi20")
        self.ap.setBinName("Y",[["eppi20", 0,9]])
        self.ap.rack("eppi20").setType( [0,9], "eppi20")
        self.ap.setBinName("tbtu",[["s120", 0,0 ],["s120", 1,0 ],["s120", 2,0 ]])
        self.ap.setBinName("nmm",[["s6", 3,0 ]])
        self.ap.setBinName("piperidine",[["apo1", 0,0]] )
        self.ap.setBinName("dmf-resin_wash",[["apo2", 0,0 ],["apo3", 0,0 ]])
        self.ap.setBinName("dmf-tip_wash",[["s25", 0,0],["s25", 0,1]] )
        self.ap.setBinName("dmf-tip_dump",[["s25", 1,0] ,["s25", 1,1]] )
    #general calculation
        volfactor = 40 if volfactor == None else volfactor
        eq = 3 if eq == None else eq
        part_aa = 0.6 / 2.8
        part_tbtu = 2/ 2.8
        part_nmm = 0.2 / 2.8
        mw_tbtu = 321.09
        mw_nmm = 101.15
        scale = resin * loading
        self.total_vol = int(scale * volfactor)
        print("Total Volume: ", self.total_vol)
        self.aa_vol_step = int(scale*volfactor * part_aa)
        self.tbtu_vol_step = int(scale * volfactor * part_tbtu)
        self.nmm_vol_step = int(scale * volfactor *part_nmm)
        aa_dissolve= part_aa * volfactor / eq
        tbtu_dissolve =part_tbtu * volfactor / eq
        nmm_dissolve=part_nmm * volfactor / eq
    #aa-calc
        for aa in seq : 
            self.mw[aa][1] += self.aa_vol_step
        for aa in self.mw:
            if self.mw[aa][1] > 0 :
                ra = self.ap.bin_names[aa][0]
                bin_count = int(self.mw[aa][1]/(self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_max-self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe))+1
                self.mw[aa][1] += self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe * bin_count
                print( "Einwaage" , aa ,": {:6.0f} DMF (µL)".format(self.mw[aa][1]), ", {:6.2f} (mg)".format(self.mw[aa][1]/1000/aa_dissolve*self.mw[aa][0]))
                self.ap.setVol(aa,int(self.mw[aa][1]))
    #tbtu_calc
        ra = self.ap.bin_names['tbtu'][0]
        tbtu_vol = self.tbtu_vol_step * len(seq)
        bin_count = int(tbtu_vol/(self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_max-self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe))+1
        tbtu_vol += self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe * bin_count
        print ("Einwaage tbtu: " ,"{:6.0f} DMF (µl)".format(tbtu_vol) ,"{:6.2f}  (mg)".format(tbtu_vol/ tbtu_dissolve * mw_tbtu/1000) )
        self.ap.setVol("tbtu" , int(tbtu_vol))
    #nmm_calc
        ra = self.ap.bin_names['nmm'][0]
        nmm_vol = self.nmm_vol_step * len(seq)
        bin_count = int(nmm_vol/(self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_max-self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe))+1
        nmm_vol += self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe * bin_count
        nmm_excess = 3
        print ("Einwaage nmm " , " DMF {:6.0f} (µL)".format(nmm_vol*(1-0.91/nmm_dissolve*nmm_excess* mw_nmm/1000)), ", NMM {:6.0f} (µl)".format(nmm_vol/nmm_dissolve*nmm_excess * mw_nmm * 0.91/1000) )
        self.ap.setVol("nmm" , int(nmm_vol))
    #piperidine_calc
        ra = self.ap.bin_names['piperidine'][0]
        piperidine_vol = self.total_vol*2 * len(seq)
        bin_count = int(piperidine_vol/(self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_max-self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe))+1
        piperidine_vol += self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe * bin_count
        print ("Piperidine: {:6.0f} (µL)".format(piperidine_vol))
        self.ap.setVol("piperidine" , int(piperidine_vol))
    #dmf-tip_wash
        ra = self.ap.bin_names['dmf-tip_wash'][0]
        self.dmf_tip_vol_step = 1000
        dmf_tip_vol= self.dmf_tip_vol_step *4 * len(seq)
        bin_count = int(dmf_tip_vol/(self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_max-self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe))+1
        dmf_tip_vol += + self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe*bin_count
        print ("dmf-tip_wash : {:6.0f} (µL)".format( dmf_tip_vol ))
        self.ap.setVol("dmf-tip_wash" , int(dmf_tip_vol))
    #dmf-resin_wash
        ra = self.ap.bin_names['dmf-resin_wash'][0]
        dmf_resin_vol = self.total_vol * 3 * (2*len(seq)+1)
        bin_count = int(dmf_resin_vol/(self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_max-self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe))+1
        dmf_resin_vol += self.ap.rack(ra[0]).bins[ra[1]][ra[2]].v_safe * bin_count
        print ("dmf-resin_wash : {:6.0f} (µL)".format(dmf_resin_vol ))
        self.ap.setVol("dmf-resin_wash" , int(dmf_resin_vol))
    
    def run(self, speed_x = None , speed_y = None , speed_z = None,verbose = None):
        if verbose: print ("Pipette aktivieren")
        self.ap.pipette.init( speed_x= speed_x, speed_y = speed_y , speed_z = speed_z)

#Swelling (3x)
        for k in range (3):
            self.ap.fill("dmf-resin_wash", self.total_vol , "syr_1", 1,1, medium="Water", count=0)
            self.peptizer.runShaker(3*60,10,50 , rpm=280)
            self.peptizer.runVac(10)
            self.ap.setVol("syr_1" , 0 )
# Amino Acid Cycle
        for aa in self.seq:
    #piperidine
            self.ap.fill("piperidine", self.total_vol , "syr_1", 1,1, medium="Water", count=0)
            self.peptizer.runShaker(10*60,10,50 , rpm=280)
            self.peptizer.runVac(10)
            self.ap.setVol("syr_1" , 0 )
            self.ap.fill("piperidine", self.total_vol, "syr_1", 1,1, medium="Water", count=0)
            self.ap.fill("dmf-tip_wash", self.dmf_tip_vol_step , "dmf-tip_dump", 1,1, medium="Water", count=0)
            self.peptizer.runShaker(20*60,10,50 , rpm=280)
            self.peptizer.runVac(10)
            self.ap.setVol("syr_1" , 0 )
    #dmf-resin_wash
            for k in range (3):
                self.ap.fill("dmf-resin_wash", self.total_vol , "syr_1", 1,1, medium="Water", count=0)
                self.peptizer.runShaker(3*60,10,50 , rpm=280)
                self.peptizer.runVac(30)
                self.ap.setVol("syr_1" , 0 )
    #Amino Acid
            self.ap.fill(aa, self.aa_vol_step , "syr_1", 1,1, medium="Water", count=0)
            self.ap.fill("dmf-tip_wash", self.dmf_tip_vol_step , "dmf-tip_dump", 1,1, medium="Water", count=0)
            self.ap.fill("tbtu", self.tbtu_vol_step, "syr_1", 1,1, medium="Water", count=0)
            self.ap.fill("dmf-tip_wash", self.dmf_tip_vol_step  , "dmf-tip_dump", 1,1, medium="Water", count=0)
            self.ap.fill("nmm", self.nmm_vol_step , "syr_1", 1,1, medium="Water", count=0)
            self.ap.fill("dmf-tip_wash",self.dmf_tip_vol_step , "dmf-tip_dump", 1,1, medium="Water", count=0)
            self.peptizer.runShaker(60*60,10,290 , rpm=280)
            self.peptizer.runVac(10)
            self.ap.setVol("syr_1" , 0 )
    #dmf-resin_wash
            for k in range (3):
                self.ap.fill("dmf-resin_wash", self.total_vol , "syr_1", 1,1, medium="Water", count=0)
                self.peptizer.runShaker(3*60,10,50 , rpm=280)
                self.peptizer.runVac(30)
                self.ap.setVol("syr_1" , 0 )
    
#########################################################
#              Standard methods for class               #
#########################################################
    
    def checkVol(self, bin=None , index = None , check = None , speed = None):
        self.ap.checkVol(bin = bin , index = index , check = check , speed = speed )
    
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
