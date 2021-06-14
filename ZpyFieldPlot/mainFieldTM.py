from funcFile import *

tic = time()
#time1=fix(clock);                   # start time, [sec]
c0 = 299792458;                   # speed of light in vacuum, [m/s]
e0=8.854187817e-12;         # vacuum permittivity 
mu0=pi*4e-7;                        # vacuum permeability

theta =(0)*pi/180;                # angle of incidence, [rad]
lambdaX=1.95;                        # wavelength in vacuum, [um]
wn=1e4/lambdaX;                  # wavenumber, [cm-1]
w = 1e6*2*pi*c0/lambdaX; # angular frequency, [rad/s]
k0 = 2*pi/lambdaX;               #wavevector
d = array([1,0.8,1])                        # thickness of each layer [um] 
N = len(d);                      # # of layers
Period =zeros([N])
Period[0:N] =0.4;                 # Period [um]
width =array([0,0.2,0])                 # width of metal strips, [um]
psi = width/Period[0]       # filling ratio of each layer
f1 = array([0,0.75,0])                     # normalized position for left-end of metal strip
f2 = f1+psi;                           # normalized position for right-end of metal strip
Num_ord = 101                # number for the highest diffraction order
e = zeros([2])
e[0] = 1;
e_m = zeros([N],dtype = complex)
e_m[0:N] = Ag(lambdaX)


e_d = zeros([N],dtype = complex)
e_d[0:N] = 1+complex(0,1)*1e-12;
e[1]= 1
Ref, Tran,W,V,Cnp,Cnn,E,Sigma,Kx = RCWA_Multi_TM(N,\
                    e_m, e_d, f1, f2, Period, d, e, lambdaX, theta, Num_ord)
x=linspace(0,Period[0],19);
layernum=np.array([50,30,50]) # The discritized number for each layer from the incident medium to substrate

z = np.zeros([N],dtype = object)
for ind in range(N):
    z[ind]=linspace(0,d[ind],layernum[ind]);

extrad = np.zeros([N])
extrad[0]=0;
for indd in range(1,len(d)):
    extrad[indd]=extrad[indd-1]+d[indd-1];

n1=np.min(np.where(x>0.25*Period[0])[0]) +1
n2=np.max(np.where(x<0.75*Period[0])[0]) + 1;
e2=np.hstack([ones([n1-1])*e_m[1],ones([n2-n1+1])*e_d[1],ones(len(x)-n2)*e_m[1]])



Ix = np.zeros([len(x),sum(layernum)],dtype = complex)

Mag = np.zeros([len(x),sum(layernum)],dtype = complex)

Iz = np.zeros([len(x),sum(layernum) ],dtype = complex)

realz =  np.zeros([1,sum(layernum)],dtype = complex)
i = complex(0,1)
for ind in range(N):
    W1=W[ind];    
    V1=V[ind];
    for indz in range(len(z[ind])):
        print(indz)
        zz=z[ind]; # current matrix for z cooridinate 
        Hy=W1@(diag(diag(exp(Sigma[ind]*k0*(zz[indz]-d[ind])))\
               )@Cnp[ind]+diag(diag(exp(-Sigma[ind]*k0*zz[indz])))@Cnn[ind]);  
        Dx=-i/c0/e0*W1@diag(diag(Sigma[ind]))@\
            (diag(diag(exp(Sigma[ind]*k0*(zz[indz]-d[ind])))\
             )@Cnp[ind]-diag(diag(exp(-Sigma[ind]*k0*zz[indz])))@Cnn[ind]);
        Ez=1/e0/c0* linalg.inv(E[ind])@(Kx@Hy);  
        Kxcolumn=diag(Kx);
        Kxcolumn = Kxcolumn.reshape(len(Kxcolumn),1)
        B=exp(i*k0*(Kxcolumn.reshape(len(Kxcolumn),1 ) @ x.reshape(1,len(x)))); 
        
        Magnety=conj(Hy.T)@B;  
        Disx=conj(Dx.T)@B;
        
        if ind ==1:
            Electx=Disx/e2;
        else:
            Electx=Disx/e_d[ind]
        
        Electz=conj(Ez.T)@B;  
        
        Magnetz=zeros([1,len(x)]);
        Magnetx=zeros([1,len(x)]);
        Electy=zeros([1,len(x)]);
        
        MagnitudeH=((np.abs(Magnety)**2));
        MagnitudeE=((np.abs(Electy)**2))
        
        Ix[0:len(x),sum(layernum[0:ind])+indz]=Magnetx; 
        Iz[0:len(x),sum(layernum[0:ind])+indz]=-Magnetz; 
        Mag[0:len(x),sum(layernum[0:ind])+indz]=log10(MagnitudeH);
        realz[0,sum(layernum[0:ind])+indz]=extrad[N-1]-(zz[indz]+extrad[ind]); # convert the coordinate for later plotting
 
X,Y = np.meshgrid(real(x), real(realz))


Z = real(Mag.T)

plt.pcolor(X, Y, Z, cmap='hot',shading = 'flat')
plt.show()