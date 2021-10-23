try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network
import dht
import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'spedy'
password = 'spedy123'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(5, Pin.OUT)
sensor = dht.DHT11(Pin(4))
def web_page():
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """
   <html>
        <head>
          <link rel="icon" href="data:,">
          <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/css/bootstrap.min.css" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.1/dist/js/bootstrap.bundle.min.js"></script>
  <style>
    html{font-family: Helvetica;
          display:inline-block;
          margin: 0px auto;
          text-align: center;}
          h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
          .button{display: inline-block;
          background-color: #e7bd3b; border: none; 
          border-radius: 4px; color: white; padding: 16px 40px;
          text-decoration: none; font-size: 30px;
          margin: 2px;
          cursor: pointer;}
      div{
          size: 100px;
          padding: 100px;
          background-color: rgb(255, 255, 255);
      }
  </style>
        </head>
          <body>
            <div class="container">
              <h1>ESP Web Server</h1> 
          <p>GPIO state: """ + gpio_state + """</p>
          <p><a href="/?led=on"><button class="btn btn-success btn-lg">ON</button></a></p>
          <p><a href="/?led=off"><button class="btn btn-danger btn-lg">OFF</button></a></p>
            </div>
          </body>
    </html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  print(led_on)
  print(led_off)
  if led_on == 6:
    print('LED ON')
    led.value(1)
  if led_off == 6:
    print('LED OFF')
    led.value(0)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
