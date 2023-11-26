import PySimpleGUI as sg
import random
import math
import sympy
from sympy import mod_inverse

def isPrime(n):
    for i in range(2,int(n**0.5)+1):
        if n%i==0:
            return False
        
    return True

primes = [i for i in range(0,1000) if isPrime(i)]

def compute_lcm(x, y):
   return int((x*y)/(math.gcd(x, y)))

class Pal():

  def generate_key(self, name):
    while(True):
      p = random.choice(primes)
      q = random.choice(primes)
      if((p!=q) and (math.gcd(p*q, (p-1)*(q-1))==1)):
        break
  
    n = p*q
    l = compute_lcm(p-1, q-1)

    while(True):
      g = random.randint(1, n**2)
      x = int(((g**l)%(n*n)-1)/n)
      if(math.gcd(x, n)==1):
        break;

    mu = mod_inverse(x, n)
    self.name = name
    keys = [n, l, g, mu]
    self.keys = keys

  def encrypt(self, original):
    n = self.keys[0]
    g = self.keys[2]
    m = int(original)
    r = random.randint(1, n-1)
    c = ((g**m)*(r**n))%(n*n)
    self.encrypted = c

  def decrypt(self, original):
    c = int(original)
    n = self.keys[0]
    l = self.keys[1]
    mu = self.keys[3]
    self.decrypted = int((((((c**l)%(n*n))-1)/n)*mu)%n)


def SSS_calculate(x1, y1, x2, y2, x3, y3):
    denom = (x1-x2) * (x1-x3) * (x2-x3);
    if denom == 0:
        return denom,denom,denom
    A = (x3 * (y2-y1) + x2 * (y1-y3) + x1 * (y3-y2)) / denom;
    B = (x3*x3 * (y1-y2) + x2*x2 * (y3-y1) + x1*x1 * (y2-y3)) / denom;
    C = (x2 * x3 * (x2-x3) * y1+x3 * x1 * (x3-x1) * y2+x1 * x2 * (x1-x2) * y3) / denom;
    return A,B,C

def unique(l):
    if len(l)==len(set(l)):
        return True
    else:
        return False

sg.theme('DarkBlack')


#Step 1: number of votes/candidates, input, keys, calculation, encrypted result

inputlayout = [[sg.Frame('Input', [[sg.Text('Enter number of votes and number of candidates')],
          [sg.Text('# of Votes'), sg.Input()],
          [sg.Text('# of Candidates'), sg.Input()],
          [sg.OK()]], title_color='yellow', border_width=3)]]

window = sg.Window('Voter Input', inputlayout, size=(1000, 500))

while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'OK'):
        break

vl = values[0]
cn = values[1]
base = int(vl) + 1

window.close()

#id number/voting candidate input

repeated = 0
votes = list()
ids = list()

while True:
    headings = ['ID #', 'Candidate #']
    header =  [[sg.Text('')] + [sg.Text(h, size=(14,1)) for h in headings]]
    if repeated == 1:
        window.close()
        header += [[sg.Text('Multiple votes have been casted by a single Id number.', text_color='red')], [sg.Text('Please enter the votes again without any overlap.', text_color='red')]]
    input_rows = [[sg.Input(size=(15,1), pad=(0,0)) for col in range(2)] for row in range(int(vl))]
    button = [[sg.OK()]]
    inputlayout = [[sg.Frame('Input', [[sg.Text('Enter number of votes and number of candidates')],
              [sg.Text('# of Votes'), sg.Text(vl)],
              [sg.Text('# of Candidates'), sg.Text(cn)]], title_color='yellow', border_width=3)]]

    tablelayout = [[sg.Frame('Vote Input', layout = header + input_rows, title_color='yellow')]]
    inputlayout2 = inputlayout + tablelayout + button
    window = sg.Window('Table Simulation', inputlayout2, size=(1000, 500))
    event, values = window.read()
    while True:
        if event in (sg.WIN_CLOSED, 'OK'):
            break
    vote_cast = list()
    for k in values:
        if k % 2 == 0:
            if values[k]:
                vote_cast.append(int(values[k]))

    if unique(vote_cast):
        for k in values:
            if k % 2 == 0:
                votes.append(int(values[k]))
            else:
                ids.append(int(values[k]))
        break
    
    
    repeated = 1

window.close()

y = Pal()
y.generate_key('vote')
total = 1

#keys

headings = ['ID #', 'Candidate #']
header =  [[sg.Text('')] + [sg.Text(h, size=(14,1)) for h in headings]]
input_rows = [[sg.Text('   '), sg.Text(ids[row]), sg.Text('                '), sg.Text(votes[row])] for row in range(int(vl))]
button = [[sg.OK()]]
inputlayout = [[sg.Frame('Input', [[sg.Text('Enter number of votes and number of candidates')],
              [sg.Text('# of Votes'), sg.Text(vl)],
              [sg.Text('# of Candidates'), sg.Text(cn)]], title_color='yellow', border_width=3)]]

tablelayout = [[sg.Frame('Vote Input', layout = header + input_rows, title_color='yellow')]]

keyoutput = [[sg.Text('public keys:'), sg.Text(y.keys[0]), sg.Text(y.keys[2])], [sg.Text('private keys:'), sg.Text(y.keys[1]), sg.Text(y.keys[3])], [sg.Text('All votes will be encrypted using the public keys, which will then be multiplied as below.')]]

layoutkey = inputlayout + tablelayout + button


#calculation

calc_layout = []

for k in values:
    if k%2==1 and values[k]:
        y.encrypt((base)**(int(values[k])))
        total = total * (y.encrypted)
        mul_enc = y.encrypted
        calc_layout += [[sg.Text('Multiplied Encrypted Value        = '), sg.Text(mul_enc)]]

calc_layout += [[sg.Text('Total Encrypted Value       = '), sg.Text(total)]]
y.decrypt(total)
total = y.decrypted
calc_framed = [[sg.Frame('Calculation', layout = keyoutput + calc_layout, title_color='yellow')]]

columnlayout = [[sg.Column(layoutkey), sg.Column(calc_framed)]]


window = sg.Window('Table Simulation', columnlayout, size=(1000, 500))

while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'OK'):
        break

window.close()


#Step 2: Private Key Coordinates

keyoutput = [[sg.Text('For security, the private keys will be converted into 3 coordinates')], [sg.Text('private keys:'), sg.Text(y.keys[1]), sg.Text(y.keys[3])]]

a = y.keys[1]
b = y.keys[3]
c = random.randint(1, 100)
p1x = list()
p1y = list()


for k in range(3):
    x = random.randint(1, 100)
    p1x.append(x)
    p1y.append(a*x*x+b*x+c)


coor_layout = keyoutput + [[sg.Text('a, b are private keys and c is a random integer in the form ax^2 + bx + c')], [sg.Text('a:'), sg.Text(a)], [sg.Text('b:'), sg.Text(b)], [sg.Text('c:'), sg.Text(c)]]

coor_explain = [[sg.Text('Then, three random coordinates will be generated using the equation:'), sg.Text(a), sg.Text('x^2'), sg.Text('+'), sg.Text(b), sg.Text('x'), sg.Text('+'), sg.Text(c)]]

coor_ = [[sg.Text('The coordinates are the following:')]]

button = [[sg.OK()]]

for k in range(3):
    coor_ += [[sg.Text('x     ='), sg.Text(p1x[k]), sg.Text('y     ='), sg.Text(p1y[k])]]
    
coorl_framed = [[sg.Frame('Equation Generation', layout = coor_layout, title_color='yellow')]]

coor_framed = [[sg.Frame('Coordinates', layout = coor_explain + coor_, title_color='yellow')]]

col_layout = [[sg.Column(coorl_framed), sg.Column(coor_framed)]] + button

window = sg.Window('Table Simulation', col_layout, size=(1000, 500))

while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'OK'):
        break

window.close()

#Step 3: Private Key Coordinate Check

repeated=0

headings = ['x', 'y']

abort = 0
coorx = list()
coory = list()

while True:
    if repeated==1:
        window.close()
        txt = [[sg.Text('Please Enter Three Coordinates of The Private Key to Gain Access to Final Results')],
               [sg.Text('Wrong! Please Try Again', text_color='Red')]]
    else:
        txt =  [[sg.Text('Please Enter Three Coordinates of The Private Key to Gain Access to Final Results')]]
    header =  [[sg.Text('')] + [sg.Text(h, size=(14,1)) for h in headings]]
    input_rows = [[sg.Input(size=(15,1), pad=(0,0)) for col in range(2)] for row in range(3)]
    button = [[sg.OK(), sg.Button('Cancel')]]
    checkframed = [[sg.Frame('Coordinate Check', layout = txt + header + input_rows + button, title_color='yellow')]]
    window = sg.Window('Private Key Confirmation', checkframed, size=(1000, 500))
    
    while True:             
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'OK'):
            break
        if event == sg.WIN_CLOSED or event == 'Cancel':
            abort = 1
            break

    A,B,C = SSS_calculate(int(values[0]), int(values[1]), int(values[2]), int(values[3]), int(values[4]), int(values[5]))
    if abort==1:
        break
        
    if a==A and b==B and c==C:
        for k in range(6):
            if not values[k]:
                abort = 1
                break
            if k % 2 == 0:
                coorx.append(int(values[k]))
            else:
                coory.append(int(values[k]))
        break
    
    repeated = 1
    
    
window.close()

#Step 4: Decryption and production of Results


coor_text = [[sg.Text('The coordinates you have entered are the following:')]]
for k in range(3):
    coor_text += [[sg.Text('x    ='), sg.Text(coorx[k]), sg.Text('y    ='), sg.Text(coory[k])]]

keyoutput = [[sg.Text('With these coordinates, the derived private keys are the following:')], [sg.Text('private keys:'), sg.Text(y.keys[1]), sg.Text(y.keys[3])]] + [[sg.Text('Decrypted with the keys, the total decrypted value is'), sg.Text(total)]]

calc_final = [[sg.Text('The final results are below')]]

for k in range(int(cn)+1):
    votes = int(total%((base)**(k+1))/(base**k))
    if k != 0:
        calc_final += [[sg.Text('candidiate #:'), sg.Text(k), sg.Text('Vote #:'), sg.Text(votes)]]
    beftot = total%((base)**(k+1))
    total = total - total%((base)**(k+1))
    if k != 0:
        calc_final += [[sg.Text('Remaining Total:'), sg.Text(total), sg.Text('Subtracted Total:'), sg.Text(beftot), sg.Text('Divided Value:'), sg.Text(base**k)]]

keyframed = [[sg.Frame('Keys', layout = coor_text + keyoutput, title_color='yellow')]]
finalframed = [[sg.Frame('Results', layout = calc_final, title_color='yellow')]]
button = [[sg.OK()]]

columnlayout = [[sg.Column(keyframed), sg.Column(finalframed)]] + button

window = sg.Window('Table Simulation', columnlayout, size=(1000, 500))

while True:             
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'OK'):
        break

window.close()


