from __future__ import print_function
import matplotlib.pyplot as plt
from os import system, getcwd, chdir,listdir,environ,makedirs
from os.path import isfile,exists,isdir
from .reax_data import get_data 
from .link import links
from .reaxfflib import write_lib
from .reax import ReaxFF,taper
from .initCheck import Init_Check
from .dingtalk import send_msg
import time
from ase import Atoms
from ase.io.trajectory import Trajectory
import tensorflow as tf
# from tensorflow.contrib.opt import ScipyOptimizerInterface
import numpy as np
import random
import pickle
import json as js
# tf_upgrade_v2 --infile reax.py --outfile reax_v1.py
# tf.compat.v1.disable_v2_behavior()
tf.compat.v1.disable_eager_execution()



class MPNN(ReaxFF):
  def __init__(self,libfile='ffield',direcs={},
               dft='ase',atoms=None,
               cons=['val','vale','rosi','ropi','ropp', # 'ovun3', # 'val8','val9','val10',
                     'bo1','bo2','bo3','bo4','bo5','bo6','Depi','Depp','lp3'], # 'hbtol'
               optmol=True,mefac=0.1,
               opt=None,optword='nocoul',
               nanv={'boc1':-2.0},
               batch_size=200,sample='uniform',
               hbshort=6.75,hblong=7.5,
               vdwcut=10.0,
               rcut=None,rcuta=None,re=None,
               bore={'C-C':0.5,'others':0.45},
               bom={'others':1.05},
               weight={'others':1.0},
               ro_scale=0.1,
               clip_op=True,
               InitCheck=True,
               nn=True,
               messages=1,
               TwoBodyOnly=False,
               mpopt=None,
               bo_layer=[2,1],
               bf_layer=[6,1],
               be_layer=[6,1],
               vdw_layer=[4,1],
               vdwnn=False,
               EnergyFunction=3,
               MessageFunction=1,
               spec=[],
               sort=False,
               pkl=False,
               spv_bm=False,
               spv_be=False,
               bo_penalty=100000.0,
               optMethod='ADAM',
               maxstep=60000,
               emse=0.9,
               convergence=0.97,
               lossConvergence=1000.0,
               losFunc='n2',
               conf_vale=None,
               huber_d=30.0,
               ncpu=None):
      '''
         Massage Passing Neural network build top on ReaxFF potentail
         version 3.0 
           Time: 2018-10-20
           Intelligence ReaxFF Neual Network: Evoluting the Force Field parameters on-the-fly
           2017-11-01
      '''
      self.messages         = messages
      self.EnergyFunction   = EnergyFunction
      self.MessageFunction  = MessageFunction
      self.bom              = bom
      self.spv_be           = spv_be
      self.spv_bm           = spv_bm
      self.TwoBodyOnly      = TwoBodyOnly
      # self.bo_layer       = bo_layer
      self.bf_layer         = bf_layer
      self.be_layer         = be_layer
      self.vdw_layer        = vdw_layer
      self.vdwnn            = vdwnn
      if mpopt is None:
         self.mpopt = [True for i in range(messages+3)]
      else:
         self.mpopt = mpopt

      ReaxFF.__init__(self,libfile=libfile,direcs=direcs,
                      dft=dft,atoms=atoms,cons=cons,opt=opt,optword=optword,
                      optmol=optmol,mefac=mefac,
                      nanv=nanv,batch_size=batch_size,sample=sample,
                      hbshort=hbshort,hblong=hblong,vdwcut=vdwcut,
                      rcut=rcut,rcuta=rcuta,re=re,ro_scale=ro_scale,
                      clip_op=clip_op,InitCheck=InitCheck,nn=nn,
                      bo_layer=bo_layer,spec=spec,sort=sort,pkl=pkl,weight=weight,
                      bore=bore,bo_penalty=bo_penalty,
                      optMethod=optMethod,maxstep=maxstep,
                      emse=emse,convergence=convergence,lossConvergence=lossConvergence,
                      losFunc=losFunc,conf_vale=conf_vale,
                      huber_d=huber_d,ncpu=ncpu)
      self.H        = []    # hiden states (or embeding states)
      self.D        = []    # degree matrix
      self.Hsi      = []
      self.Hpi      = []
      self.Hpp      = []
      self.esi      = {}
      self.fbo      = {}

  def supervise(self):
      ''' supervised learning term'''
      l_atol = 0.0
      self.diffa,self.diffb,self.diffe = {},{},{}
      for bd in self.bonds: 
          [atomi,atomj] = bd.split('-') 
          if self.nbd[bd]>0:
             if bd in self.bore:
                bore_ = self.bore[bd]
             else:
                bore_ = self.bore['others']

             if bd in self.bom:
                bm_ = self.bom[bd]
             else:
                bm_ = self.bom['others']
             
             if not self.TwoBodyOnly:
                fao = tf.where(tf.greater(self.rbd[bd],self.rcuta[bd]),1.0,0.0)      ##### r> rcuta that bo = 0.0
                self.diffa[bd]  = tf.reduce_sum(input_tensor=tf.nn.relu(self.bo0[bd]*fao-self.atol))
                l_atol = tf.add(self.diffa[bd],l_atol)

             if self.spv_bm:
                fao_= tf.where(tf.less_equal(self.rbd[bd],bm_*self.re[bd]),1.0,0.0) ##### r< 1.2*re that bo > botol
                self.diffa[bd] = tf.reduce_sum(input_tensor=tf.nn.relu(self.botol-self.bo0[bd])*fao_)
                l_atol = tf.add(self.diffa[bd],l_atol)

             #  bop should be zero if r>rcut
             fbo = tf.where(tf.less_equal(self.rbd[bd],self.rc_bo[bd]),0.0,1.0) ##### r> rc_bo that bo < botol
             self.diffb[bd]  = tf.reduce_sum(self.bop[bd]*fbo)
             l_atol  = tf.add(self.diffb[bd],l_atol)
             
             if self.spv_be:
                fe  = tf.where(tf.less_equal(self.rbd[bd],self.re[bd]),1.0,0.0) ##### r< re that bo > bore_
                self.diffe[bd]  = tf.reduce_sum(input_tensor=tf.nn.relu((bore_-self.bo0[bd])*fe))
                l_atol  = tf.add(self.diffe[bd],l_atol)
                l_atol= tf.add(tf.nn.relu(self.rc_bo[bd]-self.rcut[bd]),l_atol)
      return l_atol*self.bo_penalty

  def get_loss(self):
      self.Loss = 0.0
      for mol in self.mols:
          mol_ = mol.split('-')[0]
          if mol in self.weight:
             w_ = self.weight[mol]
          elif mol_ in self.weight:
             w_ = self.weight[mol_]
          else:
             w_ = self.weight['others']
          # print(mol,w_)

          if self.losFunc   == 'n2':
             self.loss[mol] = tf.nn.l2_loss(self.E[mol]-self.dft_energy[mol],
                                 name='loss_%s' %mol)
          elif self.losFunc == 'abs':
             self.loss[mol] = tf.compat.v1.losses.absolute_difference(self.dft_energy[mol],self.E[mol])
          elif self.losFunc == 'mse':
             self.loss[mol] = tf.compat.v1.losses.mean_squared_error(self.dft_energy[mol],self.E[mol])
          elif self.losFunc == 'huber':
             self.loss[mol] = tf.compat.v1.losses.huber_loss(self.dft_energy[mol],self.E[mol],delta=self.huber_d)

          sum_edft = tf.reduce_sum(input_tensor=tf.abs(self.dft_energy[mol]-self.max_e[mol]))
          self.accur[mol] = 1.0 - tf.reduce_sum(input_tensor=tf.abs(self.E[mol]-self.dft_energy[mol]))/(sum_edft+0.00000001)
         
          self.Loss     += self.loss[mol]*w_
          self.accuracy += self.accur[mol]

      self.ME   = 0.0
      for mol in self.mols:
          mols = mol.split('-')[0] 
          self.ME += tf.square(self.MolEnergy[mols])

      self.loss_atol = self.supervise()

      self.Loss     += self.loss_atol
      if self.optmol:
         self.Loss  += self.ME*self.mefac
      self.accuracy  = self.accuracy/self.nmol

  def build_graph(self):
      print('-  building graph ...')
      self.accuracy   = tf.constant(0.0,name='accuracy')
      self.accuracies = {}
      self.get_bond_energy()

      if self.TwoBodyOnly:
         self.get_atomic_energy()
      else:
         self.get_atom_energy()
         self.get_angle_energy()
         self.get_torsion_energy()

      self.get_vdw_energy()
      self.get_hb_energy()
      self.get_total_energy()
      self.get_loss()
      print('-  end of build.')

  def get_atomic_energy(self):
      i = 0
      for sp in self.spec:
          if self.nsp[sp]==0:
             continue
          self.eatom[sp] = -tf.ones([self.nsp[sp]])*self.p['atomic_'+sp]
          self.EATOM  = self.eatom[sp] if i==0 else tf.concat((self.EATOM,self.eatom[sp]),0)
          i += 1

      for mol in self.mols:
          mols = mol.split('-')[0] 
          zpe_ = tf.gather_nd(self.EATOM,self.atomlink[mol]) 
          self.zpe[mol] = tf.reduce_sum(input_tensor=zpe_,name='zpe') + self.MolEnergy[mols]

  def get_total_energy(self):
      for mol in self.mols:
          # mols = mol.split('-')[0] 
          if self.TwoBodyOnly:
             self.E[mol] = tf.add(self.ebond[mol] + 
                                  self.evdw[mol]  +
                                  self.ecoul[mol] +
                                  self.ehb[mol]   +
                                  self.eself[mol], 
                                  self.zpe[mol],name='E_%s' %mol)   
          else:
             self.E[mol] = tf.add(self.ebond[mol] + 
                                  self.eover[mol] +
                                  self.eunder[mol]+
                                  self.elone[mol] +
                                  self.eang[mol]  +
                                  self.epen[mol]  +
                                  self.tconj[mol] +
                                  self.etor[mol]  +
                                  self.efcon[mol] +
                                  self.evdw[mol]  +
                                  self.ecoul[mol] +
                                  self.ehb[mol]   +
                                  self.eself[mol], 
                                  self.zpe[mol],name='E_%s' %mol)  

  def f_nn(self,pre,bd,nbd,x,layer=5):
      ''' Dimention: (nbatch,4) input = 4
                 Wi:  (4,8) 
                 Wh:  (8,8)
                 Wo:  (8,1)  output = 1
      '''
      nd = len(x)
      x_ = []
      for d in x:
          x_.append(tf.reshape(d,[nbd*self.batch]))
      X   = tf.stack(x_,axis=1)        # Dimention: (nbatch,4)
                                       #        Wi:  (4,8) 
      o   =  []                        #        Wh:  (8,8)
      o.append(tf.sigmoid(tf.matmul(X,self.m[pre+'wi_'+bd],name='bop_input')+self.m[pre+'bi_'+bd]))   # input layer

      for l in range(layer):                                                   # hidden layer      
          o.append(tf.sigmoid(tf.matmul(o[-1],self.m[pre+'w_'+bd][l],name='bop_hide')+self.m[pre+'b_'+bd][l]))

      o_ = tf.sigmoid(tf.matmul(o[-1],self.m[pre+'wo_'+bd],name='bop_output') + self.m[pre+'bo_'+bd])  # output layer
      out= tf.reshape(o_,[nbd,self.batch])
      return out

  def get_tap(self,r,bd):
      if self.vdwnn:
         tp = self.f_nn('fv',bd,self.nvb[bd],[r],layer=self.vdw_layer[1])
      else:
         tp = 1.0+tf.math.divide(-35.0,tf.pow(self.vdwcut,4.0))*tf.pow(r,4.0)+ \
              tf.math.divide(84.0,tf.pow(self.vdwcut,5.0))*tf.pow(r,5.0)+ \
              tf.math.divide(-70.0,tf.pow(self.vdwcut,6.0))*tf.pow(r,6.0)+ \
              tf.math.divide(20.0,tf.pow(self.vdwcut,7.0))*tf.pow(r,7.0)
      return tp

  def fmassage(self,pre,bd,nbd,x,layer=5):
      ''' Dimention: (nbatch,4) input = 4
                 Wi:  (4,8) 
                 Wh:  (8,8)
                 Wo:  (8,3)  output = 3
      '''
      nd = len(x)
      x_ = []
      for d in x:
          x_.append(tf.reshape(d,[nbd*self.batch]))
      X   = tf.stack(x_,axis=1)        # Dimention: (nbatch,4)
                                       #        Wi:  (4,8) 
      o   =  []                        #        Wh:  (8,8)
      o.append(tf.sigmoid(tf.matmul(X,self.m[pre+'wi_'+bd],name='bop_input')+self.m[pre+'bi_'+bd]))   # input layer

      for l in range(layer):                                                   # hidden layer      
          o.append(tf.sigmoid(tf.matmul(o[-1],self.m[pre+'w_'+bd][l],name='bop_hide')+self.m[pre+'b_'+bd][l]))

      o_ = tf.sigmoid(tf.matmul(o[-1],self.m[pre+'wo_'+bd],name='bop_output') + self.m[pre+'bo_'+bd])  # output layer
      out= tf.reshape(o_,[nbd,self.batch,3])
      return out

  def get_bondorder_uc(self,bd):
      self.frc[bd] = tf.where(tf.logical_or(tf.greater(self.rbd[bd],self.rc_bo[bd]),
                                            tf.less_equal(self.rbd[bd],0.001)),
                              tf.zeros_like(self.rbd[bd]),tf.ones_like(self.rbd[bd]))

      self.bodiv1[bd] = tf.math.divide(self.rbd[bd],self.p['rosi_'+bd],name='bodiv1_'+bd)
      self.bopow1[bd] = tf.pow(self.bodiv1[bd],self.p['bo2_'+bd])
      self.eterm1[bd] = (1.0+self.botol)*tf.exp(tf.multiply(self.p['bo1_'+bd],self.bopow1[bd]))*self.frc[bd] # consist with GULP

      self.bodiv2[bd] = tf.math.divide(self.rbd[bd],self.p['ropi_'+bd],name='bodiv2_'+bd)
      self.bopow2[bd] = tf.pow(self.bodiv2[bd],self.p['bo4_'+bd])
      self.eterm2[bd] = tf.exp(tf.multiply(self.p['bo3_'+bd],self.bopow2[bd]))*self.frc[bd]

      self.bodiv3[bd] = tf.math.divide(self.rbd[bd],self.p['ropp_'+bd],name='bodiv3_'+bd)
      self.bopow3[bd] = tf.pow(self.bodiv3[bd],self.p['bo6_'+bd])
      self.eterm3[bd] = tf.exp(tf.multiply(self.p['bo5_'+bd],self.bopow3[bd]))*self.frc[bd]

      fsi_            = self.f_nn('fsi',bd, self.nbd[bd],[self.eterm1[bd]],layer=self.bo_layer[1])  
      fpi_            = self.f_nn('fpi',bd, self.nbd[bd],[self.eterm2[bd]],layer=self.bo_layer[1])  
      fpp_            = self.f_nn('fpp',bd, self.nbd[bd],[self.eterm3[bd]],layer=self.bo_layer[1]) 

      self.bop_si[bd] = fsi_ #*self.frc[bd] #*self.eterm1[bd]  
      self.bop_pi[bd] = fpi_ #*self.frc[bd] #*self.eterm2[bd]
      self.bop_pp[bd] = fpp_ #*self.frc[bd] #*self.eterm3[bd]
      self.bop[bd]    = tf.add(self.bop_si[bd],self.bop_pi[bd]+self.bop_pp[bd],name='BOp_'+bd)

  def get_bondorder(self,t,bd,atomi,atomj):
      Di      = tf.gather_nd(self.D[t-1],self.dilink[bd])
      Dj      = tf.gather_nd(self.D[t-1],self.djlink[bd])
      h       = self.H[t-1][bd]
      Dbi     = Di-h
      Dbj     = Dj-h

      b       = bd.split('-')
      bdr     = b[1]+'-'+b[0]
      flabel  = 'f'+str(t)
      if self.MessageFunction==1:
         Fi      = self.f_nn(flabel,bd, self.nbd[bd],[Dbi,Dbj,h],layer=self.bf_layer[1])
         Fj      = self.f_nn(flabel,bdr,self.nbd[bd],[Dbj,Dbi,h],layer=self.bf_layer[1])
         F       = 2.0*Fi*Fj
       
         bosi    = self.Hsi[t-1][bd]*F
         bopi    = self.Hpi[t-1][bd]*F
         bopp    = self.Hpp[t-1][bd]*F
      elif self.MessageFunction==2:
         Fi      = self.fmassage(flabel,bd, self.nbd[bd],[Dbi,Dbj,h],layer=self.bf_layer[1])
         Fj      = self.fmassage(flabel,bdr,self.nbd[bd],[Dbj,Dbi,h],layer=self.bf_layer[1])
         F       = 2.0*Fi*Fj
         Fsi,Fpi,Fpp = tf.unstack(F,axis=2)
       
         bosi    = self.Hsi[t-1][bd]*Fsi
         bopi    = self.Hpi[t-1][bd]*Fpi
         bopp    = self.Hpp[t-1][bd]*Fpp
      bo      = bosi+bopi+bopp
      return bo,bosi,bopi,bopp

  def get_bond_energy(self):
      BO = tf.zeros([1,self.batch])   # for ghost atom, the value is zero
      for bd in self.bonds:
          if self.nbd[bd]>0:
             self.get_bondorder_uc(bd)
             BO = tf.concat([BO,self.bop[bd]],0)
  
      D           = tf.gather_nd(BO,self.dlist)  
      self.Deltap = tf.reduce_sum(input_tensor=D,axis=1,name='Deltap')

      self.massage_passing()
      self.get_final_sate()

      i = 0                           # get bond energy
      for bd in self.bonds: 
          [atomi,atomj] = bd.split('-') 
          if self.nbd[bd]>0:
             [atomi,atomj] = bd.split('-') 
             self.get_ebond(bd)
             EBDA = self.EBD[bd] if i==0 else tf.concat((EBDA,self.EBD[bd]),0)
             i += 1

      for mol in self.mols:
          self.ebda[mol] = tf.gather_nd(EBDA,self.bdlink[mol])  
          self.ebond[mol]= tf.reduce_sum(input_tensor=self.ebda[mol],axis=0,name='bondenergy')

  def massage_passing(self):
      ''' finding the final Bond－order with a massage passing '''
      self.H.append(self.bop)                   # 
      self.Hsi.append(self.bop_si)              #
      self.Hpi.append(self.bop_pi)              #
      self.Hpp.append(self.bop_pp)              # 
      self.D.append(self.Deltap)                # get the initial hidden state H[0]

      for t in range(1,self.messages+1):
          print('-  message passing for t=%d ...' %t)
          self.H.append({})                     # get the hidden state H[t]
          self.Hsi.append({})                   #
          self.Hpi.append({})                   #
          self.Hpp.append({})                   #             

          BO = tf.zeros([1,self.batch])         # for ghost atom, the value is zero
          for bd in self.bonds:
              if self.nbd[bd]>0:
                 [atomi,atomj] = bd.split('-') 
                 bo,bosi,bopi,bopp = self.get_bondorder(t,bd,atomi,atomj)

                 self.H[t][bd]   = bo
                 self.Hsi[t][bd] = bosi
                 self.Hpi[t][bd] = bopi
                 self.Hpp[t][bd] = bopp

                 BO = tf.concat([BO,bo],0)
      
          D      = tf.gather_nd(BO,self.dlist)  
          Delta  = tf.reduce_sum(input_tensor=D,axis=1)
          self.D.append(Delta)                  # degree matrix

  def get_final_sate(self):     
      self.Delta  = self.D[-1]
      self.bo0    = self.H[-1]                  # fetch the final state 
      self.bosi   = self.Hsi[-1]
      self.bopi   = self.Hpi[-1]
      self.bopp   = self.Hpp[-1]

      self.BO0    = tf.zeros([1,self.batch])    # for ghost atom, the value is zero
      self.BO     = tf.zeros([1,self.batch])
      self.BOPI   = tf.zeros([1,self.batch])
      self.BSO    = tf.zeros([1,self.batch])
      BPI         = tf.zeros([1,self.batch])

      for bd in self.bonds:
          if self.nbd[bd]>0:
             # self.fbo[bd]  = taper(self.bo0[bd],rmin=self.botol,rmax=2.0*self.botol)
             self.bo[bd]   = tf.nn.relu(self.bo0[bd] - self.atol)
             self.bso[bd]  = self.p['ovun1_'+bd]*self.p['Desi_'+bd]*self.bo0[bd] 

             self.BO0 = tf.concat([self.BO0,self.bo0[bd]],0)
             self.BO  = tf.concat([self.BO,self.bo[bd]],0)
             self.BSO = tf.concat([self.BSO,self.bso[bd]],0)
             BPI      = tf.concat([BPI,self.bopi[bd]+self.bopp[bd]],0)
             self.BOPI= tf.concat([self.BOPI,self.bopi[bd]],0)

      D_  = tf.gather_nd(self.BO0,self.dlist,name='D_') 
      SO_ = tf.gather_nd(self.BSO,self.dlist,name='SO_') 
      self.BPI = tf.gather_nd(BPI,self.dlist,name='BPI') 

      self.Delta  = tf.reduce_sum(input_tensor=D_,axis=1,name='Delta')  # without valence i.e. - Val 
      self.SO     = tf.reduce_sum(input_tensor=SO_,axis=1,name='sumover')  
      self.FBOT   = taper(self.BO0,rmin=self.atol,rmax=2.0*self.atol) 
      self.FHB    = taper(self.BO0,rmin=self.hbtol,rmax=2.0*self.hbtol) 

  def get_ebond(self,bd):
      Di      = tf.gather_nd(self.Delta,self.dilink[bd])
      Dj      = tf.gather_nd(self.Delta,self.djlink[bd])

      Dbi     = Di-self.bo0[bd]
      Dbj     = Dj-self.bo0[bd]

      b       = bd.split('-')
      bdr     = b[1]+'-'+b[0]

      if self.EnergyFunction==3:
         self.esi[bd] = self.f_nn('fe',bd, self.nbd[bd],[self.bosi[bd],self.bopi[bd],self.bopp[bd]],
                                  layer=self.be_layer[1])
         self.EBD[bd]  = -self.p['Desi_'+bd]*self.esi[bd]*self.bo0[bd]
      elif self.EnergyFunction==1:
         Fsi  = self.f_nn('fesi',bd, self.nbd[bd],[self.bosi[bd]],layer=self.be_layer[1])  
         Fpi  = self.f_nn('fepi',bd, self.nbd[bd],[self.bopi[bd]],layer=self.be_layer[1])  
         Fpp  = self.f_nn('fepp',bd, self.nbd[bd],[self.bopp[bd]],layer=self.be_layer[1])  
         #   self.esi[bd]  = self.bosi[bd]*F       
         self.sieng[bd]= self.p['Desi_'+bd]*Fsi*self.bosi[bd]
         self.pieng[bd]= self.p['Desi_'+bd]*Fpi*self.bopi[bd]
         self.ppeng[bd]= self.p['Desi_'+bd]*Fpp*self.bopp[bd]
         self.EBD[bd]  = - self.sieng[bd] - self.pieng[bd] - self.ppeng[bd]
      elif self.EnergyFunction==2:
         Fi = self.f_nn('fe',bd, self.nbd[bd],[Dbi,Dbj,self.bosi[bd]],layer=self.be_layer[1])
         Fj = self.f_nn('fe',bdr,self.nbd[bd],[Dbj,Dbi,self.bosi[bd]],layer=self.be_layer[1])
         F  = 2.0*Fi*Fj
    
         self.esi[bd]  = self.bosi[bd]*F       
         self.sieng[bd]= tf.multiply(self.p['Desi_'+bd],self.esi[bd])
         self.pieng[bd]= tf.multiply(self.p['Depi_'+bd],self.bopi[bd])
         self.ppeng[bd]= tf.multiply(self.p['Depp_'+bd],self.bopp[bd]) 

         self.EBD[bd]  = - self.sieng[bd] - self.pieng[bd] - self.ppeng[bd] 
          
  def set_m(self):
      ''' set variable for neural networks '''
      self.m = {}
      bond   = []
      for si in self.spec:
          for sj in self.spec:
              bd = si + '-' + sj
              if bd not in bond:
                 bond.append(bd)

      reuse_m = True if self.bo_layer==self.bo_layer_ else False
      self.set_wb(pref='fsi',reuse_m=reuse_m,nin=1,nout=1,layer=self.bo_layer,
                  vlist=self.bonds,nnopt=self.mpopt[0],bias=2.0)
      self.set_wb(pref='fpi',reuse_m=reuse_m,nin=1,nout=1,layer=self.bo_layer,
                  vlist=self.bonds,nnopt=self.mpopt[0],bias=2.0)
      self.set_wb(pref='fpp',reuse_m=reuse_m,nin=1,nout=1,layer=self.bo_layer,
                  vlist=self.bonds,nnopt=self.mpopt[0],bias=2.0)
 
      reuse_m = True if self.bf_layer==self.bf_layer_ else False
      for t in range(1,self.messages+1):
          b = 0.881373587 if t>1 else -0.867
          nout_ = 1 if self.MessageFunction==1 else 3
          self.set_wb(pref='f'+str(t),reuse_m=reuse_m,nin=3,nout=nout_,layer=self.bf_layer,
                      vlist=bond,nnopt=self.mpopt[t],bias=b)

      if self.EnergyFunction==self.EnergyFunction_ and self.be_layer==self.be_layer_:
         reuse_m = True  
      else:
         reuse_m = False 

      if self.EnergyFunction==1:
         self.set_wb(pref='fesi',reuse_m=reuse_m,nin=1,nout=1,layer=self.be_layer,
                     vlist=self.bonds,nnopt=self.mpopt[-2],bias=2.0)
         self.set_wb(pref='fepi',reuse_m=reuse_m,nin=1,nout=1,layer=self.be_layer,
                     vlist=self.bonds,nnopt=self.mpopt[-2],bias=2.0)
         self.set_wb(pref='fepp',reuse_m=reuse_m,nin=1,nout=1,layer=self.be_layer,
                     vlist=self.bonds,nnopt=self.mpopt[-2],bias=2.0)
      elif self.EnergyFunction>=2:
         self.set_wb(pref='fe',reuse_m=reuse_m,nin=3,nout=1,layer=self.be_layer,
                     vlist=self.bonds,nnopt=self.mpopt[-2],bias=2.0)

      if self.vdwnn:
         reuse_m = True if self.vdw_layer==self.vdw_layer_ else False
         self.set_wb(pref='fv',reuse_m=reuse_m,nin=1,nout=1,layer=self.vdw_layer,
                     vlist=self.bonds,nnopt=self.mpopt[-1],bias=-0.867)

  def set_wb(self,pref='f',reuse_m=True,nnopt=True,nin=8,nout=3,layer=[8,9],vlist=None,bias=0.0):
      ''' set matix varibles '''
      if self.m_ is None:
         self.m_ = {}
      for bd in vlist:
          if pref+'wi_'+bd in self.m_ and reuse_m:                   # input layer
              if nnopt:
                 # print(self.m_['fwi_'+bd])
                 self.m[pref+'wi_'+bd] = tf.Variable(self.m_[pref+'wi_'+bd],name=pref+'wi_'+bd)
                 self.m[pref+'bi_'+bd] = tf.Variable(self.m_[pref+'bi_'+bd],name=pref+'bi_'+bd)
              else:
                 self.m[pref+'wi_'+bd] = tf.constant(self.m_[pref+'wi_'+bd],name=pref+'wi_'+bd)
                 self.m[pref+'bi_'+bd] = tf.constant(self.m_[pref+'bi_'+bd],name=pref+'bi_'+bd)
          else:
              self.m[pref+'wi_'+bd] = tf.Variable(tf.random.normal([nin,layer[0]],stddev=0.1),name=pref+'wi_'+bd)   
              self.m[pref+'bi_'+bd] = tf.Variable(tf.random.normal([layer[0]],stddev=0.1),
                                                  name=pref+'bi_'+bd)  

          self.m[pref+'w_'+bd] = []                                    # hidden layer
          self.m[pref+'b_'+bd] = []
          if pref+'w_'+bd in self.m_ and reuse_m:     
              if nnopt:                            
                 for i in range(layer[1]):   
                     self.m[pref+'w_'+bd].append(tf.Variable(self.m_[pref+'w_'+bd][i],name=pref+'wh'+str(i)+'_'+bd )) 
                     self.m[pref+'b_'+bd].append(tf.Variable(self.m_[pref+'b_'+bd][i],name=pref+'bh'+str(i)+'_'+bd )) 
              else:
                 for i in range(layer[1]):   
                     self.m[pref+'w_'+bd].append(tf.constant(self.m_[pref+'w_'+bd][i],name=pref+'wh'+str(i)+'_'+bd )) 
                     self.m[pref+'b_'+bd].append(tf.constant(self.m_[pref+'b_'+bd][i],name=pref+'bh'+str(i)+'_'+bd )) 
          else:
              for i in range(layer[1]):   
                  self.m[pref+'w_'+bd].append(tf.Variable(tf.random.normal([layer[0],layer[0]], 
                                                           stddev=0.1),name=pref+'wh'+str(i)+'_'+bd)) 
                  self.m[pref+'b_'+bd].append(tf.Variable(tf.random.normal([layer[0]], 
                                                           stddev=0.1),name=pref+'bh'+str(i)+'_'+bd )) 
          
          reuse_ = reuse_m if self.MessageFunction == self.MessageFunction_ else False

          if pref+'wo_'+bd in self.m_ and reuse_:                                 # output layer
              if nnopt:       
                 self.m[pref+'wo_'+bd] = tf.Variable(self.m_[pref+'wo_'+bd],name=pref+'wo_'+bd)
                 self.m[pref+'bo_'+bd] = tf.Variable(self.m_[pref+'bo_'+bd],name=pref+'bo_'+bd)
              else:
                 self.m[pref+'wo_'+bd] = tf.constant(self.m_[pref+'wo_'+bd],name=pref+'wo_'+bd)
                 self.m[pref+'bo_'+bd] = tf.constant(self.m_[pref+'bo_'+bd],name=pref+'bo_'+bd)
          else:
              self.m[pref+'wo_'+bd] = tf.Variable(tf.random.normal([layer[0],nout],stddev=0.0001), name=pref+'wo_'+bd)   
              self.m[pref+'bo_'+bd] = tf.Variable(tf.random.normal([nout], stddev=0.0001)+bias,
                                                  name=pref+'bo_'+bd)

  def write_lib(self,libfile='ffield',loss=None):
      p_   = self.sess.run(self.p)
      self.p_ = {}
      
      self.MolEnergy_ = self.sess.run(self.MolEnergy)
      for key in self.MolEnergy_:
          self.MolEnergy_[key] = float(self.MolEnergy_[key])

      for k in p_:
          key = k.split('_')[0]
          if key in ['V1','V2','V3','tor1','cot1']:
             k_ = k.split('_')[1]
             if k_ not in self.torp:
                continue

          self.p_[k] = float(p_[k])
          if key in self.punit:
             self.p_[k] = float(p_[k]/self.unit)

      if self.libfile.endswith('.json'):
         self.m_   = self.sess.run(self.m)

         for key in self.m_:
             k = key.split('_')[0]
             if k[0]=='f' and (k[-1]=='w' or k[-1]=='b'):
                for i,M in enumerate(self.m_[key]):
                    # if isinstance(M, np.ndarray):
                    self.m_[key][i] = M.tolist()
             else:
                self.m_[key] = self.m_[key].tolist()  # covert ndarray to list
         # print(' * save parameters to file ...')
         fj = open(libfile+'.json','w')
         j = {'p':self.p_,'m':self.m_,
              'EnergyFunction':self.EnergyFunction,
              'MessageFunction':self.MessageFunction, 
              'messages':self.messages,
              'bo_layer':self.bo_layer,
              'bf_layer':self.bf_layer,
              'be_layer':self.be_layer,
              'vdw_layer':self.vdw_layer,
              'MolEnergy':self.MolEnergy_,}
         js.dump(j,fj,sort_keys=True,indent=2)
         fj.close()
      else:
         write_lib(self.p_,self.spec,self.bonds,self.offd,
                   self.angs,self.torp,self.hbs,
                   zpe=self.zpe_,libfile=libfile,
                   loss=loss)

