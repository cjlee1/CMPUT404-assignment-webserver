    #  coding: utf-8
import socketserver
import os
# Copyright 2019 Abram Hindle, Eddie Antonio Santos,Calvin LEE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

#$ telnet localhost 8888
#GET /hello HTTP/1.1


class MyWebServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        response = self.parse_req(self.data)
        #self.request.sendall(bytearray("200\n",'utf-8'))
        self.request.sendall(bytearray(response,'utf-8'))

    def parse_req(self,req):
        request_text = req.splitlines()[0].decode("utf-8")
        # print(request_text)
        #request_text = request_text.rstrip('\r\n ')
        #print(request_text)
        self.request_method, self.line, self.version = request_text.split()
        # print(str(self.request_method),"\n ",self.line, "\n",self.version,'\n' )
        if self.request_method == "GET":
            # print(1)
            # self.response = 'HTTP/1.1 405 Method Not Allowed\nContent-Type:text/html\n'
            # return self.response
            fpath = os.getcwd()
            # print(fpath,11)
            if self.line == "/":

                index = open(fpath+"/www/index.html","r")
                self.content = index.read()
                self.headers = 'HTTP/1.1 200 Ok\r\nContent-Type:text/html\r\n\r\n'
            else:


                if ".css" in self.line:

                    if not os.path.exists(fpath+"/www"+self.line):
                        self.headers = 'HTTP/1.1 404 Page Not Found\r\n\r\n'
                        self.content = ""
                        return self.headers+self.content

                    path = open(fpath+"/www"+self.line)


                    self.content = path.read()
                    self.headers = 'HTTP/1.1 200 Ok\r\nContent-Type:text/css\r\n\r\n'
                elif ".html" in self.line:
                    if not os.path.exists(fpath+"/www"+self.line):
                        self.headers = 'HTTP/1.1 404 Page Not Found\r\n\r\n'
                        self.content = ""
                        return self.headers+self.content

                    path = open(fpath+"/www"+self.line)
                    self.content = path.read()
                    self.headers = 'HTTP/1.1 200 Ok\r\nContent-Type:text/html\r\n\r\n'
                elif self.line[-1]=="/":
                    if not os.path.exists(fpath+"/www"+self.line):
                        self.headers = 'HTTP/1.1 404 Page Not Found\r\n\r\n'
                        self.content = ""
                        return self.headers+self.content

                    index = open(fpath+"/www"+self.line+"index.html" ,"r")
                    self.content = index.read()
                    self.headers = 'HTTP/1.1 200 Ok\r\nContent-Type:text/html\r\n\r\n'
                elif "favicon.ico" in self.line:
                    self.headers = 'HTTP/1.1 404 Not Found\r\n\r\n'
                    self.content = ""
                else:
                    # print(self.line)
                    npath = os.path.abspath(fpath+"/www"+self.line)
                    # npath = os.getcwd()
                    # print(fpath,22 )
                    # print(npath,33)
                    # print(npath.startswith(fpath))
                    # print(self.line[-1].isalnum())


                    if not npath.startswith(fpath):
                        self.headers = 'HTTP/1.1 404 Page Not Found\r\n\r\n'
                        self.content = ""
                        return self.headers+self.content
                    if not os.path.exists(fpath+"/www"+self.line):
                        # if os.path.exists(fpath+ "/www"+ self.line) == fpath:


                        self.headers = 'HTTP/1.1 404 Page Not Found\r\n\r\n'
                        self.content = ""
                        return self.headers+self.content
                    if self.line[-1].isalnum() or self.line[-1]=="."  and os.path.isdir(fpath+"/www"+ self.line) :
                        self.headers = 'HTTP/1.1 301 Moved Permanently\r\n\r\n'
                        self.content = ""
                        return self.headers+self.content
                    return self.headers+self.content


            # if self.line =="/base.css":
            #     css = open(fpath+"/www/"+self.line)
            #     self.content = css.read()
            #     self.headers = 'HTTP/1.1 200 Ok\r\nContent-Type:text/css\r\n\r\n'
            # if self.line =="/deep/index.html":
            #     index = open(fpath+"/www/deep/index.html","r")
            #     self.content = index.read()
            #     self.headers = 'HTTP/1.1 200 Ok\r\nContent-Type:text/html\r\n\r\n'
            return self.headers+self.content


        elif self.request_method=="POST" or self.request_method=="PUT" or self.request_method=="DELETE"  :
            #print(20)
            self.response = 'HTTP/1.1 405 Method Not Allowed\nContent-Type:text/html\n'
            return self.response



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
