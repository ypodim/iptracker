#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Tracker server
# Author: ypod
# Date: Oct 2006
#

import select, socket, sys, time, os

host	= ""
backlog = 5
size	= 1024
hosts	= {}
port	= 5657


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host,port))

input = [server]
running = True
while running:
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:
        if s == server:
            data, address = server.recvfrom(size)
            
            data = data.strip()
            response = 'what?'
            if data and data[-1] == '?':
                hostname = data[:-1]
                response = '%s' % hosts.get(hostname)
                #print 'response: %s is on %s' % (hostname, address)
                
            if data and data[-1] != '?':
                
                hostname = data
                hosts[hostname] = address[0]
                response = 'ok'
                #print '%s is on %s' % (hostname, address[0])
                
            server.sendto( response, address )

server.close()
