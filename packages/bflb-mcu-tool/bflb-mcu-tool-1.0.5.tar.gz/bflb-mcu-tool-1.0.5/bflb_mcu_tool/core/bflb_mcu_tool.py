# -*- coding:utf-8 -*-

import re
import os
import sys
import shutil
import argparse
import traceback

try:
    import bflb_path
except ImportError:
    from libs import bflb_path
from libs import bflb_eflash_loader
from libs import bflb_efuse_boothd_create
from libs import bflb_img_create
from libs import bflb_img_loader
from libs import bflb_flash_select
from libs import bflb_utils
from libs.bflb_utils import verify_hex_num, get_eflash_loader, get_serial_ports, convert_path
from libs.bflb_configobj import BFConfigParser
import libs.bflb_ro_params_device_tree as bl_ro_device_tree
import globalvar as gol

parser_eflash = bflb_utils.eflash_loader_parser_init()
parser_image = bflb_utils.image_create_parser_init()

# Get app path
if getattr(sys, "frozen", False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(app_path)

chip_dict = {
    "bl56x": "bl60x",
    "bl60x": "bl60x",
    "bl562": "bl602",
    "bl602": "bl602",
    "bl702": "bl702",
    "bl606p": "bl606p",
}


def parse_rfpa(bin):
    with open(bin, "rb") as fp:
        content = fp.read()
        return content[1024:1032]


class BflbMcuTool(object):

    def __init__(self, chipname="bl60x", chiptype="bl60x"):
        self.chiptype = chiptype
        self.chipname = chipname
        self.efuse_load_en = False
        self.eflash_loader_cfg = os.path.join(app_path, chipname, "eflash_loader/eflash_loader_cfg.conf")
        self.eflash_loader_cfg_tmp = os.path.join(app_path, chipname, "eflash_loader/eflash_loader_cfg.ini")
        self.eflash_loader_bin = os.path.join(app_path, chipname, "eflash_loader/eflash_loader_40m.bin")
        self.img_create_path = os.path.join(app_path, chipname, "img_create_mcu")
        self.efuse_bh_path = os.path.join(app_path, chipname, "efuse_bootheader")
        self.efuse_bh_default_cfg = os.path.join(app_path, chipname, "efuse_bootheader") + "/efuse_bootheader_cfg.conf"
        self.efuse_bh_default_cfg_dp = os.path.join(app_path, chipname, "efuse_bootheader") + "/efuse_bootheader_cfg_dp.conf"
        self.img_create_cfg_org = os.path.join(app_path, chipname, "img_create_mcu") + "/img_create_cfg.conf"
        self.img_create_cfg_dp_org = os.path.join(app_path, chipname, "img_create_mcu") + "/img_create_cfg_dp.conf"
        self.img_create_cfg = os.path.join(app_path, chipname, "img_create_mcu") + "/img_create_cfg.ini"
        if not os.path.exists(self.img_create_path):
            os.makedirs(self.img_create_path)
        if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
            shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
        if os.path.isfile(self.img_create_cfg) is False:
            shutil.copy(self.img_create_cfg_org, self.img_create_cfg)
        
        self.xtal_type = gol.xtal_type[chiptype]
        self.xtal_type_ = gol.xtal_type_[chiptype]
        self.pll_clk = gol.pll_clk[chiptype]
        self.encrypt_type = gol.encrypt_type[chiptype]
        self.key_sel = gol.key_sel[chiptype]
        self.sign_type = gol.sign_type[chiptype]
        self.cache_way_disable = gol.cache_way_disable[chiptype]
        self.flash_clk_type = gol.flash_clk_type[chiptype]
        self.crc_ignore = gol.crc_ignore[chiptype]
        self.hash_ignore = gol.hash_ignore[chiptype]
        self.img_type = gol.img_type[chiptype]
        self.boot_src = gol.boot_src[chiptype]
        self.eflash_loader_t = bflb_eflash_loader.BflbEflashLoader(chiptype, chipname)

    def bl_create_flash_default_data(self, length):
        datas = bytearray(length)
        for i in range(length):
            datas[i] = 0xff
        return datas
      
    def bl_get_file_data(self, files):
        datas = []
        for file in files:
            with open(os.path.join(app_path, file), 'rb') as fp:
                data = fp.read()
            datas.append(data)
        return datas
      
    def img_addr_remap(self, addr):
        remap_list = {
            "C0": "00",
            "c0": "00",
            "C1": "21",
            "c1": "21",
            "c2": "22",
            "C2": "22",
            "D0": "10",
            "d0": "10",
            "D4": "14",
            "d4": "14"
        }
        for key, value in remap_list.items():
            if addr[0:2] == key:
                addr = value + addr[2:]
        return addr
        
    def eflash_loader_thread(self, args, eflash_loader_bin=None, callback=None, create_img_callback=None):
        ret = None
        try:
            ret = self.eflash_loader_t.efuse_flash_loader(args, None, eflash_loader_bin, callback,
                                                     None, create_img_callback)
        except Exception as e:
            traceback.print_exc(limit=5, file=sys.stdout)
            ret = str(e)
        finally:
            return ret
      
    def img_loader_thread(self, comnum, sh_baudrate, wk_baudrate, file1, file2, callback=None):
        ret = None
        try:
            img_load_t = bflb_img_loader.BflbImgLoader(self.chiptype)
            ret = img_load_t.img_load_process(comnum, sh_baudrate, wk_baudrate, file1, file2, callback,
                                              True, 50, 100, False, 50, 3)
            img_load_t.close_port()
        except Exception as e:
            traceback.print_exc(limit=5, file=sys.stdout)
            ret = str(e)
        finally:
            return ret
       
    def read_efuse_thread(self, values, callback=None):
        options = ""
        ret = None
        try:
            # create eflash_loader_tmp.ini
            cfg = BFConfigParser()
            if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
            cfg.read(self.eflash_loader_cfg_tmp)
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "interface", values["dl_device"].lower())
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "device", values["dl_comport"])
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_uart_load", values["dl_comspeed"])
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_jlink", values["dl_jlinkspeed"])
            if "dl_verify" in values.keys():
                if values["dl_verify"] == "True":
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "1")
                else:
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "0")
            cfg.write(self.eflash_loader_cfg_tmp, "w+")
            bflb_utils.printf("Save as efuse.bin")
            options = ["--read", "--efuse", "--start=0", "--end=255", "--file=efuse.bin", "-c", self.eflash_loader_cfg_tmp]
            eflash_loader_bin = os.path.join(app_path, self.chipname,
                                             "eflash_loader/" + get_eflash_loader(values["dl_xtal"]))
            args = parser_eflash.parse_args(options)
            ret = self.eflash_loader_thread(args, eflash_loader_bin, callback)
        except Exception as e:
            ret = str(e)
        finally:
            return ret
      
    def read_flash_thread(self, values, callback=None):
        options = ""
        start = ""
        end = ""
        ret = None
        try:
            # create eflash_loader_tmp.ini
            cfg = BFConfigParser()
            if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
            cfg.read(self.eflash_loader_cfg_tmp)
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "interface", values["dl_device"].lower())
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "device", values["dl_comport"])
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_uart_load", values["dl_comspeed"])
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_jlink", values["dl_jlinkspeed"])
            if "dl_verify" in values.keys():
                if values["dl_verify"] == "True":
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "1")
                else:
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "0")
            cfg.write(self.eflash_loader_cfg_tmp, "w+")
            if verify_hex_num(values["start_addr"][2:]) is True:
                if values["start_addr"][0:2] == "0x":
                    start = values["start_addr"][2:]
                else:
                    bflb_utils.printf("Error, start_addr is HEX data, must begin with 0x")
                    ret = "start_addr is HEX data, must begin with 0x"
            else:
                bflb_utils.printf("Error, Please check start_addr hex data")
                ret = "Please check start_addr hex data"
            if verify_hex_num(values["end_addr"][2:]) is True:
                if values["end_addr"][0:2] == "0x":
                    end = values["end_addr"][2:]
                else:
                    bflb_utils.printf("Error, end_addr is HEX data, must begin with 0x")
                    ret = "end_addr is HEX data, must begin with 0x"
            else:
                bflb_utils.printf("Error, Please check end_addr hex data")
                ret = "Please check end_addr hex data"
            if int(start, 16) >= int(end, 16):
                bflb_utils.printf("Error, Start addr must less than end addr")
                ret = "Start addr must less than end addr"
            if ret is not None:
                return ret
            bflb_utils.printf("Save as flash.bin")
            options = ["--read", "--flash", "--start="+start, "--end="+end, "--file=flash.bin", "-c", self.eflash_loader_cfg_tmp]
            eflash_loader_bin = os.path.join(app_path, self.chipname, "eflash_loader/" + get_eflash_loader(values["dl_xtal"]))
            args = parser_eflash.parse_args(options)
            ret = self.eflash_loader_thread(args, eflash_loader_bin, callback)
        except Exception as e:
            ret = str(e)
        finally:
            return ret
      
    def erase_flash_thread(self, values, callback=None):
        options = ""
        start = ""
        end = ""
        ret = None
        try:
            # create eflash_loader_tmp.ini
            cfg = BFConfigParser()
            if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
            cfg.read(self.eflash_loader_cfg_tmp)
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "interface", values["dl_device"].lower())
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "device", values["dl_comport"])
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_uart_load", values["dl_comspeed"])
            bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_jlink", values["dl_jlinkspeed"])
            if "dl_verify" in values.keys():
                if values["dl_verify"] == "True":
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "1")
                else:
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "0")
            cfg.write(self.eflash_loader_cfg_tmp, "w+")
            if verify_hex_num(values["start_addr"][2:]) is True:
                if values["start_addr"][0:2] == "0x":
                    start = values["start_addr"][2:]
                else:
                    bflb_utils.printf("Error, start_addr is HEX data, must begin with 0x")
                    ret = "start_addr is HEX data, must begin with 0x"
            else:
                bflb_utils.printf("Error, Please check start_addr hex data")
                ret = "Please check start_addr hex data"
            if verify_hex_num(values["end_addr"][2:]) is True:
                if values["end_addr"][0:2] == "0x":
                    end = values["end_addr"][2:]
                else:
                    bflb_utils.printf("Error, end_addr is HEX data, must begin with 0x")
                    ret = "end_addr is HEX data, must begin with 0x"
            else:
                bflb_utils.printf("Error, Please check end_addr hex data")
                ret = "Please check end_addr hex data"
            if int(start, 16) >= int(end, 16) and values["whole_chip"] is False:
                bflb_utils.printf("Error, Start addr must less than end addr")
                ret = "Start addr must less than end addr"
            if ret is not None:
                return ret
            if values["whole_chip"] is True:
                options = ["--erase", "--flash", "--end=0", "-c", self.eflash_loader_cfg_tmp]
            else:
                options = ["--erase", "--flash", "--start="+start, "--end="+end, "-c", self.eflash_loader_cfg_tmp]
            eflash_loader_bin = os.path.join(app_path, self.chipname,
                                             "eflash_loader/" + get_eflash_loader(values["dl_xtal"]))
            args = parser_eflash.parse_args(options)
            ret = self.eflash_loader_thread(args, eflash_loader_bin, callback)
        except Exception as e:
            ret = str(e)
        finally:
            return ret
    
    def bind_img(self, values):
        error = None
        # decide file name
        try:
            if self.chiptype != "bl606p":
                if values["img_type"] == "SingleCPU":
                    bootinfo_file = self.img_create_path + "/bootinfo.bin"
                    img_file = self.img_create_path + "/img.bin"
                    img_output_file = self.img_create_path + "/whole_img.bin"
                elif values["img_type"] == "BLSP_Boot2":
                    bootinfo_file = self.img_create_path + "/bootinfo_blsp_boot2.bin"
                    img_file = self.img_create_path + "/img_blsp_boot2.bin"
                    img_output_file = self.img_create_path + "/whole_img_blsp_boot2.bin"
                elif values["img_type"] == "CPU0":
                    bootinfo_file = self.img_create_path + "/bootinfo_cpu0.bin"
                    img_file = self.img_create_path + "/img_cpu0.bin"
                    img_output_file = self.img_create_path + "/whole_img_cpu0.bin"
                elif values["img_type"] == "CPU1":
                    bootinfo_file = self.img_create_path + "/bootinfo_cpu1.bin"
                    img_file = self.img_create_path + "/img_cpu1.bin"
                    img_output_file = self.img_create_path + "/whole_img_cpu1.bin"
                if values["img_type"] == "SingleCPU":
                    dummy_data = bytearray(8192)
                else:
                    dummy_data = bytearray(4096)
                for i in range(len(dummy_data)):
                    dummy_data[i] = 0xff
                fp = open(bootinfo_file, 'rb')
                data0 = fp.read() + bytearray(0)
                fp.close()
                fp = open(img_file, 'rb')
                data1 = fp.read() + bytearray(0)
                fp.close()
                fp = open(img_output_file, 'wb+')
                fp.write(data0 + dummy_data[0:len(dummy_data) - len(data0)] + data1)
                fp.close()
                bflb_utils.printf("Output:", img_output_file)
            else:
                group0_bootinfo_file = self.img_create_path + "/bootinfo_group0.bin"
                group0_img_output_file = self.img_create_path + "/img_group0.bin"
                group1_bootinfo_file = self.img_create_path + "/bootinfo_group1.bin"
                group1_img_output_file = self.img_create_path + "/img_group1.bin"
                whole_img_output_file = self.img_create_path + "/whole_img.bin"
                read_data = self.bl_get_file_data([group0_bootinfo_file])[0]
                group0_img_offset = bflb_utils.bytearray_to_int(
                    bflb_utils.bytearray_reverse(read_data[128:132]))
                group0_img_len = bflb_utils.bytearray_to_int(
                    bflb_utils.bytearray_reverse(read_data[136:140]))
                read_data = self.bl_get_file_data([group1_bootinfo_file])[0]
                group1_img_offset = bflb_utils.bytearray_to_int(
                    bflb_utils.bytearray_reverse(read_data[128:132]))
                group1_img_len = bflb_utils.bytearray_to_int(
                    bflb_utils.bytearray_reverse(read_data[136:140]))
                whole_img_len = 0
                if group0_img_offset + group0_img_len > group1_img_offset + group1_img_len:
                    whole_img_len = group0_img_offset + group0_img_len
                else:
                    whole_img_len = group1_img_offset + group1_img_len
                whole_img_data = self.bl_create_flash_default_data(whole_img_len)
                filedata = self.bl_get_file_data([group0_bootinfo_file])[0]
                whole_img_data[0:len(filedata)] = filedata
    
                filedata = self.bl_get_file_data([group1_bootinfo_file])[0]
                whole_img_data[0x1000:len(filedata)] = filedata
                filedata = self.bl_get_file_data([group0_img_output_file])[0]
                if group0_img_len != len(filedata):
                    bflb_utils.printf("group0 img len error, get %d except %d" %
                                      (group0_img_len, len(filedata)))
                whole_img_data[group0_img_offset:group0_img_offset + len(filedata)] = filedata
                filedata = self.bl_get_file_data([group1_img_output_file])[0]
                if group1_img_len != len(filedata):
                    bflb_utils.printf("group1 img len error, get %d except %d" %
                                      (group1_img_len, len(filedata)))
                whole_img_data[group1_img_offset:group1_img_offset + len(filedata)] = filedata
                fp = open(whole_img_output_file, 'wb+')
                fp.write(whole_img_data)
                fp.close()
                bflb_utils.printf("Output:", whole_img_output_file)
        except Exception as e:
            bflb_utils.printf("烧写执行出错：", e)
            error = str(e)
        return error
        
    def create_img_606p(self, chipname, chiptype, values):
        # basic check
        error = True
        group0_img_start = "0xFFFFFFFF"
        group1_img_start = "0xFFFFFFFF"
        group0_img = ""
        group1_img = ""
        cpu_list = ["m0", "m1", "d0", "d1", "lp"]
        img_addr_offset = ["0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0", "0x0"]
        segheader_file = [
            "/segheader_group0_m0.bin", "/segheader_group0_m1.bin", "/segheader_group0_d0.bin",
            "/segheader_group0_d1.bin", "/segheader_group0_lp.bin", "/segheader_group1_m0.bin",
            "/segheader_group1_m1.bin", "/segheader_group1_d0.bin", "/segheader_group1_d1.bin",
            "/segheader_group1_lp.bin"
        ]
        for index in range(5):
            num = str(index+1)
            if values["img%s_group" % num] != "unused":
                if values["img%s_file" % num] == "":
                    error = "Please select image%s file" % num
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0061")
                    return bflb_utils.errorcode_msg()
                if values["img%s_addr" % num] == "" or values["img%s_addr" % num] == "0x":
                    error = "Please set image%s address" % num
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0062")
                    return bflb_utils.errorcode_msg()
                img_start = int(values["img%s_addr" % num].replace("0x", ""), 16)
                if values["img%s_group" % num] == "group0":
                    group0_img += values["img%s_file" % num]
                    group1_img += "UNUSED"
                    img_addr_offset[index] = values["img%s_addr" % num]
                    if int(group0_img_start.replace("0x", ""), 16) > img_start:
                        group0_img_start = values["img%s_addr" % num]
                elif values["img%s_group" % num] == "group1":
                    group0_img += "UNUSED"
                    group1_img += values["img%s_file" % num]
                    img_addr_offset[index+5] = values["img%s_addr" % num]
                    if int(group1_img_start.replace("0x", ""), 16) > img_start:
                        group1_img_start = values["img%s_addr" % num]
            else:
                group0_img += "UNUSED"
                group1_img += "UNUSED"
            group0_img += "|"
            group1_img += "|"
        group0_img = group0_img.strip()
        group1_img = group1_img.strip()
        if group0_img_start == "0xFFFFFFFF":
            group0_img_start = "0x00000000"
        if group1_img_start == "0xFFFFFFFF":
            group1_img_start = "0x00000000"
        if "encrypt_type-group0" in values.keys():
            if "encrypt_key-group0" in values.keys():
                if values["encrypt_type-group0"] != "None" and values["encrypt_key-group0"] == "":
                    error = "Please set group0 AES key"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0064")
                    return bflb_utils.errorcode_msg()
            if "aes_iv-group0" in values.keys():
                if values["encrypt_type-group0"] != "None" and values["aes_iv-group0"] == "":
                    error = "Please set group0 AES IV"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0065")
                    return bflb_utils.errorcode_msg()
        if "encrypt_type-group1" in values.keys():
            if "encrypt_key-group1" in values.keys():
                if values["encrypt_type-group1"] != "None" and values["encrypt_key-group1"] == "":
                    error = "Please set group1 AES key"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0064")
                    return bflb_utils.errorcode_msg()
            if "aes_iv-group1" in values.keys():
                if values["encrypt_type-group1"] != "None" and values["aes_iv-group1"] == "":
                    error = "Please set group1 AES IV"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0065")
                    return bflb_utils.errorcode_msg()
        if "sign_type-group0" in values.keys():
            if "public_key_cfg-group0" in values.keys():
                if values["sign_type-group0"] != "None" and values["public_key_cfg-group0"] == "":
                    error = "Please set group0 public key"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0066")
                    return bflb_utils.errorcode_msg()
            if "private_key_cfg-group0" in values.keys():
                if values["sign_type-group0"] != "None" and values["private_key_cfg-group0"] == "":
                    error = "Please set group0 private key"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0067")
                    return bflb_utils.errorcode_msg()
        if "sign_type-group1" in values.keys():
            if "public_key_cfg-group1" in values.keys():
                if values["sign_type-group1"] != "None" and values["public_key_cfg-group1"] == "":
                    error = "Please set group1 public key"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0066")
                    return bflb_utils.errorcode_msg()
            if "private_key_cfg-group1" in values.keys():
                if values["sign_type-group1"] != "None" and values["private_key_cfg-group1"] == "":
                    error = "Please set group1 private key"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0067")
                    return bflb_utils.errorcode_msg()
        group0_section = "BOOTHEADER_GROUP0_CFG"
        group1_section = "BOOTHEADER_GROUP1_CFG"
        bh_cfg_file = self.efuse_bh_path + "/efuse_bootheader_cfg.ini"
        group0_bh_file = self.img_create_path + "/bootheader_group0.bin"
        group1_bh_file = self.img_create_path + "/bootheader_group1.bin"
        efuse_file = self.img_create_path + "/efusedata.bin"
        efuse_mask_file = self.img_create_path + "/efusedata_mask.bin"
        group0_bootinfo_file = self.img_create_path + "/bootinfo_group0.bin"
        group1_bootinfo_file = self.img_create_path + "/bootinfo_group1.bin"
        group0_img_output_file = self.img_create_path + "/img_group0.bin"
        group1_img_output_file = self.img_create_path + "/img_group1.bin"
        group0_img_create_section = "Img_Group0_Cfg"
        group1_img_create_section = "Img_Group1_Cfg"
        if os.path.isfile(bh_cfg_file) is False:
            bflb_utils.copyfile(self.efuse_bh_default_cfg, bh_cfg_file)
        shutil.copy(self.img_create_cfg_org, self.img_create_cfg)
        # add flash cfg
        if os.path.exists(self.eflash_loader_cfg_tmp):
            cfg1 = BFConfigParser()
            cfg1.read(self.eflash_loader_cfg_tmp)
            if cfg1.has_option("FLASH_CFG", "flash_id"):
                flash_id = cfg1.get("FLASH_CFG", "flash_id")
                if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id, bh_cfg_file, False,
                                                      group0_section) is False:
                    error = "flash_id:" + flash_id + " do not support"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0069")
                    return bflb_utils.errorcode_msg()
            else:
                error = "Do not find flash_id in eflash_loader_cfg.ini"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0070")
                return bflb_utils.errorcode_msg()
        else:
            bflb_utils.printf("Config file not found")
            bflb_utils.set_error_code("000B")
            return bflb_utils.errorcode_msg()
        # update config
        cfg = BFConfigParser()
        cfg.read(bh_cfg_file)
        for itrs in cfg.sections():
            bflb_utils.printf(itrs)
            if itrs != group0_section and itrs != group1_section and itrs != "EFUSE_CFG":
                cfg.delete_section(itrs)
        cfg.write(bh_cfg_file, "w+")
        cfg = BFConfigParser()
        cfg.read(bh_cfg_file)
        bflb_utils.update_cfg(cfg, group0_section, "boot2_enable", "0")
        bflb_utils.update_cfg(cfg, group1_section, "boot2_enable", "0")
        if "xtal_type" in values.keys():
            bflb_utils.update_cfg(cfg, group0_section, "xtal_type",
                                  self.xtal_type_.index(values["xtal_type"]))
        if "mcu_clk" in values.keys():
            bflb_utils.update_cfg(cfg, group0_section, "mcu_clk", self.pll_clk.index(values["mcu_clk"]))
            '''
            i = pll_clk.index(values["mcu_clk"])
            if i == 3 or i == 4:
                bflb_utils.update_cfg(cfg, group0_section, "mcu_bclk_div", "1")
            else:
                bflb_utils.update_cfg(cfg, group0_section, "mcu_bclk_div", "0")
            '''
        tmp = values["flash_clk_type"]
        if tmp != "Manual":
            bflb_utils.update_cfg(cfg, group0_section, "flash_clk_type",
                                  self.flash_clk_type.index(values["flash_clk_type"]))
            bflb_utils.update_cfg(cfg, group0_section, "flash_clk_div", "0")
            if "xtal_type" in values.keys():
                if tmp == "XTAL" or tmp == "XCLK" or values["xtal_type"] == "XTAL_None":
                    # 1T
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_delay", "1")
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_invert", "0x01")
                else:
                    # 1.5T
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_delay", "1")
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_invert", "0x03")
            else:
                if tmp == "XTAL" or tmp == "XCLK":
                    # 1T
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_delay", "1")
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_invert", "0x01")
                else:
                    # 1.5T
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_delay", "1")
                    bflb_utils.update_cfg(cfg, group0_section, "sfctrl_clk_invert", "0x03")
        if "sign_type-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_section, "sign",
                                  self.sign_type.index(values["sign_type-group0"]))
        if "encrypt_type-group0" in values.keys():
            tmp = self.encrypt_type.index(values["encrypt_type-group0"])
            if tmp == 4:
                bflb_utils.update_cfg(cfg, group0_section, "encrypt_type", "1")
                bflb_utils.update_cfg(cfg, group0_section, "xts_mode", "1")
            else:
                bflb_utils.update_cfg(cfg, group0_section, "encrypt_type", tmp)
                bflb_utils.update_cfg(cfg, group0_section, "xts_mode", "0")
            if tmp == 1 and len(values["encrypt_key-group0"]) != 32:
                error = "group0 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp == 2 and len(values["encrypt_key-group0"]) != 64:
                error = "group0 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp == 3 and len(values["encrypt_key-group0"]) != 48:
                error = "group0 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp == 4 and len(values["encrypt_key-group0"]) != 64:
                error = "group0 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp != 0:
                if len(values["aes_iv-group0"]) != 32:
                    error = "group0 AES IV length error"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0072")
                    return bflb_utils.errorcode_msg()
                if values["aes_iv-group0"].endswith("00000000") is False:
                    error = "group0 AES IV should endswith 4 bytes zero"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0073")
                    return bflb_utils.errorcode_msg()
        if "key_sel-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_section, "key_sel",
                                  self.key_sel.index(values["key_sel-group0"]))
        if "crc_ignore-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_section, "crc_ignore",
                                  self.crc_ignore.index(values["crc_ignore-group0"]))
        if "hash_ignore-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_section, "hash_ignore",
                                  self.hash_ignore.index(values["hash_ignore-group0"]))
        if "sign_type-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_section, "sign",
                                  self.sign_type.index(values["sign_type-group1"]))
        if "encrypt_type-group1" in values.keys():
            tmp = self.encrypt_type.index(values["encrypt_type-group1"])
            if tmp == 4:
                bflb_utils.update_cfg(cfg, group1_section, "encrypt_type", "1")
                bflb_utils.update_cfg(cfg, group1_section, "xts_mode", "1")
            else:
                bflb_utils.update_cfg(cfg, group1_section, "encrypt_type", tmp)
                bflb_utils.update_cfg(cfg, group1_section, "xts_mode", "0")
            if tmp == 1 and len(values["encrypt_key-group1"]) != 32:
                error = "group1 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp == 2 and len(values["encrypt_key-group1"]) != 64:
                error = "group1 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp == 3 and len(values["encrypt_key-group1"]) != 48:
                error = "group1 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp == 4 and len(values["encrypt_key-group1"]) != 64:
                error = "group1 key length error"
                bflb_utils.printf(error)
                bflb_utils.set_error_code("0071")
                return bflb_utils.errorcode_msg()
            if tmp != 0:
                if len(values["aes_iv-group1"]) != 32:
                    error = "group1 AES IV length error"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0072")
                    return bflb_utils.errorcode_msg()
                if values["aes_iv-group1"].endswith("00000000") is False:
                    error = "group1 AES IV should endswith 4 bytes zero"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0073")
                    return bflb_utils.errorcode_msg()
        if "key_sel-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_section, "key_sel",
                                  self.key_sel.index(values["key_sel-group1"]))
        if "crc_ignore-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_section, "crc_ignore",
                                  self.crc_ignore.index(values["crc_ignore-group1"]))
        if "hash_ignore-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_section, "hash_ignore",
                                  self.hash_ignore.index(values["hash_ignore-group1"]))
        for index in range(5):
            num = str(index+1)
            if values["img%s_group" % num] == "unused":
                bflb_utils.update_cfg(cfg, group0_section, "%s_config_enable" % cpu_list[index], "1")
                bflb_utils.update_cfg(cfg, group0_section, "%s_halt_cpu" % cpu_list[index], "1")
                bflb_utils.update_cfg(cfg, group1_section, "%s_config_enable" % cpu_list[index], "1")
                bflb_utils.update_cfg(cfg, group1_section, "%s_halt_cpu" % cpu_list[index], "1")
            elif values["img%s_group" % num] == "group0":
                bflb_utils.update_cfg(cfg, group0_section, "%s_config_enable" % cpu_list[index], "1")
                bflb_utils.update_cfg(cfg, group0_section, "%s_halt_cpu" % cpu_list[index], "0")
                bflb_utils.update_cfg(cfg, group1_section, "%s_config_enable" % cpu_list[index], "0")
                bflb_utils.update_cfg(cfg, group1_section, "%s_halt_cpu" % cpu_list[index], "0")
            elif values["img%s_group" % num] == "group1":
                bflb_utils.update_cfg(cfg, group0_section, "%s_config_enable" % cpu_list[index], "0")
                bflb_utils.update_cfg(cfg, group0_section, "%s_halt_cpu" % cpu_list[index], "0")
                bflb_utils.update_cfg(cfg, group1_section, "%s_config_enable" % cpu_list[index], "1")
                bflb_utils.update_cfg(cfg, group1_section, "%s_halt_cpu" % cpu_list[index], "0")
    
        bflb_utils.update_cfg(cfg, group0_section, "img_len_cnt", "0x100")
        bflb_utils.update_cfg(cfg, group1_section, "img_len_cnt", "0x100")
        for index in range(5):
            if int(img_addr_offset[index].replace("0x", ""), 16) > 0:
                offset = int(img_addr_offset[index].replace("0x", ""), 16) - int(
                    group0_img_start.replace("0x", ""), 16)
                bflb_utils.update_cfg(cfg, group0_section, "%s_image_address_offset" % cpu_list[index],
                                    "0x%X" % (offset))
                bflb_utils.update_cfg(cfg, group0_section, "%s_boot_entry" % cpu_list[index],
                                    "0x%X" % (int(img_addr_offset[index].replace("0x", ""), 16)))
            if int(img_addr_offset[index+5].replace("0x", ""), 16) > 0:
                offset = int(img_addr_offset[index+5].replace("0x", ""), 16) - int(
                    group1_img_start.replace("0x", ""), 16)
                bflb_utils.update_cfg(cfg, group1_section, "%s_image_address_offset" % cpu_list[index],
                                    "0x%X" % (offset))
                bflb_utils.update_cfg(cfg, group1_section, "%s_boot_entry" % cpu_list[index],
                                    "0x%X" % (int(img_addr_offset[index+5].replace("0x", ""), 16)))
    
        if values["boot_src"] == "UART/USB":
            for index in range(5):
                bflb_utils.update_cfg(cfg, group0_section, "%s_boot_entry" % cpu_list[index],
                                      self.img_addr_remap(img_addr_offset[index]))
                bflb_utils.update_cfg(cfg, group1_section, "%s_boot_entry" % cpu_list[index],
                                      self.img_addr_remap(img_addr_offset[index+5]))
        cfg.write(bh_cfg_file, "w+")
        if values["boot_src"] == "Flash":
            bflb_efuse_boothd_create.bootheader_create_process(
                chipname, chiptype, bh_cfg_file, group0_bh_file, group1_bh_file,
                self.img_create_path + "/bootheader_dummy.bin")
            bflb_efuse_boothd_create.efuse_create_process(chipname, chiptype, bh_cfg_file, efuse_file)
        else:
            bflb_efuse_boothd_create.bootheader_create_process(chipname, chiptype, bh_cfg_file,
                                                               group0_bh_file, group1_bh_file, True)
            bflb_efuse_boothd_create.efuse_create_process(chipname, chiptype, bh_cfg_file, efuse_file)
        # create img_create_cfg.ini
        cfg = BFConfigParser()
        cfg.read(self.img_create_cfg)
        bflb_utils.update_cfg(cfg, group0_img_create_section, "boot_header_file", group0_bh_file)
        bflb_utils.update_cfg(cfg, group1_img_create_section, "boot_header_file", group1_bh_file)
        bflb_utils.update_cfg(cfg, group0_img_create_section, "efuse_file", efuse_file)
        bflb_utils.update_cfg(cfg, group1_img_create_section, "efuse_file", efuse_file)
        bflb_utils.update_cfg(cfg, group0_img_create_section, "efuse_mask_file", efuse_mask_file)
        bflb_utils.update_cfg(cfg, group1_img_create_section, "efuse_mask_file", efuse_mask_file)
        # create segheader
        i = 0
        segheader_group0 = ""
        segheader_group1 = ""
        while i < len(segheader_file):
            if i < 5:
                if segheader_group0 != "":
                    segheader_group0 += " "
                segheader_group0 += self.img_create_path + segheader_file[i]
            else:
                if segheader_group1 != "":
                    segheader_group1 += " "
                segheader_group1 += self.img_create_path + segheader_file[i]
            segheader = bytearray(12)
            segheader[0:4] = bflb_utils.int_to_4bytearray_l(
                int(self.img_addr_remap(img_addr_offset[i].replace("0x", "")), 16))
            segfp = open(self.img_create_path + segheader_file[i], 'wb+')
            segfp.write(segheader)
            segfp.close()
            i = i + 1
        bflb_utils.update_cfg(cfg, group0_img_create_section, "segheader_file", segheader_group0)
        bflb_utils.update_cfg(cfg, group1_img_create_section, "segheader_file", segheader_group1)
        bflb_utils.update_cfg(cfg, group0_img_create_section, "segdata_file", group0_img)
        bflb_utils.update_cfg(cfg, group1_img_create_section, "segdata_file", group1_img)
        if "encrypt_key-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_img_create_section, "aes_key_org",
                                  values["encrypt_key-group0"])
        if "aes_iv-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_img_create_section, "aes_iv", values["aes_iv-group0"])
        if "public_key_cfg-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_img_create_section, "publickey_file",
                                  values["public_key_cfg-group0"])
        if "private_key_cfg-group0" in values.keys():
            bflb_utils.update_cfg(cfg, group0_img_create_section, "privatekey_file_uecc",
                                  values["private_key_cfg-group0"])
        if "encrypt_key-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_img_create_section, "aes_key_org",
                                  values["encrypt_key-group1"])
        if "aes_iv-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_img_create_section, "aes_iv", values["aes_iv-group1"])
        if "public_key_cfg-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_img_create_section, "publickey_file",
                                  values["public_key_cfg-group1"])
        if "private_key_cfg-group1" in values.keys():
            bflb_utils.update_cfg(cfg, group1_img_create_section, "privatekey_file_uecc",
                                  values["private_key_cfg-group1"])
        bflb_utils.update_cfg(cfg, group0_img_create_section, "bootinfo_file", group0_bootinfo_file)
        bflb_utils.update_cfg(cfg, group1_img_create_section, "bootinfo_file", group1_bootinfo_file)
        bflb_utils.update_cfg(cfg, group0_img_create_section, "img_file", group0_img_output_file)
        bflb_utils.update_cfg(cfg, group1_img_create_section, "img_file", group1_img_output_file)
        bflb_utils.update_cfg(cfg, group0_img_create_section, "whole_img_file",
                              group0_img_output_file.replace(".bin", "_if.bin"))
        bflb_utils.update_cfg(cfg, group1_img_create_section, "whole_img_file",
                              group1_img_output_file.replace(".bin", "_if.bin"))
        cfg.write(self.img_create_cfg, "w+")
        # create img
        if values["boot_src"] == "Flash":
            options = ["--image=media", "--group=all", "--signer=none"]
            args = parser_image.parse_args(options)
            bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
        else:
            options = ["--image=if", "--group=all", "--signer=none"]
            args = parser_image.parse_args(options)
            bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
        i = 0
        while i < len(segheader_file):
            os.remove(self.img_create_path + segheader_file[i])
            i = i + 1
        if os.path.exists(self.img_create_path + '/bootheader_dummy.bin'):
            os.remove(self.img_create_path + "/bootheader_dummy.bin")
        return True
    
    def create_img(self, chipname, chiptype, values):
        # basic check
        gol.GlobalVar.values = values
        error = True
        try:
            if chiptype == "bl606p":
                error = self.create_img_606p(chipname, chiptype, values)
                return error
            else:
                if values["img_file"] == "":
                    if values["device_tree"]:
                        ro_params_d = values["device_tree"]
                        try:
                            dts_hex = bl_ro_device_tree.bl_dts2hex(ro_params_d)
                            dts_bytearray = bflb_utils.hexstr_to_bytearray(dts_hex)
                        except Exception as e:
                            dts_bytearray = None
                        tlv_bin = self.img_create_path + "/tlv.bin"
                        with open(tlv_bin, "wb") as fp:
                            fp.write(dts_bytearray)
                        error = "tvl bin created"
                        return error
                    if values["dl_chiperase"] == "True":
                        bflb_utils.printf("flash chiperase operation")
                        return True
                    else:
                        error = "Please select image file"
                        bflb_utils.printf(error)
                        bflb_utils.set_error_code("0061")
                        return bflb_utils.errorcode_msg()
                else:
                    if values["device_tree"]:
                        ro_params_d = values["device_tree"]
                        try:
                            dts_hex = bl_ro_device_tree.bl_dts2hex(ro_params_d)
                            dts_bytearray = bflb_utils.hexstr_to_bytearray(dts_hex)
                        except Exception as e:
                            dts_bytearray = None
                        if dts_bytearray:
                            tlv_bin = self.img_create_path + "/tlv.bin"
                            with open(tlv_bin, "wb") as fp:
                                fp.write(dts_bytearray)
                        img_org = values["img_file"]
                        if parse_rfpa(img_org) == b'BLRFPARA' and dts_bytearray:
                            length = len(dts_bytearray)
                            with open(img_org, "rb") as fp:
                                bin_byte = fp.read()
                                bin_bytearray = bytearray(bin_byte)
                                bin_bytearray[1032:1032+length] = dts_bytearray
                            filedir, ext = os.path.splitext(img_org)
                            img_new = filedir + "_rfpa" + ext
                            with open(img_new, "wb") as fp:
                                fp.write(bin_bytearray)
                            values["img_file"] = img_new
                if values["img_addr"] == "" or values["img_addr"] == "0x":
                    error = "Please set image address"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0062")
                    return bflb_utils.errorcode_msg()
                if values["bootinfo_addr"] == "" or values["bootinfo_addr"] == "0x":
                    error = "Please set boot info address"
                    bflb_utils.printf(error)
                    bflb_utils.set_error_code("0063")
                    return bflb_utils.errorcode_msg()
                if "encrypt_type" in values.keys():
                    if "encrypt_key" in values.keys():
                        if values["encrypt_type"] != "None" and values["encrypt_key"] == "":
                            error = "Please set AES key"
                            bflb_utils.printf(error)
                            bflb_utils.set_error_code("0064")
                            return bflb_utils.errorcode_msg()
                    if "aes_iv" in values.keys():
                        if values["encrypt_type"] != "None" and values["aes_iv"] == "":
                            error = "Please set AES IV"
                            bflb_utils.printf(error)
                            bflb_utils.set_error_code("0065")
                            return bflb_utils.errorcode_msg()
                if "sign_type" in values.keys():
                    if "public_key_cfg" in values.keys():
                        if values["sign_type"] != "None" and values["public_key_cfg"] == "":
                            error = "Please set public key"
                            bflb_utils.printf(error)
                            bflb_utils.set_error_code("0066")
                            return bflb_utils.errorcode_msg()
                    if "private_key_cfg" in values.keys():
                        if values["sign_type"] != "None" and values["private_key_cfg"] == "":
                            error = "Please set private key"
                            bflb_utils.printf(error)
                            bflb_utils.set_error_code("0067")
                            return bflb_utils.errorcode_msg()
                # create bootheader_boot2.ini
                if values["img_type"] == "SingleCPU":
                    section = "BOOTHEADER_CFG"
                    bh_cfg_file = self.img_create_path + "/bootheader_cfg.ini"
                    bh_file = self.img_create_path + "/bootheader.bin"
                    efuse_file = self.img_create_path + "/efusedata.bin"
                    efuse_mask_file = self.img_create_path + "/efusedata_mask.bin"
                    bootinfo_file = self.img_create_path + "/bootinfo.bin"
                    img_output_file = self.img_create_path + "/img.bin"
                    img_create_section = "Img_Cfg"
                elif values["img_type"] == "BLSP_Boot2":
                    if chiptype == "bl60x":
                        section = "BOOTHEADER_CPU0_CFG"
                    else:
                        section = "BOOTHEADER_CFG"
                    bh_cfg_file = self.img_create_path + "/bootheader_cfg_blsp_boot2.ini"
                    bh_file = self.img_create_path + "/bootheader_blsp_boot2.bin"
                    efuse_file = self.img_create_path + "/efusedata_blsp_boot2.bin"
                    efuse_mask_file = self.img_create_path + "/efusedata_mask_blsp_boot2.bin"
                    bootinfo_file = self.img_create_path + "/bootinfo_blsp_boot2.bin"
                    img_output_file = self.img_create_path + "/img_blsp_boot2.bin"
                    if chiptype == "bl60x":
                        img_create_section = "Img_CPU0_Cfg"
                    else:
                        img_create_section = "Img_Cfg"
                elif values["img_type"] == "CPU0":
                    section = "BOOTHEADER_CPU0_CFG"
                    bh_cfg_file = self.img_create_path + "/bootheader_cfg_cpu0.ini"
                    bh_file = self.img_create_path + "/bootheader_cpu0.bin"
                    efuse_file = self.img_create_path + "/efusedata_cpu0.bin"
                    efuse_mask_file = self.img_create_path + "/efusedata_mask_cpu0.bin"
                    bootinfo_file = self.img_create_path + "/bootinfo_cpu0.bin"
                    img_output_file = self.img_create_path + "/img_cpu0.bin"
                    img_create_section = "Img_CPU0_Cfg"
                elif values["img_type"] == "CPU1":
                    section = "BOOTHEADER_CPU1_CFG"
                    bh_cfg_file = self.img_create_path + "/bootheader_cfg_cpu1.ini"
                    bh_file = self.img_create_path + "/bootheader_cpu1.bin"
                    efuse_file = self.img_create_path + "/efusedata_cpu1.bin"
                    efuse_mask_file = self.img_create_path + "/efusedata_mask_cpu1.bin"
                    bootinfo_file = self.img_create_path + "/bootinfo_cpu1.bin"
                    img_output_file = self.img_create_path + "/img_cpu1.bin"
                    img_create_section = "Img_CPU1_Cfg"
                elif values["img_type"] == "RAW":
                    bflb_utils.printf("raw data do not need create.")
                    bflb_utils.set_error_code("0068")
                    return bflb_utils.errorcode_msg()
                if values["img_type"] == "CPU0" or values["img_type"] == "CPU1":
                    bflb_utils.copyfile(self.efuse_bh_default_cfg_dp, bh_cfg_file)
                    shutil.copy(self.img_create_cfg_dp_org, self.img_create_cfg)
                elif values["img_type"] == "BLSP_Boot2":
                    if chiptype == "bl60x":
                        bflb_utils.copyfile(self.efuse_bh_default_cfg_dp, bh_cfg_file)
                        shutil.copy(self.img_create_cfg_dp_org, self.img_create_cfg)
                    else:
                        bflb_utils.copyfile(self.efuse_bh_default_cfg, bh_cfg_file)
                        shutil.copy(self.img_create_cfg_org, self.img_create_cfg)
                else:
                    bflb_utils.copyfile(self.efuse_bh_default_cfg, bh_cfg_file)
                    shutil.copy(self.img_create_cfg_org, self.img_create_cfg)
                # add flash cfg
                if os.path.exists(self.eflash_loader_cfg_tmp):
                    cfg1 = BFConfigParser()
                    cfg1.read(self.eflash_loader_cfg_tmp)
                    if cfg1.has_option("FLASH_CFG", "flash_id"):
                        flash_id = cfg1.get("FLASH_CFG", "flash_id")
                        if bflb_flash_select.update_flash_cfg(chipname, chiptype, flash_id,
                                                              bh_cfg_file, False, section) is False:
                            error = "flash_id:" + flash_id + " do not support"
                            bflb_utils.printf(error)
                            bflb_utils.set_error_code("0069")
                            return bflb_utils.errorcode_msg()
                    else:
                        error = "Do not find flash_id in eflash_loader_cfg.ini"
                        bflb_utils.printf(error)
                        bflb_utils.set_error_code("0070")
                        return bflb_utils.errorcode_msg()
                else:
                    bflb_utils.printf("Config file not found")
                    bflb_utils.set_error_code("000B")
                    return bflb_utils.errorcode_msg()
                # update config
                cfg = BFConfigParser()
                cfg.read(bh_cfg_file)
                # if section == "BOOTHEADER_CFG":
                #     cfg.update_section_name('BOOTHEADER_CPU0_CFG', section)
                for itrs in cfg.sections():
                    bflb_utils.printf(itrs)
                    if itrs != section and itrs != "EFUSE_CFG":
                        cfg.delete_section(itrs)
                cfg.write(bh_cfg_file, "w+")
                cfg = BFConfigParser()
                cfg.read(bh_cfg_file)
                if chiptype == "bl702":
                    bflb_utils.update_cfg(cfg, section, "boot2_enable", "0")
                if "xtal_type" in values.keys():
                    bflb_utils.update_cfg(cfg, section, "xtal_type",
                                          self.xtal_type_.index(values["xtal_type"]))
                if "pll_clk" in values.keys():
                    bflb_utils.update_cfg(cfg, section, "pll_clk", self.pll_clk.index(values["pll_clk"]))
                    if chiptype == "bl602":
                        i = self.pll_clk.index(values["pll_clk"])
                        if i == 3 or i == 4 or i == 5:
                            bflb_utils.update_cfg(cfg, section, "bclk_div", "1")
                        else:
                            bflb_utils.update_cfg(cfg, section, "bclk_div", "0")
                    elif chiptype == "bl702":
                        i = self.pll_clk.index(values["pll_clk"])
                        if i == 3 or i == 4:
                            bflb_utils.update_cfg(cfg, section, "bclk_div", "1")
                        else:
                            bflb_utils.update_cfg(cfg, section, "bclk_div", "0")
    
                tmp = values["flash_clk_type"]
                if tmp != "Manual":
                    bflb_utils.update_cfg(cfg, section, "flash_clk_type",
                                          self.flash_clk_type.index(values["flash_clk_type"]))
                    bflb_utils.update_cfg(cfg, section, "flash_clk_div", "0")
                    if "xtal_type" in values.keys():
                        if tmp == "XTAL" or tmp == "XCLK" or tmp == "48M" or tmp == "57P6M" or values[
                                "xtal_type"] == "XTAL_None":
                            # 1T
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_delay", "1")
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_invert", "0x01")
                        else:
                            # 1.5T
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_delay", "1")
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_invert", "0x03")
                    else:
                        if tmp == "XTAL" or tmp == "XCLK" or tmp == "48M" or tmp == "57P6M":
                            # 1T
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_delay", "1")
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_invert", "0x01")
                        else:
                            # 1.5T
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_delay", "1")
                            bflb_utils.update_cfg(cfg, section, "sfctrl_clk_invert", "0x03")
    
                if "sign_type" in values.keys():
                    bflb_utils.update_cfg(cfg, section, "sign", self.sign_type.index(values["sign_type"]))
                if "encrypt_type" in values.keys():
                    tmp = self.encrypt_type.index(values["encrypt_type"])
                    bflb_utils.update_cfg(cfg, section, "encrypt_type", tmp)
                    if tmp == 1 and len(values["encrypt_key"]) != 32:
                        error = "Key length error"
                        bflb_utils.printf(error)
                        bflb_utils.set_error_code("0071")
                        return bflb_utils.errorcode_msg()
                    if tmp == 2 and len(values["encrypt_key"]) != 64:
                        error = "Key length error"
                        bflb_utils.printf(error)
                        bflb_utils.set_error_code("0071")
                        return bflb_utils.errorcode_msg()
                    if tmp == 3 and len(values["encrypt_key"]) != 48:
                        error = "Key length error"
                        bflb_utils.printf(error)
                        bflb_utils.set_error_code("0071")
                        return bflb_utils.errorcode_msg()
                    if tmp != 0:
                        if len(values["aes_iv"]) != 32:
                            error = "AES IV length error"
                            bflb_utils.printf(error)
                            bflb_utils.set_error_code("0072")
                            return bflb_utils.errorcode_msg()
                        if values["aes_iv"].endswith("00000000") is False:
                            error = "AES IV should endswith 4 bytes zero"
                            bflb_utils.printf(error)
                            bflb_utils.set_error_code("0073")
                            return bflb_utils.errorcode_msg()
                if "key_sel" in values.keys():
                    bflb_utils.update_cfg(cfg, section, "key_sel", self.key_sel.index(values["key_sel"]))
                if "cache_way_disable" in values.keys():
                    bflb_utils.update_cfg(cfg, section, "cache_way_disable",
                                          (1 << self.cache_way_disable.index(values["cache_way_disable"])) -
                                          1)
                if "crc_ignore" in values.keys():
                    bflb_utils.update_cfg(cfg, section, "crc_ignore",
                                          self.crc_ignore.index(values["crc_ignore"]))
                if "hash_ignore" in values.keys():
                    bflb_utils.update_cfg(cfg, section, "hash_ignore",
                                          self.hash_ignore.index(values["hash_ignore"]))
                if values["img_type"] == "CPU0":
                    bflb_utils.update_cfg(cfg, section, "halt_cpu1", "0")
                elif chiptype != "bl602":
                    bflb_utils.update_cfg(cfg, section, "halt_cpu1", "1")
                # any value except 0 is ok
                bflb_utils.update_cfg(cfg, section, "img_len", "0x100")
                bflb_utils.update_cfg(cfg, section, "img_start", values["img_addr"])
                cfg.write(bh_cfg_file, "w+")
                if values["img_type"] == "CPU1":
                    bflb_efuse_boothd_create.bootheader_create_process(
                        chipname, chiptype, bh_cfg_file, self.img_create_path + "/bootheader_dummy.bin",
                        bh_file)
                elif values["boot_src"] == "UART/SDIO" or values["boot_src"] == "UART/USB":
                    bflb_efuse_boothd_create.bootheader_create_process(
                        chipname, chiptype, bh_cfg_file, bh_file,
                        self.img_create_path + "/bootheader_dummy.bin", True)
                else:
                    bflb_efuse_boothd_create.bootheader_create_process(
                        chipname, chiptype, bh_cfg_file, bh_file,
                        self.img_create_path + "/bootheader_dummy.bin")
                # create efuse data
                efuse_data = bytearray(256)
                fp = open(efuse_file, 'wb+')
                fp.write(efuse_data)
                fp.close()
                fp = open(efuse_mask_file, 'wb+')
                fp.write(efuse_data)
                fp.close()
                # create img_create_cfg.ini
                cfg = BFConfigParser()
                cfg.read(self.img_create_cfg)
                bflb_utils.update_cfg(cfg, img_create_section, "boot_header_file", bh_file)
                bflb_utils.update_cfg(cfg, img_create_section, "efuse_file", efuse_file)
                bflb_utils.update_cfg(cfg, img_create_section, "efuse_mask_file", efuse_mask_file)
                # create segheader
                segheader = bytearray(12)
                segheader[0:4] = bflb_utils.int_to_4bytearray_l(
                    int(values["img_addr"].replace("0x", ""), 16))
                segfp = open(self.img_create_path + "/segheader_tmp.bin", 'wb+')
                segfp.write(segheader)
                segfp.close()
                bflb_utils.update_cfg(cfg, img_create_section, "segheader_file",
                                     self. img_create_path + "/segheader_tmp.bin")
                bflb_utils.update_cfg(cfg, img_create_section, "segdata_file", values["img_file"])
    
                if "encrypt_key" in values.keys():
                    bflb_utils.update_cfg(cfg, img_create_section, "aes_key_org",
                                          values["encrypt_key"])
                if "aes_iv" in values.keys():
                    bflb_utils.update_cfg(cfg, img_create_section, "aes_iv", values["aes_iv"])
                if "public_key_cfg" in values.keys():
                    bflb_utils.update_cfg(cfg, img_create_section, "publickey_file",
                                          values["public_key_cfg"])
                if "private_key_cfg" in values.keys():
                    bflb_utils.update_cfg(cfg, img_create_section, "privatekey_file_uecc",
                                          values["private_key_cfg"])
    
                bflb_utils.update_cfg(cfg, img_create_section, "bootinfo_file", bootinfo_file)
                bflb_utils.update_cfg(cfg, img_create_section, "img_file", img_output_file)
                bflb_utils.update_cfg(cfg, img_create_section, "whole_img_file",
                                      img_output_file.replace(".bin", "_if.bin"))
                cfg.write(self.img_create_cfg, "w+")
                # create img
                if values["boot_src"] == "Flash":
                    if values["img_type"] == "SingleCPU":
                        # TODO: double sign
                        options = ["--image=media", "--signer=none"]
                        args = parser_image.parse_args(options)
                        bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                    elif values["img_type"] == "BLSP_Boot2":
                        if chiptype == "bl60x":
                            options = ["--image=media", "--cpu=cpu0", "--signer=none"]
                            args = parser_image.parse_args(options)
                            bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                        else:
                            options = ["--image=media", "--signer=none"]
                            args = parser_image.parse_args(options)
                            bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                    elif values["img_type"] == "CPU0":
                        options = ["--image=media", "--cpu=cpu0", "--signer=none"]
                        args = parser_image.parse_args(options)
                        bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                    elif values["img_type"] == "CPU1":
                        options = ["--image=media", "--cpu=cpu1", "--signer=none"]
                        args = parser_image.parse_args(options)
                        bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                        bflb_utils.set_error_code("0074")
                        return bflb_utils.errorcode_msg()
                else:
                    if values["img_type"] == "SingleCPU":
                        options = ["--image=if", "--signer=none"]
                        args = parser_image.parse_args(options)
                        bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                    elif values["img_type"] == "CPU0":
                        options = ["--image=if", "--cpu=cpu0", "--signer=none"]
                        args = parser_image.parse_args(options)
                        bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                    elif values["img_type"] == "CPU1":
                        options = ["--image=if", "--cpu=cpu1", "--signer=none"]
                        args = parser_image.parse_args(options)
                        bflb_img_create.img_create(args, chipname, chiptype, self.img_create_path, self.img_create_cfg)
                os.remove(self.img_create_path + "/segheader_tmp.bin")
                if os.path.exists(self.img_create_path + '/bootheader_dummy.bin'):
                    os.remove(self.img_create_path + "/bootheader_dummy.bin")
                return True
        except Exception as e:
            error = str(e)
            bflb_utils.printf(error)
            bflb_utils.set_error_code("0075")
            traceback.print_exc(limit=5, file=sys.stdout)
        finally:
            return error
        
    def program_img_thread(self, values, callback=None):
        bflb_utils.printf("========= eflash loader config =========")
        options = ""
        ret = None
        create_output_path = os.path.relpath(self.img_create_path, app_path)
        try:
            if self.chiptype != "bl606p":
                if values["img_file"] == "" and values["dl_chiperase"] == "True":
                    bflb_utils.printf("Erase Flash")
                    # program flash,create eflash_loader_cfg.ini
                    cfg = BFConfigParser()
                    if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                        shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
                    cfg.read(self.eflash_loader_cfg_tmp)
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "interface", values["dl_device"].lower())
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "device", values["dl_comport"])
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_uart_load", values["dl_comspeed"])
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_jlink", values["dl_jlinkspeed"])
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "erase", "2")
                    eflash_loader_bin = os.path.join(app_path, self.chipname, "eflash_loader/" + get_eflash_loader(values["dl_xtal"]))
                    if "dl_verify" in values.keys():
                        if values["dl_verify"] == "True":
                            bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "1")
                        else:
                            bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "0")
                    if cfg.has_option("LOAD_CFG", "xtal_type"):
                        bflb_utils.update_cfg(cfg, "LOAD_CFG", "xtal_type",
                                              self.xtal_type_.index(values["xtal_type"]))
                    cfg.write("eflash_loader_tmp.ini", "w+")
                    options = ["--erase", "--end=0", "-c", "eflash_loader_tmp.ini"]
                else:
                    # decide file name
                    if values["img_type"] == "SingleCPU":
                        bootinfo_file = create_output_path + "/bootinfo.bin"
                        img_output_file = create_output_path + "/img.bin"
                        whole_img_output_file = create_output_path + "/whole_img.bin"
                    elif values["img_type"] == "BLSP_Boot2":
                        bootinfo_file = create_output_path + "/bootinfo_blsp_boot2.bin"
                        img_output_file = create_output_path + "/img_blsp_boot2.bin"
                        whole_img_output_file = create_output_path + "/whole_img_blsp_boot2.bin"
                    elif values["img_type"] == "CPU0":
                        bootinfo_file = create_output_path + "/bootinfo_cpu0.bin"
                        img_output_file = create_output_path + "/img_cpu0.bin"
                        whole_img_output_file = create_output_path + "/whole_img_cpu0.bin"
                    elif values["img_type"] == "CPU1":
                        bootinfo_file = create_output_path + "/bootinfo_cpu1.bin"
                        img_output_file = create_output_path + "/img_cpu1.bin"
                        whole_img_output_file = create_output_path + "/whole_img_cpu1.bin"
                    # uart download
                    if values["boot_src"] == "UART/SDIO" or values["boot_src"] == "UART/USB":
                        cfg = BFConfigParser()
                        if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                            shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
                        cfg.read(self.eflash_loader_cfg_tmp)
                        boot_speed = int(cfg.get("LOAD_CFG", "speed_uart_boot"))
                        if values["img_type"] == "RAW":
                            ret = self.img_loader_thread(values["dl_comport"], boot_speed, boot_speed,
                                                    values["img_file"], None, callback)
                        else:
                            ret = self.img_loader_thread(values["dl_comport"], boot_speed, boot_speed,
                                                    img_output_file.replace(".bin", "_if.bin"), None,
                                                    callback)
                        if ret is False:
                            ret = "Img load fail"
                        return ret
                    # program flash,create eflash_loader_cfg.ini
                    cfg = BFConfigParser()
                    if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                        shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
                    cfg.read(self.eflash_loader_cfg_tmp)
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "interface", values["dl_device"].lower())
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "device", values["dl_comport"])
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_uart_load", values["dl_comspeed"])
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_jlink", values["dl_jlinkspeed"])
                    if values["dl_chiperase"] == "True":
                        bflb_utils.update_cfg(cfg, "LOAD_CFG", "erase", "2")
                    else:
                        bflb_utils.update_cfg(cfg, "LOAD_CFG", "erase", "1")
                    if "dl_verify" in values.keys():
                        if values["dl_verify"] == "True":
                            bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "1")
                        else:
                            bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "0")
    
                    eflash_loader_bin = os.path.join(
                        app_path, self.chipname, "eflash_loader/" + get_eflash_loader(values["dl_xtal"]))
    
                    if cfg.has_option("LOAD_CFG", "xtal_type"):
                        bflb_utils.update_cfg(cfg, "LOAD_CFG", "xtal_type",
                                              self.xtal_type_.index(values["xtal_type"]))
                    if values["img_type"] == "RAW":
                        bflb_utils.update_cfg(cfg, "FLASH_CFG", "file", values["img_file"])
                        bflb_utils.update_cfg(cfg, "FLASH_CFG", "address",
                                              values["img_addr"].replace("0x", ""))
                    else:
                        bind_bootinfo = True
                        if bind_bootinfo is True:
                            img_addr = int(values["img_addr"].replace("0x", ""), 16)
                            whole_img_len = img_addr + os.path.getsize(os.path.join(app_path, img_output_file))
                            whole_img_data = self.bl_create_flash_default_data(whole_img_len)
                            filedata = self.bl_get_file_data([bootinfo_file])[0]
                            whole_img_data[0:len(filedata)] = filedata
                            filedata = self.bl_get_file_data([img_output_file])[0]
                            whole_img_data[img_addr:img_addr + len(filedata)] = filedata
                            fp = open(os.path.join(app_path, whole_img_output_file), 'wb+')
                            fp.write(whole_img_data)
                            fp.close()
                            # bflb_utils.update_cfg(cfg, "FLASH_CFG", "file", convert_path(whole_img_output_file))
                            # bflb_utils.update_cfg(cfg, "FLASH_CFG", "address", values["bootinfo_addr"].replace("0x", ""))
    
                        bflb_utils.update_cfg(cfg, "FLASH_CFG", "file",
                                              convert_path(bootinfo_file) + " " + convert_path(img_output_file))
                        bflb_utils.update_cfg(cfg, "FLASH_CFG", "address",
                                              values["bootinfo_addr"].replace("0x", "") + " " + values["img_addr"].replace("0x", ""))
                    cfg.write(self.eflash_loader_cfg_tmp, "w+")
                    # call eflash_loader
                    if values["dl_device"].lower() == "uart":
                        options = ["--write", "--flash", "-p", values["dl_comport"], "-c", self.eflash_loader_cfg_tmp]
                    else:
                        options = ["--write", "--flash", "-c", self.eflash_loader_cfg_tmp]
                    if  "encrypt_key" in values.keys() and\
                        "aes_iv" in values.keys():
                        if  values["encrypt_key"] != "" and\
                            values["aes_iv"] != "":
                                options.extend(["--efuse",\
                                "--createcfg=" + self.img_create_cfg])
                                self.efuse_load_en = True
            else:
                group0_used = False
                group1_used = False
                group0_bootinfo_file = create_output_path + "/bootinfo_group0.bin"
                group0_img_output_file = create_output_path + "/img_group0.bin"
                group1_bootinfo_file = create_output_path + "/bootinfo_group1.bin"
                group1_img_output_file = create_output_path + "/img_group1.bin"
                whole_img_output_file = create_output_path + "/whole_img.bin"
                if values["img1_group"] == "group0" or\
                   values["img2_group"] == "group0" or\
                   values["img3_group"] == "group0" or\
                   values["img4_group"] == "group0" or\
                   values["img5_group"] == "group0":
                    group0_used = True
                if values["img1_group"] == "group1" or\
                   values["img2_group"] == "group1" or\
                   values["img3_group"] == "group1" or\
                   values["img4_group"] == "group1" or\
                   values["img5_group"] == "group1":
                    group1_used = True
                # uart download
                if values["boot_src"] == "UART/USB":
                    cfg = BFConfigParser()
                    if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                        shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
                    cfg.read(self.eflash_loader_cfg_tmp)
                    boot_speed = int(cfg.get("LOAD_CFG", "speed_uart_boot"))
                    if values["img_type"] == "RAW":
                        ret = self.img_loader_thread(values["dl_comport"], boot_speed, boot_speed,
                                                values["img1_file"], None, callback)
                    else:
                        if group0_used is True and group1_used is False:
                            ret = self.img_loader_thread(values["dl_comport"], boot_speed, boot_speed,
                                                    group0_img_output_file.replace(".bin", "_if.bin"),
                                                    None, callback)
                        elif group0_used is False and group1_used is True:
                            ret = self.img_loader_thread(values["dl_comport"], boot_speed, boot_speed,
                                                    group1_img_output_file.replace(".bin", "_if.bin"),
                                                    None, callback)
                        elif group0_used is True and group1_used is True:
                            ret = self.img_loader_thread(values["dl_comport"], boot_speed, boot_speed,
                                                    group0_img_output_file.replace(".bin", "_if.bin"),
                                                    group1_img_output_file.replace(".bin", "_if.bin"),
                                                    callback)
                    if ret is False:
                        ret = "Img load fail"
                    return ret
                # program flash, create eflash_loader_cfg.ini
                cfg = BFConfigParser()
                if os.path.isfile(self.eflash_loader_cfg_tmp) is False:
                    shutil.copy(self.eflash_loader_cfg, self.eflash_loader_cfg_tmp)
                cfg.read(self.eflash_loader_cfg_tmp)
                bflb_utils.update_cfg(cfg, "LOAD_CFG", "interface", values["dl_device"].lower())
                bflb_utils.update_cfg(cfg, "LOAD_CFG", "device", values["dl_comport"])
                bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_uart_load", values["dl_comspeed"])
                bflb_utils.update_cfg(cfg, "LOAD_CFG", "speed_jlink", values["dl_jlinkspeed"])
                if values["dl_chiperase"] == "True":
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "erase", "2")
                else:
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "erase", "1")
                if "dl_verify" in values.keys():
                    if values["dl_verify"] == "True":
                        bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "1")
                    else:
                        bflb_utils.update_cfg(cfg, "LOAD_CFG", "verify", "0")
    
                eflash_loader_bin = os.path.join(
                    app_path, self.chipname, "eflash_loader/" + get_eflash_loader(values["dl_xtal"]))
    
                if cfg.has_option("LOAD_CFG", "xtal_type"):
                    bflb_utils.update_cfg(cfg, "LOAD_CFG", "xtal_type",
                                          self.xtal_type_.index(values["xtal_type"]))
                if values["img_type"] == "RAW":
                    bflb_utils.update_cfg(cfg, "FLASH_CFG", "file", values["img1_file"])
                    bflb_utils.update_cfg(cfg, "FLASH_CFG", "address",
                                          values["img1_addr"].replace("0x", ""))
                else:
                    read_data = self.bl_get_file_data([group0_bootinfo_file])[0]
                    group0_img_offset = bflb_utils.bytearray_to_int(
                        bflb_utils.bytearray_reverse(read_data[128:132]))
                    group0_img_len = bflb_utils.bytearray_to_int(
                        bflb_utils.bytearray_reverse(read_data[136:140]))
                    read_data = self.bl_get_file_data([group1_bootinfo_file])[0]
                    group1_img_offset = bflb_utils.bytearray_to_int(
                        bflb_utils.bytearray_reverse(read_data[128:132]))
                    group1_img_len = bflb_utils.bytearray_to_int(
                        bflb_utils.bytearray_reverse(read_data[136:140]))
                    bind_bootinfo = True
                    if bind_bootinfo is True:
                        whole_img_len = 0
                        if group0_img_offset + group0_img_len > group1_img_offset + group1_img_len:
                            whole_img_len = group0_img_offset + group0_img_len
                        else:
                            whole_img_len = group1_img_offset + group1_img_len
                        whole_img_data = self.bl_create_flash_default_data(whole_img_len)
    
                        filedata = self.bl_get_file_data([group0_bootinfo_file])[0]
                        whole_img_data[0:len(filedata)] = filedata
    
                        filedata = self.bl_get_file_data([group1_bootinfo_file])[0]
                        whole_img_data[0x1000:len(filedata)] = filedata
    
                        filedata = self.bl_get_file_data([group0_img_output_file])[0]
                        if group0_img_len != len(filedata):
                            bflb_utils.printf("group0 img len error, get %d except %d" %
                                              (group0_img_len, len(filedata)))
                        whole_img_data[group0_img_offset:group0_img_offset + len(filedata)] = filedata
    
                        filedata = self.bl_get_file_data([group1_img_output_file])[0]
                        if group1_img_len != len(filedata):
                            bflb_utils.printf("group1 img len error, get %d except %d" %
                                              (group1_img_len, len(filedata)))
                        whole_img_data[group1_img_offset:group1_img_offset + len(filedata)] = filedata
    
                        fp = open(os.path.join(app_path, whole_img_output_file), 'wb+')
                        fp.write(whole_img_data)
                        fp.close()
                        # bflb_utils.update_cfg(cfg, "FLASH_CFG", "file", convert_path(whole_img_output_file))
                        # bflb_utils.update_cfg(cfg, "FLASH_CFG", "address", "00000000")
                    file_list = ""
                    addr_list = ""
                    if group0_used is True and group1_used is False:
                        file_list = convert_path(group0_bootinfo_file) + " "\
                                  + convert_path(group0_img_output_file)
                        addr_list = "00000000 %x" % (group0_img_offset)
                    elif group0_used is False and group1_used is True:
                        file_list = convert_path(group1_bootinfo_file.replace) + " "\
                                  + convert_path(group1_img_output_file)
                        addr_list = "00001000 %x" % (group1_img_offset)
                    elif group0_used is True and group1_used is True:
                        file_list = convert_path(group0_bootinfo_file) + " "\
                                  + convert_path(group1_bootinfo_file) + " "\
                                  + convert_path(group0_img_output_file) + " "\
                                  + convert_path(group1_img_output_file)
                        addr_list = "00000000 00001000 %x %x" % (group0_img_offset, group1_img_offset)
                    bflb_utils.update_cfg(cfg, "FLASH_CFG", "file", file_list)
                    bflb_utils.update_cfg(cfg, "FLASH_CFG", "address", addr_list.replace("0x", ""))
                cfg.write(self.eflash_loader_cfg_tmp, "w+")
                # call eflash_loader
                if values["dl_device"].lower() == "uart":
                    options = ["--write", "--flash", "-p", values["dl_comport"], "-c", self.eflash_loader_cfg_tmp]
                else:
                    options = ["--write", "--flash", "-c", self.eflash_loader_cfg_tmp]
                if  "encrypt_key-group0" in values.keys() and\
                    "encrypt_key-group1" in values.keys() and\
                    "aes_iv-group0" in values.keys() and\
                    "aes_iv-group1" in values.keys():
                        if  values["encrypt_key-group0"] != "" and\
                            values["encrypt_key-group1"] != "" and\
                            values["aes_iv-group0"] != "" and\
                            values["aes_iv-group1"] != "":
                                options.extend(["--efuse",\
                                "--createcfg=" + self.img_create_cfg])
                                self.efuse_load_en = True
            ret = bflb_img_create.compress_dir(self.chipname, "img_create_mcu", self.efuse_load_en)
            if ret is not True:
                return bflb_utils.errorcode_msg()
            args = parser_eflash.parse_args(options)
            ret = self.eflash_loader_thread(args, eflash_loader_bin, callback, self.create_img_callback)
    
        except Exception as e:
            ret = str(e)
            traceback.print_exc(limit=5, file=sys.stdout)
        finally:
            return ret
        
    def create_img_callback(self):
        error = None
        values = gol.GlobalVar.values
        error = self.create_img(self.chipname, self.chiptype, values)
        if error:
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

    
def get_value(args):
    chipname = args.chipname
    chiptype = chip_dict.get(chipname, "unkown chip type") 
    config = dict()
    config.setdefault('xtal_type', 'XTAL_38.4M')
    config.setdefault('pll_clk', '160M')
    config.setdefault('boot_src', 'Flash')
    config.setdefault('img_type', 'SingleCPU')
    config.setdefault('encrypt_type', 'None')
    config.setdefault('key_sel', '0')
    config.setdefault('cache_way_disable', 'None')
    config.setdefault('sign_type', 'None')
    config.setdefault('crc_ignore', 'False')
    config.setdefault('hash_ignore', 'False')
    config.setdefault('encrypt_key', '')
    config.setdefault('aes_iv', '')
    config.setdefault('public_key_cfg', '')
    config.setdefault('private_key_cfg', '')
    config.setdefault('bootinfo_addr', '0x0')  
    config["dl_device"] = args.interface.lower()
    config["dl_comport"] = args.port
    config["dl_comspeed"] = str(args.baudrate)
    config["dl_jlinkspeed"] = str(args.baudrate)
    config["img_file"] = args.firmware
    config["img_addr"] = "0x" + str(args.addr) 
    config["device_tree"] = args.dts
    
    if chiptype == "bl602":
        if not args.xtal: 
            config["dl_xtal"] = "40M"
            config["xtal_type"] = 'XTAL_40M'
            bflb_utils.printf("Default xtal is 40M")
        else:   
            config["dl_xtal"] = args.xtal 
            config["xtal_type"] = 'XTAL_' + args.xtal
        if not args.xtal:
            config["flash_clk_type"] = "48M"
            bflb_utils.printf("Default flash clock is 48M")
        else:      
            config["flash_clk_type"] = args.flashclk
        if not args.pllclk:
            config["pll_clk"] = "160M"
            bflb_utils.printf("Default pll clock is 160M")
        else:
            config["pll_clk"] = args.pllclk
    elif chiptype == "bl702":
        if not args.xtal: 
            config["dl_xtal"] = "32M"
            config["xtal_type"] = 'XTAL_32M'
            bflb_utils.printf("Default xtal is 32M")
        else:   
            config["dl_xtal"] = args.xtal 
            config["xtal_type"] = 'XTAL_' + args.xtal
        if not args.xtal:
            config["flash_clk_type"] = "72M"
            bflb_utils.printf("Default flash clock is 72M")
        else:      
            config["flash_clk_type"] = args.flashclk
        if not args.pllclk:
            config["pll_clk"] = "144M"
            bflb_utils.printf("Default pll clock is 144M")
        else:
            config["pll_clk"] = args.pllclk     
    elif chiptype == "bl60x":
        if not args.xtal: 
            config["dl_xtal"] = "38.4M"
            config["xtal_type"] = 'XTAL_38.4M'
        else:   
            config["dl_xtal"] = args.xtal 
            config["xtal_type"] = 'XTAL_' + args.xtal
            bflb_utils.printf("Default xtal is 38.4M")
        if not args.xtal:
            config["flash_clk_type"] = "80M"
        else:      
            config["flash_clk_type"] = args.flashclk
            bflb_utils.printf("Default flash clock is 80M")
        if not args.pllclk:
            config["pll_clk"] = "160M"
        else:
            config["pll_clk"] = args.pllclk
            bflb_utils.printf("Default pll clock is 160M")
    else:
        bflb_utils.printf("Chip type is not in bl60x/bl602/bl702")
        sys.exit(1)
        
    if config["dl_device"] == "jlink" and args.baudrate > 12000:
        config["dl_jlinkspeed"] = "12000"
                
    if args.erase:
        config["dl_chiperase"] = "True"
    else:
        config["dl_chiperase"] = "False"
    return config
    

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
    firmware_default = os.path.join(app_path, "img/project.bin")
    parser = argparse.ArgumentParser(description='bflb mcu tool')
    parser.add_argument('--chipname', required=True, help='chip name')
    parser.add_argument("--interface", dest="interface", default="uart", help="interface to use") 
    parser.add_argument("--port", dest="port", default=port, help="serial port to use")
    parser.add_argument("--baudrate", dest="baudrate", default=115200, type=int, help="the speed at which to communicate")
    parser.add_argument("--xtal", dest="xtal", help="xtal type")
    parser.add_argument("--flashclk", dest="flashclk", help="flash clock")
    parser.add_argument("--pllclk", dest="pllclk", help="pll clock")
    parser.add_argument("--firmware", dest="firmware", default=firmware_default, help="image to write") 
    parser.add_argument("--addr", dest="addr", default="2000", help="address to write") 
    parser.add_argument("--dts", dest="dts", help="device tree")
    parser.add_argument("--build", dest="build", action="store_true", help="build image")
    parser.add_argument("--erase", dest="erase", action="store_true", help="chip erase") 
    args = parser.parse_args()
    bflb_utils.printf("==================================================")
    bflb_utils.printf("Chip name is %s" % args.chipname)  
    if not args.port:
        bflb_utils.printf("Serial port is not found")
    else:
        bflb_utils.printf("Serial port is " + str(port)) 
    bflb_utils.printf("Baudrate is " + str(args.baudrate)) 
    bflb_utils.printf("Firmware is " + args.firmware)
    config = get_value(args)      
    obj_mcu = BflbMcuTool(args.chipname, chip_dict.get(args.chipname, "unkown chip type"))
    bflb_utils.printf("==================================================")
    try:
        obj_mcu.create_img(args.chipname, chip_dict[args.chipname], config)
        if args.build:
            obj_mcu.bind_img(config)
            f_org = os.path.join(app_path, args.chipname, "img_create_mcu", "whole_img.bin")
            f = "firmware.bin"
            shutil.copy(f_org, f)
        else:
            obj_mcu.program_img_thread(config)
    except Exception as e:
        error = str(e)
        bflb_utils.printf(error)
        traceback.print_exc(limit=5, file=sys.stdout)
    
if __name__ == '__main__':
    run()
    
    