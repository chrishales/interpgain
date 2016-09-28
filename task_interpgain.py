from taskinit import *
import numpy as np

# Copyright (c) 2016, Christopher A. Hales
# All rights reserved.
#
# BSD 3-Clause Licence
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * The NAMES OF ITS CONTRIBUTORS may not be used to endorse or promote
#       products derived from this software without specific prior written
#       permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL C. A. HALES BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# HISTORY:
#   1.0  28Sep2016  Initial version.
#

def interpgain(caltable,obsid,field,extrapolate):

    #
    # Task interpgain
    #
    #    Linearly interpolate missing gain solutions,
    #    overwriting the input caltable.  Optionally
    #    perform extrapolation.
    #    Christopher A. Hales
    #
    #    Version 1.0 (tested with CASA Version 4.6.0)
    #    28 September 2016
    
    casalog.origin('interpgain')
    
    if not obsid.isdigit():
        casalog.post('*** ERROR: This version does not support multiple OBSERVATION_ID selection.', 'ERROR')
        casalog.post('*** ERROR: Exiting interpgain.', 'ERROR')
        return
    
    if not field.isdigit():
        casalog.post('*** ERROR: This version does not support multiple FIELD_ID selection.', 'ERROR')
        casalog.post('*** ERROR: Exiting interpgain.', 'ERROR')
        return
    
    selection0='OBSERVATION_ID=='+obsid+'&&FIELD_ID=='+field
    
    tb.open(caltable,nomodify=False)
    
    subt=tb.query(selection0)
    spw=subt.getcol('SPECTRAL_WINDOW_ID')
    ant=subt.getcol('ANTENNA1')
    subt.done()
    
    for a in np.unique(ant):
        for s in np.unique(spw):
            selection=selection0+'&&ANTENNA1=='+str(a)+'&&SPECTRAL_WINDOW_ID=='+str(s)
            subt=tb.query(selection)
            timecol=subt.getcol('TIME')
            cparam=subt.getcol('CPARAM')
            flag=subt.getcol('FLAG')
            for p in range(2):
                if (np.sum(flag[p,0])>0) & (np.sum(flag[p,0])<=len(timecol)-2):
                    # interpolate amp and phase separately
                    amp   = np.abs(cparam[p,0])
                    phase = np.angle(cparam[p,0])
                    amp[flag[p,0]==True]   =  np.interp(timecol[flag[p,0]==True],  \
                                                        timecol[flag[p,0]==False],amp[flag[p,0]==False])
                    phase[flag[p,0]==True] = (np.interp(timecol[flag[p,0]==True],  \
                                                        timecol[flag[p,0]==False], \
                                                        np.unwrap(phase[flag[p,0]==False])) + np.pi) % \
                                             (2 * np.pi ) - np.pi
                    if extrapolate:
                        cparam[p,0] = amp * np.exp(phase*1j)
                        flag[p,0]   = False
                    else:
                        indxMIN = np.where(flag[p,0]==False)[0][0]
                        indxMAX = np.where(flag[p,0]==False)[0][-1]
                        cparam[p,0,indxMIN+1:indxMAX] = amp[indxMIN+1:indxMAX] * \
                                                        np.exp(phase[indxMIN+1:indxMAX]*1j)
                        flag[p,0,indxMIN+1:indxMAX]   = False
            
            subt.putcol('CPARAM',cparam)
            subt.putcol('FLAG',flag)
            subt.done()
    
    tb.done()
