# File viewer tab for bfit
# Derek Fujimoto
# Nov 2017

from tkinter import *
from tkinter import ttk
from multiprocessing import Process, Pipe
from bfit.gui.calculator_nqr_B0 import current2field
from bfit.backend.fitdata import fitdata
from bdata import bdata
from bfit import logger_name

import numpy as np
import matplotlib.pyplot as plt
import sys, os, time, glob, datetime
import logging


__doc__ = """
    View file contents tab.
    
    To-do:
        cumulative count viewing
    """

# =========================================================================== #
class fileviewer(object):
    """
        Data fields:
            asym_type: drawing style
            bfit: bfit object
            data: bdata object for drawing
            entry_asym_type: combobox for asym calculations
            fig_list: list of figures
            is_updating: True if update draw
            runn: IntVar() run number
            text: Text widget for displaying run information
            update_id: string, run id for the currently updating run
            year: IntVar() year of exp 
    """
    
    default_export_filename = "%d_%d.csv" # year_run.csv
    update_id = ''
    
    # ======================================================================= #
    def __init__(self, file_tab, bfit):
        """ Position tab tkinter elements"""
        
        # get logger
        self.logger = logging.getLogger(logger_name)
        self.logger.debug('Initializing')
        
        # year and filenumber entry ------------------------------------------
        entry_frame = ttk.Frame(file_tab, borderwidth=1)
        self.year = IntVar()
        self.runn = IntVar()
        self.rebin = IntVar()
        self.bfit = bfit
        
        self.year.set(self.bfit.get_latest_year())
        self.rebin.set(1)
        
        entry_year = Spinbox(entry_frame, \
                from_=2000, to=datetime.datetime.today().year, 
                textvariable=self.year, width=5)
        self.entry_runn = Spinbox(entry_frame, \
                from_=0, to=50000, 
                textvariable=self.runn, width=7)
        self.runn.set(40000)
        
        # fetch button
        fetch = ttk.Button(entry_frame, text='Fetch', command=self.get_data)
            
        # draw button
        draw = ttk.Button(entry_frame, text='Draw', 
                          command=lambda:self.draw(figstyle='inspect'))
        
        # grid and labels
        entry_frame.grid(column=0, row=0, sticky=N)
        ttk.Label(entry_frame, text="Year:").grid(column=0, row=0, sticky=E)
        entry_year.grid(column=1, row=0, sticky=E)
        ttk.Label(entry_frame, text="Run Number:").grid(column=2, row=0, sticky=E)
        self.entry_runn.grid(column=3, row=0, sticky=E)
        fetch.grid(column=4, row=0, sticky=E)
        draw.grid(column=5, row=0, sticky=E)
        
        # padding 
        for child in entry_frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        # viewer frame -------------------------------------------------------
        view_frame = ttk.Frame(file_tab, borderwidth=2)
        
        self.text_nw = Text(view_frame, width=88, height=20, state='normal')
        self.text_ne = Text(view_frame, width=88, height=20, state='normal')
        self.text_sw = Text(view_frame, width=88, height=20, state='normal')
        self.text_se = Text(view_frame, width=88, height=20, state='normal')
        
        ttk.Label(view_frame, text="Run Info").grid(column=0, row=0, sticky=N, pady=5)
        ttk.Label(view_frame, text="PPG Parameters").grid(column=1, row=0, sticky=N, pady=5)
        ttk.Label(view_frame, text="Camp").grid(column=0, row=2, sticky=N, pady=5)
        ttk.Label(view_frame, text="EPICS").grid(column=1, row=2, sticky=N, pady=5)
        
        self.text_nw.grid(column=0, row=1, sticky=(N, W, E, S), padx=5)
        self.text_ne.grid(column=1, row=1, sticky=(N, W, E, S), padx=5)
        self.text_sw.grid(column=0, row=3, sticky=(N, W, E, S), padx=5)
        self.text_se.grid(column=1, row=3, sticky=(N, W, E, S), padx=5)
        
        view_frame.grid(column=0, row=1, sticky=(N, E, W))
        
        # details frame: stuff at the bottom ----------------------------------
        details_frame = ttk.Frame(file_tab)
        entry_rebin = Spinbox(details_frame, from_=1, to=100, width=3, \
                textvariable=self.rebin)
        
        # update check box
        self.is_updating = BooleanVar()
        self.is_updating.set(False)
        update_box = ttk.Checkbutton(details_frame, text='Periodic Redraw', 
                command=self.do_update, variable=self.is_updating, onvalue=True, 
                offvalue=False)

        # asymmetry type combobox
        self.asym_type = StringVar()
        self.asym_type.set('')
        self.entry_asym_type = ttk.Combobox(details_frame, \
                textvariable=self.asym_type, state='readonly', width=25)
        self.entry_asym_type['values'] = ()
                
        # gridding
        ttk.Label(details_frame, text="Rebin:").grid(column=0, row=0, sticky=E)
        entry_rebin.grid(column=1, row=0, sticky=E)
        self.entry_asym_type.grid(column=2, row=0, sticky=E)
        update_box.grid(column=3, row=0, sticky=E)
        details_frame.grid(column=0, row=2, sticky=S)
        
        # padding 
        for child in details_frame.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
            
        # resizing
        file_tab.grid_rowconfigure(1, weight=1)
        file_tab.grid_columnconfigure(0, weight=1)
        
        entry_frame.grid_columnconfigure(0, weight=2)
        entry_frame.grid_columnconfigure(2, weight=1)
        entry_frame.grid_rowconfigure(0, weight=1)
        
        for i in range(2):
            view_frame.grid_columnconfigure(i, weight=1)
        view_frame.grid_rowconfigure(1, weight=1)
        view_frame.grid_rowconfigure(3, weight=1)
        
        for t in [self.text_nw, self.text_ne, self.text_sw, self.text_se]:
            for i in range(5):
                t.grid_columnconfigure(i, weight=1)
                t.grid_rowconfigure(i, weight=1)
            
        self.logger.debug('Initialization success.')
            
    # ======================================================================= #
    def __del__(self):
        pass
        
    # ======================================================================= #
    def _get_latest_run(self, year, run):
        """
            Get run number of latest run in local file system, given an initial 
            part of the run number
        """
        
        runlist = []
            
        # look for latest run by run number
        for d in [self.bfit.bnmr_archive_label, self.bfit.bnqr_archive_label]:
            dirloc = os.environ[d]
            runlist.extend(glob.glob(os.path.join(dirloc, str(year), '0%d*.msr'%run)))
        runlist = [int(os.path.splitext(os.path.basename(r))[0]) for r in runlist]
        
        # get latest run by max run number
        try:
            run = max(runlist)
        except ValueError:
            self.logger.exception('Run fetch failed')
            for t in [self.text_nw, self.text_ne, self.text_sw, self.text_se]:
                self.set_textbox_text(t, 'Run not found.')  
            return False
        else:
            return run
        
    # ======================================================================= #
    def draw(self, figstyle, quiet=False):
        """Get data then draw."""
        self.bfit.logger.info('Draw button pressed')
        
        if self.get_data(quiet=quiet):
            self.bfit.draw(self.data, 
                    self.bfit.asym_dict[self.asym_type.get()], rebin=self.rebin.get(), 
                    label=self.bfit.get_label(self.data), 
                    figstyle=figstyle)
            
    # ======================================================================= #
    def draw_diagnostics(self): #incomplete
        """
            Get data then draw in debug mode.
        """
        
        # isssue with data fetch
        if not self.get_data(quiet=quiet):
            return
        
        # get data
        dat = self.data
    
        # make figure
        fix, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=2, ncols=2)
    
        # get asym
        a = data.asym(hist_select=self.bit.hist_select)
        x = a[self.x_tag[data.mode]]
        xlabel = self.xlabel_dict[data.mode]
            
        # draw 2e mode 
        if '2e' == dat.mode:
            pass 
            
        # draw TD mode
        elif '2' in dat.mode:
            
            # draw combined asym -------------------------
            tag = a.c[0]!=0 # remove zero asym
            ax1.errorbar(x[tag], a.c[0][tag], a.c[1][tag])
            ax1.set_xlabel(xlabel)
            ax1.set_ylabel(self.bfit.ylabel_dict['c'])
            
            # draw split asym ----------------------------
            
            # remove zero asym
            ap = a.p[0]
            an = a.n[0]
            tag_p = ap!=0
            tag_n = an!=0
            tag_cmb = tag_p*tag_n
            
            # get average
            avg = np.mean(ap[tag_cmb]+an[tag_cmb])/2
            
            # draw
            ax2.errorbar(x[tag_p], ap[tag_p], a.p[1][tag_p], label='+')
            ax2.errorbar(x[tag_n], an[tag_n], a.n[1][tag_n], label="-")
            ax2.axhline(avg, color='k', linestyle='--')
            ax2.set_xlabel(xlabel)
            ax2.set_ylabel(self.bfit.ylabel_dict['h'])
        
            # draw histograms  --------------------------
            hist = data.hist
            
            # draw
            keylist = ('F+', 'F-', 'B+', 'B-', 'L+', 'R+', 'L-', 'R-', 
                         'NBMF+', 'NBMF-', 'NBMB+', 'NBMB-', 'AL0+', 'AL0-')
            for i, h in enumerate(keylist):
                
                # get bins
                try:
                    x = np.arange(len(hist[h].data))
                except KeyError:
                    continue
                
                # check for non-empty histograms, then draw
                if np.mean(hist[h].data) > 0:                        
                    ax3.plot(x, hist[h].data, label=h)
                    
            ax3.ylabel(self.bfit.ylabel_dict['rhist'])
            ax3.xlabel('Bin')
        
        # draw TI mode
        elif '1' in dat.mode:
            pass
        
        # unknown mode
        else:
            raise RuntimeError('Unknown mode type')
    
    # ======================================================================= #
    def export(self):
        """Export data as csv"""
        
        self.logger.info('Export button pressed')
        
        # get data
        if not self.get_data():
            return
        data = self.data
        
        # get filename 
        filename = filedialog.asksaveasfilename(
                initialfile=self.default_export_filename%(data.year, data.run), 
                filetypes=[('csv', '*.csv'), 
                           ('allfiles', '*')], 
                defaultextension='.csv')
        
        # write to file
        if filename:
            self.bfit.export(data, filename, rebin=self.rebin.get())
    
    # ======================================================================= #
    def get_data(self, quiet=False):
        """
            Display data and send bdata object to bfit draw list. 
            Return True on success, false on Failure
        """
        
        # settings
        mode_dict = {"1f":"Frequency Scan", 
                     "1w":"Frequency Comb", 
                     "1n":"Rb Cell Scan", 
                     "1e":"Field Scan", 
                     "20":"SLR", 
                     '2h':'SLR with Alpha Tracking', 
                     '2s':'Spin Echo', 
                     '2e':'Randomized Frequency Scan'}
        
        # fetch year
        try:
            year = self.year.get()
        except ValueError:
            for t in [self.text_nw, self.text_ne, self.text_sw, self.text_se]:
                self.set_textbox_text(t, 'Year input must be integer valued')  
                self.logger.exception('Year input must be integer valued')
            return False
        
        # fetch run number
        run = self.runn.get()
        
        self.logger.debug('Parsing run input %s', run)
        
        if run < 40000:
            run = self._get_latest_run(year, run)
            if run is False:
                return False
        
        self.logger.info('Fetching run %s from %s', run, year)
        
        # get data
        try: 
            data = fitdata(self.bfit, bdata(run, year=year))
        except ValueError:
            self.logger.exception('File read failed.')
            for t in [self.text_nw, self.text_sw, self.text_se, self.text_ne]:
                self.set_textbox_text(t, 'File read failed.')
            return False
        except RuntimeError:
            self.logger.exception('File does not exist.')
            for t in [self.text_nw, self.text_sw, self.text_se, self.text_ne]:
                self.set_textbox_text(t, 'File does not exist.')
            return False
        
        # set data field
        self.data = data
        
        # set draw parameters
        self.bfit.set_asym_calc_mode_box(data.mode, self, data.area)
        
        # set nbm variable
        self.set_nbm()
        
        # quiet mode: don't update text
        if quiet: return True
        
        # NE -----------------------------------------------------------------
        
        # get data: headers
        mode = mode_dict[data.mode]
        try:
            if data.ppg.rf_enable.mean and data.mode == '20' and \
                                                        data.ppg.rf_on.mean > 0:
                mode = "Hole Burning"
        except AttributeError:
            pass
        
        mins, sec = divmod(data.duration, 60)
        duration = "%dm %ds" % (mins, sec)
        
        # set dictionary
        data_nw =  {"Run":'%d (%d)' % (data.run, data.year), 
                    "Area": data.area, 
                    "Run Mode": "%s (%s)" % (mode, data.mode), 
                    "Title": data.title, 
                    "Experimenters": data.experimenter, 
                    "Sample": data.sample, 
                    "Orientation":data.orientation, 
                    "Experiment":str(data.exp), 
                    "Run Duration": duration, 
                    "Start": data.start_date, 
                    "End": data.end_date, 
                    "":"", 
                    }
        
        # set key order 
        key_order_nw = ['Run', 'Run Mode', 'Title', '', 
                        'Start', 'End', 'Run Duration', '', 
                        'Sample', 'Orientation', '', 
                        'Experiment', 'Area', 'Experimenters', 
                        ]
        
        # SW -----------------------------------------------------------------
        data_sw = {'':''}
        key_order_sw = []
                        
        # get data: temperature and fields
        try:
            temp = data.temperature.mean
            temp_stdv = data.temperature.std
            data_sw["Temperature"] = "%.2f +/- %.2f K" % (temp, temp_stdv)
            key_order_sw.append('Temperature')
        except AttributeError:
            pass
        
        try:
            curr = data.camp.smpl_current
            data_sw["Heater Current"] = "%.2f +/- %.2f A" % (curr.mean, curr.std)
            key_order_sw.append('Heater Current')
        except AttributeError:
            pass
        
        try:
            temp = data.camp.oven_readC.mean
            temp_stdv = data.camp.oven_readC.std
            data_sw['Oven Temperature'] = "%.2f +/- %.2f K" % (temp, temp_stdv)
            key_order_sw.append('Oven Temperature')
        except AttributeError:
            pass
        
        try:
            curr = data.camp.oven_current
            data_sw['Oven Current'] = "%.2f +/- %.2f A" % (curr.mean, curr.std)
            key_order_sw.append('Oven Current')
        except AttributeError:
            pass
        
        try: 
            field = np.around(data.camp.b_field.mean, 3)
            field_stdv = np.around(data.camp.b_field.std, 3)
            data_sw['Magnetic Field'] = "%.3f +/- %.3f T" % (field, field_stdv)
            key_order_sw.append('Magnetic Field')
        except AttributeError:
            pass
            
        try: 
            val = current2field(data.epics.hh_current.mean)
            data_sw['Magnetic Field'] = "%.3f Gauss" % val
            key_order_sw.append('Magnetic Field')
        except AttributeError:
            pass
            
        key_order_sw.append('')
                
        # cryo options
        try: 
            mass = data.camp.mass_read
            data_sw['Mass Flow'] = "%.3f +/- %.3f" % (mass.mean, mass.std)
            key_order_sw.append('Mass Flow')
        except AttributeError:
            pass
    
        try: 
            mass = data.camp.he_read
            data_sw['Mass Flow'] = "%.3f +/- %.3f" % (mass.mean, mass.std)
            key_order_sw.append('Mass Flow')
        except AttributeError:
            pass
    
        try: 
            cryo = data.camp.cryo_read
            data_sw['CryoEx Mass Flow'] = "%.3f +/- %.3f" % (cryo.mean, cryo.std)
            key_order_sw.append('CryoEx Mass Flow')
        except AttributeError:
            pass    
            
        try: 
            data_sw['Needle Setpoint'] = "%.3f turns" % data.camp.needle_set.mean
            key_order_sw.append('Needle Setpoint')
        except AttributeError:
            pass    
            
        try: 
            data_sw['Needle Readback'] = "%.3f turns" % data.camp.needle_pos.mean
            key_order_sw.append('Needle Readback')
        except AttributeError:
            pass    
            
        try:
            lift_set = np.around(data.camp.clift_set.mean, 3)
            data_sw['Cryo Lift Setpoint'] = "%.3f mm" % lift_set
            key_order_sw.append('Cryo Lift Setpoint')
        except AttributeError:
            pass
        
        try:
            lift_read = np.around(data.camp.clift_read.mean, 3)
            data_sw['Cryo Lift Readback'] = "%.3f mm" % lift_read
            key_order_sw.append('Cryo Lift Readback')
        except AttributeError:
            pass
    
        key_order_sw.append('')
        
        # rates and counts
        hist = ('F+', 'F-', 'B-', 'B+') if data.area == 'BNMR' \
                                     else ('L+', 'L-', 'R-', 'R+')
        try:     
            val = int(np.sum([data.hist[h].data for h in hist]))
            data_sw['Total Counts Sample'] = f'{val:,}'.replace(',', ' ')
            key_order_sw.append('Total Counts Sample')
        except (AttributeError, KeyError):
            pass
        
        try: 
            val = int(np.sum([data.hist[h].data for h in hist])/data.duration)
            data_sw['Rate Sample'] =  f'{val:,} (1/s)'.replace(',', ' ')
            key_order_sw.append('Rate Sample')
        except (AttributeError, KeyError):
            pass
        
        hist = ('F+', 'F-', 'B-', 'B+')    
        try: 
            val = int(np.sum([data.hist['NBM'+h].data for h in hist]))
            data_sw['Total Counts NBM'] = f'{val:,}'.replace(',', ' ')
            key_order_sw.append('Total Counts NBM')
        except (AttributeError, KeyError):
            pass
        
        try: 
            val = int(np.sum([data.hist['NBM'+h].data for h in hist])/data.duration)
            data_sw['Rate NBM'] = f'{val:,} (1/s)'.replace(',', ' ')
            key_order_sw.append('Rate NBM')
        except (AttributeError, KeyError):
            pass
            
        # rf dac
        if mode != 'SLR':
            key_order_sw.append('')
            try: 
                data_sw['rf_dac'] = "%d" % int(data.camp.rf_dac.mean)
                key_order_sw.append('rf_dac')
            except AttributeError:
                pass
            
            try: 
                data_sw['RF Amplifier Gain'] = "%.2f" % data.camp.rfamp_rfgain.mean
                key_order_sw.append('RF Amplifier Gain')
            except AttributeError:
                pass    
        
        # SE -----------------------------------------------------------------
        data_se = {'':''}
        key_order_se = []
            
        # get data: biases 
        try:
            if 'nqr_bias' in data.epics.keys():
                bias =      data.epics.nqr_bias.mean/1000.
                bias_std =  data.epics.nqr_bias.std/1000.
            elif 'nmr_bias' in data.epics.keys():
                bias =      data.epics.nmr_bias.mean
                bias_std =  data.epics.nmr_bias.std
            
            data_se["Platform Bias"] = "%.3f +/- %.3f kV" % \
                    (np.around(bias, 3), np.around(bias_std, 3))
            key_order_se.append("Platform Bias")
            
        except UnboundLocalError:
            pass
        
        try:
            data_se["BIAS15"] = "%.3f +/- %.3f V" % \
                    (np.around(data.epics.bias15.mean, 3), 
                     np.around(data.epics.bias15.std, 3))
            key_order_se.append('BIAS15')
        except AttributeError:
            pass
        
        # get data: beam energy
        try: 
            init_bias = data.epics.target_bias.mean
            init_bias_std = data.epics.target_bias.std
        except AttributeError:
            try:
                init_bias = data.epics.target_bias.mean
                init_bias_std = data.epics.target_bias.std
            except AttributeError:
                pass
            
        try:
            val = np.around(init_bias/1000., 3)
            std = np.around(init_bias_std/1000., 3)
            data_se["Initial Beam Energy"] = "%.3f +/- %.3f keV" % (val, std)
            key_order_se.append('Initial Beam Energy')
        except UnboundLocalError:
            pass
        
        # Get final beam energy
        try: 
            val = np.around(data.beam_kev, 3)
            std = np.around(data.beam_kev_err, 3)
            data_se['Implantation Energy'] = "%.3f +/- %.3f keV" % (val, std)
            key_order_se.append('Implantation Energy')
        except AttributeError:
            pass
        
        key_order_se.append('')
        
        # laser stuff
        try: 
            val = data.epics.las_pwr
            data_se['Laser Power'] = "%.3f +/- %.3f A" % (val.mean, val.std)
            key_order_se.append('Laser Power')
        except AttributeError:
            pass
        
        # magnet stuff
        try: 
            val = data.epics.hh_current.mean
            std = data.epics.hh_current.std
            data_se['Magnet Current'] = "%.3f +/- %.3f A" % (val, std)
            key_order_se.append('Magnet Current')            
        except AttributeError:
            pass
        
        # NE -----------------------------------------------------------------
        data_ne = {'':''}
        key_order_ne = []
        
        # get data: SLR data
        if data.mode in ['20', '2h']:
            try:
                dwell = int(data.ppg.dwelltime.mean)
                data_ne['Dwell Time'] = "%d ms" % dwell
                key_order_ne.append('Dwell Time')
            except AttributeError:
                pass
            
            try:    
                beam = int(data.ppg.prebeam.mean)            
                data_ne['Number of Prebeam Dwelltimes'] = "%d dwelltimes" % beam
                key_order_ne.append('Number of Prebeam Dwelltimes')
            except AttributeError:
                pass
            
            try:    
                beam = int(data.ppg.beam_on.mean)            
                data_ne['Number of Beam On Dwelltimes'] = "%d dwelltimes" % beam
                key_order_ne.append('Number of Beam On Dwelltimes')
            except AttributeError:
                pass
            
            try: 
                beam = int(data.ppg.beam_off.mean)
                data_ne['Number of Beam Off Dwelltimes'] = "%d dwelltimes" % beam
                key_order_ne.append('Number of Beam Off Dwelltimes')
            except AttributeError:
                pass
            
            try:    
                rf = int(data.ppg.rf_on_delay.mean)
                data_ne['RF On Delay'] = "%d dwelltimes" % rf
                key_order_ne.append('RF On Delay')
            except AttributeError:
                pass
            
            try:    
                rf = int(data.ppg.rf_on.mean)
                data_ne['RF On Duration'] = "%d dwelltimes" % rf
                key_order_ne.append('RF On Duration')
            except AttributeError:
                pass
            
            try:    
                hel = bool(data.ppg.hel_enable.mean)
                data_ne['Flip Helicity'] = str(hel)
                key_order_ne.append('Flip Helicity')
            except AttributeError:
                pass
            
            try:    
                hel = int(data.ppg.hel_sleep.mean)
                data_ne['Helicity Flip Sleep'] = "%d ms" % hel
                key_order_ne.append('Helicity Flip Sleep')
            except AttributeError:
                pass
        
            key_order_ne.append('')
            
            try:
                rf = bool(data.ppg.rf_enable.mean)
                data_ne['RF Enable'] = str(rf)
                key_order_ne.append('RF Enable')
                
                if rf:
                    freq = int(data.ppg.freq.mean)    
                    data_ne['Frequency'] = "%d Hz" % freq
                    key_order_ne.append('Frequency')
            except AttributeError:
                pass
            
        # get 1F specific data
        elif data.mode == '1f':
            try:
                val = int(data.ppg.dwelltime.mean)
                data_ne['Bin Width'] = "%d ms" % val
                key_order_ne.append('Bin Width')
            except AttributeError:
                pass
            
            try:    
                val = int(data.ppg.nbins.mean)
                data_ne['Number of Bins'] = "%d" % val
                key_order_ne.append('Number of Bins')
            except AttributeError:
                pass
            
            try:
                val = bool(data.ppg.const_t_btwn_cycl.mean)
                data_ne['Enable Const Time Between Cycles'] = str(val)
                key_order_ne.append('Enable Const Time Between Cycles')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.freq_start.mean)
                data_ne['Frequency Scan Start'] = '%d Hz' % val
                key_order_ne.append('Frequency Scan Start')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.freq_stop.mean)
                data_ne['Frequency Scan End'] = '%d Hz' % val
                key_order_ne.append('Frequency Scan End')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.freq_incr.mean)
                data_ne['Frequency Scan Increment'] = '%d Hz' % val
                key_order_ne.append('Frequency Scan Increment')
            except AttributeError:
                pass
            
            try:
                val = bool(data.ppg.hel_enable.mean)
                data_ne['Flip Helicity'] = str(val)
                key_order_ne.append('Flip Helicity')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.hel_sleep.mean)
                data_ne['Helicity Flip Sleep'] = "%d ms" % val
                key_order_ne.append('Helicity Flip Sleep')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.ncycles.mean)
                data_ne['Number of Cycles per Scan Increment'] = '%d' % val
                key_order_ne.append('Number of Cycles per Scan Increment')
            except AttributeError:
                pass
                
        # get 1E specific data
        elif data.mode == '1e':
            try:
                val = int(data.ppg.dwelltime.mean)
                data_ne['Bin Width'] = "%d ms" % val
                key_order_ne.append('Bin Width')
            except AttributeError:
                pass
            
            try:    
                val = int(data.ppg.nbins.mean)
                data_ne['Number of Bins'] = "%d" % val
                key_order_ne.append('Number of Bins')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.field_start.mean)
                data_ne['Field Scan Start'] = '%d G' % val
                key_order_ne.append('Field Scan Start')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.field_stop.mean)
                data_ne['Field Scan End'] = '%d G' % val
                key_order_ne.append('Field Scan End')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.field_incr.mean)
                data_ne['Field Scan Increment'] = '%d G' % val
                key_order_ne.append('Field Scan Increment')
            except AttributeError:
                pass
            
            try:
                val = bool(data.ppg.hel_enable.mean)
                data_ne['Flip Helicity'] = str(val)
                key_order_ne.append('Flip Helicity')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.hel_sleep.mean)
                data_ne['Helicity Flip Sleep'] = "%d ms" % val
                key_order_ne.append('Helicity Flip Sleep')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.ncycles.mean)
                data_ne['Number of Cycles per Scan Increment'] = '%d' % val
                key_order_ne.append('Number of Cycles per Scan Increment')
            except AttributeError:
                pass
                
        # get 1W specific data
        elif data.mode == '1w':
            try:
                val = int(data.ppg.dwelltime.mean)
                data_ne['Bin Width'] = "%d ms" % val
                key_order_ne.append('Bin Width')
            except AttributeError:
                pass
            
            try:    
                val = int(data.ppg.nbins.mean)
                data_ne['Number of Bins'] = "%d" % val
                key_order_ne.append('Number of Bins')
            except AttributeError:
                pass
            
            try:
                val = bool(data.ppg.const_t_btwn_cycl.mean)
                data_ne['Enable Const Time Between Cycles'] = str(val)
                key_order_ne.append('Enable Const Time Between Cycles')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.service_t.mean)
                data_ne['DAQ Service Time'] = "%d ms" % val
                key_order_ne.append('DAQ Service Time')
            except AttributeError:
                pass    
            
            try:
                val = int(data.ppg.xstart.mean)
                data_ne['Parameter x Start'] = '%d' % val
                key_order_ne.append('Parameter x Start')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.xstop.mean)
                data_ne['Parameter x Stop'] = '%d' % val
                key_order_ne.append('Parameter x Stop')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.xincr.mean)
                data_ne['Parameter x Increment'] = '%d' % val
                key_order_ne.append('Parameter x Increment')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.yconst.mean)
                data_ne['Parameter y (constant)'] = '%d' % val
                key_order_ne.append('Parameter y (constant)')
            except AttributeError:
                pass
                
            try:
                val = str(data.ppg.freqfn_f1.units)
                data_ne['CH1 Frequency Function(x)'] = val
                key_order_ne.append('CH1 Frequency Function(x)')
            except AttributeError:
                pass
            
            try:
                val = str(data.ppg.freqfn_f2.units)
                data_ne['CH2 Frequency Function(x)'] = val
                key_order_ne.append('CH2 Frequency Function(x)')
            except AttributeError:
                pass
            
            try:
                val = str(data.ppg.freqfn_f3.units)
                data_ne['CH3 Frequency Function(x)'] = val
                key_order_ne.append('CH3 Frequency Function(x)')
            except AttributeError:
                pass
            
            try:
                val = str(data.ppg.freqfn_f4.units)
                data_ne['CH4 Frequency Function(x)'] = val
                key_order_ne.append('CH4 Frequency Function(x)')
            except AttributeError:
                pass
             
            try:
                val = bool(data.ppg.hel_enable.mean)
                data_ne['Flip Helicity'] = str(val)
                key_order_ne.append('Flip Helicity')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.hel_sleep.mean)
                data_ne['Helicity Flip Sleep'] = "%d ms" % val
                key_order_ne.append('Helicity Flip Sleep')
            except AttributeError:
                pass        
            
            try:
                val = int(data.ppg.ncycles.mean)
                data_ne['Number of Cycles per Scan Increment'] = '%d' % val
                key_order_ne.append('Number of Cycles per Scan Increment')
            except AttributeError:
                pass
            
            try:
                val = bool(data.ppg.fref_enable.mean)
                data_ne['Freq Reference Enabled'] = str(val)
                key_order_ne.append('Freq Reference Enabled')
            except AttributeError:
                pass
         
            try:
                val = int(data.ppg.fref_scale.mean)
                data_ne['Freq Reference Scale Factor'] = '%d' % val
                key_order_ne.append('Freq Reference Scale Factor')
            except AttributeError:
                pass
            
        # get Rb Cell specific data
        elif data.mode in ['1n']:
            
            try:
                dwell = int(data.ppg.dwelltime.mean)
                data_ne['Bin Width'] = "%d ms" % dwell
                key_order_ne.append('Bin Width')
            except AttributeError:
                pass
            
            # get mode
            try: 
                custom_enable = bool(data.ppg.customv_enable.mean)
            except AttributeError:
                custom_enable = False
            
            # custom varible scan
            if custom_enable:
                
                try:
                    val = str(data.ppg.customv_name_write.units)
                    data_ne['EPICS variable name (for writing)'] = '%s' % val
                    key_order_ne.append('EPICS variable name (for writing)')
                except AttributeError:
                    pass
            
                try:
                    val = str(data.ppg.customv_name_read.units)
                    data_ne['EPICS variable name (for readback)'] = '%s' % val
                    key_order_ne.append('EPICS variable name (for readback)')
                except AttributeError:
                    pass
            
                try:
                    val = int(data.ppg.customv_scan_start.mean)
                    data_ne['Scan start value'] = '%d' % val
                    key_order_ne.append('Scan start value')
                except AttributeError:
                    pass
            
                try:
                    val = int(data.ppg.customv_scan_stop.mean)
                    data_ne['Scan stop value'] = '%d' % val
                    key_order_ne.append('Scan stop value')
                except AttributeError:
                    pass
            
                try:
                    val = int(data.ppg.customv_scan_incr.mean)
                    data_ne['Scan increment'] = '%d' % val
                    key_order_ne.append('Scan increment')
                except AttributeError:
                    pass
            
            # normal Rb cell scan
            else:
                try:
                    val = int(data.ppg.volt_start.mean)
                    data_ne['Start Rb Scan'] = '%d Volts' % val
                    key_order_ne.append('Start Rb Scan')
                except AttributeError:
                    pass
                
                try:    
                    val = int(data.ppg.volt_stop.mean)
                    data_ne['Stop Rb Scan'] = '%d Volts' % val
                    key_order_ne.append('Stop Rb Scan')
                except AttributeError:
                    pass
                
                try:
                    val = int(data.ppg.volt_incr.mean)
                    data_ne['Scan Increment'] = '%d Volts' % val
                    key_order_ne.append('Scan Increment')
                except AttributeError:
                    pass
                
            try:
                val = int(data.ppg.nbins.mean)
                data_ne['Number of Bins'] = '%d' % val
                key_order_ne.append('Number of Bins')
            except AttributeError:
                pass
                
            try:
                val = bool(data.ppg.hel_enable.mean)
                data_ne['Flip Helicity'] = str(val)
                key_order_ne.append('Flip Helicity')
            except AttributeError:
                pass
            
            try:
                val = int(data.ppg.hel_sleep.mean)
                data_ne['Helicity Flip Sleep'] = "%d ms" % val
                key_order_ne.append('Helicity Flip Sleep')
            except AttributeError:
                pass
        
        # get 2e mode specific data
        elif data.mode in ['2e']:
            
            try:
                val = int(data.ppg.rf_on_ms.mean)
                data_ne['RF On Time'] = "%d ms" % val
                key_order_ne.append('RF On Time')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.rf_on_delay.mean)
                data_ne['Number of RF On Delays'] = "%d" % val
                key_order_ne.append('Number of RF On Delays')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.beam_off_ms.mean)
                data_ne['Beam Off Time'] = "%d ms" % val
                key_order_ne.append('Beam Off Time')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.ndwell_post_on.mean)
                data_ne['Number of post RF BeamOn Dwelltimes'] = "%d" % val
                key_order_ne.append('Number of post RF BeamOn Dwelltimes')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.ndwell_per_f.mean)
                data_ne['Number of Dwelltimes per Frequency'] = "%d" % val
                key_order_ne.append('Number of Dwelltimes per Frequency')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.freq_start.mean)
                data_ne['Frequency Scan Start'] = "%d Hz" % val
                key_order_ne.append('Frequency Scan Start')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.freq_stop.mean)
                data_ne['Frequency Scan Stop'] = "%d Hz" % val
                key_order_ne.append('Frequency Scan Stop')
            except AttributeError:
                pass
                
            try:
                val = int(data.ppg.freq_incr.mean)
                data_ne['Frequency Scan Increment'] = "%d Hz" % val
                key_order_ne.append('Frequency Scan Increment')
            except AttributeError:
                pass
                
            try:
                val = bool(data.ppg.rand_freq_val.mean)
                data_ne['Randomize Frequency Scan Increments'] = str(val)
                key_order_ne.append('Randomize Frequency Scan Increments')
            except AttributeError:
                pass
                
            try:
                val = bool(data.ppg.hel_enable.mean)
                data_ne['Flip Helicity'] = str(val)
                key_order_ne.append('Flip Helicity')
            except AttributeError:
                pass
                
            try:
                val = bool(data.ppg.hel_enable.mean)
                data_ne['Helicity Flip Sleep'] = "%d ms" % val
                key_order_ne.append('Helicity Flip Sleep')
            except AttributeError:
                pass
                
            key_order_ne.append('')
            
        # set viewer string
        def set_str(data_dict, key_order, txtbox):
        
            m = max(max(map(len, list(data_dict.keys()))) + 1, 5)
            lines = [k.rjust(m)+':   ' + data_dict[k] for k in key_order]
            lines = [l if l.strip() != ':' else '' for l in lines]
            
            self.set_textbox_text(txtbox, '\n'.join(lines))
        
        set_str(data_nw, key_order_nw, self.text_nw)
        set_str(data_ne, key_order_ne, self.text_ne)
        set_str(data_sw, key_order_sw, self.text_sw)
        set_str(data_se, key_order_se, self.text_se)
        
        return True
   
    # ======================================================================= #
    def set_nbm(self):
        """
            Set the nbm variable based on the run mode
        """
        
        # check if data
        if not hasattr(self, 'data'):
            return
        
        # check run mode
        mode = self.data.mode
        
        self.bfit.set_nbm(mode)

    # ======================================================================= #
    def set_textbox_text(self, textbox, text):
        """Set the text in a tkinter Text widget"""
        textbox.delete('1.0', END)
        textbox.insert('1.0', text)
        
    # ======================================================================= #
    def do_update(self, first=True, runid=''):
        self.logger.debug('Draw via periodic update')
        
        # update stop condition
        if runid and runid != self.update_id:
            return
        
        # select period drawing figure
        if first:
            
            first = False
            
            # check that there is a canvas, if not, draw
            if self.bfit.plt.active['inspect'] == 0:
                self.draw('inspect', quiet=False)
                first = True
            
            # set up updating canvas
            fig = self.bfit.plt.gcf('inspect')
            fig.canvas.set_window_title('Figure %d (Inspect - Updating)'%fig.number)
            self.bfit.plt.plots['periodic'] = [fig.number]
            self.bfit.plt.active['periodic'] = self.bfit.plt.active['inspect']
            
            runid = self.data.id
            self.update_id = runid
            
            # repeat
            if not first:
                self.bfit.root.after(self.bfit.update_period*1000, 
                                     lambda:self.do_update(first=False, 
                                                           runid=runid))
                return
        
        # update 
        if self.is_updating.get():
            
            # check that figure exists or is not updating (was closed)
            if self.bfit.plt.active['periodic'] not in self.bfit.plt.plots['inspect']: 
                self.is_updating.set(False)
                del self.bfit.plt.plots['periodic'][0]
                self.bfit.plt.active['periodic'] = 0
                return
            
            # Get the updating figure
            fig = self.bfit.plt.gcf('periodic')
            title = fig.canvas.get_window_title()

            # Check that the figure is still updating
            if 'Updating' not in title:
                self.is_updating.set(False)
                del self.bfit.plt.plots['periodic'][0]
                self.bfit.plt.active['periodic'] = 0
                return
            
            # update run
            year, run = tuple(map(int, runid.split('.')[:2]))
            current_year = self.year.get()
            current_run = self.runn.get()
            
            self.year.set(year)
            self.runn.set(run)
            
            # check current run 
            if current_run < 40000:
                current_run2 = self._get_latest_run(current_year, current_run)
                if current_run2 is False:
                    return 
            else:
                current_run2 = current_run
                
            # update only in stack mode
            draw_style = self.bfit.draw_style.get()
            self.bfit.draw_style.set('stack')
            self.bfit.plt.autoscale('periodic', False)
            self.draw(figstyle='periodic', quiet=True)
            draw_style = self.bfit.draw_style.set(draw_style)
            
            # reset year and run 
            do_quiet = (current_run2 != run) or (current_year != year)
            
            self.year.set(current_year)
            self.runn.set(current_run)
            self.get_data(quiet=do_quiet)
            
            # Print update message
            print('Updated figure at:', str(datetime.datetime.now()).split('.')[0], 
                  flush=True)
            
            # repeat
            self.bfit.root.after(self.bfit.update_period*1000, 
                                 lambda:self.do_update(first=False, runid=runid))
            
        # remove window from updating list
        else:
            # check if window already removed 
            if self.bfit.plt.active['periodic'] != 0:
                
                # remove window
                fig = self.bfit.plt.gcf('periodic')
                fig.canvas.set_window_title('Figure %d (Inspect)'%fig.number)
                del self.bfit.plt.plots['periodic'][0]
                self.bfit.plt.active['periodic'] = 0
            
# =========================================================================== #

