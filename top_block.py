#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Top Block
# Generated: Tue Dec 10 09:49:11 2013
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital;import cmath
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class top_block(grc_wxgui.top_block_gui):

    def __init__(self, rxPort=52002, txPort=52001):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")

        ##################################################
        # Parameters
        ##################################################
        self.rxPort = rxPort
        self.txPort = txPort

        ##################################################
        # Variables
        ##################################################
        self.localOscillator = localOscillator = 14070000
        self.threshold = threshold = -200
        self.samp_rate = samp_rate = 48000
        self.rxPhase = rxPhase = .84
        self.rxMagnitude = rxMagnitude = 0.854
        self.freqFine = freqFine = 0
        self.freq = freq = localOscillator
        self.bandwidth = bandwidth = 50

        ##################################################
        # Blocks
        ##################################################
        _threshold_sizer = wx.BoxSizer(wx.VERTICAL)
        self._threshold_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_threshold_sizer,
        	value=self.threshold,
        	callback=self.set_threshold,
        	label="threshold",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._threshold_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_threshold_sizer,
        	value=self.threshold,
        	callback=self.set_threshold,
        	minimum=-500,
        	maximum=500,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_threshold_sizer)
        self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "tuning")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "scope")
        self.Add(self.notebook_0)
        _freqFine_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freqFine_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freqFine_sizer,
        	value=self.freqFine,
        	callback=self.set_freqFine,
        	label="Tuning",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freqFine_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freqFine_sizer,
        	value=self.freqFine,
        	callback=self.set_freqFine,
        	minimum=-500,
        	maximum=500,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freqFine_sizer)
        _freq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	label="Frequency",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_sizer,
        	value=self.freq,
        	callback=self.set_freq,
        	minimum=localOscillator-samp_rate,
        	maximum=localOscillator+samp_rate,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_sizer)
        _bandwidth_sizer = wx.BoxSizer(wx.VERTICAL)
        self._bandwidth_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	label="Signal Bandwidth",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._bandwidth_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	minimum=30,
        	maximum=5000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_bandwidth_sizer)
        self.wxgui_waterfallsink2_0_0_0 = waterfallsink2.waterfall_sink_c(
        	self.notebook_0.GetPage(1).GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=125*8,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.notebook_0.GetPage(1).Add(self.wxgui_waterfallsink2_0_0_0.win)
        self.wxgui_waterfallsink2_0_0 = waterfallsink2.waterfall_sink_c(
        	self.notebook_0.GetPage(0).GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=125*8,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_waterfallsink2_0_0.win)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.notebook_0.GetPage(0).GetWin(),
        	baseband_freq=localOscillator,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_waterfallsink2_0.win)
        self.low_pass_filter_0_1 = filter.fir_filter_ccf(samp_rate/125/8, firdes.low_pass(
        	1, samp_rate, 500, 500, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0 = filter.interp_fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 30, 30, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(samp_rate/125/8, firdes.low_pass(
        	1, samp_rate, bandwidth, bandwidth, firdes.WIN_HAMMING, 6.76))
        self.digital_mpsk_receiver_cc_0 = digital.mpsk_receiver_cc(2, 0, cmath.pi/100.0, -0.5, 0.5, 0.25, 0.01, 125*8/31.25, 0.001, 0.001)
        self.blocks_transcendental_1 = blocks.transcendental("sin", "float")
        self.blocks_transcendental_0 = blocks.transcendental("cos", "float")
        self.blocks_throttle_0_1 = blocks.throttle(gr.sizeof_float*1, samp_rate)
        self.blocks_throttle_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_char*1, 31.25)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(1e-12, 1e-12, 0)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, int(samp_rate/31.25))
        self.blocks_null_source_1 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_source_0_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_multiply_xx_0_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_vff((rxMagnitude, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((2, ))
        self.blocks_multiply_conjugate_cc_0 = blocks.multiply_conjugate_cc(1)
        self.blocks_float_to_complex_1_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1, ))
        self.blks2_tcp_source_0 = grc_blks2.tcp_source(
        	itemsize=gr.sizeof_char*1,
        	addr="127.0.0.1",
        	port=txPort,
        	server=False,
        )
        self.blks2_tcp_sink_0 = grc_blks2.tcp_sink(
        	itemsize=gr.sizeof_char*1,
        	addr="127.0.0.1",
        	port=rxPort,
        	server=False,
        )
        self.audio_source_0 = audio.source(samp_rate, "", True)
        self.audio_sink_0 = audio.sink(samp_rate, "", True)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(threshold, 1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, -freqFine, 1, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq+freqFine-localOscillator, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, -(freq-localOscillator), 1, 0)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, rxPhase*3.14159/180.0)
        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0)
        self.analog_agc_xx_0.set_max_gain(65536)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blks2_tcp_source_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_throttle_0_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_1, 0), (self.blocks_multiply_xx_0_1, 1))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_transcendental_1, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_transcendental_0, 0))
        self.connect((self.blocks_transcendental_0, 0), (self.blocks_float_to_complex_0_1, 0))
        self.connect((self.blocks_transcendental_1, 0), (self.blocks_float_to_complex_0_1, 1))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_float_to_complex_1, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.blocks_float_to_complex_1, 1))
        self.connect((self.blocks_float_to_complex_1, 0), (self.blocks_multiply_xx_0_1, 0))
        self.connect((self.blocks_null_source_0_0, 0), (self.blocks_float_to_complex_1_0, 1))
        self.connect((self.audio_source_0, 1), (self.blocks_float_to_complex_1_0, 0))
        self.connect((self.blocks_float_to_complex_1_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0_0, 0))
        self.connect((self.blocks_null_source_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_throttle_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.blks2_tcp_sink_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_multiply_conjugate_cc_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.blocks_multiply_conjugate_cc_0, 1))
        self.connect((self.digital_mpsk_receiver_cc_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_conjugate_cc_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_throttle_0_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_xx_0_2, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_0_2, 1))
        self.connect((self.blocks_multiply_xx_0_2, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.low_pass_filter_0_1, 0))
        self.connect((self.low_pass_filter_0_1, 0), (self.wxgui_waterfallsink2_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.digital_mpsk_receiver_cc_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.wxgui_waterfallsink2_0_0_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.audio_sink_0, 1))
        self.connect((self.blocks_complex_to_float_0, 1), (self.audio_sink_0, 0))
        self.connect((self.blocks_throttle_0_0, 0), (self.wxgui_waterfallsink2_0, 0))


# QT sink close method reimplementation

    def get_rxPort(self):
        return self.rxPort

    def set_rxPort(self, rxPort):
        self.rxPort = rxPort

    def get_txPort(self):
        return self.txPort

    def set_txPort(self, txPort):
        self.txPort = txPort

    def get_localOscillator(self):
        return self.localOscillator

    def set_localOscillator(self, localOscillator):
        self.localOscillator = localOscillator
        self.set_freq(self.localOscillator)
        self.analog_sig_source_x_0.set_frequency(-(self.freq-self.localOscillator))
        self.analog_sig_source_x_0_0.set_frequency(self.freq+self.freqFine-self.localOscillator)
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.localOscillator)

    def get_threshold(self):
        return self.threshold

    def set_threshold(self, threshold):
        self.threshold = threshold
        self.analog_simple_squelch_cc_0.set_threshold(self.threshold)
        self._threshold_slider.set_value(self.threshold)
        self._threshold_text_box.set_value(self.threshold)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0_1.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, 30, 30, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0_1.set_taps(firdes.low_pass(1, self.samp_rate, 500, 500, firdes.WIN_HAMMING, 6.76))
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, self.bandwidth, firdes.WIN_HAMMING, 6.76))
        self.blocks_throttle_0_0.set_sample_rate(self.samp_rate)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

    def get_rxPhase(self):
        return self.rxPhase

    def set_rxPhase(self, rxPhase):
        self.rxPhase = rxPhase
        self.analog_const_source_x_0.set_offset(self.rxPhase*3.14159/180.0)

    def get_rxMagnitude(self):
        return self.rxMagnitude

    def set_rxMagnitude(self, rxMagnitude):
        self.rxMagnitude = rxMagnitude
        self.blocks_multiply_const_vxx_2.set_k((self.rxMagnitude, ))

    def get_freqFine(self):
        return self.freqFine

    def set_freqFine(self, freqFine):
        self.freqFine = freqFine
        self.analog_sig_source_x_1.set_frequency(-self.freqFine)
        self.analog_sig_source_x_0_0.set_frequency(self.freq+self.freqFine-self.localOscillator)
        self._freqFine_slider.set_value(self.freqFine)
        self._freqFine_text_box.set_value(self.freqFine)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_slider.set_value(self.freq)
        self._freq_text_box.set_value(self.freq)
        self.analog_sig_source_x_0.set_frequency(-(self.freq-self.localOscillator))
        self.analog_sig_source_x_0_0.set_frequency(self.freq+self.freqFine-self.localOscillator)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self._bandwidth_slider.set_value(self.bandwidth)
        self._bandwidth_text_box.set_value(self.bandwidth)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, self.bandwidth, firdes.WIN_HAMMING, 6.76))

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    parser.add_option("-r", "--rxPort", dest="rxPort", type="intx", default=52002,
        help="Set recieve_port [default=%default]")
    parser.add_option("-t", "--txPort", dest="txPort", type="intx", default=52001,
        help="Set transmit_port [default=%default]")
    (options, args) = parser.parse_args()
    tb = top_block(rxPort=options.rxPort, txPort=options.txPort)
    tb.Start(True)
    tb.Wait()

