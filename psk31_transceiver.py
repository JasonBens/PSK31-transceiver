#!/usr/bin/python

import socket, termios, fcntl, sys, os, time, collections, tty, atexit

def exit_handler():
  termios.tcsetattr(fd, termios.TCSADRAIN, old)

# End function definition


def readKeypress():
  fd = sys.stdin.fileno()
  
  oldterm = termios.tcgetattr(fd)
  newattr = termios.tcgetattr(fd)
  newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
  termios.tcsetattr(fd, termios.TCSANOW, newattr)
  
  oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)

  fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)  

  try:
    try:
      c = sys.stdin.read(1)
    except IOError:
      c = 0
  finally:
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)

  return c

# End function definition

def getBit():
  return ord(rxConn.recv(1))

# end function definition

def sendBit():
  bit = txBuffer.popleft()
  if bit == '0':
    lastTx[0] = not lastTx[0]
  txConn.send(chr(lastTx[0]))

# end function definition

def addCharToBuffer(char):
  [txBuffer.append(c) for c in list(varicode[char] + '00')]
  idleCounter[0] = 0
  with open(outputFile, 'a') as outFile:
    outFile.write(char)
  sys.stdout.write(char)
  sys.stdout.flush()

# end function definition

def addRawStringToBuffer(string):
  [txBuffer.append(c) for c in list(string)]

# end function definition

def radioFSM_idle():
  """
  No message received recently.  Check for data
  
  From radioFSM_idle, the FSM can enter radioFSM_rx, radioFSM_tx, or radioFSM_idle
  
  radioFSM_rx: Data received
  radioFSM_tx: No data received, user enters keystroke
  radioFSM_idle: No data received, no keystroke received
  """

  # Check for data.  If received, change state to radioFSM_rx
  if getBit():
    currentCode[0] = ''.join('1')
    return radioFSM_rx

  # Check for keystroke.  If received, change state to radioFSM_tx
  char = readKeypress()
  if char:
    txBuffer.clear()
    addRawStringToBuffer('0000000000000000')
    with open(outputFile, 'a') as outFile:
      outFile.write('\n>>>')
    sys.stdout.write('\n>>>') 
    addCharToBuffer(char)
    return radioFSM_tx

  # No data received, no keystroke, return to radioFSM_idle  
  return radioFSM_idle

# End function definition

def radioFSM_rxIdle():
  if getBit():
    currentCode[0] = ''.join('1')
    return radioFSM_rx
  else:
    currentCode[0] += '0'
    if '0000000000000000000000000000000000000000000000000000000000000000' in currentCode[0]:
      with open(outputFile, 'a') as outFile:
        outFile.write('\n')
      sys.stdout.write('\n')
      sys.stdout.flush()
      return radioFSM_idle

  char = readKeypress()
  if char:
    txBuffer.clear()
    addRawStringToBuffer('0000000000000000')
    sys.stdout.write('\n>>>')
    sys.stdout.flush()
    addCharToBuffer(char)
    if char == '\n':
      with open(outputFile, 'a') as outFile:
        outFile.write('>>>')
      sys.stdout.write('>>>')
    return radioFSM_tx

  return radioFSM_rxIdle

# End function definition    

def radioFSM_rx():
  currentCode[0] += str(getBit())
  if '00' in currentCode[0]:
    try:
      with open(outputFile, 'a') as outFile:
        outFile.write(varicode[currentCode[0].strip('0')])
      sys.stdout.write(varicode[currentCode[0].strip('0')])
      sys.stdout.flush()
    except KeyError:
      with open(outputFile, 'a') as outFile:
        outFile.write('|')
      sys.stdout.write('|')
      sys.stdout.flush()
    return radioFSM_rxIdle

  char = readKeypress()
  if char:
    txBuffer.clear()
    addRawStringToBuffer('0000000000000000')
    with open(outputFile, 'a') as outFile:
      outFile.write('\n>>>')
    sys.stdout.write('\n>>>')
    sys.stdout.flush()
    addCharToBuffer(char)
    if char == '\n':
      with open(outputFile, 'a') as outFile:
        outFile.write('>>>')
      sys.stdout.write('>>>')
    return radioFSM_tx

  return radioFSM_rx

# End function definition

def radioFSM_tx():
  char = readKeypress()
  if char:
    addCharToBuffer(char)
    if char == '\n':
      with open(outputFile, 'a') as outFile:
        outFile.write('>>>')
      sys.stdout.write('>>>')

  if time.time() - FSMTimer[0] >= 1/31.25:
    FSMTimer[0] = time.time()
    sendBit()
 
  if not len(txBuffer):
    return radioFSM_txIdle
  return radioFSM_tx

# End function definition

def radioFSM_txIdle():
  char = readKeypress()
  if char:
    addCharToBuffer(char)
    return radioFSM_tx
  
  if time.time() - FSMTimer[0] >= 1/31.25:
    FSMTimer[0] = time.time()
    addRawStringToBuffer('0')
    sendBit()
    idleCounter[0] += 1
  
  if idleCounter[0] >= 32*3:
    with open(outputFile, 'a') as outFile:
      outFile.write('\n')
    sys.stdout.write('\n')
    sys.stdout.flush()
    return radioFSM_idle
  return radioFSM_txIdle

# End function definition

varicode = {    
        '\x00' : '1010101011', '\x01' : '1011011011', '\x02' : '1011101101',
        '\x03' : '1101110111', '\x04' : '1011101011', '\x05' : '1101011111',
        '\x06' : '1011101111', '\x07' : '1011111101', '\x08' : '1011111111',
        '\x09' : '11101111'  , '\x0A' : '11101'     , '\x0B' : '1101101111',
        '\x0C' : '1011011101', '\x0D' : '11111'     , '\x0E' : '1101110101',
        '\x0F' : '1110101011', '\x10' : '1011110111', '\x11' : '1011110101',
        '\x12' : '1110101101', '\x13' : '1110101111', '\x14' : '1101011011',
        '\x15' : '1101101011', '\x16' : '1101101101', '\x17' : '1101010111',
        '\x18' : '1101111011', '\x19' : '1101111101', '\x1A' : '1110110111',
        '\x1B' : '1101010101', '\x1C' : '1101011101', '\x1D' : '1110111011',
        '\x1E' : '1011111011', '\x1F' : '1101111111', ' '    : '1'         ,
        '!'    : '111111111' , '"'    : '101011111' , '#'    : '111110101' ,
        '$'    : '111011011' , '%'    : '1011010101', '&'    : '1010111011',
        '\''   : '101111111' , '('    : '11111011'  , ')'    :   '11110111',
        '*'    : '101101111' , '+'    : '111011111' , ','    : '1110101'   ,
        '-'    : '110101'    , '.'    : '1010111'   , '/'    : '110101111' ,
        '0'    : '10110111'  , '1'    : '10111101'  , '2'    : '11101101'  ,
        '3'    : '11111111'  , '4'    : '101110111' , '5'    : '101011011' ,
        '6'    : '101101011' , '7'    : '110101101' , '8'    : '110101011' ,
        '9'    : '110110111' , ':'    : '11110101'  , ';'    : '110111101' ,
        '<'    : '111101101' , '='    : '1010101'   , '>'    : '111010111' ,
        '?'    : '1010101111', '@'    : '1010111101', 'A'    : '1111101'   ,
        'B'    : '11101011'  , 'C'    : '10101101'  , 'D'    : '10110101'  ,
        'E'    : '1110111'   , 'F'    : '11011011'  , 'G'    : '11111101'  ,
        'H'    : '101010101' , 'I'    : '1111111'   , 'J'    : '111111101' ,
        'K'    : '101111101' , 'L'    : '11010111'  , 'M'    : '10111011'  ,
        'N'    : '11011101'  , 'O'    : '10101011'  , 'P'    : '11010101'  ,
        'Q'    : '111011101' , 'R'    : '10101111'  , 'S'    : '1101111'   ,
        'T'    : '1101101'   , 'U'    : '101010111' , 'V'    : '110110101' ,
        'W'    : '101011101' , 'X'    : '101110101' , 'Y'    : '101111011' ,
        'Z'    : '1010101101', '['    : '111110111' , '\\'   : '111101111' ,
        ']'    : '111111011' , '^'    : '1010111111', '_'    : '101101101' ,
        '`'    : '1011011111', 'a'    : '1011'      , 'b'    : '1011111'   ,
        'c'    : '101111'    , 'd'    : '101101'    , 'e'    : '11'        ,
        'f'    : '111101'    , 'g'    : '1011011'   , 'h'    : '101011'    ,
        'i'    : '1101'      , 'j'    : '111101011' , 'k'    : '10111111'  ,
        'l'    : '11011'     , 'm'    : '111011'    , 'n'    : '1111'      ,
        'o'    : '111'       , 'p'    : '111111'    , 'q'    : '110111111' ,
        'r'    : '10101'     , 's'    : '10111'     , 't'    : '101'       ,
        'u'    : '110111'    , 'v'    : '1111011'   , 'w'    : '1101011'   ,
        'x'    : '11011111'  , 'y'    : '1011101'   , 'z'    : '111010101' ,
        '{'    : '1010110111', '|'    : '110111011' , '}'    : '1010110101',
        '~'    : '1011010111', '\x7F' : '1110110101'}
varicode.update(dict((v,k) for k,v in varicode.items()))

# End dictionary definition


########################################################################
# Start of main script
########################################################################

txHost = '127.0.0.1'
txPort = 52001
rxHost = '127.0.0.1'
rxPort = 52002

# Disable console echo.  Transmitted characters must be echoed manually
fd = sys.stdin.fileno()
old = termios.tcgetattr(fd)
atexit.register(exit_handler)
tty.setcbreak(fd)

outputFile = './output.txt'

print "Listening for connections..."

txSock = socket.socket()
txSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
txSock.bind((txHost, txPort))
txSock.listen(1)
txConn, txAddr = txSock.accept()

rxSock = socket.socket()
rxSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rxSock.bind((rxHost, rxPort))
rxSock.listen(1)
rxConn, rxAddr = rxSock.accept()

print "Connected"

radioFSM = radioFSM_idle
currentCode = ['0']
txBuffer = collections.deque([], 256)
idleCounter = [0]
lastTx = [False]

FSMTimer = [time.time()]

while True:
  radioFSM = radioFSM()

