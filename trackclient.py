#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Tracker client
# Author: ypod
# Date: Oct 2006
#


import select, socket, os, sys, time


class TrackClient():
    timeout = 4
    interval= 2
    size    = 1024
    host    = "bluescan.media.mit.edu"
    port    = 5657
    hostname = os.popen("hostname").readlines()[0].strip()
    ip      = ''
    
    def advertisement_loop(self):
        while True:
            try:
                self.client.sendto( self.hostname, (self.host, self.port) )
            except socket.error, (code,message):
                print "Error: socket broken: " + message
                
            time.sleep(self.interval)


    def __init__(self, req=''):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        except socket.error, (code,message):
            if self.client:
                self.client.close()
            print "Could not open socket: " + message
            sys.exit(1)


        if req:
            try:
                req = req+'?'
                self.client.sendto( req, (self.host, self.port) )
                s = select.select([self.client], [], [], self.timeout)
                if s[0]:
                    data = self.client.recv(self.size).strip()
                    if data == 'None':
                        print 'not found'
                    else:
                        self.ip = data
                        print data
                else:
                    print "timed out while waiting for response from", self.host
            except Exception, e:
                print '%s' % e
        else:
            try:
                self.advertisement_loop()
            except:
                self.client.close()


    def __unicode__(self):
        return '%s' % self.ip
    def __str__(self):
        return self.__unicode__()
        
if __name__=='__main__':
    arg = ''
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
    t = TrackClient(arg)
