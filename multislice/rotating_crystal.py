from utils import displayStandards as dsp
from math import pi,sqrt
import matplotlib.pyplot as plt
import numpy as np



def orient_crystal(coords,ez=[0,0,1],n_u=[0,0,1],T=True):
    ''' Rotate the object so that n becomes e_z [1] :\n
    - coords : 3xN (or Nx3 array if T=True)
    - n : axis to align e_z against
    [1] [rotation matrix from axis and angle](https://en.wikipedia.org/wiki/Rotation_matrix#Rotation_matrix_from_axis_and_angle)
    '''
    e_z,n = np.array(ez)/np.linalg.norm(ez),np.array(n_u)/np.linalg.norm(n_u)
    n_not_ez = np.linalg.norm(n-e_z)
    if n_not_ez:
        u,ct = np.cross(n,e_z), np.dot(e_z,n)
        u /= np.linalg.norm(u)
        st = np.sqrt(1-ct**2)
        ux,uy,uz = u
        ux2,uy2,uz2 = u**2
        R = np.array([
            [ct+ux2*(1-ct), ux*uy*(1-ct)-uz*st, ux*uz*(1-ct)+uy*st ],
            [uy*ux*(1-ct)+uz*st, ct+uy2*(1-ct), uy*uz*(1-ct)-ux*st ],
            [uz*ux*(1-ct)-uy*st, uz*uy*(1-ct)+ux*st, ct+uz2*(1-ct) ],
            ])
        if T :
            coords = R.dot(coords.T).T
        else:
            coords = R.dot(coords)
    return coords


##########################################################################
### def : utils
def get_plane(n=[1,0,0],u=[0,1,0],w=1,h=1,x0=[0,0,0]):
    x,y = np.meshgrid([-w/2,w/2],[-h/2,h/2])
    u1,u2 = u,np.cross(n,u)
    Xp = x*u1[0] + y*u2[0] + x0[0]
    Yp = x*u1[1] + y*u2[1] + x0[1]
    Zp = x*u1[2] + y*u2[2] + x0[2]
    return Xp,Yp,Zp

def get_cylinder(ti,tf,r0=1,h=1,npts=10,x0=[0,0,0]):
    t,z,h2 = np.linspace(ti,tf,npts),np.array([-1,1])[:,None],h/2
    Xc = r0*np.tile(np.cos(t),[2,1])  + x0[0]
    Yc = r0*np.tile(np.sin(t),[2,1])  + x0[1]
    Zc = h2*np.tile(z,[1,npts]) + x0[2]
    return Xc,Yc,Zc

##########################################################################
#def:figures
##########################################################################
def get_cubic_cell_mesh(lat_params,opt=0):
    a1,a2,a3 = lat_params
    #Cube faces
    (x00,y00),z00 = np.meshgrid([0,a1],[0,a2]), np.zeros((2,2))
    (x10,z10),y10 = np.meshgrid([0,a1],[0,a2]), np.zeros((2,2))
    (y20,z20),x20 = np.meshgrid([0,a2],[0,a3]), np.zeros((2,2))
    (x01,y01),z01 = np.meshgrid([0,a1],[0,a2]), np.ones((2,2))*a3
    (x11,z11),y11 = np.meshgrid([0,a1],[0,a3]), np.ones((2,2))*a2
    (y21,z21),x21 = np.meshgrid([0,a2],[0,a3]), np.ones((2,2))*a1
    if opt:
        Xfaces = [  np.array([x00,x10,x20,x01,x11,x21]),
                    np.array([y00,y10,y20,y01,y11,y21]),
                    np.array([z00,z10,z20,z01,z11,z21]),]
    else:
        Xfaces = [[x00,y00,z00],[x10,y10,z10],[x20,y20,z20],
                  [x01,y01,z01],[x11,y11,z11],[x21,y21,z21]]

    return Xfaces
def show_unit_cell(ax,n=[0,0,1],a=0.2,c='b',lw=2,lat_params=[1,1,1]):
    Xfaces = get_cubic_cell_mesh(lat_params)
    #chnage cube orientation and plot
    for X,i in zip(Xfaces,range(len(Xfaces))) :
        x,y,z = X
        coords = np.array([x,y,z]).reshape(3,4).T
        coords = orient_crystal(coords,n_u=n)
        x,y,z  = coords.T.reshape(3,2,2)
        Xfaces[i] = [x,y,z]
        ax.plot_surface(x,y,z,color=c,alpha=a+(i==0)*0.2,linewidth=lw,edgecolor=c)
    #cube diagonals
    (x0,x1),(y0,y1),(z0,z1) = np.array(Xfaces[0])[:,:,0]
    (x2,x3),(y2,y3),(z2,z3) = np.array(Xfaces[3])[:,:,1]
    ax.plot([x0,x3],[y0,y3],[z0,z3],'--',color=dsp.unicolor(0.5))
    ax.plot([x1,x2],[y1,y2],[z1,z2],'--',color=dsp.unicolor(0.5))

# def show_trihedron(ax,x0=[0,0,0],cs=None,labs=None,lw=2,ll=1.0,rc=0.1,h=0.2):
#     '''
#     x0 : position of trihedron
#     ll,rc,h : length,radius and height af arrow/cones
#     cs,labs : colors and labels of cones (default black and None)
#     '''
#     txts,x0=[],np.array(x0)
#     if not cs : cs=['k']*3
#     if labs :
#         xtxt = x0 + 1.1*ll*np.diag([1,1,1]);#print(xtxt)
#         for i in range(3):
#             xt0,yt0,zt0 = xtxt[i,:]
#             txts += [[xt0,yt0,zt0,labs[i],cs[i]]]
#     cx,cy,cz = cs
#     u = np.linspace(0,2*np.pi,15)
#     v = np.linspace(0,np.pi/2,2)
#     x = rc*np.outer(np.cos(u),np.sin(v))
#     y = rc*np.outer(np.sin(u),np.sin(v))
#     z = h*np.outer(np.ones(u.shape),np.cos(v))
#     (xlx,xly,xlz) = (np.array([[0,ll],[0,0],[0,0]]).T + x0).T
#     (ylx,yly,ylz) = (np.array([[0,0],[0,ll],[0,0]]).T + x0).T
#     (zlx,zly,zlz) = (np.array([[0,0],[0,0],[0,ll]]).T + x0).T
#     plots = [[xlx,xly,xlz,cx],
#              [ylx,yly,ylz,cy],
#              [zlx,zly,zlz,cz],]
#     surfs = [[x0[0]+z+ll    ,x0[1]+x    ,x0[2]+y    ,cx,None,lw,cx],
#              [x0[0]+x       ,x0[1]+z+ll ,x0[2]+y    ,cy,1,lw,cy],
#              [x0[0]+x       ,x0[1]+y    ,x0[2]+z+ll ,cz,1,lw,cz],]
#     dsp.stddisp(ax=ax,texts=txts,plots=plots,surfs=surfs,lw=lw,std=0)

def show_trihedron(ax,uvw=None,x0=[0,0,0],cs=None,labs=None,lw=2,rc=0.1,h=0.2):
    '''
    x0 : position of trihedron
    uvw : 3x3 ndarray
    ll,rc,h : length,radius and height af arrow/cones
    cs,labs : colors and labels of cones (default black and None)
    '''
    if not isinstance(uvw,np.ndarray) : uvw = np.identity(3)
    txts,x0=[],np.array(x0)
    if not cs : cs=['k']*3
    if labs :
        xtxt = x0 + 1.1*uvw
        for i in range(3):
            xt0,yt0,zt0 = xtxt[i,:]
            txts += [[xt0,yt0,zt0,labs[i],cs[i]]]
    plots,surfs = [],[]
    for u,cu in zip(uvw,cs) :
        (x,y,z),(xl,yl,zl) = get_arrow_3d(u,x0,rc=0.1,h=0.2)
        plots += [[xl,yl,zl,cu]]
        surfs += [[x,y,z,cu,None,lw,cu]]
    dsp.stddisp(ax=ax,texts=txts,plots=plots,surfs=surfs,lw=lw,std=0)


def get_arrow_3d(n,x0,rc=0.1,h=0.2):
    nu,nv = 15,2; #print(u)
    shape = (nu,nv)
    u = np.linspace(0,2*np.pi,nu)
    v = np.linspace(0,np.pi/2,nv)
    x = np.outer(np.cos(u),np.sin(v))*h/2
    y = np.outer(np.sin(u),np.sin(v))*h/2
    z = np.outer(np.ones(u.shape),np.cos(v))*h
    coords = np.array([x.flatten(),y.flatten(),z.flatten()]);#print(coords.shape)
    #uvec = np.array(n);print(n)
    x,y,z = orient_crystal(coords,n,[0,0,1],T=False)
    x,y,z = np.reshape(x,shape),np.reshape(y,shape),np.reshape(z,shape)

    O = np.array([0,0,0]);#print(x0)#,x0 + np.array([O,n]))
    xl,yl,zl = (x0 + np.array([O,n])).T ;#print(xl,yl,zl)
    return [x+x0[0]+n[0],y+x0[1]+n[1],z+x0[2]+n[2]],[xl,yl,zl]


def show_diffraction_planes(r0=1,h=2,npts=10,**kwargs):
    n10,n01,n11,u = [1,0],[0,1],np.array([1,-1])/sqrt(2),[0,0,1]
    Xc0,Yc0,Zc0=get_cylinder(0,pi/2 ,r0,h,npts)
    Xc1,Yc1,Zc1=get_cylinder(pi,3*pi/2,r0,h,npts)
    Xp10,Yp10,Zp10=get_plane(n10,u,w=2*r0,h=h)
    Xp01,Yp01,Zp01=get_plane(n01,u,w=2*r0,h=h)
    Xp11,Yp11,Zp11=get_plane(n11,u,w=2*r0,h=h)
    fig,ax=dsp.stddisp(rc='3d',legOpt=0)
    ax.plot_surface(Xc0, Yc0, Zc0, color='b', alpha=0.2)#,edgecolor='b',linewidth=2)#
    ax.plot_surface(Xc1, Yc1, Zc1, color='b', alpha=0.2 )#,edgecolor='b',linewidth=2)#
    ax.plot_surface(Xp10, Yp10, Zp10, color='b', alpha=0.2,linewidth=2,edgecolor='b'   )#
    ax.plot_surface(Xp01, Yp01, Zp01, color='b', alpha=0.2,linewidth=2,edgecolor='b'   )#
    ax.plot_surface(Xp11, Yp11, Zp11, color='r', alpha=0.4,linewidth=2,edgecolor='r'   )#
    ax.plot([0,0],[0,0],[-h/2,h/2],color ='k',linewidth=2)

    W = 0.75*max(2*r0,h)
    xylims = [-W/2,W/2,-W/2,W/2,-W/2,W/2]
    dsp.standardDisplay(ax,xylims=xylims,axPos=[0,0,1,1],setPos=1,is_3d=1,gridOn=0,ticksOn=0,legOpt=0,**kwargs)

########################################################################
# def : test
########################################################################
def bcc_coords():
    (x,y,z),xc  = np.meshgrid([0,1],[0,1],[0,1]), [0.5,0.5,0.5] #bcc
    coords = np.array([x.flatten(),y.flatten(),z.flatten()]).T
    coords = np.concatenate((coords,[xc]),axis=0)
    return coords

def test_orient(n=[1,1,1],**kwargs):
    coords = bcc_coords()
    coords = orient_crystal(coords,n)
    scat    = coords.T.tolist()
    fig,ax  = dsp.stddisp(scat=scat,ms=100,rc='3d',opt='',legOpt=0)
    show_unit_cell(ax,n,a=0.1,c='b',lw=2)
    W = np.sqrt(3);xylims = [-W/2,W/2,-W/2,W/2,0,W]
    dsp.standardDisplay(ax,xylims=xylims,gridOn=0,ticksOn=0,legOpt=0,**kwargs)

def _test_trihedron():
    fig,ax = dsp.stddisp(rc='3d',std=0)
    show_trihedron(ax,x0=[0,0,0],cs=None,labs=None,
        lw=1,rc=0.1,h=0.2)
    uvw = np.array([[1,0,0],[0,2,2],[1,1,1]])
    show_trihedron(ax,uvw,x0=[-2,-2,-2],cs=['r','g','b'],labs=['$x$','$y$','$z$'],
        lw=2,rc=0.1,h=0.2)
    dsp.stddisp(ax=ax,pOpt='e',opt='p')

def _test_get_arrow():
    #N = 1
    U = np.array([[0,1,1],[1,1,1],[1,0,1]])
    x0 = [0,0,1]
    cs,lw = dsp.getCs('viridis',U.shape[0]),2
    plots,surfs = [],[]
    for u,cu in zip(U,cs) :
        (x,y,z),(xl,yl,zl) = get_arrow_3d(u,x0,rc=0.1,h=0.2)
        plots += [[xl,yl,zl,cu]]
        surfs += [[x,y,z,cu,None,lw,cu]]

    dsp.stddisp(rc='3d',plots=plots,surfs=surfs,lw=lw,pOpt='e')#,texts=txts)

if __name__ == "__main__":
    plt.close('all')
    #_test_get_arrow()
    #show_diffraction_planes(name='figures/cylinder.png',figopt='t2', opt='p')
    #test_orient(n=[0,0,1],name='docs_fig/orient_crystal001.png',figopt='2',view=[10,-30],opt='p')#;dsp.crop_fig('docs_fig/orient_crystal001.png',[800,800,600,500])
    #test_orient(n=[1,1,0],name='docs_fig/orient_crystal110.png',figopt='2',view=[10,-30],opt='p')#;dsp.crop_fig('docs_fig/orient_crystal110.png',[800,800,300,400])
    #test_orient(n=[1,1,1],name='docs_fig/orient_crystal111.png',figopt='2',view=[10,-30],opt='p')#;dsp.crop_fig('docs_fig/orient_crystal111.png',[800,800,450,350])
    _test_trihedron()
