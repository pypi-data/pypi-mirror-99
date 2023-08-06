# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

from pkg_resources import parse_version
import kaitaistruct
from kaitaistruct import KaitaiStruct, KaitaiStream, BytesIO


if parse_version(kaitaistruct.__version__) < parse_version('0.9'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.9 or later is required, but you have %s" % (kaitaistruct.__version__))

class Grbalpha(KaitaiStruct):
    """:field callsign: ax25_frame.ax25_header.dest_callsign_raw.callsign_ror.callsign
    :field ssid_mask: ax25_frame.ax25_header.dest_ssid_raw.ssid_mask
    :field ssid: ax25_frame.ax25_header.dest_ssid_raw.ssid
    :field src_callsign_raw_callsign: ax25_frame.ax25_header.src_callsign_raw.callsign_ror.callsign
    :field src_ssid_raw_ssid_mask: ax25_frame.ax25_header.src_ssid_raw.ssid_mask
    :field src_ssid_raw_ssid: ax25_frame.ax25_header.src_ssid_raw.ssid
    :field repeater_rpt_instance_rpt_callsign_raw_callsign: ax25_frame.ax25_header.repeater.rpt_instance.rpt_callsign_raw.callsign_ror.callsign
    :field repeater_rpt_instance_rpt_ssid_raw_ssid_mask: ax25_frame.ax25_header.repeater.rpt_instance.rpt_ssid_raw.ssid_mask
    :field repeater_rpt_instance_rpt_ssid_raw_ssid: ax25_frame.ax25_header.repeater.rpt_instance.rpt_ssid_raw.ssid
    :field ctl: ax25_frame.ax25_header.ctl
    :field pid: ax25_frame.payload.pid
    :field packet_type: ax25_frame.payload.ax25_info.packet_type
    :field pkt_type: ax25_frame.payload.ax25_info.body.pkt_type
    :field uptime_total: ax25_frame.payload.ax25_info.body.uptime_total
    :field uptime_since_last: ax25_frame.payload.ax25_info.body.uptime_since_last
    :field reset_count: ax25_frame.payload.ax25_info.body.reset_count
    :field mcu_10mv: ax25_frame.payload.ax25_info.body.mcu_10mv
    :field batt: ax25_frame.payload.ax25_info.body.batt
    :field temp_cpu: ax25_frame.payload.ax25_info.body.temp_cpu
    :field temp_pa_ntc: ax25_frame.payload.ax25_info.body.temp_pa_ntc
    :field sig_rx_immediate: ax25_frame.payload.ax25_info.body.sig_rx_immediate
    :field sig_rx_avg: ax25_frame.payload.ax25_info.body.sig_rx_avg
    :field sig_rx_max: ax25_frame.payload.ax25_info.body.sig_rx_max
    :field sig_background_avg: ax25_frame.payload.ax25_info.body.sig_background_avg
    :field sig_background_immediate: ax25_frame.payload.ax25_info.body.sig_background_immediate
    :field sig_background_max: ax25_frame.payload.ax25_info.body.sig_background_max
    :field rf_packets_received: ax25_frame.payload.ax25_info.body.rf_packets_received
    :field rf_packets_transmitted: ax25_frame.payload.ax25_info.body.rf_packets_transmitted
    :field ax25_packets_received: ax25_frame.payload.ax25_info.body.ax25_packets_received
    :field ax25_packets_transmitted: ax25_frame.payload.ax25_info.body.ax25_packets_transmitted
    :field digipeater_rx_count: ax25_frame.payload.ax25_info.body.digipeater_rx_count
    :field digipeater_tx_count: ax25_frame.payload.ax25_info.body.digipeater_tx_count
    :field csp_received: ax25_frame.payload.ax25_info.body.csp_received
    :field csp_transmitted: ax25_frame.payload.ax25_info.body.csp_transmitted
    :field i2c1_received: ax25_frame.payload.ax25_info.body.i2c1_received
    :field i2c1_transmitted: ax25_frame.payload.ax25_info.body.i2c1_transmitted
    :field i2c2_received: ax25_frame.payload.ax25_info.body.i2c2_received
    :field i2c2_transmitted: ax25_frame.payload.ax25_info.body.i2c2_transmitted
    :field rs485_received: ax25_frame.payload.ax25_info.body.rs485_received
    :field rs485_transmitted: ax25_frame.payload.ax25_info.body.rs485_transmitted
    :field csp_mcu_received: ax25_frame.payload.ax25_info.body.csp_mcu_received
    :field csp_mcu_transmitted: ax25_frame.payload.ax25_info.body.csp_mcu_transmitted
    :field string: ax25_frame.payload.ax25_info.body.string
    """
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self._read()

    def _read(self):
        self.ax25_frame = Grbalpha.Ax25Frame(self._io, self, self._root)

    class Ax25Frame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ax25_header = Grbalpha.Ax25Header(self._io, self, self._root)
            _on = (self.ax25_header.ctl & 19)
            if _on == 0:
                self.payload = Grbalpha.IFrame(self._io, self, self._root)
            elif _on == 3:
                self.payload = Grbalpha.UiFrame(self._io, self, self._root)
            elif _on == 19:
                self.payload = Grbalpha.UiFrame(self._io, self, self._root)
            elif _on == 16:
                self.payload = Grbalpha.IFrame(self._io, self, self._root)
            elif _on == 18:
                self.payload = Grbalpha.IFrame(self._io, self, self._root)
            elif _on == 2:
                self.payload = Grbalpha.IFrame(self._io, self, self._root)


    class Ax25Header(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.dest_callsign_raw = Grbalpha.CallsignRaw(self._io, self, self._root)
            self.dest_ssid_raw = Grbalpha.SsidMask(self._io, self, self._root)
            self.src_callsign_raw = Grbalpha.CallsignRaw(self._io, self, self._root)
            self.src_ssid_raw = Grbalpha.SsidMask(self._io, self, self._root)
            if (self.src_ssid_raw.ssid_mask & 1) == 0:
                self.repeater = Grbalpha.Repeater(self._io, self, self._root)

            self.ctl = self._io.read_u1()


    class UiFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Grbalpha.Tlm(_io__raw_ax25_info, self, self._root)


    class Callsign(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.callsign = (self._io.read_bytes(6)).decode(u"ASCII")


    class IFrame(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pid = self._io.read_u1()
            self._raw_ax25_info = self._io.read_bytes_full()
            _io__raw_ax25_info = KaitaiStream(BytesIO(self._raw_ax25_info))
            self.ax25_info = Grbalpha.Tlm(_io__raw_ax25_info, self, self._root)


    class SsidMask(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.ssid_mask = self._io.read_u1()

        @property
        def ssid(self):
            if hasattr(self, '_m_ssid'):
                return self._m_ssid if hasattr(self, '_m_ssid') else None

            self._m_ssid = ((self.ssid_mask & 15) >> 1)
            return self._m_ssid if hasattr(self, '_m_ssid') else None


    class Repeaters(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_callsign_raw = Grbalpha.CallsignRaw(self._io, self, self._root)
            self.rpt_ssid_raw = Grbalpha.SsidMask(self._io, self, self._root)


    class Repeater(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.rpt_instance = []
            i = 0
            while True:
                _ = Grbalpha.Repeaters(self._io, self, self._root)
                self.rpt_instance.append(_)
                if (_.rpt_ssid_raw.ssid_mask & 1) == 1:
                    break
                i += 1


    class Comd(KaitaiStruct):
        """
        .. seealso::
           Source - https://needronix.eu/products/cormorant/hamradio-user-guide/
        """
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.pkt_type = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_uptime = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uptime_total_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.uptime_since_last_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_resets = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.reset_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_mcuv = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.mcu_10mv_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_battv = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.batt_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_temp = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.temp_cpu_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.temp_pa_ntc_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_sig = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_rx_immediate_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_rx_avg_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_rx_max_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_background_immediate_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_background_avg_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.sig_background_max_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_rf = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.rf_packets_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.rf_packets_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_ax25 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.ax25_packets_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.ax25_packets_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_digi = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.digipeater_rx_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.digipeater_tx_count_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_csp = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.csp_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.csp_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_i2c1 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.i2c1_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.i2c1_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_i2c2 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.i2c2_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.i2c2_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_rs485 = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.rs485_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.rs485_transmitted_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.pass_csp_mcu = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.csp_mcu_received_raw = (self._io.read_bytes_term(44, False, True, True)).decode(u"utf8")
            self.csp_mcu_transmitted_raw = (self._io.read_bytes_full()).decode(u"utf8")

        @property
        def sig_rx_max(self):
            if hasattr(self, '_m_sig_rx_max'):
                return self._m_sig_rx_max if hasattr(self, '_m_sig_rx_max') else None

            self._m_sig_rx_max = int(self.sig_rx_max_raw)
            return self._m_sig_rx_max if hasattr(self, '_m_sig_rx_max') else None

        @property
        def temp_pa_ntc(self):
            if hasattr(self, '_m_temp_pa_ntc'):
                return self._m_temp_pa_ntc if hasattr(self, '_m_temp_pa_ntc') else None

            self._m_temp_pa_ntc = int(self.temp_pa_ntc_raw)
            return self._m_temp_pa_ntc if hasattr(self, '_m_temp_pa_ntc') else None

        @property
        def csp_transmitted(self):
            if hasattr(self, '_m_csp_transmitted'):
                return self._m_csp_transmitted if hasattr(self, '_m_csp_transmitted') else None

            self._m_csp_transmitted = int(self.csp_transmitted_raw)
            return self._m_csp_transmitted if hasattr(self, '_m_csp_transmitted') else None

        @property
        def batt(self):
            if hasattr(self, '_m_batt'):
                return self._m_batt if hasattr(self, '_m_batt') else None

            self._m_batt = int(self.batt_raw)
            return self._m_batt if hasattr(self, '_m_batt') else None

        @property
        def sig_rx_avg(self):
            if hasattr(self, '_m_sig_rx_avg'):
                return self._m_sig_rx_avg if hasattr(self, '_m_sig_rx_avg') else None

            self._m_sig_rx_avg = int(self.sig_rx_avg_raw)
            return self._m_sig_rx_avg if hasattr(self, '_m_sig_rx_avg') else None

        @property
        def sig_background_immediate(self):
            if hasattr(self, '_m_sig_background_immediate'):
                return self._m_sig_background_immediate if hasattr(self, '_m_sig_background_immediate') else None

            self._m_sig_background_immediate = int(self.sig_background_immediate_raw)
            return self._m_sig_background_immediate if hasattr(self, '_m_sig_background_immediate') else None

        @property
        def uptime_total(self):
            if hasattr(self, '_m_uptime_total'):
                return self._m_uptime_total if hasattr(self, '_m_uptime_total') else None

            self._m_uptime_total = int(self.uptime_total_raw)
            return self._m_uptime_total if hasattr(self, '_m_uptime_total') else None

        @property
        def rs485_received(self):
            if hasattr(self, '_m_rs485_received'):
                return self._m_rs485_received if hasattr(self, '_m_rs485_received') else None

            self._m_rs485_received = int(self.rs485_received_raw)
            return self._m_rs485_received if hasattr(self, '_m_rs485_received') else None

        @property
        def i2c1_received(self):
            if hasattr(self, '_m_i2c1_received'):
                return self._m_i2c1_received if hasattr(self, '_m_i2c1_received') else None

            self._m_i2c1_received = int(self.i2c1_received_raw)
            return self._m_i2c1_received if hasattr(self, '_m_i2c1_received') else None

        @property
        def temp_cpu(self):
            if hasattr(self, '_m_temp_cpu'):
                return self._m_temp_cpu if hasattr(self, '_m_temp_cpu') else None

            self._m_temp_cpu = int(self.temp_cpu_raw)
            return self._m_temp_cpu if hasattr(self, '_m_temp_cpu') else None

        @property
        def ax25_packets_transmitted(self):
            if hasattr(self, '_m_ax25_packets_transmitted'):
                return self._m_ax25_packets_transmitted if hasattr(self, '_m_ax25_packets_transmitted') else None

            self._m_ax25_packets_transmitted = int(self.ax25_packets_transmitted_raw)
            return self._m_ax25_packets_transmitted if hasattr(self, '_m_ax25_packets_transmitted') else None

        @property
        def ax25_packets_received(self):
            if hasattr(self, '_m_ax25_packets_received'):
                return self._m_ax25_packets_received if hasattr(self, '_m_ax25_packets_received') else None

            self._m_ax25_packets_received = int(self.ax25_packets_received_raw)
            return self._m_ax25_packets_received if hasattr(self, '_m_ax25_packets_received') else None

        @property
        def digipeater_tx_count(self):
            if hasattr(self, '_m_digipeater_tx_count'):
                return self._m_digipeater_tx_count if hasattr(self, '_m_digipeater_tx_count') else None

            self._m_digipeater_tx_count = int(self.digipeater_tx_count_raw)
            return self._m_digipeater_tx_count if hasattr(self, '_m_digipeater_tx_count') else None

        @property
        def csp_mcu_transmitted(self):
            if hasattr(self, '_m_csp_mcu_transmitted'):
                return self._m_csp_mcu_transmitted if hasattr(self, '_m_csp_mcu_transmitted') else None

            self._m_csp_mcu_transmitted = int(self.csp_mcu_transmitted_raw)
            return self._m_csp_mcu_transmitted if hasattr(self, '_m_csp_mcu_transmitted') else None

        @property
        def csp_mcu_received(self):
            if hasattr(self, '_m_csp_mcu_received'):
                return self._m_csp_mcu_received if hasattr(self, '_m_csp_mcu_received') else None

            self._m_csp_mcu_received = int(self.csp_mcu_received_raw)
            return self._m_csp_mcu_received if hasattr(self, '_m_csp_mcu_received') else None

        @property
        def i2c1_transmitted(self):
            if hasattr(self, '_m_i2c1_transmitted'):
                return self._m_i2c1_transmitted if hasattr(self, '_m_i2c1_transmitted') else None

            self._m_i2c1_transmitted = int(self.i2c1_transmitted_raw)
            return self._m_i2c1_transmitted if hasattr(self, '_m_i2c1_transmitted') else None

        @property
        def mcu_10mv(self):
            if hasattr(self, '_m_mcu_10mv'):
                return self._m_mcu_10mv if hasattr(self, '_m_mcu_10mv') else None

            self._m_mcu_10mv = int(self.mcu_10mv_raw)
            return self._m_mcu_10mv if hasattr(self, '_m_mcu_10mv') else None

        @property
        def uptime_since_last(self):
            if hasattr(self, '_m_uptime_since_last'):
                return self._m_uptime_since_last if hasattr(self, '_m_uptime_since_last') else None

            self._m_uptime_since_last = int(self.uptime_since_last_raw)
            return self._m_uptime_since_last if hasattr(self, '_m_uptime_since_last') else None

        @property
        def sig_background_max(self):
            if hasattr(self, '_m_sig_background_max'):
                return self._m_sig_background_max if hasattr(self, '_m_sig_background_max') else None

            self._m_sig_background_max = int(self.sig_background_max_raw)
            return self._m_sig_background_max if hasattr(self, '_m_sig_background_max') else None

        @property
        def sig_rx_immediate(self):
            if hasattr(self, '_m_sig_rx_immediate'):
                return self._m_sig_rx_immediate if hasattr(self, '_m_sig_rx_immediate') else None

            self._m_sig_rx_immediate = int(self.sig_rx_immediate_raw)
            return self._m_sig_rx_immediate if hasattr(self, '_m_sig_rx_immediate') else None

        @property
        def reset_count(self):
            if hasattr(self, '_m_reset_count'):
                return self._m_reset_count if hasattr(self, '_m_reset_count') else None

            self._m_reset_count = int(self.reset_count_raw)
            return self._m_reset_count if hasattr(self, '_m_reset_count') else None

        @property
        def rs485_transmitted(self):
            if hasattr(self, '_m_rs485_transmitted'):
                return self._m_rs485_transmitted if hasattr(self, '_m_rs485_transmitted') else None

            self._m_rs485_transmitted = int(self.rs485_transmitted_raw)
            return self._m_rs485_transmitted if hasattr(self, '_m_rs485_transmitted') else None

        @property
        def rf_packets_received(self):
            if hasattr(self, '_m_rf_packets_received'):
                return self._m_rf_packets_received if hasattr(self, '_m_rf_packets_received') else None

            self._m_rf_packets_received = int(self.rf_packets_received_raw)
            return self._m_rf_packets_received if hasattr(self, '_m_rf_packets_received') else None

        @property
        def rf_packets_transmitted(self):
            if hasattr(self, '_m_rf_packets_transmitted'):
                return self._m_rf_packets_transmitted if hasattr(self, '_m_rf_packets_transmitted') else None

            self._m_rf_packets_transmitted = int(self.rf_packets_transmitted_raw)
            return self._m_rf_packets_transmitted if hasattr(self, '_m_rf_packets_transmitted') else None

        @property
        def digipeater_rx_count(self):
            if hasattr(self, '_m_digipeater_rx_count'):
                return self._m_digipeater_rx_count if hasattr(self, '_m_digipeater_rx_count') else None

            self._m_digipeater_rx_count = int(self.digipeater_rx_count_raw)
            return self._m_digipeater_rx_count if hasattr(self, '_m_digipeater_rx_count') else None

        @property
        def sig_background_avg(self):
            if hasattr(self, '_m_sig_background_avg'):
                return self._m_sig_background_avg if hasattr(self, '_m_sig_background_avg') else None

            self._m_sig_background_avg = int(self.sig_background_avg_raw)
            return self._m_sig_background_avg if hasattr(self, '_m_sig_background_avg') else None

        @property
        def i2c2_received(self):
            if hasattr(self, '_m_i2c2_received'):
                return self._m_i2c2_received if hasattr(self, '_m_i2c2_received') else None

            self._m_i2c2_received = int(self.i2c2_received_raw)
            return self._m_i2c2_received if hasattr(self, '_m_i2c2_received') else None

        @property
        def i2c2_transmitted(self):
            if hasattr(self, '_m_i2c2_transmitted'):
                return self._m_i2c2_transmitted if hasattr(self, '_m_i2c2_transmitted') else None

            self._m_i2c2_transmitted = int(self.i2c2_transmitted_raw)
            return self._m_i2c2_transmitted if hasattr(self, '_m_i2c2_transmitted') else None

        @property
        def csp_received(self):
            if hasattr(self, '_m_csp_received'):
                return self._m_csp_received if hasattr(self, '_m_csp_received') else None

            self._m_csp_received = int(self.csp_received_raw)
            return self._m_csp_received if hasattr(self, '_m_csp_received') else None


    class Obc(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.string = (self._io.read_bytes_full()).decode(u"utf8")


    class CallsignRaw(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self._raw__raw_callsign_ror = self._io.read_bytes(6)
            self._raw_callsign_ror = KaitaiStream.process_rotate_left(self._raw__raw_callsign_ror, 8 - (1), 1)
            _io__raw_callsign_ror = KaitaiStream(BytesIO(self._raw_callsign_ror))
            self.callsign_ror = Grbalpha.Callsign(_io__raw_callsign_ror, self, self._root)


    class Tlm(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self._read()

        def _read(self):
            self.packet_type = self._io.read_u1()
            _on = self.packet_type
            if _on == 44:
                self.body = Grbalpha.Comd(self._io, self, self._root)
            else:
                self.body = Grbalpha.Obc(self._io, self, self._root)



