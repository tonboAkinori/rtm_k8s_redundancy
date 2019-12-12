#!/usr/bin/env python
# -*- coding: euc-jp -*

ESCAPE_S = '\033[33m'
ESCAPE_E = '\033[0m'


import sys
from omniORB import CORBA
import RTM

import CORBA_IORUtil

import RTC
import OpenRTM_aist

import time

def main(argv):
    
    orb = CORBA.ORB_init([], CORBA.ORB_ID)

    flip_ip_add = []

    camera_ip_add = "corbaloc:iiop:192.168.11.70:2810/manager"
    
    for i in range(0, len(argv), 2):
        flip_ip_add.append("corbaloc:iiop:{}:{}/manager".format(argv[i],argv[i+1]))

    print camera_ip_add

    for i in range(len(flip_ip_add)):
        print flip_ip_add[i]

    print ""
        
    ###################
    # Flip            #
    ###################
    flip_orb     = []
    flip_manager = []
    flip_objref  = []
    flip_portref = []
    
    for i in range(len(flip_ip_add)):
        flip_orb.append(orb.string_to_object(flip_ip_add[i]))
        flip_manager.append(flip_orb[i]._narrow(RTM.Manager))
        flip_objref.append(flip_manager[i].get_components())
        flip_portref.append(flip_objref[i][0].get_ports())

    ###################
    # Camera/Viewer   # 
    ###################
    camera_orb = orb.string_to_object(camera_ip_add)
    camera_manager = camera_orb._narrow(RTM.Manager)
    camera_objref = camera_manager.get_components()
    
    if 'OpenCVCamera0' == camera_objref[0].get_component_profile().instance_name :
        camera_port = camera_objref[0].get_ports()
        viewer_port = camera_objref[1].get_ports()
    else:
        camera_port = camera_objref[1].get_ports()
        viewer_port = camera_objref[0].get_ports()

        
    for i in range(len(flip_ip_add)):
        flip_portref[i][0].disconnect_all() 
    print ""
    camera_port[0].disconnect_all()
    viewer_port[0].disconnect_all()

    
    #connect ports(Camera.out <- Flip.in)
    camera_flip_connect = []
    for i in range(len(flip_ip_add)):
        tmp_string = 'camera_connect_{}'.format(3)
        camera_flip_connect = RTC.ConnectorProfile(tmp_string, "", [flip_portref[i][0], camera_port[0]], [])
        OpenRTM_aist.CORBA_SeqUtil.push_back(camera_flip_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.interface_type",
                                                                   "corba_cdr"))
        
        OpenRTM_aist.CORBA_SeqUtil.push_back(camera_flip_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type",
                                                                       "push"))
        
        OpenRTM_aist.CORBA_SeqUtil.push_back(camera_flip_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.subscription_type",
                                                                       "New"))
        
        OpenRTM_aist.CORBA_SeqUtil.push_back(camera_flip_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.publisher.push_policy",
                                                                "new"))
        
        print '\033[44m'+ "@@@@@ Camera -Flip[{}] Connecting...  @@@@@".format(i) + '\033[0m'
        ret =  flip_portref[i][0].connect(camera_flip_connect)
        print ret
        print ""
        
    time.sleep(1)
    
    # connect ports(Flip.out -> Viewer.in)
    flip_viwer_connect = []
    for i in range(len(flip_ip_add)):
        tmp_string = 'viewer_connect_{}'.format(4)
        flip_viewer_connect = RTC.ConnectorProfile(tmp_string, "", [flip_portref[i][1], viewer_port[0]], [])
        OpenRTM_aist.CORBA_SeqUtil.push_back(flip_viewer_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.interface_type",
                                                                       "corba_cdr"))
        
        OpenRTM_aist.CORBA_SeqUtil.push_back(flip_viewer_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.dataflow_type",
                                                                       "push"))
        
        OpenRTM_aist.CORBA_SeqUtil.push_back(flip_viewer_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.subscription_type",
                                                                       "New"))
        
        OpenRTM_aist.CORBA_SeqUtil.push_back(flip_viewer_connect.properties,
                                             OpenRTM_aist.NVUtil.newNV("dataport.publisher.push_policy",
                                                                       "new"))
        
        print '\033[44m'+ "@@@@@ Flip - Viewer Connecting...  @@@@@" + '\033[0m'
        ret = flip_portref[i][1].connect(flip_viewer_connect)
        print ret
        print ""
        

    
    # Activate PC RTC
#    camera_rtc = camera_objref[0].get_owned_contexts()
#    viewer_rtc = camera_objref[1].get_owned_contexts()
#    flip_rtc = flip_objref[0].get_owned_contexts()

#    viewer_rtc[0].deactivate_component(camera_objref[1])
#    camera_rtc[0].deactivate_component(camera_objref[0])
#    flip_rtc[0].deactivate_component(flip1_objref[0])
    
#    viewer_rtc[0].activate_component(camera_objref[1])
#    camera_rtc[0].activate_component(camera_objref[0])
#    flip_rtc[0].activate_component(flip1_objref[0])

    sys.exit(1)

if __name__ == "__main__":
    main(sys.argv[1:])

