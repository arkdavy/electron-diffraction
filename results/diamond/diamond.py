from utils import*                  #;imp.reload(dsp)
from EDutils import viewers as vw       ;imp.reload(vw)
from multislice import postprocess as pp#;imp.reload(pp)
from multislice import multislice as ms ;imp.reload(ms)
from blochwave import bloch as bl       #;imp.reload(bl)

plt.close('all')
opts = 'v'
path = 'dat/'

# v = vw.Viewer(path='dat',cif_file='diamond',init_opts='R')
if 'v' in opts:
    v = vw.Viewer(config=path+'config.pkl')



if 'b' in opts:
    tag='fft0-'
    multi = pp.load(path+'multi',tag+'001')
    fig,ax = multi.beam_vs_thickness(bOpt='O',opt='')
    # fig,ax = multi.beam_vs_thickness(tol=1e-3,opt='')
    bloch = bl.load_Bloch(path+'bloch/',tag+'0001')
    bloch.set_beams_vs_thickness((0,350,1000))#bloch.solve()
    bloch.show_beams_vs_thickness(ax=ax,linespec='--')

if 'i' in opts:
    multi = pp.load(path+'multi','2beams001')
    idx = np.array([[512,613],[512,512]])
    args = {'Iopt':'csn','Imax':5e4,'gs':0.025,'rmax':25,'Nmax':512}
    multi.integrate_reflections(idx,N=5,**args)
