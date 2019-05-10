# -*- coding: utf-8 -*-
import math
import requests
import time
import dill as pickle

class Bin:
    x = 0
    y = 0
    z = 0      # Actual Fill level measured from z_0 Positive direction
    z_0 = 0    # Bottom of top edge negative direction
    z_max = 0  # from top edge negative direction
    h = 0      # Height vessel  
    d = 0
    vol = 0
    t = 20
    bin_type = "empty"

class Rack:
    def __init__(self,h_rack):
        self.x=0
        self.y=0
        self.z=0
        self.h_rack = int(h_rack*160)
        self.h_max = 0
        self.bins = []
        self.init=False
        self.bin_types = {"schnappi6":[40.2 ,16,38.5,8,self.vzschnappi6, 200 , 6000],
                "schnappi8":[40.5 ,18 ,38.5 ,5,self.vzschnappi8 , 250 , 8000],
                "schnappi12":[45, 20 , 43.6,10,self.vzschnappi12 , 320 , 12000 ],
                "schnappi25":[70.5, 23.5 , 70.375 ,10 , self.vzschnappi25,450 , 25000],
                "eppi15": [1.93+10,0,38.2+10,5.6+10,self.vzeppi15, 20 , 1500 ],
                "eppi20" : [1.93 +10 ,0 , 38.8 + 10 , 5.6 + 10 , self.vzeppi20,20 , 2000],
                "wp96": [14.5 ,7,11,2,self.vzwp96,40, 1000 ],
                "wp96deep": [55.35 ,7,31.25,2,self.vzwp96, 40 , 1000],
                "apo100" : [97.5 , 52 , 97.5, 41.15 , self.vzapo100 , 1200 , 100000],
                "tip200" : [ 5.125+8.875 ,0, 49.5 + 8.875 ,0,self.dummy , 0 , 0],
                "tip1000" : [ 5.125 , 0 , 69.5 , 0 , self.dummy , 0 , 0 ],
                "tipbin" : [ 29.3125 , 11.875, 78.375 , 0 , self.dummy , 0 , 0 ], 
                "syringe10" : [65.20 , 15.5 , 42 , 20 , self.vzsyringe10  , 0 , 10000 ]  }
    
    def setXY(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        self.init=True
    
    def setType(self,ind,ty):
        bin = self.bins[ind[0]][ind[1]]
        bin.bin_type = ty
        bin.z_0 = int(self.bin_types[ty][2]*160)
        bin.h = int(self.bin_types[ty][0]*160)
        bin.z_max = int(self.bin_types[ty][3]*160)
        bin.v_safe = self.bin_types[ty][5]
        bin.v_max = self.bin_types[ty][6]
        if bin.h + self.h_rack > self.h_max:  self.h_max = bin.h + self.h_rack
        
    def setVol (self,ind,vol):
        bin = self.bins[ind[0]][ind[1]]
        if vol==None:
            return bin.vol
        else :
            bin.z = self.bin_types[bin.bin_type][4](vol)
            bin.vol = vol
            return bin.vol
    
    def addVol(self,ind,vol):
        self.bins[ind[0]][ind[1]].vol += vol
        assert self.bins[ind[0]][ind[1]].vol>=0
    
    def setTemp(self,ind,temp):
        self.bins[ind[0]][ind[1]].t = temp 
    
    def getPos(self, ind, v=None, dip_in=None):
        v = 0 if v==None else v
        dip_in = 0 if dip_in==None else dip_in
        bin=self.bins[ind[0]][ind[1]]
        v = v + bin.vol
        #print("vol:" , v)
        assert v >=0
        h_add = self.bin_types[bin.bin_type][4](v)
        if h_add -dip_in > 0 : h_add -= dip_in
        return [self.x + bin.x,
                self.y + bin.y , 
                self.h_rack+bin.h-bin.z_0+h_add]
    
    def getZ0(self,ind):
        return self.bins[ind[0]][ind[1]].z_0
    
    def vzschnappi6(self,v):
        return int(v*4/math.pi/(self.bin_types["schnappi6"][1]**2)*160)
    
    def vzschnappi8(self,v):
        return int(v*4/math.pi/(self.bin_types["schnappi8"][1]**2) * 160 )
    
    def vzschnappi12(self,v):
        return int(v*4/math.pi/(self.bin_types["schnappi12"][1]**2)*160 )
    
    def vzschnappi25(self,v):
        return int(v*4/math.pi/(self.bin_types["schnappi25"][1]**2)*160 )
    
    def vzwp96(self,v):
        return int(v*4 /(self.bin_types["wp96"][1]**2 * math.pi )*160)
    
    def vzapo100(self,v):
        return int(v*4 /(self.bin_types["apo100"][1]**2 * math.pi )*160)
    
    def vzsyringe10(self,v):
        return int(v*4 /(self.bin_types["syringe10"][1]**2 * math.pi )*160)
    
    def vzeppi15(self,v):
        return int(0.5798857072*((v*0.6235728054)**0.5902092035)*160)
#        if v < 13:
#            return int((0)*160)
#        elif v < 509 :
#            return int((1.74 + (v -13)*3 / (math.pi * 30.5625))*160)
#        else:
#            return int((15.9+1.74 + (v-509)*3/(math.pi*58.7725))*160)
    
    def vzeppi20(self,v):
        if v < 257 :
            return int(2.37043505089479*((v*0.0227431435410815)**0.567537882105625)*160)
        else:
            return int((0.015817414* v + 2.621071723)*160)
    
    def dummy(self,v):
        return 0
    
    def setupRack(self, raster_x,i,j,raster_y=None, bin_type=None):
        if not bin_type == None:
            z_0 = int(self.bin_types[bin_type][2]*160)
            h = int(self.bin_types[bin_type][0]*160)
            z_max = int(self.bin_types[bin_type][3]*160)
            d = int(self.bin_types[bin_type][1]*160)
            v_safe = self.bin_types[bin_type][5]
            v_max = self.bin_types[bin_type][6]
        raster_y = raster_x if raster_y==None else raster_y
        for iy in range(i):
            self.bins.append([])
            for ix in range(j):
                bin = Bin()
                bin.x = int(raster_x * ix *160)
                bin.y = int(raster_y * iy *160 )
                bin.z_0 = z_0
                bin.d = d
                bin.z = 0
                bin.z_max = z_max
                bin.h = h
                bin.bin_type = bin_type
                bin.v_safe = v_safe
                bin.v_max = v_max
                self.bins[iy].append(bin)
        self.h_max = self.h_rack + h
    



"""
P200
Piston diameter 4
200 µl equals 16 mm/Hub => 0,08 mm / µl => *537 steps => 42.96 steps/µl
200 µl 42.96 

P1000
Piston diameter 8 
1000 µl equals 19.9  mm Hub => 0,02 mm / µl  * 537 steps/ mm => 10.686 stpes/µl

200 steps * 32 microsteps / rotation
GT2 toothed belt Pitch = 2mm
Pulley with 20 teeth
-> 40 mm  / rotation
-> 200 *32 / 40  = 160 steps / mm
"""
class Peptidizer:
    
    START_SHAKER = "0"
    STOP_SHAKER = "1"
    START_VAC ="2"
    STOP_VAC = "3"
    
    def __init__(self , url, rpm = None , power = None, verbose = None, sim = None):
        self.url = url
        self.rpm = 250 if rpm == None else rpm 
        self.sim = False if sim == None else sim 
        self.power = 1023 if power == None else power
        self.verbose = False if verbose == None else verbose
        self.statShaker = False
        self.statVac = False
        self.to = 0.5   # time out for simulation
        try:
            r = requests.get (self.url+"/version", timeout=(self.to , 30) )
            print(r.status_code , r.text )
        except requests.exceptions.Timeout:
            assert self.sim == True
            print ("Peptizer not connected")
        
    def startShaker (self, time , rpm = None):
        rpm = self.rpm if rpm == None else rpm
        values = {'action' : self.START_SHAKER,
                  'time' : time ,
                  'rpm' : rpm}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if self.verbose : print(r.status_code , r.text )
            if r.status_code == 200 : self.statShaker = True
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.statShaker = True
            print ("sim Shaker started")
    
    def runShaker(self, tges , tein, tpause, rpm= None):
        rpm = self.rpm if rpm == None else rpm
        angle = int(tein * rpm/60) * 360
        tein= angle/rpm*60/360
        cycles = int(tges/(tein+tpause))
        tpause = (tges/cycles - tein)
        values = {'action' : self.START_SHAKER,
                  'angle' : angle,
                  'rpm' : rpm}
        for i in range(cycles):
            try:
                r = requests.post(self.url, values,timeout=(self.to , 30))
                if self.verbose : print(r.status_code , r.text )
                if r.status_code == 200 : self.statShaker = True
            except requests.exceptions.Timeout:
                assert self.sim == True 
                self.statShaker = True
                if self.verbose : print ("sim Shaker started ",angle , tein , tpause)
                return
            time.sleep(tpause+tein)
    
    def runVac (self, mytime , power=None):
        power = self.power if power == None else power
        values = {'action' : self.START_VAC,
                  'time'   : mytime ,
                  'power'  : power }
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if self.verbose : print(r.status_code , r.text )
            if r.status_code == 200 : 
                self.statVac = True
                if self.verbose : print ("Vac started ",mytime)
                time.sleep(mytime)
            else: print ("Vac failed to start") 
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.statVac = True
            print ("sim Vac started")
    
    def stopShaker(self):
        values = {'action' : self.STOP_SHAKER}    
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if self.verbose : print(r.status_code , r.text )
            if r.status_code == 200 : self.statShaker = False
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.statShaker = False
            print ("sim Shaker stopped")
    
    def stopVac(self):
        values = {'action' : self.STOP_VAC}    
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if self.verbose : print(r.status_code , r.text )
            if r.status_code == 200 : self.statVac = False
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.statShaker = False
            print ("sim Shaker stopped")
    

class Pipette:
# Roboter Actions
    INIT = "0"
    GET = "1"
    PUT = "2"
#    WET = "3"
#    FLUSH = "4"
    RESET = "5"
    MOVE_X = "6"
    MOVE_Y = "7"
    MOVE_Z = "8"
    MOVE_PIP = "9"
    MOVE_XY = "10"
    SET_POS = "11"
# substances "name" : (v_pip , density)
    media = {"Water" : [ 20 , 0.998 ] ,
             "Water_f" : [ 40, 0.998 ] ,
             "DMSO"  : [ 20 , 1.1 ] ,
             "Puffer": [ 20 , 1.05 ] ,
             "Enzym" : [ 20 , 1 ] }
    
    pip_type = { "P200" : [43.806174,0.977553,2.382654, 200 , 5 , 3 ] ,
                 "P1000" : [10.8345 , 0.9812308 , 9.4327139 , 1000 , 2 , 3 ] }
    
    #non_lin = [0,1,0]  #Coefficients equalization parabola
    
    def __init__(self,h,url, p_type ,tip=None , calib = None, verbose = None, to=None , sim = None ):
        self.backtrack = self.pip_type[p_type][4] * 537
        self.verbose = False if verbose == None else verbose
        self.to = 0.5 if to == None else to
        self.sim = False if sim == None else sim
        self.vol_max=self.pip_type[p_type][3]    #usable volume   -> z = vol_max +backtrack
        self.temp_amb=20
        self.moist=50 
        self.calib=[self.pip_type[p_type][0],self.pip_type[p_type][1],self.pip_type[p_type][2]] if calib == None else calib
        self.speed_x = 120
        self.speed_y = 120
        self.speed_z = 120
        self.speed_pip = 20
        self.def_speed = 40
        self.def_count = 4
        self.dip_in = self.pip_type[p_type][5] * 160 
        self.vol_act = 0
        self.status = False
        self.z_0 = 0
        self.h = h*160
        self.tip = False
        self.tip_type = ""
        if tip != None :
            self.tip_type = tip
            self.tip = True
            self.z_0 = int((Rack(0).bin_types[tip][2] - Rack(0).bin_types[tip][0])*160)
        self.pos = [0,0,self.h-self.z_0,0,0]
        self.url=url  #"http://10.0.3.1"
        try:
            r = requests.get (self.url+"/version", timeout=(self.to , 30) )
            print(r.status_code , r.text )
        except requests.exceptions.Timeout:
            print ("Pipette not connected")
            assert self.sim == True
            
    
    def init(self, temp= None , moist= None, 
                  speed_x= None,speed_y = None, speed_z= None,
                  backtrack= None,dip_in= None):
        if self.status == True: return
        self.temp = self.temp_amb if temp==None else temp
        self.moist = self.moist if moist==None else moist
        self.speed_x = self.speed_x if speed_x==None else speed_x
        self.speed_y = self.speed_y if speed_y==None else speed_y
        self.speed_z = self.speed_z if speed_z==None else speed_z
        self.backtrack = self.backtrack if backtrack==None else backtrack
        self.dip_in = self.dip_in if dip_in==None else dip_in
        self.pos[2] = self.h-self.z_0
        self.vol_act = 0
        values = {'action' : self.INIT,
                  'temp_amb' : self.temp ,
                  'moist' : self.moist,
                  'calib' : self.calib,
                  'x' : self.speed_x,
                  'y' : self.speed_y,
                  'z' : self.speed_z,
                  'pip' : self.backtrack,
                  'z_0' : self.pos[2]}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if r.status_code == 200: self.status = True
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose : print(r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.pos[3] = self.backtrack
            self.status = True
            print ("sim Init" , self.pos)
    
    def reset(self, h ):
        if self.status == False: return
        speed = 120
        self.moveZ(h,120)
        self.moveXY([0,0], 120)
        self.moveZ(self.h- self.z_0,120 )
        self.movePip(0,20)
        self.pos = [0,0,self.h- self.z_0,0,0]
        self.vol_act = 0
        values = {'action' : self.RESET}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            self.status = False
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose : print(r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.status = False
            print ("sim reset" , self.pos)
    
    def get(self,rack,substance, vol,count, speed ,medium,vol_wet):
        count = 0 if count==None else count
        if self.pos[2] < rack.h_max:
            self.moveZ(rack.h_max, speed)
        pos = rack.getPos(substance, -vol, self.dip_in)
        self.moveXY(pos , speed)
        med = self.media[medium]
        if count > 0:
            pos_wet = rack.getPos(substance, -vol_wet, self.dip_in)
            self.moveZ(pos_wet[2] ,speed)
            for i in range(count):
                self.movePip(int(self.calib[0]*med[1]*(vol_wet*self.calib[1]+self.calib[2]) +self.backtrack),med[0])
                self.movePip(self.backtrack, med[0])
            self.moveZ(pos[2] + 2000 , speed)
            self.movePip(0, med[0])
            self.movePip(self.backtrack,med[0])
        self.moveZ(pos[2] , speed)
        self.movePip(int(self.calib[0]*med[1]*(vol*self.calib[1]+self.calib[2])+self.backtrack),med[0])
        rack.addVol(substance,-vol)
        self.moveZ(rack.h_max, speed)
    
    def put(self,rack,substance, vol,speed , medium):
        if self.pos[2] < rack.h_max:
            self.moveZ(rack.h_max,speed)
        pos = rack.getPos(substance,vol, self.dip_in)
        self.moveXY (pos,speed)
        self.moveZ(pos[2],speed)
        med = self.media[medium]
        #self.vol_act = self.vol_act-vol
#pip_pos = int(self.fu_vol(self.vol_act) *self.calib)+self.backtrack
        if self.pos[3] - int((vol*med[1]*self.calib[1])*self.calib[0]) <= self.backtrack+500:
#if pip_pos <= self.backtrack+20:
            self.movePip(0,med[0])
            self.moveZ(rack.h_max,speed)
            self.movePip(self.backtrack,med[0])
            #self.vol_act = 0
        else:
            self.movePip(self.pos[3] - int((vol*med[1]*self.calib[1])*self.calib[0]),med[0])
#self.movePip(pip_pos,speed_pip)
            self.moveZ(rack.h_max,speed)
        rack.addVol(substance,vol)
    
    def moveXY(self,pos,speed):
        speed = min(self.speed_x if speed==None else speed,self.speed_y if speed==None else speed)
        assert pos[1] >= 0 and pos[1] < 66000
        assert pos[0] >= 0 and pos[0] < 45000
        values = {'action' : self.MOVE_XY,
            'x' : pos[0],
            'y' : pos[1],
            'rpm' : speed}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if r.status_code != 200:
                print ("CMD failed")
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose : print (r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.pos[0] = pos[0]
            self.pos[1] = pos[1]
            print ("sim XY" , self.pos)
    
    def moveX (self,x,speed):
        speed = self.speed_x if speed==None else speed
        assert x >=0 and x < 45000
        values = {'action' : self.MOVE_X,
            'x' : x,
            'rpm' : speed}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if r.status_code != 200:
                print ("CMD failed")
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose : print (r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.pos[0] = x
            print ("sim X" , self.pos)
    
    def moveY (self,y,speed):
        speed = self.speed_y if speed==None else speed
        assert y >= 0 and y < 66000
        values = {'action' : self.MOVE_Y,
            'y' : y,
            'rpm' : speed}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if r.status_code != 200:
                print ("CMD failed")
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose: print (r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.pos[1] = y
            print ("sim Y" , self.pos)
    
    def moveZ (self,z,speed):
        speed = self.speed_z if speed==None else speed
        #print ("z..." , z)
        assert z-(self.h-self.z_0) >= 0 and z -(self.h-self.z_0) < 15800
        values = {'action' : self.MOVE_Z,
            'z' : z,
            'rpm' : speed}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if r.status_code != 200:
                print ("CMD failed")
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose : print (r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.pos[2] = z
            print ("sim Z" , self.pos)
    
    def movePip (self,pip,speed):
        speed = self.speed_pip if speed==None else speed
        assert pip >= 0 and pip < 12500
        values = {'action' : self.MOVE_PIP,
            'pip' : pip,
            'rpm' : speed}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if r.status_code != 200:
                print ("CMD failed")
            time.sleep(0.5 + 1.5/10000*abs(self.pos[3]-pip))
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose : print (r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            self.pos[3] = pip
            print ("sim Pip" , self.pos)
    
    def getTip(self,rack,ind,speed):
        if self.tip : return
        if self.pos[2] < rack.h_max:
            self.moveZ(rack.h_max,speed)
        pos = rack.getPos(ind)
        bin = rack.bins[ind[0]][ind[1]]
        self.moveXY(pos, speed)
        self.moveZ(rack.h_max -(bin.h+3*160),speed)
        self.z_0 = bin.z_0 - bin.h
        self.pos[2] -= bin.z_0 - bin.h
        self.setPos()
        self.tip = True
        self.tip_type = bin.bin_type
        self.moveZ(rack.h_max,speed)
    
    def remTip(self, rack, speed):
        if not self.tip : return
        if self.pos[2] < rack.h_max:
            self.moveZ(rack.h_max,speed)
        pos = rack.getPos([0,0])
        bin = rack.bins[0][0]
        self.moveXY(pos,speed)
        self.moveZ(pos[2],speed)
        self.moveY(self.pos[1]- bin.d , speed)
        self.pos[2] += self.z_0
        self.setPos()
        self.z_0 = 0
        self.tip = False
        self.moveZ(rack.h_max,speed)
    
    def fill(self,source,source_bin,v, dest, dest_pos, j, i, count, vol_max ,speed,medium,vol_wet):
        vol_max = self.vol_max if vol_max==None else vol_max
        if self.pos[2] < dest.h_max:
            self.moveZ(dest.h_max,speed)
        anzahl = i*j
        v_total = v* anzahl
        v_pip = 0
        for k in range(j):
            for l in range(i):
                v_put = v
                while v_put > 0 :
                    if v_pip == 0:
                        if v < vol_max :
                            v_pip =  int( vol_max / (v/2 if (not v % 2 and v/2 > 0.1* vol_max) else v)) * (v/2 if (not v % 2 and v/2 > 0.1* vol_max) else v)
                        else:
                            v_pip=min(vol_max,v_total)
                            if abs(v_put-v_pip) <= int(0.1 * vol_max) and v_put-v_pip != 0:
                                m= 0 if v_put<v_pip else 1
                                v_pip -= int(0.1* vol_max) *m -(v_put-v_pip)
                        v_pip=min(v_pip,v_total)
                        self.get(source,source_bin,v_pip,count,speed,medium,vol_wet)
                    v_out = int( min ( v_pip,v_put))
                    #print("v_out" , v_out)
                    self.put(dest, dest_pos,v_out,speed,medium)
                    v_pip -=v_out
                    v_total -= v_out
                    v_put -= v_out
                dest_pos[1] += 1
            dest_pos[1] -= i 
            dest_pos[0] += 1
    
    def dilute(self,source, source_name, vol,dest,dest_pos, j,i ,count, speed,speed_pip,vol_wet):
        count = 3 if count==None else count
        self.get(source,source_name,vol, count , speed, speed_pip,vol_wet)
        if self.pos[2] < dest.h_max:
            self.moveZ(dest.h_max,speed)
        for k in range(j):
            for l in range(i):
                self.put(dest,dest_pos,vol,speed, speed_pip)
                self.get(dest,dest_pos,vol,count,speed,speed_pip,vol_wet)
                dest_pos[1] +=1
            if k < j-1:
                dest_pos[1] -= i
                dest_pos[0] += 1
            else:
                dest_pos[1] -=1
                self.put(dest,dest_pos,vol,speed, speed_pip)
    
    def checkLevel(self,rack,bin,speed):
        if type(bin) is str:
            bin = rack.names[bin]
        if self.pos[2] < rack.h_max:
            self.moveZ(rack.h_max,speed)
        pos = rack.getPos(bin,0,0)
        self.moveXY(pos,speed)
        self.moveZ(pos[2],speed)
        time.sleep(3)
        self.moveZ(rack.h_max,speed)
    
    def setPos(self):
        values = {'action' : self.SET_POS,
                  'x' : self.pos[0],
                  'y' : self.pos[1],
                  'z' : self.pos[2],
                  'pip' : self.pos[3]}
        try:
            r = requests.post(self.url, values,timeout=(self.to , 30))
            if r.status_code != 200:
                print ("CMD failed")
            self.pos = list(map(int,r.text.split(";")))
            if self.verbose : print (r.status_code , list(map(int,r.text.split(";"))))
        except requests.exceptions.Timeout:
            assert self.sim == True
            print ("sim Pos" , self.pos)
    
    def checkPos(self,rack, bin, speed , level):
        checklevel= False
        if bin == None :
            pos = rack.getPos([0,0])
        else:
            if level : checklevel = True
            pos = rack.getPos(bin)
        if self.pos[2] < rack.h_max:
            self.moveZ(rack.h_max,speed)
        self.moveXY(pos,speed)
        self.moveZ(rack.h_max,speed )
        if checklevel : self.checkLevel(rack,bin,speed)


def loadWSP (path):
    wsp = pickle.load(open( path+'.p','rb'))
    wsp.rack_list = pickle.load(open( path+'_racks.p','rb'))
    wsp.bin_names = pickle.load(open( path+'_bnames.p','rb'))
    wsp.rack_names = pickle.load(open(path+'_rnames.p','rb'))
    return wsppa


class WorkingSpace:
    pipette = 0
    pep = 0
    url = "empty"
    rack_names = {}
    bin_names = {}
    rack_list = []
    h_max_max = 0
    
    def __init__(self, pipette , peptizer = None):
        self.pipette = pipette
        self.pep = peptizer
        #command_list
        #schnappi_rack = 23 / 32.4
        rob = __import__(__name__)
        s6 = None
        s6 = rob.Rack(23)
        s6.setXY([24700,4700])
        s6.setupRack(32.4 , 4 , 1 , bin_type="schnappi6")
        self.addRack("s6" , s6)
        
        s8 = None
        s8 = rob.Rack(23)
        s8.setXY([5184,4000])
        s8.setupRack(32.4 , 4 , 1 , bin_type="schnappi8")
        self.addRack("s8" , s8)
        
        s120 = None
        s120= rob.Rack(23)
        s120.setXY([1,4000])
        s120.setupRack(32.4 , 4 , 1 , bin_type="schnappi12")
        self.addRack("s120" , s120)
        
        s121 = None
        s121= rob.Rack(23)
        s121.setXY([29700,4700])
        s121.setupRack(32.4 , 4 , 1 , bin_type="schnappi12")
        self.addRack("s121" , s121)
        
        s25 = None
        s25 = rob.Rack(23)
        s25.setXY([38200,12500])
        s25.setupRack(32.4 , 2 , 2 , bin_type="schnappi25")
        self.addRack("s25" , s25)
        
        #eppi_rack= 63 / 21 
        eppi15 = None
        eppi15 = rob.Rack(63)
        eppi15.setXY([1,26000])
        eppi15.setupRack(21 , 1 , 10, bin_type="eppi15")
        self.addRack("eppi15" , eppi15)
        
        #eppi_rack= 63 / 21 
        eppi20 = None
        eppi20 = rob.Rack(63)
        eppi20.setXY([1,29500])
        eppi20.setupRack(21 , 1, 10 , bin_type="eppi15")
        self.addRack("eppi20" , eppi20)
        
        #well_plate= 27.9 / 9 
        wp96 = None
        wp96 = rob.Rack(27.9)
        wp96.setXY([9700,4500])
        wp96.setupRack(9, 12 , 8 , bin_type="wp96")
        self.addRack("wp96" , wp96)
        
        #deepwell_plate= 27.9 / 9 
        wp96deep = None
        wp96deep = rob.Rack(27.9)
        wp96deep.setXY([9700,4500])
        wp96deep.setupRack(9, 12 , 8 , bin_type="wp96deep")
        self.addRack("wp96deep" , wp96deep)
        
        #aponorm 100 = 10 / 0
        apo1= None
        apo1= rob.Rack(18.625)
        apo1.setXY([42100,50100])
        apo1.setupRack( 0 , 1,1 , bin_type="apo100")
        self.addRack("apo1" , apo1)
        
        apo2= None
        apo2= rob.Rack(18.625)
        apo2.setXY([41600,39300])
        apo2.setupRack( 0 , 1,1 , bin_type="apo100")
        self.addRack("apo2" , apo2)
        
        apo3= None
        apo3= rob.Rack(18.625)
        apo3.setXY([30900,50100])
        apo3.setupRack( 0 , 1,1 , bin_type="apo100")
        self.addRack("apo3" , apo3)
        
        #syringe2
        syr2= None
        syr2= rob.Rack(52)
        syr2.setXY([42000,64200])
        syr2.setupRack( 0 , 1,1 , bin_type="syringe10")
        self.addRack("syr2" , syr2)
        
        #tip  = 87.5 / 
        tip = None
        tip = rob.Rack(87.5)
        tip.setXY([35900, 23000])
        tip.setupRack( 10.5 , 6 , 6, bin_type="tip200")
        self.addRack("tip" , tip)
        
        #tip_bin  72.1875
        tipbin = None
        tipbin = rob.Rack(72.1875)
        tipbin.setXY([41150,3000])
        tipbin.setupRack(0 ,1,1,bin_type="tipbin")
        self.addRack("tipbin" , tipbin)
        # 1100  , höhe 3700 
    
    def init(self, speed_x = None , speed_y = None , speed_z = None ):
        self.pipette.init(speed_x= speed_x,speed_y=speed_y, speed_z=speed_z )
    
    def reset(self):
        self.pipette.reset(self.h_max_max)
    
    def addRack(self,rack_name , rack):
        self.rack_list.append(rack)
        self.rack_names[rack_name] = len(self.rack_list)-1
        if rack.h_max > self.h_max_max : self.h_max_max = rack.h_max
    
    def rack(self,rack_name):
        return self.rack_list[self.rack_names[rack_name]]
    
    def checkPos(self,rack_str = None, speed = None, level = None , bin = None , index = None):
        if rack_str == None :
            for d in self.rack_names:
                self.pipette.checkPos(self.rack_list[self.rack_names[d]],bin, speed,level)
                time.sleep(2)
        elif  rack_str in self.rack_names:
            self.pipette.checkPos(self.rack_list[self.rack_names[rack_str]],bin,speed,level)
        else :
            ind = 0 if index == None else index
            rack = self.rack(self.bin_names[rack_str][ind][0])
            j = self.bin_names[rack_str][ind][1]
            i = self.bin_names[rack_str][ind][2]
            self.pipette.checkPos(rack, [j,i],speed,level)
    
    def setBinName(self, name_str, rack_spec):
        self.bin_names[name_str] = rack_spec
    
    def delBinName(self , name = None):
        if name == None :
            for n in self.bin_names:
                self.bin_names.pop(n , None)
        else:
            self.bin_names.pop(name, None)
    
    def fill(self, source_str , v ,  dest_str , j , i , dil=None , NtoN= None , count = None,vol_wet=None ,speed = None , vol_max= None,  medium = None):
        source = self.getVolBin(source_str , -1*v)
        dest = self.getVolBin(dest_str , v)
        medium = "Water" if medium == None else medium
        vol_max =  self.pipette.vol_max  if vol_max == None else vol_max
        vol_wet =  min(v, vol_max) if vol_wet == None else vol_wet
        if NtoN != None :
            start_i = 0
            end_i = i
            step_i = 1
            start_j = 0
            end_j = j
            step_j = 1
            if i < 0:
                start_i = -i-1
                end_i = 0-1
                step_i = -1
            if j < 0:
                start_j= -j-1
                end_j = 0-1
                step_j = -1
            for k in range(start_j,end_j,step_j):
                for l in range(start_i,end_i,step_i):
                    self.pipette.fill(source[0],[source[1]+k,source[2]+l],v,dest[0],[dest[1]+k,dest[2]+l], 1,1, count,vol_max,speed,medium,vol_wet)
        elif dil !=None:
            self.pipette.dilute(source[0],[source[1],source[2]],v,dest[0],[dest[1],dest[2]], j,i, count,speed,medium,vol_wet)
        else:
            self.pipette.fill(source[0],[source[1],source[2]],v,dest[0],[dest[1],dest[2]], j,i,count,vol_max,speed,medium,vol_wet)
    
    def setVol(self, name_str , v , index = None ,  check=None , speed = None):
        ind = 0 if index == None else index
        ret = ""
        while v== None or v>=0 :
            assert ( ind < len(self.bin_names[name_str]))
            bin = self.bin_names[name_str][ind]
            ra = self.rack(bin[0])
            v = ra.bins[bin[1]][bin[2]].vol if v == None else v
            v_max = ra.bins[bin[1]][bin[2]].v_max
            if v > v_max : 
                v_fill =  v_max
                v -= v_fill
            else : 
                v_fill = v
                v = -1
            ret += name_str +" ("+ str(ind) + "): " + str(ra.setVol([bin[1],bin[2]] , v_fill)) + " 10-6 l\n"
            if check : self.pipette.checkLevel(ra,[bin[1],bin[2]],speed )            
            ind +=1
        return print(ret)
    
    def getTip(self,tipbin , tip , j , i , speed = None):
        self.pipette.remTip(self.rack_list[self.rack_names[tipbin]] , speed)
        self.pipette.getTip(self.rack_list[self.rack_names[tip]] , [j,i],speed)
    
    def save (self, path ):
        pickle.dump(self, open( path + ".p" , "wb"))
        pickle.dump(self.rack_names , open(path +"_rnames.p" , "wb"))
        pickle.dump(self.bin_names , open(path+"_bnames.p" , "wb"))
        pickle.dump(self.rack_list , open(path+"_racks.p" , "wb"))
        
    def getVolBin (self, bin_str , v ):
        ind = 0
        length = len(self.bin_names[bin_str])
        while True :
            rack = self.rack(self.bin_names[bin_str][ind][0])
            j = self.bin_names[bin_str][ind][1]
            i = self.bin_names[bin_str][ind][2]
            v_bin = rack.bins[j][i].vol
            v_safe = rack.bins[j][i].v_safe
            v_max = rack.bins[j][i].v_max
            #print ( ind , v_bin , v , v_safe , v_max )
            if (v > 0 and v_bin + v <= v_max ) or (v < 0 and v_bin + v >= v_safe) :
                return [rack , j , i ]
            ind += 1
            assert ( ind- 1 <= length)
    
    def checkVol(self, bin=None , index = None , check = None , speed = None):
        if bin == None :
            for n in self.bin_names:
                if index == None :
                    for k in range(len(self.bin_names[n]) ):
                        self.setVol(n, None ,index = k ,  check = check , speed = speed )
                else:  self.setVol( n, None ,index = index ,  check = check , speed = speed )
                
        else:
            if index == None :
                for l in range(len(self.bin_names[bin]) ):
                    self.setVol(bin, None , index = l , check = check, speed = speed)
            else: self.setVol(bin, None ,index = index ,  check = check , speed = speed )
        
    

def loadWSP (path):
    wsp = pickle.load(open( path+'.p','rb'))
    wsp.rack_list = pickle.load(open( path+'_racks.p','rb'))
    wsp.bin_names = pickle.load(open( path+'_bnames.p','rb'))
    wsp.rack_names = pickle.load(open(path+'_rnames.p','rb'))
    return wsp

"""
ap = rob.WorkingSpace( rob.Pipette(63,"http://10.0.3.1" ,"P200", tip="tip200" , calib=42.96 ,verbose = True))

rob.assay(ap , wp96 ,0 ,speed_x = 120 , speed_y = 120 , speed_z = 120)

"""



