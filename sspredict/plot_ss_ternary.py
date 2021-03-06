import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import re
import argparse
import pandas as pd
from matplotlib.mlab import griddata


def read_file(st_name):
    lines = open(st_name).readlines()
    print('reading file...')
    for line in lines[0:12]:
        if ('temperature') in line:
            try:T = line.strip('\n').split(':')[1].strip(' ');
            except:print('temperature input invalid');quit();
        if ('e:') in line:
            try:g_e = [e.strip(' ') for e in (line.strip('\n').strip('e:').split(","))]
            except:print('element input invalid');quit();
        if ('ratio') in line:
            try:ratios = (line.strip('\n').strip('ratio:').split(","))
            except:print('ratio input invalid');quit();
        if ('strain_r') in line:
            try: ep = (line.strip('\n').split(':')[1].strip(' '));
            except:print('strain rate input invalid')

    for line in lines :
        if ('Start of Predicted Data') in line:
            N = lines.index(line)+1;#print(N)
    try: data =pd.read_csv(st_name,header=N,delimiter=',');#print(data)
    except:print('illegal input file format');quit()
    return data,T,g_e,ep,ratios

def seg_length():
    axlim=(np.sqrt((plt.xlim())[1]**2+(plt.xlim())[0]**2))
    seg_l = axlim/100;
    seg_1 = seg_l*np.sqrt(3)/2
    seg_2 = seg_l/2
    return seg_l,seg_1,seg_2
def make_segments(seg_l,seg_1,seg_2,xys,Cr,tp):
    bottom_seg=[];left_seg=[];right_seg=[]
    for xy in xys:
        bot_xy = [[xy,xy-seg_2],[0,-seg_1]];bottom_seg.append(bot_xy)
        left_xy = [[(Cr-xy)/2, (Cr-xy)/2-seg_2],[tp*Cr-tp*xy,tp*Cr-tp*xy+seg_1]];left_seg.append(left_xy)
        right_xy = [[Cr-xy/2,Cr-xy/2+seg_l],[tp*xy,tp*xy]];right_seg.append(right_xy)
    return bottom_seg,left_seg,right_seg

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '-filename', type=str, help='input filename for plotting')
    parser.add_argument('-s', '-save' ,type=str, default=None,
                         help='to save the figure ')
    args = parser.parse_args()
    st_name = args.f

    element = ['psA','psB','psC']

    np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})
    fig= plt.figure(figsize=(14,6))
    ax = fig.add_subplot(121);
    ax.set_ylim((-0.1,1.1))
    ax.set_xlim((-0.1,1.1))
    plt.gca().set_aspect('equal', adjustable='box')
    ax.axis('off')
    ax2 = fig.add_subplot(122)
    ax2.set_ylim((-0.1,1.1))
    ax2.set_xlim((-0.1,1.1))
    plt.gca().set_aspect('equal', adjustable='box')
    ax2.axis('off')
     # Create triangulation.
    tp = np.sqrt(3)/2;step=10;Clim = 0#float(input('alloying composition:'))
    Cr = round((1-Clim),2)
    #-----------
    #X_C = C2 + C3/2
    #Y_C = C3 * np.sqrt(3)/2
    #-----------
    x = np.linspace(0,Cr,step+1)
    y = np.linspace(0,0,step+1)
    a = np.linspace(0,0.5*Cr,step+1)
    b = np.linspace(0,tp*(Cr),step+1)
    c = np.linspace(0.5*(Cr),Cr,step+1)
    d = np.linspace(tp*(Cr),0,step+1)

    bline = Line2D(x,y, color='k',LineWidth=1.5,solid_capstyle='round');bline2 = Line2D(x,y, color='k',LineWidth=1.5,solid_capstyle='round')
    lline = Line2D(a,b, color='k',LineWidth=1.5,solid_capstyle='round');lline2 = Line2D(a,b, color='k',LineWidth=1.5,solid_capstyle='round')
    rline = Line2D(c,d, color='k',label='Content',LineWidth=1.5,solid_capstyle='round');rline2 = Line2D(c,d, color='k',label='Content',LineWidth=1.5,solid_capstyle='round')
    ax.add_line(bline);ax.add_line(rline);ax.add_line(lline)
    ax2.add_line(bline2);ax2.add_line(rline2);ax2.add_line(lline2)
    ax.annotate(r'$ \mathrm{%s} $' % element[0] ,xy=(0,0),xytext=(-0.17,-0.1),FontSize=15,weight = 'bold');ax2.annotate(r'$ \mathrm{%s} $' % element[0],xy=(0,0),xytext=(-0.17,-0.1),FontSize=15,weight = 'bold')
    ax.annotate(r'$ \mathrm{%s} $' % element[1],xy=(Cr,0),xytext=(Cr+0.03,-0.1),FontSize=15,weight = 'bold');ax2.annotate(r'$ \mathrm{%s} $' % element[1],xy=(Cr,0),xytext=(Cr+0.03,-0.1),FontSize=15,weight = 'bold')
    ax.annotate(r'$ \mathrm{%s} $' % element[2],xy=(Cr/2,tp*Cr),xytext=(Cr/2-0.05,tp*Cr+0.07),FontSize=15,weight = 'bold');ax2.annotate(r'$ \mathrm{%s} $' % element[2],xy=(Cr/2,tp*Cr),xytext=(Cr/2-0.05,tp*Cr+0.07),FontSize=15,weight = 'bold')
    xys = np.linspace(0,Cr,6)[1:-1]
    seg_l,seg_1,seg_2 = seg_length();#print(seg_1)
    bottom_seg,left_seg,right_seg = make_segments(seg_l,seg_1,seg_2,xys,Cr,tp)
    i=0
    while i < len(bottom_seg):
        ax.plot(bottom_seg[i][0],bottom_seg[i][1],'k',solid_capstyle='round');#ax.text(bottom_seg[i][0][1],bottom_seg[i][1][1],('%.2f' % bottom_seg[i][0][0]),FontSize=12)
        ax2.plot(bottom_seg[i][0],bottom_seg[i][1],'k',solid_capstyle='round')

        ax.plot(left_seg[i][0],left_seg[i][1],'k',solid_capstyle='round')
        ax2.plot(left_seg[i][0],left_seg[i][1],'k',solid_capstyle='round')

        ax.plot(right_seg[i][0],right_seg[i][1],'k',solid_capstyle='round')
        ax2.plot(right_seg[i][0],right_seg[i][1],'k',solid_capstyle='round')
        i+=1

    #method to calculate  Cartesian coordinates from barycentric coordinates

    if len(element) == 3:
        XYlist = [];Xlist = [];Ylist = [];Zlist = [];XYZlist = []
        #find the elements with the same composition:
        data,T,g_e,ep,ratios  = read_file(st_name) #with open('%s.txt' % name, 'name','a') as f:
        data =data.dropna()
        #print(data.index)
        #count_row = data.shape[0];print(count_row)
        row = 0
        for row in data.index:
            comp = [float(data[i][row]) for i in element]
            C1 = comp[0];C2 = comp[1];C3 = comp[2]
            Z = np.float32(data['Delta_sigma_ss'][row]);
            X_C = C2 + C3/2; Y_C = C3 * np.sqrt(3)/2
            Xlist.append(X_C); Ylist.append(Y_C); XYlist.append([X_C,Y_C])
            Zlist.append(Z); XYZlist.append([X_C,Y_C,Z])
            row+=1
        #X,Y = np.meshgrid(Xlist,Ylist)
        #Z = X^2 + Y^2
        X = np.array(Xlist)
        Y = np.array(Ylist)
        Z = np.array(Zlist)
    #color = [str(item) for item in Z]
    #print(Z,type(Z),color)
    lowerlim = round(min(Z)/100,0)*100-50;upperlim = round(max(Z)/100,0)*100+50
    level = np.arange(lowerlim, upperlim+1, 10);ticks = ([item for item in level if item % 50 ==0])
    #print(lowerlim,upperlim)
    cm = plt.cm.get_cmap('inferno')
    plt.subplot(1, 2, 1)
    Ch = plt.scatter(X,Y,c=Z,s=200,cmap=cm)
    Cl = plt.colorbar(Ch,shrink=0.75,orientation='vertical',ticks = ticks)
    #Cl.set_label(label=r'$\Delta E_{SISF} \ (mJ/m^2)$',FontSize=15,weight='bold')
    plt.clim(lowerlim, upperlim);

    plt.subplot(1, 2, 2)
    Xi = np.linspace(min(X),max(X),1000);Yi = np.linspace(min(Y),max(Y),1000)
    XX,YY = np.meshgrid(Xi, Yi)
    ZZ = griddata(X,Y,Z,Xi,Yi,interp='nn')
    #print(XX)

    Ch2 = plt.contourf(XX,YY,ZZ, level, cmap=cm)
    Cl2 = plt.colorbar(Ch2,shrink=0.75,orientation='vertical',ticks = ticks)
    Cl2.set_label(label=r'$\Delta \sigma_{ss} \ (MPa)$',FontSize=15,weight='bold')
    fig.suptitle('psA = '+g_e[0]+', psB = '+g_e[1]+', psC = '+g_e[2]+'\n'+
            'rA = '+ratios[0]+', rB = '+ratios[1]+', rC = '+ratios[2]+'\n'+
            'strain rate = '+ep+r'$(s^{-1}) \ $'+ ', T = '+ T + ' K' +'\n' )
    plt.clim(lowerlim, upperlim);
    if args.s != None:
        plt.savefig(str(args.s+'.png'),dpi=500)
    plt.show()

if __name__ == '__main__':
    main()
