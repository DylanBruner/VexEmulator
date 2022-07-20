import socket, threading, datetime
from httpServer import utils

class Server(object):
    def __init__(self, name: str, host: str, port: int):
        self.name   = name
        self.host   = host
        self.port   = port
        self.routes = []

        self.mainloop = True

    def stop(self): self.mainloop = False
    
    def route(self, url: str, methods=['GET','POST','PUT','DELETE']) -> None:
        def wrapper(func):
            self.routes.append((url, func))
            return func
        return wrapper

    def _form_response(self, response_content: str, code=200, content_type='text/html'):
        crafted_response = ""

        response_content = response_content.encode()
        crafted_response += f"HTTP/1.1 {code} {utils.RequestCodeToMessage(code)}\n"
        crafted_response += f"Date: {datetime.datetime.now().strftime('%a, %d %b, %Y %H:%M:%S GMT')}\n"
        crafted_response += f"Server: Test\n"
        crafted_response += f"Last-Modified: Tue, 01 Dec 2009 20:18:22 GMT\n"
        crafted_response += f"Accept-Range: bytes\n"
        crafted_response += f"Content-Length: {len(response_content)}\n"
        crafted_response += f"Content-Type: {content_type}\n"
        crafted_response += f"Cache-Control: no-cache, no-store, must-revalidate\n"
        crafted_response += f"\n{response_content.decode()}"
        crafted_response = crafted_response.encode()


        return crafted_response

    def _handle_request(self, client: socket.socket, addr: tuple, data: bytes):
        request = utils.DecodeRequest(data)

        for route in self.routes:
            if utils.DoesRequestMatchRoute(route[0], request.url):
                response = self._form_response(route[1](*utils.getArgsFromRequest(route[0], request.url)))
                client.send(response)
                client.close()
                break
        else:
            response = self._form_response('', code=404)
            client.send(response)

    def run(self, debug=False) -> None:
        print(f"[+] Running Http Server on {self.host}:{self.port}")

        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soc.bind((self.host, self.port))
        self.soc.listen(5)
        while self.mainloop:
            client, addr = self.soc.accept()
            data = client.recv(8024)
            threading.Thread(target=self._handle_request, args=(client, addr, data)).start()