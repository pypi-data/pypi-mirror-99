# -*- coding:utf-8 -*-

import re
import os
import sys
import shutil
import argparse
import subprocess
import traceback
import hashlib
import lzma

try:
    import bflb_path
except ImportError:
    from libs import bflb_path
from libs import bflb_utils
from libs import bflb_eflash_loader
from libs import bflb_toml as toml
from libs import bflb_flash_select
from libs.bflb_utils import verify_hex_num, get_eflash_loader, get_serial_ports, convert_path
from libs.bflb_configobj import BFConfigParser
import libs.bflb_pt_creater as partition
import libs.bflb_eflash_loader as eflash_loader
import libs.bflb_efuse_boothd_create as eb_create
import libs.bflb_img_create as img_create
import libs.bflb_ro_params_device_tree as bl_ro_device_tree
import globalvar as gol

parser_eflash = bflb_utils.eflash_loader_parser_init()

# Get app path
if getattr(sys, "frozen", False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)

try:
    import changeconf as cgc
    conf_sign = True
except ImportError:
    conf_sign = False

if conf_sign:
    chip_dict = {cgc.lower_name: "bl602"}
    chip_xtal = cgc.choice_xtal
    chip_brd = cgc.choice_board
    bl_factory_params_file_prefix = cgc.show_text_first_value
else:
    chip_dict = {
        "bl56x": "bl60x",
        "bl60x": "bl60x",
        "bl562": "bl602",
        "bl602": "bl602",
        "bl702": "bl702",
        "bl606p": "bl606p",
    }
    chip_xtal = 'bl60x_xtal'
    chip_brd = 'bl60x_brd'
    bl_factory_params_file_prefix = 'bl_factory_params_'


def parse_rfpa(bin):
    with open(bin, "rb") as fp:
        content = fp.read()
        return content[1024:1032]


def flash_type(chip_flash_name):
    cfg_file_name_list = chip_flash_name.split("_")
    _type = cfg_file_name_list[1]
    vendor = cfg_file_name_list[2]
    size = cfg_file_name_list[3]
    return (_type, vendor, size)


def img_create_sha256_data(data_bytearray):
    hashfun = hashlib.sha256()
    hashfun.update(data_bytearray)
    return bflb_utils.hexstr_to_bytearray(hashfun.hexdigest())


def bl_get_largest_addr(addrs, files):
    maxlen = 0
    datalen = 0
    for i in range(len(addrs)):
        if int(addrs[i], 16) > maxlen:
            maxlen = int(addrs[i], 16)
            datalen = os.path.getsize(os.path.join(app_path, files[i]))
    return maxlen + datalen


def bl_get_file_data(files):
    datas = []
    for file in files:
        with open(os.path.join(app_path, file), 'rb') as fp:
            data = fp.read()
        datas.append(data)
    return datas


def bl_create_flash_default_data(length):
    datas = bytearray(length)
    for i in range(length):
        datas[i] = 0xff
    return datas


def generate_romfs_img(romfs_dir, dst_img_name):
    exe = None
    if os.name == 'nt':
        exe = os.path.join(app_path, 'common/genromfs', 'genromfs.exe')
    elif os.name == 'posix':
        machine = os.uname().machine
        if machine == 'x86_64':
            exe = os.path.join(app_path, 'common/genromfs', 'genromfs_amd64')
        elif machine == 'armv7l':
            exe = os.path.join(app_path, 'common/genromfs', 'genromfs_armel')
    if exe is None:
        bflb_utils.printf('NO supported genromfs exe for your platform!')
        return -1
    dir = os.path.abspath(romfs_dir)
    dst = os.path.abspath(dst_img_name)
    bflb_utils.printf('Generating romfs image %s using directory %s ... ' % (dst, dir))
    return subprocess.call([exe, '-d', dir, '-f', dst])


def exe_genitor(list_args):
    p = subprocess.Popen(list_args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    while subprocess.Popen.poll(p) is None:
        try:
            r = p.stdout.readline().strip().decode('utf-8')
            if r == '':
                break
            bflb_utils.printf(r)
        except UnicodeDecodeError:
            continue


class BflbIotTool(object):

    def __init__(self, chipname="bl60x", chiptype="bl60x"):
        self.efuse_load_en = False
        self.config = {}
        self.chipname = chipname
        self.chiptype = chiptype
        self.eflash_loader_t = bflb_eflash_loader.BflbEflashLoader()
     
        eflash_loader_cfg_org = os.path.join(app_path, chipname, "eflash_loader/eflash_loader_cfg.conf")
        self.eflash_loader_cfg = os.path.join(app_path, chipname, "eflash_loader/eflash_loader_cfg.ini")
        if os.path.isfile(self.eflash_loader_cfg) is False:
            shutil.copy(eflash_loader_cfg_org, self.eflash_loader_cfg)
        if chiptype == "bl60x":
            bh_cfg_file_org = os.path.join(app_path, chipname,
                                           "efuse_bootheader/efuse_bootheader_cfg_dp.conf")
        else:
            bh_cfg_file_org = os.path.join(app_path, chipname,
                                           "efuse_bootheader/efuse_bootheader_cfg.conf")
        self.bh_cfg_file = os.path.join(app_path, chipname, "efuse_bootheader/efuse_bootheader_cfg.ini")
        if os.path.isfile(self.bh_cfg_file) is False:
            shutil.copy(bh_cfg_file_org, self.bh_cfg_file)
        
        ini_file_kw = 'efuse_bootheader_cfg_'
        ini_file_kw_len = len(ini_file_kw)
        chip_flash_type_config = {}
        bl60x_boards = set()
        bl60x_board_xtal = set()
        bl_factory_params_file_prefix_len = len(bl_factory_params_file_prefix)
        self.bl60x_boards_xtal_selectbox = []
        self.bl60x_boards_selectbox = []
        try:
            bl_factory_params_files = os.listdir(os.path.join(app_path, chipname, 'device_tree'))
            for bl_fac_p_f in bl_factory_params_files:
                if not os.path.isdir(bl_fac_p_f):
                    drop_idx_start = bl_fac_p_f.find(bl_factory_params_file_prefix)
                    if drop_idx_start != -1:
                        drop_idx_end = drop_idx_start + bl_factory_params_file_prefix_len
                        drop_value_l = bl_fac_p_f[drop_idx_end:-4].split('_')
                        bl60x_boards.add(drop_value_l[0].strip())
                        bl60x_board_xtal.add(drop_value_l[1].strip())
            self.bl60x_boards_selectbox = list(bl60x_boards)
            self.bl60x_boards_xtal_selectbox = list(bl60x_board_xtal)
        except Exception as e:
            bflb_utils.printf(e)


    def bl60x_fw_boot_head_gen(self,
                               boot2,
                               xtal,
                               config,
                               encrypt=False,
                               sign=False,
                               chipname="bl60x",
                               chiptype="bl60x",
                               cpu_type=None,
                               boot2_en=False):
        cfg = BFConfigParser()
        cfg.read(config)
        dict_xtal = gol.xtal_type[chiptype]
    
        if cpu_type is not None:
            bootheader_section_name = "BOOTHEADER_" + cpu_type + "_CFG"
        else:
            if "BOOTHEADER_CPU0_CFG" in cfg.sections():
                bootheader_section_name = "BOOTHEADER_CPU0_CFG"
            else:
                bootheader_section_name = "BOOTHEADER_CFG"
    
        if chiptype == "bl702":
            if boot2_en is True:
                cfg.set(bootheader_section_name, 'boot2_enable', 1)
            else:
                cfg.set(bootheader_section_name, 'boot2_enable', 0)
        if boot2 is True:
            cfg.set(bootheader_section_name, 'img_start', '0x2000')
            cfg.set(bootheader_section_name, 'cache_enable', '1')
            if cpu_type is not None:
                cfg.set(bootheader_section_name, 'halt_cpu1', '1')
            #cfg.set(bootheader_section_name, 'key_sel', '0')
    
        if encrypt:
            cfg.set(bootheader_section_name, 'encrypt_type', '1')
        else:
            cfg.set(bootheader_section_name, 'encrypt_type', '0')
    
        if sign:
            cfg.set(bootheader_section_name, 'sign', '1')
        else:
            cfg.set(bootheader_section_name, 'sign', '0')
    
        bflb_utils.printf('bl60x_fw_boot_head_gen xtal: %s' % xtal)
        cfg.set(bootheader_section_name, 'xtal_type', dict_xtal.index(xtal))
    
        cfg.write(config)
        eb_create.efuse_boothd_create_process(chipname, chiptype, config)
    
    
    def bl60x_mfg_boot_head_gen(self,
                                mfg_addr,
                                xtal,
                                config,
                                chipname="bl60x",
                                chiptype="bl60x",
                                cpu_type=None):
        cfg = BFConfigParser()
        cfg.read(config)
        bflb_utils.printf(mfg_addr)
        dict_xtal = gol.xtal_type[chiptype]
    
        if cpu_type is not None:
            bootheader_section_name = "BOOTHEADER_" + cpu_type + "_CFG"
        else:
            if "BOOTHEADER_CPU0_CFG" in cfg.sections():
                bootheader_section_name = "BOOTHEADER_CPU0_CFG"
            else:
                bootheader_section_name = "BOOTHEADER_CFG"
    
        cfg.set(bootheader_section_name, 'img_start', mfg_addr)
        cfg.set(bootheader_section_name, 'cache_enable', '1')
        if cpu_type is not None:
            cfg.set(bootheader_section_name, 'halt_cpu1', '1')
        cfg.set(bootheader_section_name, 'halt_cpu1', '1')
        #cfg.set(bootheader_section_name, 'key_sel', '0')
    
        bflb_utils.printf('bl60x_mfg_boot_head_gen xtal: %s' % xtal)
        cfg.set(bootheader_section_name, 'xtal_type', dict_xtal.index(xtal))
    
        cfg.write(config)
        eb_create.efuse_boothd_create_process(chipname, chiptype, config)
    
    
    def bl60x_image_gen_cfg(self,
                            chipname,
                            chiptype,
                            raw_bin_name,
                            bintype,
                            key=None,
                            iv=None,
                            publickey=None,
                            privatekey=None,
                            cfg_ini=None,
                            cpu_type=None):
        efuse_file = os.path.join(app_path, chipname, "efuse_bootheader/efusedata.bin")
        efuse_mask_file = os.path.join(app_path, chipname, "efuse_bootheader/efusedata_mask.bin")
        if chiptype == "bl60x":
            bh_file = os.path.join(app_path, chipname, "efuse_bootheader/bootheader_cpu0.bin")
        else:
            bh_file = os.path.join(app_path, chipname, "efuse_bootheader/bootheader.bin")
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            if chiptype == "bl60x":
                f_org = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg_dp.conf")
            else:
                f_org = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg.conf")
            f = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg.ini")
            if os.path.isfile(f) is False:
                shutil.copy(f_org, f)
        else:
            f = cfg_ini
        cfg.read(f)
        if bintype == "fw":
            if cpu_type is None:
                bootinfo_file = os.path.join(app_path, chipname, "img_create_iot", "bootinfo.bin")
                img_file = os.path.join(app_path, chipname, "img_create_iot", "img.bin")
            else:
                bootinfo_file = os.path.join(app_path, chipname,
                                             "img_create_iot", "bootinfo_{0}.bin".format(cpu_type.lower()))
                img_file = os.path.join(app_path, chipname,
                                        "img_create_iot", "img_{0}.bin".format(cpu_type.lower()))
        else:
            bootinfo_file = os.path.join(app_path, chipname,
                                         "img_create_iot", "bootinfo_{0}.bin".format(bintype))
            img_file = os.path.join(app_path, chipname, "img_create_iot", "img_{0}.bin".format(bintype))
    
        if cpu_type is not None:
            img_section_name = "Img_" + cpu_type + "_Cfg"
        else:
            if "Img_CPU0_Cfg" in cfg.sections():
                img_section_name = "Img_CPU0_Cfg"
            else:
                img_section_name = "Img_Cfg"
        cfg.set(img_section_name, 'boot_header_file', bh_file)
        cfg.set(img_section_name, 'efuse_file', efuse_file)
        cfg.set(img_section_name, 'efuse_mask_file', efuse_mask_file)
        cfg.set(img_section_name, 'segdata_file', raw_bin_name)
        cfg.set(img_section_name, 'bootinfo_file', bootinfo_file)
        cfg.set(img_section_name, 'img_file', img_file)
        if key:
            cfg.set(img_section_name, 'aes_key_org', key)
        if iv:
            cfg.set(img_section_name, 'aes_iv', iv)
        if publickey:
            cfg.set(img_section_name, 'publickey_file', publickey)
        if privatekey:
            cfg.set(img_section_name, 'privatekey_file_uecc', privatekey)
        cfg.write(f, 'w')
        return f
    
    
    def bl60x_mfg_ota_header(self, chipname, file_bytearray, use_xz):
        ota_cfg = os.path.join(app_path, chipname, "conf/ota.toml")
        parsed_toml = toml.load(ota_cfg)
        header_len = 512
        header = bytearray()
        file_len = len(file_bytearray)
        m = hashlib.sha256()
    
        # 16 Bytes header
        data = b'BL60X_OTA_Ver1.0'
        for b in data:
            header.append(b)
        # 4 Byte ota file type
        if use_xz:
            data = b'XZ  '
        else:
            data = b'RAW '
        for b in data:
            header.append(b)
    
        # 4 Bytes file length
        file_len_bytes = file_len.to_bytes(4, byteorder='little')
        for b in file_len_bytes:
            header.append(b)
    
        # 8 Bytes pad
        header.append(0x01)
        header.append(0x02)
        header.append(0x03)
        header.append(0x04)
        header.append(0x05)
        header.append(0x06)
        header.append(0x07)
        header.append(0x08)
    
        # 16 Bytes Hardware version
        data = bytearray(parsed_toml["ota"]["version_hardware"].encode())
        data_len = 16 - len(data)
        for b in data:
            header.append(b)
        while data_len > 0:
            header.append(0x00)
            data_len = data_len - 1
    
        # 16 Bytes firmware version
        data = bytearray(parsed_toml["ota"]["version_software"].encode())
        data_len = 16 - len(data)
        for b in data:
            header.append(b)
        while data_len > 0:
            header.append(0x00)
            data_len = data_len - 1
    
        # 32 Bytes SHA256
        m.update(file_bytearray)
        hash_bytes = m.digest()
        for b in hash_bytes:
            header.append(b)
        header_len = header_len - len(header)
        while header_len > 0:
            header.append(0xFF)
            header_len = header_len - 1
        return header
    
  
    def bl60x_mfg_ota_xz_gen(self, chipname="bl60x", chiptype="bl60x", cpu_type=None):
        bl60x_xz_filters = [
            {
                "id": lzma.FILTER_LZMA2,
                "dict_size": 32768
            },
        ]
    
        fw_ota_bin = bytearray()
        fw_ota_bin_xz = bytearray()
        if cpu_type is None:
            fw_ota_path = os.path.join(app_path, chipname, "ota/FW_OTA.bin")
        else:
            fw_ota_path = os.path.join(app_path, chipname, "ota/" + cpu_type + "_OTA.bin")
        with open(fw_ota_path, mode="rb") as bin_f:
            file_bytes = bin_f.read()
            for b in file_bytes:
                fw_ota_bin.append(b)
        if cpu_type is None:
            fw_ota_path = os.path.join(app_path, chipname, "ota/FW_OTA.bin.xz")
        else:
            fw_ota_path = os.path.join(app_path, chipname, "ota/" + cpu_type + "_OTA.bin.xz")
        with lzma.open(fw_ota_path, mode="wb", check=lzma.CHECK_CRC32,
                       filters=bl60x_xz_filters) as xz_f:
            xz_f.write(fw_ota_bin)
        with open(fw_ota_path, mode="rb") as f:
            file_bytes = f.read()
            for b in file_bytes:
                fw_ota_bin_xz.append(b)
        fw_ota_bin_xz_ota = self.bl60x_mfg_ota_header(chipname, fw_ota_bin_xz, use_xz=1)
        for b in fw_ota_bin_xz:
            fw_ota_bin_xz_ota.append(b)
        if cpu_type is None:
            fw_ota_path = os.path.join(app_path, chipname, "ota/FW_OTA.bin.xz.ota")
        else:
            fw_ota_path = os.path.join(app_path, chipname, "ota/" + cpu_type + "_OTA.bin.xz.ota")
        with open(fw_ota_path, mode="wb") as f:
            f.write(fw_ota_bin_xz_ota)
        with open(fw_ota_path.replace(".ota", ".hash"), mode="wb") as f:
            f.write(fw_ota_bin_xz + img_create_sha256_data(fw_ota_bin_xz))
    
    
    def bl60x_mfg_ota_bin_gen(self, chipname="bl60x", chiptype="bl60x", cpu_type=None):
        fw_header_len = 4096
        fw_ota_bin = bytearray()
    
        ota_path = os.path.join(app_path, chipname, "ota")
        if os.path.isdir(ota_path) is False:
            os.mkdir(ota_path)
    
        if cpu_type is None:
            bootinfo_fw_path = os.path.join(app_path, chipname, "img_create_iot", "bootinfo.bin")
        else:
            bootinfo_fw_path = os.path.join(app_path, chipname,
                                            "img_create_iot", "bootinfo_" + cpu_type.lower() + ".bin")
        with open(bootinfo_fw_path, mode="rb") as f:
            file_bytes = f.read(4096)
            for b in file_bytes:
                fw_ota_bin.append(b)
        i = fw_header_len - len(fw_ota_bin)
        bflb_utils.printf("FW Header is %d, %d still needed" % (len(fw_ota_bin), i))
        while i > 0:
            fw_ota_bin.append(0xFF)
            i = i - 1
        bflb_utils.printf("FW OTA bin header is Done. Len is %d" % len(fw_ota_bin))
        if cpu_type is None:
            img_fw_path = os.path.join(app_path, chipname, "img_create_iot", "img.bin")
        else:
            img_fw_path = os.path.join(app_path, chipname,
                                       "img_create_iot", "img_" + cpu_type.lower() + ".bin")
        with open(img_fw_path, mode="rb") as f:
            file_bytes = f.read()
            for b in file_bytes:
                fw_ota_bin.append(b)
        fw_ota_bin_header = self.bl60x_mfg_ota_header(chipname, fw_ota_bin, use_xz=0)
        if cpu_type is None:
            fw_ota_path = os.path.join(app_path, chipname, "ota/FW_OTA.bin")
        else:
            fw_ota_path = os.path.join(app_path, chipname, "ota/" + cpu_type + "_OTA.bin")
        with open(fw_ota_path, mode="wb") as f:
            f.write(fw_ota_bin)
        for b in fw_ota_bin:
            fw_ota_bin_header.append(b)
        if cpu_type is None:
            fw_ota_path = os.path.join(app_path, chipname, "ota/FW_OTA.bin.ota")
        else:
            fw_ota_path = os.path.join(app_path, chipname, "ota/" + cpu_type + "_OTA.bin.ota")
        with open(fw_ota_path, mode="wb") as f:
            f.write(fw_ota_bin_header)
        bflb_utils.printf("FW OTA bin is Done. Len is %d" % len(fw_ota_bin))
        self.bl60x_mfg_ota_xz_gen(chipname, chiptype, cpu_type)
        bflb_utils.printf("FW OTA xz is Done")
    
    
    def bl60x_image_gen(self,
                        chipname,
                        chiptype,
                        cpu_type,
                        bintype,
                        raw_bin_name,
                        key=None,
                        iv=None,
                        publickey=None, 
                        privarekey=None,
                        cfg_ini=None):
        # python bflb_img_create.py -c np -i media -s none
        f = self.bl60x_image_gen_cfg(chipname, chiptype, raw_bin_name, bintype, key, iv, publickey, privarekey, cfg_ini, cpu_type)
        if key or (publickey is not None and privarekey is not None):
            img_cfg = BFConfigParser()
            img_cfg.read(f)
            efusefile = img_cfg.get("Img_Cfg", "efuse_file")
            efusemaskfile = img_cfg.get("Img_Cfg", "efuse_mask_file")
            cfg = BFConfigParser()
            cfg.read(self.eflash_loader_cfg)
            cfg.set('EFUSE_CFG', 'file', convert_path(os.path.relpath(efusefile, app_path)))
            cfg.set('EFUSE_CFG', 'maskfile', convert_path(os.path.relpath(efusemaskfile, app_path)))
            cfg.write(self.eflash_loader_cfg, 'w')
            self.efuse_load_en = True
        else:
            self.efuse_load_en = False
        return img_create.create_sp_media_image_file(f, chiptype, cpu_type)
    
    
    def bl60x_mfg_flasher_cfg(self, uart, baudrate='57600', cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        cfg.set('LOAD_CFG', 'interface', 'uart')
        cfg.set('LOAD_CFG', 'device', uart)
        cfg.set('LOAD_CFG', 'speed_uart_load', baudrate)
        cfg.write(f, 'w')
    
    
    def bl60x_mfg_flasher_jlink_cfg(self, rate="1000", cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        cfg.set('LOAD_CFG', 'interface', 'jlink')
        cfg.set('LOAD_CFG', 'speed_jlink', rate)
        cfg.write(f, 'w')
    
    
    def bl60x_mfg_flasher_openocd_cfg(self, rate="8000", cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        cfg.set('LOAD_CFG', 'interface', 'openocd')
        cfg.set('LOAD_CFG', 'speed_jlink', rate)
        cfg.write(f, 'w')
    
    
    def bl60x_mfg_flasher_erase_all(self, erase, cfg_ini=None):
        cfg = BFConfigParser()
        if cfg_ini in [None, '']:
            f = self.eflash_loader_cfg
        else:
            f = cfg_ini
        cfg.read(f)
        if erase is True:
            cfg.set('LOAD_CFG', 'erase', '2')
        else:
            cfg.set('LOAD_CFG', 'erase', '1')
        cfg.write(f, 'w')
    
   
    def bl_write_flash_img(self, d_addrs, d_files, flash_size):
        whole_img_len = bl_get_largest_addr(d_addrs, d_files)
        whole_img_data = bl_create_flash_default_data(whole_img_len)
        whole_img_file = os.path.join(app_path, self.chipname, "img_create_iot", "whole_flash_data.bin")
        filedatas = bl_get_file_data(d_files)
        # create_whole_image_flash
        for i in range(len(d_addrs)):
            start_addr = int(d_addrs[i], 16)
            whole_img_data[start_addr:start_addr + len(filedatas[i])] = filedatas[i]
        fp = open(whole_img_file, 'wb+')
        fp.write(whole_img_data)
        fp.close()
    
    
    def bl60x_mfg_flasher_eflash_loader_cfg(self,
                                            chipname,
                                            chiptype,
                                            bin_file,
                                            boot2,
                                            ro_params,
                                            pt_parcel,
                                            media,
                                            mfg,
                                            flash_opt="1M"):
        bflb_utils.printf("========= eflash loader config =========")
        d_files = []
        d_addrs = []
        bind_bootinfo = True
        chipnamedir = os.path.join(app_path, chipname)
    
        if pt_parcel is None:
            bflb_utils.set_error_code("007B")
            return bflb_utils.errorcode_msg()
    
        if boot2 is True:
            if bind_bootinfo is True:
                whole_img = chipnamedir + "/img_create_iot/whole_img_boot2.bin"
                whole_img_len = 0x2000 + os.path.getsize(
                    chipnamedir + "/img_create_iot/img_boot2.bin")
                whole_img_data = bl_create_flash_default_data(whole_img_len)
                filedata = bl_get_file_data([chipname + "/img_create_iot/bootinfo_boot2.bin"])[0]
                whole_img_data[0:len(filedata)] = filedata
                filedata = bl_get_file_data([chipname + "/img_create_iot/img_boot2.bin"])[0]
                whole_img_data[0x2000:0x2000 + len(filedata)] = filedata
                fp = open(whole_img, 'wb+')
                fp.write(whole_img_data)
                fp.close()
                d_files.append(chipname + "/img_create_iot/whole_img_boot2.bin")
                d_addrs.append("00000000")
            else:
                d_files.append(chipname + "/img_create_iot/bootinfo_boot2.bin")
                d_addrs.append("00000000")
                d_files.append(chipname + "/img_create_iot/img_boot2.bin")
                d_addrs.append("00002000")
        elif chiptype == "bl702":
            bflb_utils.printf("========= copy bootinfo_boot2.bin =========")
            bflb_utils.copyfile(chipname + "/img_create_iot/bootinfo.bin",
                                chipname + "/img_create_iot/bootinfo_boot2.bin")
            d_files.append(chipname + "/img_create_iot/bootinfo_boot2.bin")
            d_addrs.append("00000000")
    
        if pt_parcel is not None and len(pt_parcel) > 0 and pt_parcel['pt_new'] is True:
            d_files.append(chipname + "/partition/partition.bin")
            d_addrs.append(hex(pt_parcel['pt_addr0'])[2:])
            d_files.append(chipname + "/partition/partition.bin")
            d_addrs.append(hex(pt_parcel['pt_addr1'])[2:])
    
        if bin_file is True and 'fw_cpu0_addr' in pt_parcel:
            if bind_bootinfo is True:
                whole_img = chipnamedir + "/img_create_iot/whole_img_cpu0.bin"
                whole_img_len = 0x1000 + os.path.getsize(
                    chipnamedir + "/img_create_iot/img_cpu0.bin")
                whole_img_data = bl_create_flash_default_data(whole_img_len)
                filedata = bl_get_file_data([chipname + "/img_create_iot/bootinfo_cpu0.bin"])[0]
                whole_img_data[0:len(filedata)] = filedata
                filedata = bl_get_file_data([chipname + "/img_create_iot/img_cpu0.bin"])[0]
                whole_img_data[0x1000:0x1000 + len(filedata)] = filedata
                fp = open(whole_img, 'wb+')
                fp.write(whole_img_data)
                fp.close()
                d_files.append(chipname + "/img_create_iot/whole_img_cpu0.bin")
                d_addrs.append(hex(pt_parcel['fw_cpu0_addr'])[2:])
            else:
                d_files.append(chipname + "/img_create_iot/bootinfo_cpu0.bin")
                d_addrs.append(hex(pt_parcel['fw_cpu0_addr'])[2:])
                d_files.append(chipname + "/img_create_iot/img_cpu0.bin")
                d_addrs.append(hex(pt_parcel['fw_cpu0_addr'] + 0x1000)[2:])
    
        if bin_file is True and 'fw_addr' in pt_parcel:
            if bind_bootinfo is True:
                whole_img = chipnamedir + "/img_create_iot/whole_img.bin"
                whole_img_len = 0x1000 + os.path.getsize(
                    chipnamedir + "/img_create_iot/img.bin")
                whole_img_data = bl_create_flash_default_data(whole_img_len)
                filedata = bl_get_file_data([chipname + "/img_create_iot/bootinfo.bin"])[0]
                whole_img_data[0:len(filedata)] = filedata
                filedata = bl_get_file_data([chipname + "/img_create_iot/img.bin"])[0]
                whole_img_data[0x1000:0x1000 + len(filedata)] = filedata
                fp = open(whole_img, 'wb+')
                fp.write(whole_img_data)
                fp.close()
                d_files.append(chipname + "/img_create_iot/whole_img.bin")
                d_addrs.append(hex(pt_parcel['fw_addr'])[2:])
            else:
                d_files.append(chipname + "/img_create_iot/bootinfo.bin")
                d_addrs.append(hex(pt_parcel['fw_addr'])[2:])
                d_files.append(chipname + "/img_create_iot/img.bin")
                d_addrs.append(hex(pt_parcel['fw_addr'] + 0x1000)[2:])
    
        if ro_params is not None and len(ro_params) > 0 and pt_parcel['conf_addr'] is not None:
            bl_ro_device_tree.bl_ro_params_device_tree(ro_params,
                                                       chipname + "/device_tree/ro_params.dtb")
            d_files.append(chipname + "/device_tree/ro_params.dtb")
            d_addrs.append(hex(pt_parcel['conf_addr'])[2:])
    
        if media is True and pt_parcel['media_addr'] is not None:
            d_files.append(chipname + "/img_create_iot/media.bin")
            d_addrs.append(hex(pt_parcel['media_addr'])[2:])
    
        if mfg is True:
            if bind_bootinfo is True:
                whole_img = chipnamedir + "/img_create_iot/whole_img_mfg.bin"
                whole_img_len = 0x1000 + os.path.getsize(
                    chipnamedir + "/img_create_iot/img_mfg.bin")
                whole_img_data = bl_create_flash_default_data(whole_img_len)
                filedata = bl_get_file_data([chipname + "/img_create_iot/bootinfo_mfg.bin"])[0]
                whole_img_data[0:len(filedata)] = filedata
                filedata = bl_get_file_data([chipname + "/img_create_iot/img_mfg.bin"])[0]
                whole_img_data[0x1000:0x1000 + len(filedata)] = filedata
                fp = open(whole_img, 'wb+')
                fp.write(whole_img_data)
                fp.close()
                d_files.append(chipname + "/img_create_iot/whole_img_mfg.bin")
                d_addrs.append(hex(pt_parcel['mfg_addr'])[2:])
            else:
                d_files.append(chipname + "/img_create_iot/bootinfo_mfg.bin")
                d_addrs.append(hex(pt_parcel['mfg_addr'])[2:])
                d_files.append(chipname + "/img_create_iot/img_mfg.bin")
                d_addrs.append(hex(pt_parcel['mfg_addr'] + 0x1000)[2:])
    
        if len(d_files) > 0 and len(d_addrs) > 0:
            cfg = BFConfigParser()
            cfg.read(self.eflash_loader_cfg)
            self.bl_write_flash_img(d_addrs, d_files, flash_opt)
            files_str = " ".join(d_files)
            addrs_str = " ".join(d_addrs)
            cfg.set('FLASH_CFG', 'file', files_str)
            cfg.set('FLASH_CFG', 'address', addrs_str)
            cfg.write(self.eflash_loader_cfg, 'w')
    
            ret = img_create.compress_dir(chipname, "img_create_iot", self.efuse_load_en)
            if ret is not True:
                return bflb_utils.errorcode_msg()
            return True
        else:
            bflb_utils.set_error_code("0060")
            return bflb_utils.errorcode_msg()
    
    
    def bl60x_mfg_uart_flasher(self, uart, baudrate='57600', cfg_ini=None):
        self.bl60x_mfg_flasher_cfg(uart, baudrate, cfg_ini)
        exe_genitor([
            'python', os.path.join(app_path, "libs/bflb_eflash_loader.py"), '--write', '--flash', '-c', self.eflash_loader_cfg
        ])


    def flasher_download_cfg_ini_gen(self, chipname, chiptype, cpu_type, config):
        bin_d = False
        boot2_d = False
        ro_params_d = None
        pt_parcel = None
        media_bin_d = False
        mfg_d = False
        boot2_en = False
        dts_bytearray = None
        
        partition_path = os.path.join(app_path, chipname, "partition/partition.bin")
        error = "Please check your partition table file"
        #gol.GlobalVar.values = config
        self.config = config

        cfg = BFConfigParser()
        cfg.read(self.eflash_loader_cfg)
        if cfg.has_option("FLASH_CFG", "flash_id"):
            flash_id = cfg.get("FLASH_CFG", "flash_id")
            bflb_utils.printf("========= chip flash id: %s =========" % flash_id)
            if chiptype == "bl602" or chiptype == "bl702":
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False,
                                                      "BOOTHEADER_CFG") is False:
                    error = "flash_id:" + flash_id + " do not support"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0069")
                    return bflb_utils.errorcode_msg()
            elif chiptype == "bl60x":
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, self.bh_cfg_file, False,
                                                      "BOOTHEADER_CPU0_CFG") is False:
                    error = "flash_id:" + flash_id + " do not support"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0069")
                    return bflb_utils.errorcode_msg()
        else:
            error = "Do not find flash_id in eflash_loader_cfg.ini"
            bflb_utils.printf(error)
            bflb_utils.set_error_code("0070")
            return bflb_utils.errorcode_msg()
    
        pt = config['input_path']['pt_bin_input']
        if pt is not None and len(pt) > 0:
            pt_helper = partition.PtCreater(pt)
            # TODO name should not a fixed value
            if config["check_box"]['partition_download'] is True:
                bflb_utils.printf("create partition.bin, pt_new is True")
                pt_helper.create_pt_table(partition_path)
            pt_parcel = pt_helper.construct_table()
        else:
            bflb_utils.set_error_code("0076")
            return bflb_utils.errorcode_msg()
    
        if config["check_box"]["encrypt"] is True:
            aes_key = config["param"]["aes_key"].replace(" ", "")
            aes_iv = config["param"]["aes_iv"].replace(" ", "")
            if (verify_hex_num(aes_key) is not True) or (len(aes_key) != 32):
                error = "Error: Please check AES key data and len"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0077")
                return bflb_utils.errorcode_msg()
            if (verify_hex_num(aes_iv) is not True) or (len(aes_iv) != 32):
                error = "Error: Please check AES iv data and len"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0078")
                return bflb_utils.errorcode_msg()
            if aes_iv.endswith("00000000") is False:
                error = "AES IV should endswith 4 bytes zero"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0073")
                return bflb_utils.errorcode_msg()
    
        if config["check_box"]["sign"] is True:
            if not config["input_path"]["publickey"]:
                error = "Please set public key"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0066")
                return bflb_utils.errorcode_msg()
            if not config["input_path"]["privatekey"]:
                error = "Please set private key"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0067")
                return bflb_utils.errorcode_msg()
    
        if chiptype == "bl702":
            if config["check_box"]['boot2_download'] is True:
                boot2_en = False
            else:
                boot2_en = True
    
        if config["check_box"]['boot2_download'] is True:
            boot2 = config['input_path']['boot2_bin_input']
            if boot2 is not None and len(boot2) > 0:
                self.bl60x_fw_boot_head_gen(True, config['param'][chip_xtal], self.bh_cfg_file,
                                       config["check_box"]['encrypt'], config["check_box"]['sign'],
                                       chipname, chiptype, cpu_type, boot2_en)
                f_org = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg_boot2.conf")
                f = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg_boot2.ini")
                if os.path.isfile(f) is False:
                    shutil.copy(f_org, f)
                self.bl60x_image_gen(chipname, chiptype, cpu_type, "boot2", boot2,
                                config["param"]['aes_key'], config["param"]['aes_iv'], 
                                config["input_path"]["publickey"], config["input_path"]["privatekey"], 
                                f)
                boot2_d = True
        elif chiptype == "bl702":
            self.bl60x_fw_boot_head_gen(True, config['param'][chip_xtal], self.bh_cfg_file,
                                   config["check_box"]['encrypt'], config["check_box"]['sign'],
                                   chipname, chiptype, cpu_type, boot2_en)
    
        if config["check_box"]['ro_params_download'] is True:
            suffix = config['param'][chip_brd] + '_' + \
                config['param'][chip_xtal] + '.dts'
            ro = os.path.join(app_path, chipname, 'device_tree',
                              bl_factory_params_file_prefix + suffix)
            if not os.path.isfile(ro):
                bflb_utils.printf("Don't Find %s as bl_factory image" % ro)
                error = "Don't Find %s as bl_factory image" % ro
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0079")
                return bflb_utils.errorcode_msg()
            if ro is not None and len(ro) > 0:
                ro_params_d = ro
                try:
                    dts_hex = bl_ro_device_tree.bl_dts2hex(ro_params_d)
                    dts_bytearray = bflb_utils.hexstr_to_bytearray(dts_hex)
                except Exception as e:
                    dts_bytearray = None
                
        if config["check_box"]['bin_download'] is True:
            bin = config['input_path']['cfg2_bin_input']
            if bin is not None and len(bin) > 0:
                if parse_rfpa(bin) == b'BLRFPARA' and dts_bytearray:
                    length = len(dts_bytearray)
                    with open(bin, "rb") as fp:
                        bin_byte = fp.read()
                        bin_bytearray = bytearray(bin_byte)
                        bin_bytearray[1032:1032+length] = dts_bytearray
                    filedir, ext = os.path.splitext(bin)
                    bin = filedir + "_rfpa" + ext
                    with open(bin, "wb") as fp:
                        fp.write(bin_bytearray)
                self.bl60x_fw_boot_head_gen(False, config['param'][chip_xtal], self.bh_cfg_file,
                                       config["check_box"]['encrypt'], config["check_box"]['sign'],
                                       chipname, chiptype, cpu_type, boot2_en)
                self.bl60x_image_gen(chipname, chiptype, cpu_type, "fw", bin, 
                                config["param"]['aes_key'], config["param"]['aes_iv'],
                                config["input_path"]["publickey"], config["input_path"]["privatekey"])
                self.bl60x_mfg_ota_bin_gen(chipname, chiptype, cpu_type)
                bin_d = True
    
        if config["check_box"]['media_download'] is True:
            media_bin = config['input_path']['meida_bin_input']
            if media_bin is not None and len(media_bin) > 0:
                try:
                    shutil.copy(media_bin, os.path.join(app_path, chipname, "img_create_iot", "media.bin"))
                except Exception as e:
                    bflb_utils.printf(e)
            media_bin_d = True
    
        if config["check_box"]['use_romfs'] is True:
            romfs_dir = config['input_path']['romfs_dir_input']
            if romfs_dir is not None and len(romfs_dir) > 0:
                ret = generate_romfs_img(romfs_dir,
                                         os.path.join(app_path, chipname, "img_create_iot", "media.bin"))
                if ret != 0:
                    bflb_utils.printf('ERROR, ret %s.' % ret)
                    error = 'ERROR, ret %s.' % ret
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("007A")
                    return bflb_utils.errorcode_msg()
                media_bin_d = True
    
        if config["check_box"]['mfg_download'] is True:
            mfg = config['input_path']['mfg_bin_input']
            if mfg is not None and len(mfg) > 0:
                if parse_rfpa(mfg) == b'BLRFPARA' and dts_bytearray:
                    length = len(dts_bytearray)
                    with open(mfg, "rb") as fp:
                        bin_byte = fp.read()
                        bin_bytearray = bytearray(bin_byte)
                        bin_bytearray[1032:1032+length] = dts_bytearray
                    filedir, ext = os.path.splitext(mfg)
                    mfg = filedir + "_rfpa" + ext
                    with open(mfg, "wb") as fp:
                        fp.write(bin_bytearray)
    
                self.bl60x_mfg_boot_head_gen(hex(pt_parcel['mfg_addr']), config['param'][chip_xtal],
                                        self.bh_cfg_file, chipname, chiptype, cpu_type)
                f_org = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg_mfg.conf")
                f = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg_mfg.ini")
                if os.path.isfile(f) is False:
                    shutil.copy(f_org, f)
                self.bl60x_image_gen(chipname, chiptype, cpu_type, "mfg", mfg, 
                                config["param"]['aes_key'], config["param"]['aes_iv'], 
                                config["input_path"]["publickey"], config["input_path"]["privatekey"],
                                f)
                mfg_d = True
        return self.bl60x_mfg_flasher_eflash_loader_cfg(chipname, chiptype, bin_d, boot2_d, ro_params_d,
                                                   pt_parcel, media_bin_d, mfg_d)
    
    

    def flasher_download_thread(self, chipname, chiptype, act, config, callback=None):
        self.config = config
        error = None
        cpu_type = None   
        ota_path = os.path.join(app_path, chipname, "ota")
        imgcreate2_path = os.path.join(app_path, chipname, "img_create_mcu")
        if not os.path.exists(ota_path):
            os.makedirs(ota_path)
        if not os.path.exists(imgcreate2_path):
            os.makedirs(imgcreate2_path)
    
        if chipname in gol.cpu_type.keys():
            cpu_type = gol.cpu_type[chipname][0]
    
        if act != "build" and act != "download":
            return "no such action!"
        try:
            # config loader ini
            if config['param']['interface_type'] == 'Uart':
                uart = config['param']['comport_uart']
                uart_brd = config['param']['speed_uart']
                bflb_utils.printf("========= Interface is Uart =========")
                self.bl60x_mfg_flasher_cfg(uart, uart_brd)
            elif config['param']['interface_type'] == 'JLink':
                jlink_brd = config['param']['speed_jlink']
                bflb_utils.printf("========= Interface is JLink =========")
                self.bl60x_mfg_flasher_jlink_cfg(rate=jlink_brd)
            else:
                openocd_brd = config['param']['speed_jlink']
                bflb_utils.printf("========= Interface is Openocd =========")
                self.bl60x_mfg_flasher_openocd_cfg(rate=openocd_brd)
    
            cfg = BFConfigParser()
            cfg.read(self.eflash_loader_cfg)
            if "dl_verify" in config["param"].keys():
                if config["param"]["verify"] == "True":
                    cfg.set('LOAD_CFG', 'verify', '1')
                else:
                    cfg.set('LOAD_CFG', 'verify', '0')
            cfg.write(self.eflash_loader_cfg, 'w')
    
            bl60x_xtal = config["param"][chip_xtal]
            bflb_utils.printf("eflash loader bin is " + get_eflash_loader(bl60x_xtal))
            eflash_loader_bin = os.path.join(app_path, chipname,
                                             "eflash_loader/" + get_eflash_loader(bl60x_xtal))
    
            if config["check_box"]["download_single"] is True and act == "download":
                cfg = BFConfigParser()
                cfg.read(self.eflash_loader_cfg)
                files_str = config["input_path"]["img_bin_input"]
                addrs_str = config["param"]["addr"].replace("0x", "")
                cfg.set('FLASH_CFG', 'file', files_str)
                cfg.set('FLASH_CFG', 'address', addrs_str)
                cfg.write(self.eflash_loader_cfg, 'w')
                self.eflash_loader_t = eflash_loader.BflbEflashLoader(chiptype)
                if config["check_box"]['ckb_erase_all'] == "True":
                    self.bl60x_mfg_flasher_erase_all(True)
                else:
                    self.bl60x_mfg_flasher_erase_all(False)
                if config['param']['interface_type'] == 'Uart':
                    options = ["--write", "--flash", "-p", uart]
                    args = parser_eflash.parse_args(options)
                    error = self.eflash_loader_t.efuse_flash_loader(args, self.eflash_loader_cfg,
                                                               eflash_loader_bin, callback, None, None)
                else:
                    options = ["--write", "--flash"]
                    args = parser_eflash.parse_args(options)
                    error = self.eflash_loader_t.efuse_flash_loader(args, self.eflash_loader_cfg,
                                                               eflash_loader_bin, callback, None, None)
            # generation partition table/boot2/fw bin files and rf files
            elif self.flasher_download_cfg_ini_gen(chipname, chiptype, cpu_type, config) is True:
                if act == "download":
                    # burn into flash
                    self.eflash_loader_t = eflash_loader.BflbEflashLoader(chiptype)
                    if config["check_box"]['ckb_erase_all'] == "True":
                        self.bl60x_mfg_flasher_erase_all(True)
                    else:
                        self.bl60x_mfg_flasher_erase_all(False)
                    options = ["--write", "--flash"]
                    if  config["check_box"]["encrypt"] is True or\
                        config["check_box"]["sign"] is True:
                        # options.append("--efuse")
                        options.extend(["--efuse"])
                        if  config["check_box"]["encrypt"] is True or\
                            config["check_box"]["sign"] is True:
                            cfg_file = os.path.join(app_path, chipname, "img_create_iot", "img_create_cfg.ini")
                            options.extend(["--createcfg=" + cfg_file])
                    if config['param']['interface_type'] == 'Uart':
                        options.extend(["-p", uart])
                    args = parser_eflash.parse_args(options)
                    error = self.eflash_loader_t.efuse_flash_loader(args, self.eflash_loader_cfg,
                                                               eflash_loader_bin, callback,
                                                               self.create_simple_callback, None)
            else:
                error = self.flasher_download_cfg_ini_gen(chipname, chiptype, cpu_type, config)
                bflb_utils.printf("Please check your partition table file")
        except Exception as e:
            traceback.print_exc(limit=10, file=sys.stdout)
            error = str(e)
        finally:
            return error
        
        
    def create_simple_callback(self):
        cpu_type = None
        if self.chipname in gol.cpu_type.keys():
            cpu_type = gol.cpu_type[self.chipname][0]
        # values = gol.GlobalVar.values
        values = self.config
        error = self.flasher_download_cfg_ini_gen(self.chipname, self.chiptype, cpu_type, values)
        if error is not True:
            bflb_utils.printf(error)
        return error
    
    def log_read_thread(self):
        try:
            ret, data = self.eflash_loader_t.log_read_process()
            self.eflash_loader_t.close_port()
            return ret, data
        except Exception as e:
            traceback.print_exc(limit=10, file=sys.stdout)
            ret = str(e)
            return False, ret
    

def flasher_download_cmd(args):
    config = toml.load(args.config)
    chipname = args.chipname
    chiptype = chip_dict.get(chipname, "unkown chip type") 
    if chiptype not in ["bl60x", "bl602", "bl702"]: 
        bflb_utils.printf("Chip type is not in bl60x/bl602/bl702")
        return
    act = "download"
    obj_iot = BflbIotTool(chipname, chiptype)
    obj_iot.flasher_download_thread(chipname, chiptype, act, config)
    

def iot_download_cmd(args):
    chipname = args.chipname
    chiptype = chip_dict.get(chipname, "unkown chip type") 
    partition_cfg = os.path.join(app_path, chipname, "partition/partition_cfg_2M.toml") 
    config = dict()
    config["param"] = dict()
    config["check_box"] = dict()
    config["input_path"] = dict()
    config["param"]["interface_type"] = args.interface.capitalize()
    config["param"]["comport_uart"] =  args.port
    config["param"]["speed_uart"] = str(args.baudrate)
    config["param"]["speed_jlink"] = str(args.baudrate)
    config["param"]["bl60x_brd"] = args.board
    config["param"]["bl60x_xtal"] = args.xtal
    config["param"]["aes_key"] = ""
    config["param"]["aes_iv"] = ""
    config["check_box"]["partition_download"] = True
    config["check_box"]["bin_download"] = True
    config["check_box"]["media_download"] = False
    config["check_box"]["use_romfs"] = False
    config["check_box"]["mfg_download"] = False
    config["check_box"]["ro_params_download"] = True
    config["check_box"]["ckb_erase_all"] = args.erase
    config["check_box"]["encrypt"] = False
    config["check_box"]["sign"] = False
    config["input_path"]["pt_bin_input"] = partition_cfg
    config["input_path"]["cfg2_bin_input"] = args.firmware
    config["input_path"]["meida_bin_input"] = ""
    config["input_path"]["romfs_dir_input"] = ""
    config["input_path"]["mfg_bin_input"] = ""
    config["input_path"]["publickey"] = ""
    config["input_path"]["privatekey"] = ""
    config["check_box"]["download_single"] = args.single
    config["input_path"]["img_bin_input"] = args.firmware
    config["param"]["addr"] = "0x" + args.addr
    
    if chiptype == "bl702":
        config["check_box"]["boot2_download"] = False
        config["input_path"]["boot2_bin_input"] = ""
        if not args.xtal: 
            config["param"]["bl60x_xtal"] = "32M"
        else:   
            config["param"]["bl60x_xtal"] = args.xtal 
        if not args.board: 
            config["param"]["bl60x_brd"] = "IoTKitA"
        else:   
            config["param"]["bl60x_brd"] = args.board
    elif chiptype == "bl602":
        config["check_box"]["boot2_download"] = True
        config["input_path"]["boot2_bin_input"] = os.path.join(app_path, chipname, "builtin_imgs", "blsp_boot2.bin")
        if not args.xtal: 
            config["param"]["bl60x_xtal"] = "40M"
        else:   
            config["param"]["bl60x_xtal"] = args.xtal 
        if not args.board: 
            config["param"]["bl60x_brd"] = "IoTKitA"
        else:   
            config["param"]["bl60x_brd"] = args.board
    elif chiptype == "bl60x":
        config["check_box"]["boot2_download"] = True
        config["input_path"]["boot2_bin_input"] = os.path.join(app_path, chipname, "builtin_imgs", "blsp_boot2.bin")
        if not args.xtal: 
            config["param"]["bl60x_xtal"] = "38.4M"
        else:   
            config["param"]["bl60x_xtal"] = args.xtal 
        if not args.board: 
            config["param"]["bl60x_brd"] = "avb"
        else:   
            config["param"]["bl60x_brd"] = args.board
    else:
        bflb_utils.printf("Chip type is not in bl60x/bl602/bl702")
        return
    
    if config["param"]["interface_type"].lower() == "jlink" and args.baudrate > 12000:
        config["param"]["speed_jlink"] = "12000"
                  
    if args.build:
        act = "build"
    else:
        act = "download"
    
    obj_iot = BflbIotTool(chipname, chiptype)
    obj_iot.flasher_download_thread(chipname, chiptype, act, config)
    if act == "build":
        f_org = os.path.join(app_path, args.chipname, "img_create_iot", "whole_flash_data.bin")
        f = "firmware.bin"
        shutil.copy(f_org, f)
    
    
def run():
    port = None
    ports = []
    for item in get_serial_ports():
        ports.append(item["port"])
    if ports:
        try:
            port = sorted(ports, key=lambda x: int(re.match('COM(\d+)', x).group(1)))[0]
        except Exception:
            port = sorted(ports)[0]
    firmware_default = os.path.join(app_path, "img", "project.bin")
    parser = argparse.ArgumentParser(description='bflb iot tool')
    parser.add_argument('--chipname', required=True, help='chip name')
    parser.add_argument("--interface", dest="interface", default="uart", help="interface to use") 
    parser.add_argument("--port", dest="port", default=port, help="serial port to use")
    parser.add_argument("--baudrate", dest="baudrate", default=115200, type=int, help="the speed at which to communicate")
    parser.add_argument("--xtal", dest="xtal", help="xtal type")
    parser.add_argument("--board", dest="board", help="board type")
    parser.add_argument("--firmware", dest="firmware", default=firmware_default, help="image to write")  
    parser.add_argument("--build", dest="build", action="store_true", help="build image") 
    parser.add_argument("--erase", dest="erase", action="store_true", help="chip erase")
    parser.add_argument("--single", dest="single", action="store_true", help="single download")
    parser.add_argument("--addr", dest="addr", default="0", help="address to write")
    parser.add_argument('--config', dest="config", help='config file')
    args = parser.parse_args()
    bflb_utils.printf("==================================================")
    bflb_utils.printf("Chip name is %s" % args.chipname)  
    if not args.port:
        bflb_utils.printf("Serial port is not found")
    else:
        bflb_utils.printf("Serial port is " + str(port)) 
    bflb_utils.printf("Baudrate is " + str(args.baudrate)) 
    bflb_utils.printf("Firmware is " + args.firmware)      
    bflb_utils.printf("==================================================")
    if args.config:
        parser.set_defaults(func=flasher_download_cmd)
    else:
        parser.set_defaults(func=iot_download_cmd)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    print(sys.argv)
    run()    
    
