# goal - implement http v1.1 

#import asyncio
import socket

def handle_get(uri: str, file):
    # https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Messages

    if uri == '/':
        uri = '/index.html'
    try: 
        with open("./site"+uri,"r") as index_html:
            content = index_html.read()
            file.write("HTTP/1.1 200")
            file.write("\n")
            file.write("OK")
            file.write("\n")
            file.write("Content-Type: text/html; charset=UTF-8")
            file.write("\n")
            file.write("Content-Length: "+str(len(content)))
            file.write("\n") # marks the end of headers
            file.write("\n")
            file.write(content)
    except FileNotFoundError:
        file.write("HTTP/1.1 404 \n")
    

#async def handle(sock: socket):
def handle(sock: socket):
    # Wait for an incoming connection.

    #loop = asyncio.get_running_loop()
    #conn, addr = await loop.sock_accept(sock)

    conn, addr = sock.accept() 
    print(addr) # (client ip, request id)
    file = conn.makefile("w")  # SocketIO
    filer = conn.makefile("r") # SocketIO
    """ request for http://localhost:8000/pqr
       GET /pqr HTTP/1.1
       Host: localhost:8000
       User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0
       Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
       Accept-Language: en-US,en;q=0.9
       Accept-Encoding: gzip, deflate, br, zstd
       Sec-GPC: 1
       Connection: keep-alive
       Upgrade-Insecure-Requests: 1
       Sec-Fetch-Dest: document
       Sec-Fetch-Mode: navigate
       Sec-Fetch-Site: none
       Sec-Fetch-User: ?1
       Priority: u=0, i
    """

    # - printing the request - 
    #print(filer.read()) # this does not work as browser dont explicitly close the connection

    #line = filer.readline()
    #while line.strip() != "":
    #    print(line)
    #    line = filer.readline()

    # - processing the request -  
    # vim align selection with  :'<,'>!column -t -s=
    line                       =   filer.readline() # GET /pqr HTTP/1.1
    request_params             =   line.split(' ')
    print(request_params)
    verb                       =   request_params[0].strip()
    uri                        =   request_params[1].strip()
    spec                       =   request_params[2].strip()
    if spec != 'HTTP/1.1':
        file.write("HTTP/1.1 500 \n")
    if verb == 'GET':
        handle_get(uri, file)

    print(" -------- ")

def main():
    address = ('', 8000)
    """
     https://github.com/python/cpython/blob/3.14/Lib/socket.py
     the socket implementation comes from Modules/socketmodule.c
     which creates os dependent TCP sockets from c
     eg fd = WSASocketW(family, type, proto,
                        NULL, 0,
                        WSA_FLAG_OVERLAPPED | WSA_FLAG_NO_HANDLE_INHERIT);
     on Windows
     or on UNIX as fd = socket(family, type, proto);

     init - sock_initobj_impl(...)
     bind - sock_bind(...) -> <sys/socket.h> bind
     listen - sock_listen(...) -> <sys/socket.h> listen
     accept - _accept -> sock_accept_imp(....) -> <sys/socket.h> accpet
     makefile - 
        raw = SocketIO(self, rawmode)
        buffer = io.BufferedWriter(raw, buffering)
        encoding = io.text_encoding(encoding)
        file = io.TextIOWrapper(buffer, encoding, errors, newline)
        file.mode = mode
     close - _socket_socket_close_impl -> SOCKETCLOSE(fd) -> closesocket(..) windows or close(..) for unix

    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.setblocking(False)
    sock.setblocking(True)

    try:
        try:
            sock.bind(address)
        except error as err:
            msg = '%s (while attempting to bind on address %r)' % \
                    (err.strerror, address)
            raise error(err.errno, msg) from None
        sock.listen()
    except error:
        sock.close()
        raise

    #asyncio.run(handle(sock))
    while True:
        handle(sock)

    sock.close()

if __name__ == '__main__':
    main()
