# coding=utf8
# Copyright 2016-2019 Lenovo
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import binascii
from datetime import datetime
import errno
import fnmatch
import json
import math
import os.path
import random
import re
import socket
import struct
import weakref

import six

import pyghmi.constants as pygconst
import pyghmi.exceptions as pygexc
import pyghmi.ipmi.oem.lenovo.config as config
import pyghmi.ipmi.oem.lenovo.energy as energy
import pyghmi.ipmi.private.session as ipmisession
import pyghmi.ipmi.private.util as util
from pyghmi.ipmi import sdr
import pyghmi.media as media
import pyghmi.storage as storage
import pyghmi.util.webclient as webclient

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


numregex = re.compile('([0-9]+)')
funtypes = {
    0: 'RAID Controller',
    1: 'Ethernet',
    2: 'Fibre Channel',
    3: 'Infiniband',
    4: 'GPU',
    10: 'NVMe Controller',
    12: 'Fabric Controller',
}


def naturalize_string(key):
    """Analyzes string in a human way to enable natural sort

    :param key: string for the split
    :returns: A structure that can be consumed by 'sorted'
    """
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(numregex, key)]


def natural_sort(iterable):
    """Return a sort using natural sort if possible

    :param iterable:
    :return:
    """
    try:
        return sorted(iterable, key=naturalize_string)
    except TypeError:
        # The natural sort attempt failed, fallback to ascii sort
        return sorted(iterable)


def fixup_uuid(uuidprop):
    baduuid = ''.join(uuidprop.split())
    uuidprefix = (baduuid[:8], baduuid[8:12], baduuid[12:16])
    a = struct.pack('<IHH', *[int(x, 16) for x in uuidprefix])
    a = binascii.hexlify(a)
    if not isinstance(a, str):
        a = a.decode('utf-8')
    uuid = (a[:8], a[8:12], a[12:16], baduuid[16:20], baduuid[20:])
    return '-'.join(uuid).upper()


def fixup_str(propstr):
    if propstr is None:
        return ''
    return ''.join([chr(int(c, 16)) for c in propstr.split()]).strip(
        ' \xff\x00')


class IMMClient(object):
    logouturl = '/data/logout'
    bmcname = 'IMM'
    ADP_URL = '/designs/imm/dataproviders/imm_adapters.php'
    ADP_NAME = 'adapter.adapterName'
    ADP_FUN = 'adapter.functions'
    ADP_FU_URL = None
    ADP_LABEL = 'adapter.connectorLabel'
    ADP_SLOTNO = 'adapter.slotNo'
    ADP_OOB = 'adapter.oobSupported'
    ADP_PARTNUM = 'vpd.partNo'
    ADP_SERIALNO = 'vpd.serialNo'
    ADP_VENID = 'generic.vendorId'
    ADP_SUBVENID = 'generic.subVendor'
    ADP_DEVID = 'generic.devId'
    ADP_SUBDEVID = 'generic.subDevId'
    ADP_FRU = 'vpd.cardSKU'
    BUSNO = 'generic.busNo'
    PORTS = 'network.pPorts'
    DEVNO = 'generic.devNo'

    def __init__(self, ipmicmd):
        self.ipmicmd = weakref.proxy(ipmicmd)
        self.updating = False
        self.imm = ipmicmd.bmc
        srv = self.imm
        if ':' in srv:
            srv = '[{0}]'.format(srv)
        self.adp_referer = 'https://imm/designs/imm/index-console.php'
        if ipmicmd.ipmi_session.password:
            self.username = ipmicmd.ipmi_session.userid.decode('utf-8')
            self.password = ipmicmd.ipmi_session.password.decode('utf-8')
        self._wc = None  # The webclient shall be initiated on demand
        self._energymanager = None
        self.datacache = {}
        self.webkeepalive = None
        self._keepalivesession = None
        self.fwc = None
        self.fwo = None
        self.fwovintage = None

    @staticmethod
    def _parse_builddate(strval):
        if not isinstance(strval, str) and isinstance(strval, bytes):
            strval = strval.decode('utf-8')
        try:
            return datetime.strptime(strval, '%Y/%m/%d %H:%M:%S')
        except ValueError:
            pass
        try:
            return datetime.strptime(strval, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            pass
        try:
            return datetime.strptime(strval, '%Y/%m/%d')
        except ValueError:
            pass
        try:
            return datetime.strptime(strval, '%m/%d/%Y')
        except ValueError:
            pass
        try:
            return datetime.strptime(strval, '%Y-%m-%d')
        except ValueError:
            pass
        try:
            return datetime.strptime(strval, '%m %d %Y')
        except ValueError:
            pass
        return None

    @classmethod
    def parse_imm_buildinfo(cls, buildinfo):
        buildid = bytes(buildinfo[:9]).rstrip(b' \x00')
        if not isinstance(buildid, str):
            buildid = buildid.decode('utf-8')
        bdt = b' '.join(bytes(buildinfo[9:]).replace(b'\x00', b' ').split())
        bdate = cls._parse_builddate(bdt)
        return buildid, bdate

    @classmethod
    def datefromprop(cls, propstr):
        if propstr is None:
            return None
        return cls._parse_builddate(propstr)

    def get_system_configuration(self, hideadvanced=True, fetchimm=False):
        if not self.fwc:
            self.fwc = config.LenovoFirmwareConfig(self.ipmicmd)
        try:
            self.fwo = self.fwc.get_fw_options(fetchimm=fetchimm)
        except Exception:
            raise Exception('%s failed to retrieve UEFI configuration'
                            % self.bmcname)
        self.fwovintage = util._monotonic_time()
        retcfg = {}
        for opt in self.fwo:
            if 'MegaRAIDConfigurationTool' in opt:
                # Suppress the Avago configuration to be consistent with
                # other tools.
                continue
            if (hideadvanced and self.fwo[opt]['lenovo_protect']
                    or self.fwo[opt]['hidden']):
                # Do not enumerate hidden settings
                continue
            retcfg[opt] = {}
            retcfg[opt]['value'] = self.fwo[opt]['current']
            retcfg[opt]['default'] = self.fwo[opt]['default']
            retcfg[opt]['help'] = self.fwo[opt]['help']
            retcfg[opt]['possible'] = self.fwo[opt]['possible']
            retcfg[opt]['sortid'] = self.fwo[opt]['sortid']
        return retcfg

    def set_system_configuration(self, changeset):
        if not self.fwc:
            self.fwc = config.LenovoFirmwareConfig(self.ipmicmd)
        fetchimm = False
        if not self.fwo or util._monotonic_time() - self.fwovintage > 30:
            self.fwo = self.fwc.get_fw_options(fetchimm=fetchimm)
            self.fwovintage = util._monotonic_time()
        for key in list(changeset):
            if key not in self.fwo:
                found = False
                for rkey in self.fwo:
                    if fnmatch.fnmatch(rkey.lower(), key.lower()):
                        changeset[rkey] = changeset[key]
                        found = True
                    elif self.fwo[rkey].get('alias', None) != rkey:
                        calias = self.fwo[rkey]['alias']
                        if fnmatch.fnmatch(calias.lower(), key.lower()):
                            changeset[rkey] = changeset[key]
                            found = True
                if not found and not fetchimm:
                    fetchimm = True
                    self.fwo = self.fwc.get_fw_options(fetchimm=fetchimm)
                    if key in self.fwo:
                        continue
                    else:
                        found = False
                        for rkey in self.fwo:
                            if fnmatch.fnmatch(rkey.lower(), key.lower()):
                                changeset[rkey] = changeset[key]
                                found = True
                            elif self.fwo[rkey].get('alias', None) != rkey:
                                calias = self.fwo[rkey]['alias']
                                if fnmatch.fnmatch(
                                        calias.lower(), key.lower()):
                                    changeset[rkey] = changeset[key]
                                    found = True
                if found:
                    del changeset[key]
                else:
                    raise pygexc.InvalidParameterValue(
                        '{0} not a known setting'.format(key))
        self.merge_changeset(changeset)
        if changeset:
            try:
                self.fwc.set_fw_options(self.fwo)
            finally:
                self.fwo = None
                self.fwovintage = 0

    def merge_changeset(self, changeset):
        for key in changeset:
            if isinstance(changeset[key], six.string_types):
                changeset[key] = {'value': changeset[key]}
            newvalue = changeset[key]['value']
            if self.fwo[key]['is_list'] and not isinstance(newvalue, list):
                if '=' in newvalue:
                    # ASU set a precedent of = delimited settings
                    # for now, honor that delimiter as well
                    newvalues = newvalue.split('=')
                else:
                    newvalues = newvalue.split(',')
            else:
                newvalues = [newvalue]
            newnewvalues = []
            for newvalue in newvalues:
                newv = re.sub(r'\s+', ' ', newvalue)
                if (self.fwo[key]['possible']
                        and newvalue not in self.fwo[key]['possible']):
                    candlist = []
                    for candidate in self.fwo[key]['possible']:
                        candid = re.sub(r'\s+', ' ', candidate)
                        if newv.lower().startswith(candid.lower()):
                            newvalue = candidate
                            break
                        if candid.lower().startswith(newv.lower()):
                            candlist.append(candidate)
                    else:
                        if len(candlist) == 1:
                            newvalue = candlist[0]
                        else:
                            raise pygexc.InvalidParameterValue(
                                '{0} is not a valid value for {1} '
                                '({2})'.format(
                                    newvalue, key,
                                    ','.join(self.fwo[key]['possible'])))
                newnewvalues.append(newvalue)
            if len(newnewvalues) == 1:
                self.fwo[key]['new_value'] = newnewvalues[0]
            else:
                self.fwo[key]['new_value'] = newnewvalues

    def clear_bmc_configuration(self):
        self.ipmicmd.xraw_command(0x2e, 0xcc,
                                  data=(0x5e, 0x2b, 0, 0xa, 1, 0xff, 0, 0, 0))

    def set_property(self, propname, value):
        if not isinstance(value, int) or value > 255:
            raise Exception('Unsupported property value')
        propname = propname.encode('utf-8')
        proplen = len(propname) | 0b10000000
        valuelen = 0x11  # The value is always one byte, for now
        cmdlen = len(propname) + 4  # the flags byte, two tlv bytes, and value
        cdata = bytearray([3, 0, cmdlen, 1, proplen]) + propname
        cdata += bytearray([valuelen, value])
        rsp = self.ipmicmd.xraw_command(netfn=0x3a, command=0xc4, data=cdata)
        rsp['data'] = bytearray(rsp['data'])
        if rsp['data'][0] != 0:
            raise Exception('Unknown response setting property: {0}'.format(
                rsp['data'][0]))

    def get_property(self, propname):
        propname = propname.encode('utf-8')
        proplen = len(propname) | 0b10000000
        cmdlen = len(propname) + 1
        cdata = bytearray([0, 0, cmdlen, proplen]) + propname
        rsp = self.ipmicmd.xraw_command(netfn=0x3a, command=0xc4, data=cdata)
        rsp['data'] = bytearray(rsp['data'])
        if rsp['data'][0] != 0:
            return None
        propdata = rsp['data'][3:]  # second two bytes are size, don't need it
        if propdata[0] & 0b10000000:  # string, for now assume length valid
            ret = bytes(propdata[1:]).rstrip(b' \x00')
            if not isinstance(ret, str):
                ret = ret.decode('utf-8')
            return ret
        if propdata[0] == 0x44:  # dword
            return propdata[1:5]
        else:
            raise Exception('Unknown format for property: ' + repr(propdata))

    def get_webclient(self):
        cv = self.ipmicmd.certverify
        wc = webclient.SecureHTTPConnection(self.imm, 443, verifycallback=cv)
        wc.vintage = None
        try:
            wc.connect()
        except socket.error as se:
            if se.errno != errno.ECONNREFUSED:
                raise
            return None
        adata = urlencode({'user': self.username,
                           'password': self.password,
                           'SessionTimeout': 60})
        headers = {'Connection': 'keep-alive',
                   'Origin': 'https://imm/',
                   'Host': 'imm',
                   'Referer': 'https://imm/designs/imm/index.php',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        wc.request('POST', '/data/login', adata, headers)
        rsp = wc.getresponse()
        if rsp.status == 200:
            rspdata = json.loads(rsp.read())
            if rspdata['authResult'] == '0' and rspdata['status'] == 'ok':
                if 'token2_name' in rspdata and 'token2_value' in rspdata:
                    wc.set_header(rspdata['token2_name'],
                                  rspdata['token2_value'])
                if 'token3_name' in rspdata and 'token3_value' in rspdata:
                    self.uploadtoken = {rspdata['token3_name']:
                                        rspdata['token3_value']}
                else:
                    self.uploadtoken = {}
                wc.set_header('Referer', self.adp_referer)
                wc.set_header('Host', 'imm')
                wc.set_header('Origin', 'https://imm/')
                return wc

    @property
    def wc(self):
        if (not self._wc or (self._wc.vintage
                             and self._wc.vintage < util._monotonic_time()
                             - 30)):
            if not self.updating and self._wc:
                # in case the existing session is still valid
                # dispose of the session
                self.weblogout()
            self._wc = self.get_webclient()
        return self._wc

    def fetch_grouped_properties(self, groupinfo):
        retdata = {}
        for keyval in groupinfo:
            retdata[keyval] = self.get_property(groupinfo[keyval])
            if keyval == 'date':
                retdata[keyval] = self.datefromprop(retdata[keyval])
        returnit = False
        for keyval in list(retdata):
            if retdata[keyval] in (None, ''):
                del retdata[keyval]
            else:
                returnit = True
        if returnit:
            return retdata

    def grab_cacheable_json(self, url, age=30):
        data = self.get_cached_data(url, age)
        if not data:
            data, status = self.wc.grab_json_response_with_status(url)
            if status == 401:
                self._wc = None
                data, status = self.wc.grab_json_response_with_status(url)
            if status != 200:
                data = {}
            self.datacache[url] = (data, util._monotonic_time())
        return data

    def get_cached_data(self, attribute, age=30):
        try:
            kv = self.datacache[attribute]
            if kv[1] > util._monotonic_time() - age:
                return kv[0]
        except KeyError:
            return None

    def upload_media(self, filename, progress=None, data=None):
        xid = random.randint(0, 1000000000)
        alloc = self.wc.grab_json_response(
            '/data/set',
            'RP_VmAllocateLoc({0},{1},1)'.format(self.username, filename))
        if alloc['return'] != 'Success':
            raise Exception('Unexpected reply to allocation: ' + repr(alloc))
        slotid = alloc['slotId']
        uploadfields = self.uploadtoken
        uploadfields['filePath'] = alloc['filePath']
        uploadfields['uploadType'] = 'iframe'
        uploadfields['available'] = alloc['available']
        uploadfields['checksum'] = xid
        ut = webclient.FileUploader(
            self.wc, '/designs/imm/upload/rp_image_upload.esp', filename, data,
            otherfields=uploadfields)
        ut.start()
        while ut.isAlive():
            ut.join(3)
            if progress:
                progress({'phase': 'upload',
                          'progress': 100 * self.wc.get_upload_progress()})
        status = self.wc.grab_json_response(
            '/designs/imm/upload/rp_image_upload_status.esp',
            'filePath={0}'.format(alloc['filePath']))
        if not status['rpImgUploadResult'].endswith('Success'):
            raise Exception(
                'Upload status returned unexpected data: ' + repr(alloc))
        ups = self.wc.grab_json_response(
            '/data/set',
            'RP_VmUpdateSize({1}, {0})'.format(status['originalFileSize'],
                                               slotid))
        if ups['return'] != 'Success':
            raise Exception('Unexpected return to update size: ' + repr(ups))
        ups = self.wc.grab_json_response('/data/set',
                                         'RP_VmMount({0})'.format(slotid))
        if ups['return'] != 'Success':
            raise Exception('Unexpected return to mount: ' + repr(ups))
        if progress:
            progress({'phase': 'complete'})

    def attach_remote_media(self, url, user, password):
        url = url.replace(':', '\\:')
        params = urlencode({
            'RP_VmAllocateMountUrl({0},{1},1,,)'.format(
                self.username, url): ''
        })
        result = self.wc.grab_json_response('/data?set', params,
                                            referer=self.adp_referer)
        if not result:
            result = self.wc.grab_json_response('/data/set', params,
                                                referer=self.adp_referer)
        if result['return'] != 'Success':
            raise Exception(result['reason'])
        self.weblogout()

    def list_media(self):
        rt = self.wc.grab_json_response(
            '/designs/imm/dataproviders/imm_rp_images.php',
            referer=self.adp_referer)
        for item in rt['items']:
            if 'images' in item:
                for uload in item['images']:
                    if uload['status'] != 0:
                        yield media.Media(uload['filename'])
            for attached in item.get('urls', []):
                filename = attached['url']
                filename = filename.split('/')[-1]
                url = '/'.join(attached['url'].split('/')[:-1])
                yield media.Media(filename, url)

    def detach_remote_media(self):
        mnt = self.wc.grab_json_response(
            '/designs/imm/dataproviders/imm_rp_images.php',
            referer=self.adp_referer)
        removeurls = []
        for item in mnt['items']:
            if 'urls' in item:
                for url in item['urls']:
                    removeurls.append(url['url'])
            if 'images' in item:
                for uload in item['images']:
                    self.wc.grab_json_response(
                        '/data/set', 'RP_RemoveFile({0}, 0)'.format(
                            uload['slotId']))
        for url in removeurls:
            url = url.replace(':', '\\:')
            params = urlencode({
                'RP_VmAllocateUnMountUrl({0},{1},0,)'.format(
                    self.username, url): ''})
            result = self.wc.grab_json_response('/data?set', params,
                                                referer=self.adp_referer)
            if not result:
                result = self.wc.grab_json_response('/data/set', params,
                                                    referer=self.adp_referer)
            if result['return'] != 'Success':
                raise Exception(result['reason'])
        self.weblogout()

    def fetch_psu_firmware(self):
        return []

    def fetch_agentless_firmware(self):
        cd = self.get_cached_data('lenovo_cached_adapters_fu')
        if cd:
            adapterdata, fwu = cd
        else:
            adapterdata = None
        if not adapterdata:
            if self.updating:
                raise pygexc.TemporaryError(
                    'Cannot read extended inventory during firmware update')
            if self.wc:
                adapterdata = self.wc.grab_json_response(
                    self.ADP_URL, referer=self.adp_referer)
                if self.ADP_FU_URL:
                    fwu = self.wc.grab_json_response(
                        self.ADP_FU_URL, referer=self.adp_referer)
                else:
                    fwu = {}
                if adapterdata:
                    self.datacache['lenovo_cached_adapters_fu'] = (
                        (adapterdata, fwu), util._monotonic_time())
        if adapterdata and 'items' in adapterdata:
            anames = {}
            for adata in adapterdata['items']:
                aname = adata[self.ADP_NAME]
                if aname in anames:
                    anames[aname] += 1
                    aname = '{0} {1}'.format(aname, anames[aname])
                else:
                    anames[aname] = 1
                donenames = set([])
                for fundata in adata[self.ADP_FUN]:
                    fdata = fundata.get('firmwares', ())
                    for firm in fdata:
                        fname = firm['firmwareName'].rstrip()
                        if '.' in fname:
                            fname = firm['description'].rstrip()
                        if fname in donenames:
                            # ignore redundant entry
                            continue
                        if not fname:
                            continue
                        donenames.add(fname)
                        bdata = {}
                        if 'versionStr' in firm and firm['versionStr']:
                            bdata['version'] = firm['versionStr']
                        if ('releaseDate' in firm
                                and firm['releaseDate']
                                and firm['releaseDate'] != 'N/A'):
                            try:
                                bdata['date'] = self._parse_builddate(
                                    firm['releaseDate'])
                            except ValueError:
                                pass
                        yield '{0} {1}'.format(aname, fname), bdata
                for fwi in fwu.get('items', []):
                    if fwi.get('key', -1) == adata.get('key', -2):
                        if fwi.get('fw_status', 0) == 2:
                            bdata = {}
                            if 'fw_version_pend' in fwi:
                                bdata['version'] = fwi['fw_version_pend']
                            yield '{0} Pending Update'.format(aname), bdata
        for disk in self.disk_inventory():
            yield disk
        self.weblogout()

    def disk_inventory(self, mode=0):
        if mode == 1:
            # Bypass IMM hardware inventory for now
            return
        storagedata = self.get_cached_data('lenovo_cached_storage')
        if not storagedata:
            if self.wc:
                storagedata = self.wc.grab_json_response(
                    '/designs/imm/dataproviders/raid_alldevices.php')
                if storagedata:
                    self.datacache['lenovo_cached_storage'] = (
                        storagedata, util._monotonic_time())
        if storagedata and 'items' in storagedata:
            for adp in storagedata['items']:
                if 'storage.vpd.productName' not in adp:
                    continue
                adpname = adp['storage.vpd.productName']
                if 'children' not in adp:
                    adp['children'] = ()
                for diskent in adp['children']:
                    bdata = {}
                    diskname = '{0} Disk {1}'.format(
                        adpname,
                        diskent['storage.slotNo'])
                    bdata['model'] = diskent[
                        'storage.vpd.productName'].rstrip()
                    bdata['version'] = diskent['storage.firmwares'][0][
                        'versionStr']
                    yield (diskname, bdata)

    def get_hw_inventory(self):
        hwmap = self.hardware_inventory_map()
        for key in natural_sort(hwmap):
            yield (key, hwmap[key])

    def get_hw_descriptions(self):
        hwmap = self.hardware_inventory_map()
        for key in natural_sort(hwmap):
            yield key

    def get_component_inventory(self, compname):
        hwmap = self.hardware_inventory_map()
        try:
            return hwmap[compname]
        except KeyError:
            return None

    def get_oem_sensor_names(self, ipmicmd):
        try:
            if self._energymanager is None:
                self._energymanager = energy.EnergyManager(ipmicmd)
            return self._energymanager.supportedmeters
        except pygexc.UnsupportedFunctionality:
            return ()

    def get_oem_sensor_descriptions(self, ipmicmd):
        return [{'name': x, 'type': 'Energy'
                 } for x in self.get_oem_sensor_names(ipmicmd)]

    def get_oem_sensor_reading(self, name, ipmicmd):
        if self._energymanager is None:
            self._energymanager = energy.EnergyManager(ipmicmd)
        if name == 'AC Energy':
            kwh = self._energymanager.get_ac_energy(ipmicmd)
        elif name == 'DC Energy':
            kwh = self._energymanager.get_dc_energy(ipmicmd)
        else:
            raise pygexc.UnsupportedFunctionality('No sunch sensor ' + name)
        return sdr.SensorReading({'name': name, 'imprecision': None,
                                  'value': kwh, 'states': [],
                                  'state_ids': [],
                                  'health': pygconst.Health.Ok,
                                  'type': 'Energy'}, 'kWh')

    def weblogout(self):
        if self._wc:
            try:
                self._wc.grab_json_response(self.logouturl)
            except Exception:
                pass
            self._wc = None

    def hardware_inventory_map(self):
        hwmap = self.get_cached_data('lenovo_cached_hwmap')
        if hwmap:
            return hwmap
        hwmap = {}
        enclosureuuid = self.get_property('/v2/ibmc/smm/chassis/uuid')
        if enclosureuuid:
            bay = hex(int(self.get_property('/v2/cmm/sp/7'))).replace(
                '0x', '')
            serial = self.get_property('/v2/ibmc/smm/chassis/sn')
            model = self.get_property('/v2/ibmc/smm/chassis/mtm')
            hwmap['Enclosure'] = {
                'UUID': fixup_uuid(enclosureuuid),
                'Bay': bay,
                'Model': fixup_str(model),
                'Serial': fixup_str(serial),
            }
        for disk in self.disk_inventory(mode=1):  # hardware mode
            hwmap[disk[0]] = disk[1]
        adapterdata = self.get_cached_data('lenovo_cached_adapters')
        if not adapterdata:
            if self.updating:
                raise pygexc.TemporaryError(
                    'Cannot read extended inventory during firmware update')
            if self.wc:
                adapterdata = self.wc.grab_json_response(
                    self.ADP_URL, referer=self.adp_referer)
                if adapterdata:
                    self.datacache['lenovo_cached_adapters'] = (
                        adapterdata, util._monotonic_time())
        if adapterdata and 'items' in adapterdata:
            anames = {}
            for adata in adapterdata['items']:
                skipadapter = False
                clabel = adata[self.ADP_LABEL]
                if clabel == 'Unknown':
                    continue
                if clabel != 'Onboard':
                    aslot = adata[self.ADP_SLOTNO]
                    if clabel == 'ML2':
                        clabel = 'ML2 (Slot {0})'.format(aslot)
                    else:
                        clabel = 'Slot {0}'.format(aslot)
                aname = adata[self.ADP_NAME]
                bdata = {'location': clabel, 'name': aname}
                if aname in anames:
                    anames[aname] += 1
                    aname = '{0} {1}'.format(aname, anames[aname])
                else:
                    anames[aname] = 1
                for fundata in adata[self.ADP_FUN]:
                    bdata['pcislot'] = '{0:02x}:{1:02x}'.format(
                        fundata[self.BUSNO], fundata[self.DEVNO])
                    serialdata = fundata.get(self.ADP_SERIALNO, None)
                    if (serialdata and serialdata != 'N/A'
                            and '---' not in serialdata):
                        bdata['serial'] = serialdata
                    partnum = fundata.get(self.ADP_PARTNUM, None)
                    if partnum and partnum != 'N/A':
                        bdata['Part Number'] = partnum
                    cardtype = funtypes.get(fundata.get('funType', None),
                                            None)
                    if cardtype is not None:
                        bdata['Type'] = cardtype
                    venid = fundata.get(self.ADP_VENID, None)
                    if venid is not None:
                        bdata['PCI Vendor ID'] = '{0:04x}'.format(venid)
                    devid = fundata.get(self.ADP_DEVID, None)
                    if devid is not None:
                        bdata['PCI Device ID'] = '{0:04x}'.format(devid)
                    venid = fundata.get(self.ADP_SUBVENID, None)
                    if venid is not None:
                        bdata['PCI Subsystem Vendor ID'] = '{0:04x}'.format(
                            venid)
                    devid = fundata.get(self.ADP_SUBDEVID, None)
                    if devid is not None:
                        bdata['PCI Subsystem Device ID'] = '{0:04x}'.format(
                            devid)
                    fruno = fundata.get(self.ADP_FRU, None)
                    if fruno is not None:
                        bdata['FRU Number'] = fruno
                    if self.PORTS in fundata:
                        for portinfo in fundata[self.PORTS]:
                            for lp in portinfo['logicalPorts']:
                                ma = lp['networkAddr']
                                ma = ':'.join(
                                    [ma[i:i + 2] for i in range(
                                        0, len(ma), 2)]).lower()
                                bdata['MAC Address {0}'.format(
                                    portinfo['portIndex'])] = ma
                    elif clabel == 'Onboard':  # skip the various non-nic
                        skipadapter = True
                if not skipadapter:
                    hwmap[aname] = bdata
            self.datacache['lenovo_cached_hwmap'] = (hwmap,
                                                     util._monotonic_time())
        self.weblogout()
        return hwmap

    def get_firmware_inventory(self, bmcver, components):
        # First we fetch the system firmware found in imm properties
        # then check for agentless, if agentless, get adapter info using
        # https, using the caller TLS verification scheme
        components = set(components)
        if not components or set(('imm', 'xcc', 'bmc', 'core')) & components:
            rsp = self.ipmicmd.xraw_command(netfn=0x3a, command=0x50)
            immverdata = self.parse_imm_buildinfo(rsp['data'])
            bmcmajor, bmcminor = [int(x) for x in bmcver.split('.')]
            bmcver = '{0}.{1:02d}'.format(bmcmajor, bmcminor)
            bdata = {
                'version': bmcver, 'build': immverdata[0],
                'date': immverdata[1]}
            yield (self.bmcname, bdata)
            bdata = self.fetch_grouped_properties({
                'build': '/v2/ibmc/dm/fw/imm2/backup_build_id',
                'version': '/v2/ibmc/dm/fw/imm2/backup_build_version',
                'date': '/v2/ibmc/dm/fw/imm2/backup_build_date'})
            if bdata:
                yield ('{0} Backup'.format(self.bmcname), bdata)
                bdata = self.fetch_grouped_properties({
                    'build': '/v2/ibmc/trusted_buildid',
                })
            if bdata:
                yield ('{0} Trusted Image'.format(self.bmcname), bdata)
        if not components or set(('uefi', 'bios', 'core')) & components:
            bdata = self.fetch_grouped_properties({
                'build': '/v2/bios/build_id',
                'version': '/v2/bios/build_version',
                'date': '/v2/bios/build_date'})
            if bdata:
                yield ('UEFI', bdata)
            else:
                yield ('UEFI', {'version': 'unknown'})
            bdata = self.fetch_grouped_properties({
                'build': '/v2/ibmc/dm/fw/bios/backup_build_id',
                'version': '/v2/ibmc/dm/fw/bios/backup_build_version'})
            if bdata:
                yield ('UEFI Backup', bdata)
            # Note that the next pending could be pending for either primary
            # or backup, so can't promise where it will go
            bdata = self.fetch_grouped_properties({
                'build': '/v2/bios/pending_build_id'})
            if bdata:
                yield ('UEFI Pending Update', bdata)
        if not components or set(('fpga', 'core')) & components:
            try:
                fpga = self.ipmicmd.xraw_command(netfn=0x3a, command=0x6b,
                                                 data=(0,))
                fpga = '{0}.{1}.{2}'.format(*bytearray(fpga['data']))
                yield ('FPGA', {'version': fpga})
            except pygexc.IpmiException as ie:
                if ie.ipmicode != 193:
                    raise
        if (not components or (components - set((
                'core', 'uefi', 'bios', 'bmc', 'xcc', 'imm', 'fpga',
                'lxpm')))):
            for firm in self.fetch_agentless_firmware():
                yield firm


class XCCClient(IMMClient):
    logouturl = '/api/providers/logout'
    bmcname = 'XCC'
    ADP_URL = '/api/dataset/imm_adapters?params=pci_GetAdapters'
    ADP_NAME = 'adapterName'
    ADP_FUN = 'functions'
    ADP_FU_URL = '/api/function/adapter_update?params=pci_GetAdapterListAndFW'
    ADP_LABEL = 'connectorLabel'
    ADP_SLOTNO = 'slotNo'
    ADP_OOB = 'oobSupported'
    ADP_PARTNUM = 'vpd_partNo'
    ADP_SERIALNO = 'vpd_serialNo'
    ADP_VENID = 'generic_vendorId'
    ADP_SUBVENID = 'generic_subVendor'
    ADP_DEVID = 'generic_devId'
    ADP_SUBDEVID = 'generic_subDevId'
    ADP_FRU = 'vpd_cardSKU'
    BUSNO = 'generic_busNo'
    PORTS = 'network_pPorts'
    DEVNO = 'generic_devNo'

    def __init__(self, ipmicmd):
        super(XCCClient, self).__init__(ipmicmd)
        self.adp_referer = None

    def reseat(self):
        rsp = self.wc.grab_json_response_with_status(
            '/api/providers/virt_reseat', '{}')
        if rsp[1] != 200 or rsp[0].get('return', 1) != 0:
            raise pygexc.UnsupportedFunctionality(
                'This platform does not support AC reseat.')

    def get_description(self):
        dsc = self.wc.grab_json_response('/DeviceDescription.json')
        dsc = dsc[0]
        if not dsc.get('u-height', None):
            if dsc.get('enclosure-machinetype-model', '').startswith('7Y36'):
                return {'height': 2, 'slot': 0}
            else:
                return {}
        return {'height': int(dsc['u-height']), 'slot': int(dsc['slot'])}

    def get_extended_bmc_configuration(self):
        immsettings = self.get_system_configuration(fetchimm=True)
        for setting in list(immsettings):
            if not setting.startswith('IMM.'):
                del immsettings[setting]
        return immsettings

    def get_bmc_configuration(self):
        settings = {}
        passrules = self.wc.grab_json_response('/api/dataset/imm_users_global')
        passrules = passrules.get('items', [{}])[0]
        settings['password_reuse_count'] = {
            'value': passrules.get('pass_min_resuse')}
        settings['password_change_interval'] = {
            'value': passrules.get('pass_change_interval')}
        settings['password_expiration'] = {
            'value': passrules.get('pass_expire_days')}
        settings['password_login_failures'] = {
            'value': passrules.get('max_login_failures')}
        settings['password_complexity'] = {
            'value': passrules.get('pass_complex_required')}
        settings['password_min_length'] = {
            'value': passrules.get('pass_min_length')}
        settings['password_lockout_period'] = {
            'value': passrules.get('lockout_period')}
        presassert = self.wc.grab_json_response('/api/dataset/imm_rpp')
        asserted = presassert.get('items', [{}])[0].get('rpp_Assert', None)
        if asserted is not None:
            settings['presence_assert'] = {
                'value': 'Enable' if asserted else 'Disable'
            }
        try:
            enclosureinfo = self.ipmicmd.xraw_command(0x3a, 0xf1, data=[0])
        except pygexc.IpmiException:
            return settings
        settings['smm'] = {
            'default': 'Disable',
            'possible': ['Enable', 'Disable', 'IPMI'],
            'help': 'Enables or disables the network of the '
                    'enclosure manager. IPMI Enables with IPMI '
                    'for v2 systems.',
        }
        if bytearray(enclosureinfo['data'])[0] == 2:
            settings['smm']['value'] = 'Disable'
        elif bytearray(enclosureinfo['data'])[0] == 1:
            settings['smm']['value'] = 'Enable'
        elif bytearray(enclosureinfo['data'])[0] == 4:
            settings['smm']['value'] = 'IPMI'
        else:
            settings['smm']['value'] = None
        smmip = self.get_property('/v2/ibmc/smm/smm_ip')
        if smmip:
            smmip = socket.inet_ntoa(bytes(smmip[-1::-1]))
            settings['smm_ip'] = {
                'help': 'Current IPv4 address as reported by SMM, read-only',
                'value': smmip,
            }
        return settings

    rulemap = {
        'password_change_interval': 'USER_GlobalMinPassChgInt',
        'password_reuse_count': 'USER_GlobalMinPassReuseCycle',
        'password_expiration': 'USER_GlobalPassExpPeriod',
        'password_login_failures': 'USER_GlobalMaxLoginFailures',
        'password_complexity': 'USER_GlobalPassComplexRequired',
        'password_min_length': 'USER_GlobalMinPassLen',
        'password_lockout_period': 'USER_GlobalLockoutPeriod',
    }

    def set_bmc_configuration(self, changeset):
        ruleset = {}
        for key in changeset:
            if isinstance(changeset[key], six.string_types):
                changeset[key] = {'value': changeset[key]}
            currval = changeset[key].get('value', None)
            if 'smm'.startswith(key.lower()):
                if 'enabled'.startswith(currval.lower()):
                    self.ipmicmd.xraw_command(0x3a, 0xf1, data=[1])
                elif 'disabled'.startswith(currval.lower()):
                    self.ipmicmd.xraw_command(0x3a, 0xf1, data=[2])
                elif 'ipmi'.startswith(currval.lower()):
                    self.ipmicmd.xraw_command(0x3a, 0xf1, data=[4])
            elif key.lower() in self.rulemap:
                ruleset[self.rulemap[key.lower()]] = changeset[key]['value']
                if key.lower() == 'password_expiration':
                    warntime = str(int(int(changeset[key]['value']) * 0.08))
                    ruleset['USER_GlobalPassExpWarningPeriod'] = warntime
            elif 'presence_asserted'.startswith(key.lower()):
                assertion = changeset[key]['value']
                if 'enabled'.startswith(assertion.lower()):
                    self.wc.grab_json_response('/api/dataset',
                                               {'IMM_RPPAssert': '0'})
                    self.wc.grab_json_response('/api/dataset',
                                               {'IMM_RPPAssert': '1'})
                elif 'disabled'.startswith(assertion.lower()):
                    self.wc.grab_json_response('/api/dataset',
                                               {'IMM_RPPAssert': '0'})
                else:
                    raise pygexc.InvalidParameterValue(
                        '"{0}" is not a recognized value for {1}'.format(
                            assertion, key))
            else:
                raise pygexc.InvalidParameterValue(
                    '{0} not a known setting'.format(key))
        if ruleset:
            self.wc.grab_json_response('/api/dataset', ruleset)

    def clear_system_configuration(self):
        res = self.wc.grab_json_response_with_status(
            '/redfish/v1/Systems/1/Bios/Actions/Bios.ResetBios',
            {'Action': 'Bios.ResetBios'},
            headers={
                'Authorization': 'Basic %s' % base64.b64encode(
                    (self.username + ':' + self.password).encode('utf8')
                ).decode('utf8'),
                'Content-Type': 'application/json'
            }
        )
        if res[1] < 200 or res[1] >= 300:
            raise Exception(
                'Unexpected response to clear configuration: {0}'.format(
                    res[0]))

    def get_webclient(self, login=True):
        cv = self.ipmicmd.certverify
        wc = webclient.SecureHTTPConnection(self.imm, 443, verifycallback=cv)
        wc.vintage = util._monotonic_time()
        try:
            wc.connect()
        except socket.error as se:
            if se.errno != errno.ECONNREFUSED:
                raise
            return None
        if not login:
            return wc
        adata = json.dumps({'username': self.username,
                            'password': self.password
                            })
        headers = {'Connection': 'keep-alive',
                   'Referer': 'https://xcc/',
                   'Host': 'xcc',
                   'Content-Type': 'application/json'}
        wc.request('POST', '/api/login', adata, headers)
        rsp = wc.getresponse()
        if rsp.status == 200:
            rspdata = json.loads(rsp.read())
            wc.set_header('Content-Type', 'application/json')
            wc.set_header('Referer', 'https://xcc/')
            wc.set_header('Host', 'xcc')
            wc.set_header('Authorization', 'Bearer ' + rspdata['access_token'])
            if '_csrf_token' in wc.cookies:
                wc.set_header('X-XSRF-TOKEN', wc.cookies['_csrf_token'])
            return wc

    def _raid_number_map(self, controller):
        themap = {}
        cid = controller.split(',')
        rsp = self.wc.grab_json_response(
            '/api/function/raid_conf?'
            'params=raidlink_GetDisksToConf,{0}'.format(cid[0]))
        if rsp.get('return') == 22:  # New style firmware
            if cid[2] == 2:
                arg = '{0},{1}'.format(cid[1], cid[2])
            else:
                arg = '{0},{1}'.format(cid[0], cid[2])
            arg = 'params=raidlink_GetDisksToConf,{0}'.format(arg)
            rsp = self.wc.grab_json_response(
                '/api/function/raid_conf?{0}'.format(arg))
        for lvl in rsp['items'][0]['supported_raidlvl']:
            mapdata = (lvl['rdlvl'], lvl['maxSpan'])
            raidname = lvl['rdlvlstr'].replace(' ', '').lower()
            themap[raidname] = mapdata
            raidname = raidname.replace('raid', 'r')
            themap[raidname] = mapdata
            raidname = raidname.replace('r', '')
            themap[raidname] = mapdata
        return themap

    def check_storage_configuration(self, cfgspec=None):
        rsp = self.wc.grab_json_response(
            '/api/function/raid_conf?params=raidlink_GetStatus')
        if rsp['items'][0]['status'] != 2:
            raise pygexc.TemporaryError('Storage configuration unavailable in '
                                        'current state (try boot to setup or '
                                        'an OS)')
        if not cfgspec:
            return True
        for pool in cfgspec.arrays:
            self._parse_storage_cfgspec(pool)
        self.weblogout()
        return True

    def get_diagnostic_data(self, savefile, progress=None, autosuffix=False):
        self.wc.grab_json_response('/api/providers/ffdc',
                                   {'Generate_FFDC': 1})
        percent = 0
        while percent != 100:
            ipmisession.Session.pause(3)
            result = self.wc.grab_json_response('/api/providers/ffdc',
                                                {'Generate_FFDC_status': 1})
            self._refresh_token()
            if progress:
                progress({'phase': 'initializing', 'progress': float(percent)})
            percent = result['progress']
        while 'FileName' not in result:
            result = self.wc.grab_json_response('/api/providers/ffdc',
                                                {'Generate_FFDC_status': 1})
        url = '/ffdc/{0}'.format(result['FileName'])
        if autosuffix and not savefile.endswith('.tzz'):
            savefile += '-{0}'.format(result['FileName'])
        fd = webclient.FileDownloader(self.wc, url, savefile)
        fd.start()
        while fd.isAlive():
            fd.join(1)
            if progress and self.wc.get_download_progress():
                progress({'phase': 'download',
                          'progress': 100 * self.wc.get_download_progress()})
            self._refresh_token()
        if fd.exc:
            raise fd.exc
        if progress:
            progress({'phase': 'complete'})
        return savefile

    def disk_inventory(self, mode=0):
        # mode 0 is firmware, 1 is hardware
        storagedata = self.get_cached_data('lenovo_cached_storage')
        if not storagedata:
            if self.wc:
                storagedata = self.wc.grab_json_response(
                    '/api/function/raid_alldevices?params=storage_GetAllDisks')
                if storagedata:
                    self.datacache['lenovo_cached_storage'] = (
                        storagedata, util._monotonic_time())
        if storagedata and 'items' in storagedata:
            for adp in storagedata['items']:
                for diskent in adp.get('disks', ()):
                    if mode == 0:
                        yield self.get_disk_firmware(diskent)
                    elif mode == 1:
                        yield self.get_disk_hardware(diskent)
                for diskent in adp.get('aimDisks', ()):
                    if mode == 0:
                        yield self.get_disk_firmware(diskent)
                    elif mode == 1:
                        yield self.get_disk_hardware(diskent)
                if mode == 1:
                    bdata = {'Description': 'Unmanaged Disk'}
                    if adp.get('m2Type', -1) == 2:
                        yield 'M.2 Disk', bdata
                    for umd in adp.get('unmanagedDisks', []):
                        yield 'Disk {0}'.format(umd['slotNo']), bdata

    def get_disk_hardware(self, diskent, prefix=''):
        bdata = {}
        if not prefix and diskent.get('location', '').startswith('M.2'):
            prefix = 'M.2-'
        diskname = 'Disk {1}{0}'.format(diskent['slotNo'], prefix)
        bdata['Model'] = diskent['productName'].rstrip()
        bdata['Serial Number'] = diskent['serialNo'].rstrip()
        bdata['FRU Number'] = diskent['fruPartNo'].rstrip()
        bdata['Description'] = diskent['type'].rstrip()
        return (diskname, bdata)

    def get_disk_firmware(self, diskent, prefix=''):
        bdata = {}
        if not prefix and diskent.get('location', '').startswith('M.2'):
            prefix = 'M.2-'
        diskname = 'Disk {1}{0}'.format(diskent['slotNo'], prefix)
        bdata['model'] = diskent[
            'productName'].rstrip()
        bdata['version'] = diskent['fwVersion']
        return (diskname, bdata)

    def _parse_array_spec(self, arrayspec):
        controller = None
        if arrayspec.disks:
            for disk in list(arrayspec.disks) + list(arrayspec.hotspares):
                if controller is None:
                    controller = disk.id[0]
                if controller != disk.id[0]:
                    raise pygexc.UnsupportedFunctionality(
                        'Cannot span arrays across controllers')
            raidmap = self._raid_number_map(controller)
            if not raidmap:
                raise pygexc.InvalidParameterValue(
                    'There are no available drives for a new array')
            requestedlevel = str(arrayspec.raid).lower()
            if requestedlevel not in raidmap:
                raise pygexc.InvalidParameterValue(
                    'Requested RAID "{0}" not available on this '
                    'system with currently available drives'.format(
                        requestedlevel))
            rdinfo = raidmap[str(arrayspec.raid).lower()]
            rdlvl = str(rdinfo[0])
            defspan = 1 if rdinfo[1] == 1 else 2
            spancount = defspan if arrayspec.spans is None else arrayspec.spans
            drivesperspan = str(len(arrayspec.disks) // int(spancount))
            hotspares = arrayspec.hotspares
            drives = arrayspec.disks
            if hotspares:
                hstr = '|'.join([str(x.id[1]) for x in hotspares]) + '|'
            else:
                hstr = ''
            drvstr = '|'.join([str(x.id[1]) for x in drives]) + '|'
            ctl = controller.split(',')
            pth = '/api/function/raid_conf?params=raidlink_CheckConfisValid'
            args = [pth, ctl[0], rdlvl, spancount, drivesperspan, drvstr,
                    hstr]
            url = ','.join([str(x) for x in args])
            rsp = self.wc.grab_json_response(url)
            if rsp.get('return', -1) == 22:
                args.append(ctl[1])
                args = [pth, ctl[0], rdlvl, spancount, drivesperspan, drvstr,
                        hstr, ctl[1]]
                url = ','.join([str(x) for x in args])
                rsp = self.wc.grab_json_response(url)
            if rsp['items'][0]['errcode'] == 16:
                raise pygexc.InvalidParameterValue('Incorrect number of disks')
            elif rsp['items'][0]['errcode'] != 0:
                raise pygexc.InvalidParameterValue(
                    'Invalid configuration: {0}'.format(
                        rsp['items'][0]['errcode']))
            return {
                'capacity': rsp['items'][0]['freeCapacity'],
                'controller': controller,
                'drives': drvstr,
                'hotspares': hstr,
                'raidlevel': rdlvl,
                'spans': spancount,
                'perspan': drivesperspan,
            }
        else:
            # TODO(): adding new volume to existing array would be here
            pass

    def _make_jbod(self, disk, realcfg):
        currstatus = self._get_status(disk, realcfg)
        if currstatus.lower() == 'jbod':
            return
        self._make_available(disk, realcfg)
        self._set_drive_state(disk, 16)

    def _make_global_hotspare(self, disk, realcfg):
        currstatus = self._get_status(disk, realcfg)
        if currstatus.lower() == 'global hot spare':
            return
        self._make_available(disk, realcfg)
        self._set_drive_state(disk, 1)

    def _make_available(self, disk, realcfg):
        # 8 if jbod, 4 if hotspare.., leave alone if already...
        currstatus = self._get_status(disk, realcfg)
        newstate = None
        if currstatus == 'Unconfigured Good':
            return
        elif currstatus.lower() == 'global hot spare':
            newstate = 4
        elif currstatus.lower() == 'jbod':
            newstate = 8
        self._set_drive_state(disk, newstate)

    def _get_status(self, disk, realcfg):
        for cfgdisk in realcfg.disks:
            if disk.id == cfgdisk.id:
                currstatus = cfgdisk.status
                break
        else:
            raise pygexc.InvalidParameterValue('Requested disk not found')
        return currstatus

    def _set_drive_state(self, disk, state):
        rsp = self.wc.grab_json_response(
            '/api/function',
            {'raidlink_DiskStateAction': '{0},{1}'.format(disk.id[1], state)})
        if rsp.get('return', -1) != 0:
            raise Exception(
                'Unexpected return to set disk state: {0}'.format(
                    rsp.get('return', -1)))

    def clear_storage_arrays(self):
        rsp = self.wc.grab_json_response(
            '/api/function', {'raidlink_ClearRaidConf': '1'})
        self.weblogout()
        if rsp['return'] != 0:
            raise Exception('Unexpected return to clear config: ' + repr(rsp))

    def remove_storage_configuration(self, cfgspec):
        realcfg = self.get_storage_configuration(False)
        for pool in cfgspec.arrays:
            for volume in pool.volumes:
                cid = volume.id[0].split(',')
                if cid[2] == 2:
                    vid = '{0},{1},{2}'.format(volume.id[1], cid[1], cid[2])
                else:
                    vid = '{0},{1},{2}'.format(volume.id[1], cid[0], cid[2])
                rsp = self.wc.grab_json_response(
                    '/api/function', {'raidlink_RemoveVolumeAsync': vid})
                if rsp.get('return', -1) == 2:
                    # older firmware
                    vid = '{0},{1}'.format(volume.id[1], cid[0])
                    rsp = self.wc.grab_json_response(
                        '/api/function', {'raidlink_RemoveVolumeAsync': vid})
                if rsp.get('return', -1) != 0:
                    raise Exception(
                        'Unexpected return to volume deletion: ' + repr(rsp))
                self._wait_storage_async()
        for disk in cfgspec.disks:
            self._make_available(disk, realcfg)
        self.weblogout()

    def apply_storage_configuration(self, cfgspec):
        realcfg = self.get_storage_configuration(False)
        for disk in cfgspec.disks:
            if disk.status.lower() == 'jbod':
                self._make_jbod(disk, realcfg)
            elif disk.status.lower() == 'hotspare':
                self._make_global_hotspare(disk, realcfg)
            elif disk.status.lower() in ('unconfigured', 'available', 'ugood',
                                         'unconfigured good'):
                self._make_available(disk, realcfg)
        for pool in cfgspec.arrays:
            if pool.disks:
                self._create_array(pool)
        self.weblogout()

    def _create_array(self, pool):
        params = self._parse_array_spec(pool)
        cid = params['controller'].split(',')[0]
        url = '/api/function/raid_conf?params=raidlink_GetDefaultVolProp'
        args = (url, cid, 0, params['drives'])
        props = self.wc.grab_json_response(','.join([str(x) for x in args]))
        props = props['items'][0]
        volumes = pool.volumes
        remainingcap = params['capacity']
        nameappend = 1
        vols = []
        currvolnames = None
        currcfg = None
        for vol in volumes:
            if vol.name is None:
                # need to iterate while there exists a volume of that name
                if currvolnames is None:
                    currcfg = self.get_storage_configuration(False)
                    currvolnames = set([])
                    for pool in currcfg.arrays:
                        for volume in pool.volumes:
                            currvolnames.add(volume.name)
                name = props['name'] + '_{0}'.format(nameappend)
                nameappend += 1
                while name in currvolnames:
                    name = props['name'] + '_{0}'.format(nameappend)
                    nameappend += 1
            else:
                name = vol.name
            if vol.stripsize is not None:
                stripsize = int(math.log(vol.stripsize * 2, 2))
            else:
                stripsize = props['stripsize']
            if vol.read_policy is not None:
                read_policy = vol.read_policy
            else:
                read_policy = props["cpra"]
            if vol.write_policy is not None:
                write_policy = vol.write_policy
            else:
                write_policy = props["cpwb"]
            strsize = 'remainder' if vol.size is None else str(vol.size)
            if strsize in ('all', '100%'):
                volsize = params['capacity']
            elif strsize in ('remainder', 'rest'):
                volsize = remainingcap
            elif strsize.endswith('%'):
                volsize = int(params['capacity']
                              * float(strsize.replace('%', '')) / 100.0)
            else:
                try:
                    volsize = int(strsize)
                except ValueError:
                    raise pygexc.InvalidParameterValue(
                        'Unrecognized size ' + strsize)
            remainingcap -= volsize
            if remainingcap < 0:
                raise pygexc.InvalidParameterValue(
                    'Requested sizes exceed available capacity')
            vols.append('{0};{1};{2};{3};{4};{5};{6};{7};{8};|'.format(
                name, volsize, stripsize, write_policy, read_policy,
                props['cpio'], props['ap'], props['dcp'], props['initstate']))
        url = '/api/function'
        cid = params['controller'].split(',')
        cnum = cid[0]
        arglist = '{0},{1},{2},{3},{4},{5},'.format(
            cnum, params['raidlevel'], params['spans'],
            params['perspan'], params['drives'], params['hotspares'])
        arglist += ''.join(vols)
        parms = {'raidlink_AddNewVolWithNaAsync': arglist}
        rsp = self.wc.grab_json_response(url, parms)
        if rsp['return'] == 14:  # newer firmware
            if cid[2] == 2:
                cnum = cid[1]
            arglist = '{0},{1},{2},{3},{4},{5},'.format(
                cnum, params['raidlevel'], params['spans'],
                params['perspan'], params['drives'], params['hotspares'])
            arglist += ''.join(vols) + ',{0}'.format(cid[2])
            parms = {'raidlink_AddNewVolWithNaAsync': arglist}
            rsp = self.wc.grab_json_response(url, parms)
        if rsp['return'] != 0:
            raise Exception(
                'Unexpected response to add volume command: ' + repr(rsp))
        self._wait_storage_async()

    def _wait_storage_async(self):
        rsp = {'items': [{'status': 0}]}
        while rsp['items'][0]['status'] == 0:
            ipmisession.Session.pause(1)
            rsp = self.wc.grab_json_response(
                '/api/function/raid_conf?params=raidlink_QueryAsyncStatus')

    def extract_drivelist(self, cfgspec, controller, drives):
        for drive in cfgspec['drives']:
            ctl, drive = self._extract_drive_desc(drive)
            if controller is None:
                controller = ctl
            if ctl != controller:
                raise pygexc.UnsupportedFunctionality(
                    'Cannot span arrays across controllers')
            drives.append(drive)
        return controller

    def get_oem_sensor_names(self, ipmicmd):
        oemsensornames = super(XCCClient, self).get_oem_sensor_names(ipmicmd)
        therminfo = self.grab_cacheable_json(
            '/api/dataset/pwrmgmt?params=GetThermalRealTimeData', 1)
        if therminfo:
            for name in sorted(therminfo['items'][0]):
                if 'DIMM' in name and 'Temp' in name:
                    oemsensornames = oemsensornames + (name,)
        return oemsensornames

    def get_oem_sensor_descriptions(self, ipmicmd):
        oemdesc = [{'name': x, 'type': 'Energy'} for x in super(
            XCCClient, self).get_oem_sensor_names(ipmicmd)]
        therminfo = self.grab_cacheable_json(
            '/api/dataset/pwrmgmt?params=GetThermalRealTimeData', 1)
        if therminfo:
            for name in sorted(therminfo['items'][0]):
                if 'DIMM' in name and 'Temp' in name:
                    oemdesc.append({'name': name, 'type': 'Temperature'})
        return oemdesc

    def get_oem_sensor_reading(self, name, ipmicmd):
        if 'Energy' in name:
            return super(XCCClient, self).get_oem_sensor_reading(name, ipmicmd)
        therminfo = self.grab_cacheable_json(
            '/api/dataset/pwrmgmt?params=GetThermalRealTimeData', 1)
        temp = therminfo.get('items', [{}])[0].get(name, None)
        if temp is None:
            raise pygexc.UnsupportedFunctionality('No sunch sensor ' + name)
        return sdr.SensorReading({'name': name, 'imprecision': None,
                                  'value': temp, 'states': [],
                                  'state_ids': [],
                                  'health': pygconst.Health.Ok,
                                  'type': 'Temperature'}, '°C')

    def get_storage_configuration(self, logout=True):
        rsp = self.wc.grab_json_response(
            '/api/function/raid_alldevices?params=storage_GetAllDevices,0')
        if not rsp:
            rsp = self.wc.grab_json_response(
                '/api/function/raid_alldevices?params=storage_GetAllDevices')
        standalonedisks = []
        pools = []
        for item in rsp.get('items', []):
            for cinfo in item['controllerInfo']:
                cid = '{0},{1},{2}'.format(
                    cinfo['id'], cinfo.get('slotNo', -1), cinfo.get(
                        'type', -1))
                for pool in cinfo['pools']:
                    volumes = []
                    disks = []
                    spares = []
                    for volume in pool['volumes']:
                        volumes.append(
                            storage.Volume(name=volume['name'],
                                           size=volume['capacity'],
                                           status=volume['statusStr'],
                                           id=(cid, volume['id'])))
                    for disk in pool['disks']:
                        diskinfo = storage.Disk(
                            name=disk['name'], description=disk['type'],
                            id=(cid, disk['id']), status=disk['RAIDState'],
                            serial=disk['serialNo'], fru=disk['fruPartNo'])
                        if disk['RAIDState'] == 'Dedicated Hot Spare':
                            spares.append(diskinfo)
                        else:
                            disks.append(diskinfo)
                    totalsize = pool['totalCapacityStr'].replace('GB', '')
                    totalsize = int(float(totalsize) * 1024)
                    freesize = pool['freeCapacityStr'].replace('GB', '')
                    freesize = int(float(freesize) * 1024)
                    pools.append(storage.Array(
                        disks=disks, raid=pool['rdlvlstr'], volumes=volumes,
                        id=(cid, pool['id']), hotspares=spares,
                        capacity=totalsize, available_capacity=freesize))
                for disk in cinfo.get('unconfiguredDisks', ()):
                    # can be unused, global hot spare, or JBOD
                    standalonedisks.append(
                        storage.Disk(
                            name=disk['name'], description=disk['type'],
                            id=(cid, disk['id']), status=disk['RAIDState'],
                            serial=disk['serialNo'], fru=disk['fruPartNo']))
        if logout:
            self.weblogout()
        return storage.ConfigSpec(disks=standalonedisks, arrays=pools)

    def attach_remote_media(self, url, user, password):
        proto, host, path = util.urlsplit(url)
        if proto == 'smb':
            proto = 'cifs'
        rq = {'Option': '', 'Domain': '', 'Write': 0}
        # nfs == 1, cifs == 0
        if proto == 'nfs':
            rq['Protocol'] = 1
            rq['Url'] = '{0}:{1}'.format(host, path)
        elif proto == 'cifs':
            rq['Protocol'] = 0
            rq['Credential'] = '{0}:{1}'.format(user, password)
            rq['Url'] = '//{0}{1}'.format(host, path)
        elif proto in ('http', 'https'):
            rq['Protocol'] = 7
            rq['Url'] = url
        else:
            raise pygexc.UnsupportedFunctionality(
                '"{0}" scheme is not supported on this system or '
                'invalid url format'.format(proto))
        rt = self.wc.grab_json_response('/api/providers/rp_vm_remote_connect',
                                        json.dumps(rq))
        if 'return' not in rt or rt['return'] != 0:
            if rt['return'] in (657, 659, 656):
                raise pygexc.InvalidParameterValue(
                    'Given location was unreachable by the XCC')
            if rt['return'] == 32:
                raise pygexc.InvalidParameterValue(
                    'XCC does not have required license for operation')
            raise Exception('Unhandled return: ' + repr(rt))
        rt = self.wc.grab_json_response('/api/providers/rp_vm_remote_mountall',
                                        '{}')
        if 'return' not in rt or rt['return'] != 0:
            if rt['return'] in (657, 659, 656):
                raise pygexc.InvalidParameterValue(
                    'Given location was unreachable by the XCC')
            raise Exception('Unhandled return: ' + repr(rt))
        if not self.webkeepalive:
            self._keepalivesession = self._wc
            self.webkeepalive = self.ipmicmd.ipmi_session.register_keepalive(
                self.keepalive, None)
        self._wc = None

    def keepalive(self):
        self._refresh_token_wc(self._keepalivesession)

    def fetch_psu_firmware(self):
        psudata = self.get_cached_data('lenovo_cached_psu')
        if not psudata:
            if self.wc:
                psudata = self.wc.grab_json_response(
                    '/api/function/psu_update?params=GetPsuListAndFW')
                if psudata:
                    self.datacache['lenovo_cached_psu'] = (
                        psudata, util._monotonic_time())
        if not psudata:
            return
        for psu in psudata.get('items', ()):
            yield ('PSU {0}'.format(psu['slot']),
                   {'model': psu['model'],
                    'version': psu['version']})

    def get_firmware_inventory(self, bmcver, components):
        # First we fetch the system firmware found in imm properties
        # then check for agentless, if agentless, get adapter info using
        # https, using the caller TLS verification scheme
        components = set(components)
        if (not components
                or set(('core', 'imm', 'bmc', 'xcc')) & components):
            rsp = self.ipmicmd.xraw_command(netfn=0x3a, command=0x50)
            immverdata = self.parse_imm_buildinfo(rsp['data'])
            bmcmajor, bmcminor = [int(x) for x in bmcver.split('.')]
            bmcver = '{0}.{1:02d}'.format(bmcmajor, bmcminor)
            bdata = {'version': bmcver,
                     'build': immverdata[0],
                     'date': immverdata[1]}
            yield self.bmcname, bdata
            bdata = self.fetch_grouped_properties({
                'build': '/v2/ibmc/dm/fw/imm3/backup_pending_build_id',
                'version': '/v2/ibmc/dm/fw/imm3/backup_pending_build_version',
                'date': '/v2/ibmc/dm/fw/imm3/backup_pending_build_date'})
            if bdata:
                yield '{0} Backup'.format(self.bmcname), bdata
            else:
                bdata = self.fetch_grouped_properties({
                    'build': '/v2/ibmc/dm/fw/imm3/backup_build_id',
                    'version': '/v2/ibmc/dm/fw/imm3/backup_build_version',
                    'date': '/v2/ibmc/dm/fw/imm3/backup_build_date'})
                if bdata:
                    yield '{0} Backup'.format(self.bmcname), bdata
                    bdata = self.fetch_grouped_properties({
                        'build': '/v2/ibmc/trusted_buildid',
                    })
            if bdata:
                bdata = self.fetch_grouped_properties({
                    'build': '/v2/ibmc/trusted_buildid',
                })
            if bdata:
                yield '{0} Trusted Image'.format(self.bmcname), bdata
            bdata = self.fetch_grouped_properties({
                'build': '/v2/ibmc/dm/fw/imm3/primary_pending_build_id',
                'version': '/v2/ibmc/dm/fw/imm3/primary_pending_build_version',
                'date': '/v2/ibmc/dm/fw/imm3/primary_pending_build_date'})
            if bdata:
                yield '{0} Pending Update'.format(self.bmcname), bdata
        if not components or set(('core', 'uefi', 'bios')) & components:
            bdata = self.fetch_grouped_properties({
                'build': '/v2/bios/build_id',
                'version': '/v2/bios/build_version',
                'date': '/v2/bios/build_date'})
            if bdata:
                yield 'UEFI', bdata
            # Note that the next pending could be pending for either primary
            # or backup, so can't promise where it will go
            bdata = self.fetch_grouped_properties({
                'build': '/v2/bios/pending_build_id'})
            if bdata:
                yield 'UEFI Pending Update', bdata
        if not components or set(('lxpm', 'core')) & components:
            bdata = self.fetch_grouped_properties({
                'build': '/v2/tdm/build_id',
                'version': '/v2/tdm/build_version',
                'date': '/v2/tdm/build_date'})
            if bdata:
                yield 'LXPM', bdata
            bdata = self.fetch_grouped_properties({
                'build': '/v2/drvwn/build_id',
                'version': '/v2/drvwn/build_version',
                'date': '/v2/drvwn/build_date',
            })
            if bdata:
                yield 'LXPM Windows Driver Bundle', bdata
            bdata = self.fetch_grouped_properties({
                'build': '/v2/drvln/build_id',
                'version': '/v2/drvln/build_version',
                'date': '/v2/drvln/build_date',
            })
            if bdata:
                yield 'LXPM Linux Driver Bundle', bdata
        if not components or set(('core', 'fpga')) in components:
            try:
                fpga = self.ipmicmd.xraw_command(netfn=0x3a, command=0x6b,
                                                 data=(0,))
                fpga = '{0}.{1}.{2}'.format(
                    *struct.unpack('BBB', fpga['data']))
                yield 'FPGA', {'version': fpga}
            except pygexc.IpmiException as ie:
                if ie.ipmicode != 193:
                    raise
        if (not components or components - set((
                'core', 'uefi', 'bios', 'xcc', 'bmc', 'imm', 'fpga',
                'lxpm'))):
            for firm in self.fetch_agentless_firmware():
                yield firm
            for firm in self.fetch_psu_firmware():
                yield firm

    def detach_remote_media(self):
        if self.webkeepalive:
            self.ipmicmd.ipmi_session.unregister_keepalive(self.webkeepalive)
            self._keepalivesession = None
        rt = self.wc.grab_json_response('/api/providers/rp_vm_remote_getdisk')
        if 'items' in rt:
            slots = []
            for mount in rt['items']:
                slots.append(mount['slotId'])
            for slot in slots:
                rt = self.wc.grab_json_response(
                    '/api/providers/rp_vm_remote_unmount',
                    json.dumps({'Slot': str(slot)}))
                if 'return' not in rt or rt['return'] != 0:
                    raise Exception("Unrecognized return: " + repr(rt))
        rdocs = self.wc.grab_json_response('/api/providers/rp_rdoc_imagelist')
        for rdoc in rdocs['items']:
            filename = rdoc['filename']
            rt = self.wc.grab_json_response('/api/providers/rp_rdoc_unmount',
                                            {'ImageName': filename})
            if rt.get('return', 1) != 0:
                raise Exception("Unrecognized return: " + repr(rt))
        self.weblogout()

    def list_media(self):
        rt = self.wc.grab_json_response('/api/providers/rp_vm_remote_getdisk')
        if 'items' in rt:
            for mt in rt['items']:
                url = mt['remotepath']
                if url.startswith('//'):
                    url = 'smb:' + url
                elif (not url.startswith('http://')
                      and not url.startswith('https://')):
                    url = url.replace(':', '')
                    url = 'nfs://' + url
                yield media.Media(mt['filename'], url)
        rt = self.wc.grab_json_response('/api/providers/rp_rdoc_imagelist')
        if 'items' in rt:
            for mt in rt['items']:
                yield media.Media(mt['filename'])
        self.weblogout()

    def upload_media(self, filename, progress=None, data=None):
        xid = random.randint(0, 1000000000)
        self._refresh_token()
        uploadthread = webclient.FileUploader(
            self.wc, '/upload?X-Progress-ID={0}'.format(xid), filename, data)
        uploadthread.start()
        while uploadthread.isAlive():
            uploadthread.join(3)
            rsp = self.wc.grab_json_response(
                '/upload/progress?X-Progress-ID={0}'.format(xid))
            if progress and rsp['state'] == 'uploading':
                progress({'phase': 'upload',
                          'progress': 100.0 * rsp['received'] / rsp['size']})
            self._refresh_token()
        rsp = json.loads(uploadthread.rsp)
        if progress:
            progress({'phase': 'upload',
                      'progress': 100.0})
        thepath = rsp['items'][0]['path']
        thename = rsp['items'][0]['name']
        writeable = 1 if filename.lower().endswith('.img') else 0
        addfile = {"Url": thepath, "Protocol": 6, "Write": writeable,
                   "Credential": ":", "Option": "", "Domain": "",
                   "WebUploadName": thename}
        rsp = self.wc.grab_json_response('/api/providers/rp_rdoc_addfile',
                                         addfile)
        self._refresh_token()
        if rsp.get('return', -1) != 0:
            errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
            raise Exception('Unrecognized return: ' + errmsg)
        ready = False
        while not ready:
            ipmisession.Session.pause(3)
            rsp = self.wc.grab_json_response('/api/providers/rp_rdoc_getfiles')
            if 'items' not in rsp or len(rsp['items']) == 0:
                raise Exception(
                    'Image upload was not accepted, it may be too large')
            ready = rsp['items'][0]['size'] != 0
        self._refresh_token()
        rsp = self.wc.grab_json_response('/api/providers/rp_rdoc_mountall',
                                         {})
        self._refresh_token()
        if rsp.get('return', -1) != 0:
            errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
            raise Exception('Unrecognized return: ' + errmsg)
        if progress:
            progress({'phase': 'complete'})
        self.weblogout()

    def update_firmware(self, filename, data=None, progress=None, bank=None):
        result = None
        if self.updating:
            raise pygexc.TemporaryError('Cannot run multiple updates to same '
                                        'target concurrently')
        self.updating = True
        try:
            result = self.update_firmware_backend(filename, data, progress,
                                                  bank)
        except Exception:
            self.updating = False
            self._refresh_token()
            self.wc.grab_json_response('/api/providers/fwupdate', json.dumps(
                {'UPD_WebCancel': 1}))
            self.weblogout()
            raise
        self.updating = False
        self.weblogout()
        return result

    def _refresh_token(self):
        self._refresh_token_wc(self.wc)

    def _refresh_token_wc(self, wc):
        wc.grab_json_response('/api/providers/identity')
        if '_csrf_token' in wc.cookies:
            wc.set_header('X-XSRF-TOKEN', self.wc.cookies['_csrf_token'])
            wc.vintage = util._monotonic_time()

    def set_hostname(self, hostname):
        self.wc.grab_json_response('/api/dataset', {'IMM_HostName': hostname})
        self.wc.grab_json_response('/api/dataset', {'IMM_DescName': hostname})
        self.weblogout()

    def get_hostname(self):
        rsp = self.wc.grab_json_response('/api/dataset/sys_info')
        self.weblogout()
        return rsp['items'][0]['system_name']

    def update_firmware_backend(self, filename, data=None, progress=None,
                                bank=None):
        self.weblogout()
        self._refresh_token()
        rsv = self.wc.grab_json_response('/api/providers/fwupdate', json.dumps(
            {'UPD_WebReserve': 1}))
        if rsv['return'] == 103:
            raise Exception('Update already in progress')
        if rsv['return'] != 0:
            raise Exception('Unexpected return to reservation: ' + repr(rsv))
        xid = random.randint(0, 1000000000)
        uploadthread = webclient.FileUploader(
            self.wc, '/upload?X-Progress-ID={0}'.format(xid), filename, data)
        uploadthread.start()
        uploadstate = None
        while uploadthread.isAlive():
            uploadthread.join(3)
            rsp = self.wc.grab_json_response(
                '/upload/progress?X-Progress-ID={0}'.format(xid))
            if rsp['state'] == 'uploading':
                progress({'phase': 'upload',
                          'progress': 100.0 * rsp['received'] / rsp['size']})
            elif rsp['state'] != 'done':
                if (rsp.get('status', None) == 413
                        or uploadthread.rspstatus == 413):
                    raise Exception('File is larger than supported')
                raise Exception('Unexpected result:' + repr(rsp))
            uploadstate = rsp['state']
            self._refresh_token()
        while uploadstate != 'done':
            rsp = self.wc.grab_json_response(
                '/upload/progress?X-Progress-ID={0}'.format(xid))
            uploadstate = rsp['state']
            self._refresh_token()
        rsp = json.loads(uploadthread.rsp)
        if rsp['items'][0]['name'] != os.path.basename(filename):
            raise Exception('Unexpected response: ' + repr(rsp))
        progress({'phase': 'validating',
                  'progress': 0.0})
        ipmisession.Session.pause(3)
        # aggressive timing can cause the next call to occasionally
        # return 25 and fail
        self._refresh_token()
        rsp = self.wc.grab_json_response('/api/providers/fwupdate', json.dumps(
            {'UPD_WebSetFileName': rsp['items'][0]['path']}))
        if rsp.get('return', 0) in (25, 108):
            raise Exception('Temporary error validating update, try again')
        if rsp.get('return', -1) != 0:
            errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
            raise Exception('Unexpected return to set filename: ' + errmsg)
        self._refresh_token()
        progress({'phase': 'validating',
                  'progress': 25.0})
        rsp = self.wc.grab_json_response('/api/providers/fwupdate', json.dumps(
            {'UPD_WebVerifyUploadFile': 1}))
        if rsp.get('return', 0) == 115:
            raise Exception('Update image not intended for this system')
        elif rsp.get('return', -1) == 108:
            raise Exception('Temporary error validating update, try again')
        elif rsp.get('return', -1) == 109:
            raise Exception('Invalid update file or component does '
                            'not support remote update')
        elif rsp.get('return', -1) != 0:
            errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
            raise Exception('Unexpected return to verify: ' + errmsg)
        verifystatus = 0
        verifyuploadfilersp = None
        while verifystatus != 1:
            self._refresh_token()
            rsp, status = self.wc.grab_json_response_with_status(
                '/api/providers/fwupdate',
                json.dumps({'UPD_WebVerifyUploadFileStatus': 1}))
            if not rsp or status != 200 or rsp.get('return', -1) == 2:
                # The XCC firmware predates the FileStatus api
                verifyuploadfilersp = rsp
                break
            if rsp.get('return', -1) == 109:
                raise Exception('Invalid update file or component does '
                                'not support remote update')
            if rsp.get('return', -1) != 0:
                errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
                raise Exception(
                    'Unexpected return to verifystate: {0}'.format(errmsg))
            verifystatus = rsp['status']
            if verifystatus == 2:
                raise Exception('Failed to verify firmware image')
            if verifystatus != 1:
                ipmisession.Session.pause(1)
            if verifystatus not in (0, 1, 255):
                errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
                raise Exception(
                    'Unexpected reply to verifystate: ' + errmsg)
        progress({'phase': 'validating',
                  'progress': 99.0})
        self._refresh_token()
        rsp = self.wc.grab_json_response('/api/dataset/imm_firmware_success')
        if len(rsp['items']) != 1:
            raise Exception('Unexpected result: ' + repr(rsp))
        firmtype = rsp['items'][0]['firmware_type']
        if not firmtype:
            raise Exception('Unknown firmware description returned: ' + repr(
                rsp['items'][0]) + ' last verify return was: ' + repr(
                    verifyuploadfilersp) + ' with code {0}'.format(status))
        if firmtype not in (
                'TDM', 'WINDOWS DRIV', 'LINUX DRIVER', 'UEFI', 'IMM'):
            # adapter firmware
            webid = rsp['items'][0]['webfile_build_id']
            locations = webid[webid.find('[') + 1:webid.find(']')]
            locations = locations.split(':')
            validselectors = set([])
            for loc in locations:
                validselectors.add(loc.replace('#', '-'))
            self._refresh_token()
            rsp = self.wc.grab_json_response(
                '/api/function/adapter_update?params=pci_GetAdapterListAndFW')
            foundselectors = []
            for adpitem in rsp['items']:
                selector = '{0}-{1}'.format(adpitem['location'],
                                            adpitem['slotNo'])
                if selector in validselectors:
                    foundselectors.append(selector)
                    if len(foundselectors) == len(validselectors):
                        break
            else:
                raise Exception('Could not find matching adapter for update')
            self._refresh_token()
            rsp = self.wc.grab_json_response('/api/function', json.dumps(
                {'pci_SetOOBFWSlots': '|'.join(foundselectors)}))
            if rsp.get('return', -1) != 0:
                errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
                raise Exception(
                    'Unexpected result from PCI select: ' + errmsg)
            self.set_property('/v2/ibmc/uefi/force-inventory', 1)
        else:
            self._refresh_token()
            rsp = self.wc.grab_json_response(
                '/api/dataset/imm_firmware_update')
            if rsp['items'][0]['upgrades'][0]['id'] != 1:
                raise Exception('Unexpected answer: ' + repr(rsp))
        self._refresh_token()
        progress({'phase': 'apply',
                  'progress': 0.0})
        if bank in ('primary', None):
            rsp = self.wc.grab_json_response(
                '/api/providers/fwupdate', json.dumps(
                    {'UPD_WebStartDefaultAction': 1}))
        elif bank == 'backup':
            rsp = self.wc.grab_json_response(
                '/api/providers/fwupdate', json.dumps(
                    {'UPD_WebStartOptionalAction': 2}))

        if rsp.get('return', -1) != 0:
            errmsg = repr(rsp) if rsp else self.wc.lastjsonerror
            raise Exception('Unexpected result starting update: %s' % errmsg)
        complete = False
        while not complete:
            self._refresh_token()
            ipmisession.Session.pause(3)
            rsp = self.wc.grab_json_response(
                '/api/dataset/imm_firmware_progress')
            progress({'phase': 'apply',
                      'progress': rsp['items'][0]['action_percent_complete']})
            if rsp['items'][0]['action_state'] == 'Idle':
                complete = True
                break
            if rsp['items'][0]['action_state'] == 'Complete OK':
                complete = True
                if rsp['items'][0]['action_status'] != 0:
                    raise Exception('Unexpected failure: ' + repr(rsp))
                break
            if (rsp['items'][0]['action_state'] == 'In Progress'
                    and rsp['items'][0]['action_status'] == 2):
                raise Exception('Unexpected failure: ' + repr(rsp))
            if rsp['items'][0]['action_state'] != 'In Progress':
                raise Exception(
                    'Unknown condition waiting for '
                    'firmware update: ' + repr(rsp))
        if bank == 'backup':
            return 'complete'
        return 'pending'

    def add_psu_hwinfo(self, hwmap):
        psud = self.wc.grab_json_response('/api/dataset/imm_power_supplies')
        if not psud:
            return
        for psus in psud['items'][0]['power']:
            hwmap['PSU {0}'.format(psus['name'])] = {
                'Wattage': psus['rated_power'],
                'FRU Number': psus['fru_number'],
            }

    def augment_psu_info(self, info, psuname):
        psud = self.get_cached_data('lenovo_cached_psuhwinfo')
        if not psud:
            psud = self.wc.grab_json_response(
                '/api/dataset/imm_power_supplies')
            if not psud:
                return
            self.datacache['lenovo_cached_psuhwinfo'] = (
                psud, util._monotonic_time())
        matchname = int(psuname.split(' ')[1])
        for psus in psud['items'][0]['power']:
            if psus['name'] == matchname:
                info['Wattage'] = psus['rated_power']
                break

    def get_health(self, summary):
        try:
            wc = self.get_webclient(False)
        except (socket.timeout, socket.error):
            wc = None
        if not wc:
            summary['health'] = pygconst.Health.Critical
            summary['badreadings'].append(
                sdr.SensorReading({'name': 'HTTPS Service',
                                   'states': ['Unreachable'],
                                   'state_ids': [3],
                                   'health': pygconst.Health.Critical,
                                   'type': 'BMC'}, ''))
            raise pygexc.BypassGenericBehavior()
        rsp = wc.grab_json_response('/api/providers/imm_active_events')
        if 'items' in rsp and len(rsp['items']) == 0:
            ledcheck = self.wc.grab_json_response(
                '/api/dataset/imm_status_power')
            for led in ledcheck.get('items', [{}])[0].get('LEDs', ()):
                if led.get('name', None) == 'Fault':
                    if led.get('status', 0) == 0:
                        raise pygexc.BypassGenericBehavior()
                    break
            else:
                # The XCC reports healthy, no need to interrogate
                raise pygexc.BypassGenericBehavior()
        fallbackdata = []
        hmap = {
            'I': pygconst.Health.Ok,
            'E': pygconst.Health.Critical,
            'W': pygconst.Health.Warning,
        }
        infoevents = False
        for item in rsp.get('items', ()):
            # while usually the ipmi interrogation shall explain things,
            # just in case there is a gap, make sure at least the
            # health field is accurately updated
            itemseverity = hmap.get(item.get('severity', 'E'),
                                    pygconst.Health.Critical)
            if itemseverity == pygconst.Health.Ok:
                infoevents = True
                continue
            if (summary['health'] < itemseverity):
                summary['health'] = itemseverity
            if item['cmnid'] == 'FQXSPPW0104J':
                # This event does not get modeled by the sensors
                # add a made up sensor to explain
                summary['badreadings'].append(
                    sdr.SensorReading({'name': item['source'],
                                       'states': ['Not Redundant'],
                                       'state_ids': [3],
                                       'health': pygconst.Health.Warning,
                                       'type': 'Power'}, ''))
            elif item['cmnid'] == 'FQXSFMA0041K':
                summary['badreadings'].append(
                    sdr.SensorReading({
                        'name': 'Optane DCPDIMM',
                        'health': pygconst.Health.Warning,
                        'type': 'Memory',
                        'states': [item['message']]},
                        '')
                )
            else:
                fallbackdata.append(sdr.SensorReading({
                    'name': item['source'],
                    'states': [item['message']],
                    'health': itemseverity,
                    'type': item['source'],
                }, ''))
        if (summary.get('health', pygconst.Health.Ok) == pygconst.Health.Ok
                and not infoevents):
            # Fault LED is lit without explanation, mark to encourage
            # examination
            summary['health'] = pygconst.Health.Warning
            if not fallbackdata:
                fallbackdata.append(sdr.SensorReading({
                    'name': 'Fault LED',
                    'states': ['Active'],
                    'health': pygconst.Health.Warning,
                    'type': 'LED',
                }, ''))
        return fallbackdata
        # Will use the generic handling for unhealthy systems

    def get_licenses(self):
        licdata = self.wc.grab_json_response('/api/providers/imm_fod')
        for lic in licdata.get('items', [{}])[0].get('keys', []):
            if lic['status'] == 0:
                yield {'name': lic['feature'], 'state': 'Active'}
            elif lic['status'] == 10:
                yield {'name': lic['feature'],
                       'state': 'Missing required license'}

    def save_licenses(self, directory):
        licdata = self.wc.grab_json_response('/api/providers/imm_fod')
        for lic in licdata.get('items', [{}])[0].get('keys', []):
            licid = ','.join((str(lic['type']), str(lic['id'])))
            rsp = self.wc.grab_json_response(
                '/api/providers/imm_fod', {'FOD_LicenseKeyExport': licid})
            filename = rsp.get('FileName', None)
            if filename:
                url = '/download/' + filename
                savefile = os.path.join(directory, filename)
                fd = webclient.FileDownloader(self.wc, url, savefile)
                fd.start()
                while fd.isAlive():
                    fd.join(1)
                    self._refresh_token()
                yield savefile

    def delete_license(self, name):
        licdata = self.wc.grab_json_response('/api/providers/imm_fod')
        for lic in licdata.get('items', [{}])[0].get('keys', []):
            if lic.get('feature', None) == name:
                licid = ','.join((str(lic['type']), str(lic['id'])))
                self.wc.grab_json_response(
                    '/api/providers/imm_fod', {'FOD_LicenseKeyDelete': licid})
                break

    def apply_license(self, filename, progress=None, data=None):
        license_errors = {
            310: "License is for a different model of system",
            311: "License is for a different system serial number",
            312: "License is invalid",
            313: "License is expired",
            314: "License usage limit reached",
        }
        uploadthread = webclient.FileUploader(self.wc, '/upload', filename,
                                              data=data)
        uploadthread.start()
        uploadthread.join()
        rsp = json.loads(uploadthread.rsp)
        licpath = rsp.get('items', [{}])[0].get('path', None)
        if licpath:
            rsp = self.wc.grab_json_response(
                '/api/providers/imm_fod', {'FOD_LicenseKeyInstall': licpath})
            if rsp.get('return', 0) in license_errors:
                raise pygexc.InvalidParameterValue(
                    license_errors[rsp['return']])
        return self.get_licenses()

    def get_user_expiration(self, uid):
        uid = uid - 1
        userinfo = self.wc.grab_json_response('/api/dataset/imm_users')
        for user in userinfo['items'][0]['users']:
            if user['users_user_id'] == uid:
                days = user['users_pass_left_days']
                if days == 366:
                    return 0
                else:
                    return days
