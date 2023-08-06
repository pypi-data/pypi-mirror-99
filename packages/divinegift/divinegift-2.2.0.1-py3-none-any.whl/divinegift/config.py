from divinegift import main
from divinegift import logger
from divinegift import cipher
#########################################################################
import sys
import os
from datetime import datetime
from copy import deepcopy

class EmptyConfig(Exception):
    pass


class Settings:
    parse_settings_cnt = 0
    def __init__(self):
        self.settings = {}
        self.settings_encrypted = {}
        self.cipher_key = None
        self.passwords_cnt = 0

    def get_settings(self, param=None, default=None):
        if param:
            return self.settings.get(param, default)
        return self.settings

    def set_settings(self, json_str: object):
        self.settings = deepcopy(json_str)
        self.decrypt_passwords()
        self.settings_encrypted = deepcopy(json_str)

    def decrypt_passwords(self):
        logger.log_debug('Try to decrypt all passwords')
        for key in self.settings.keys():
            try:
                for subkey in self.settings.get(key).keys():
                    try:
                        self.decrypt_password(key, subkey)
                        logger.log_debug(f'Password for {key}[{subkey}] decrypted')
                        self.passwords_cnt += 1
                    except:
                        pass
            except:
                pass

    def parse_settings(self, file_: str = './settings.ini', encoding: str = 'utf-8',
                       log_changes: bool = True, use_yaml=True, ignore_parse_cnt=False):
        """
        Parse settings from file_
        :param file_: Filename with settings
        :param encoding: Encoding
        :return: None
        """
        if not ignore_parse_cnt:
            self.__class__.parse_settings_cnt += 1
            if self.__class__.parse_settings_cnt > 2:
                raise EmptyConfig('Settings not parsed. Is there any data?')
        
        if use_yaml:
            c = main.Yaml(file_, encoding=encoding)
        else:
            c = main.Json(file_, encoding=encoding)

        json_data = c.parse()

        if log_changes and json_data:
            dict_c = main.dict_compare(self.settings_encrypted, json_data)
            added, removed, modified, same = dict_c.values()
            if len(added) > 0:
                for r in list(added):
                    logger.log_warning(f'Added {r}: {json_data.get(r)}')
            if len(removed) > 0:
                for r in list(removed):
                    logger.log_warning(f'Removed {r}: {self.settings_encrypted.get(r)}')
            if len(modified) > 0:
                for r in list(modified):
                    logger.log_warning(f'Modified {r}: {modified.get(r)[0]} -> {modified.get(r)[1]}')
        elif not json_data:
            try:
                # self.convert_config(file_, file_, encoding=encoding, use_yaml=use_yaml)
                self.parse_settings(file_, encoding, not use_yaml)
            except EmptyConfig as ms:
                logger.log_err(ms)
                sys.exit(-1)
            except Exception as ex:
                raise Exception('Settings not parsed. Is there any data 2?')

        self.set_settings(json_data)

    def initialize_cipher(self, ck_fname: str = 'key.ck'):
        self.cipher_key = cipher.get_key()
        cipher.write_key(ck_fname, self.cipher_key)

    def encrypt_password(self, conn_name: str, pass_field: str ='db_pass', ck_fname: str = 'key.ck'):
        if not self.cipher_key:
            self.cipher_key = cipher.read_key(ck_fname)
            if not self.cipher_key:
                self.initialize_cipher()
        cipher_ = cipher.get_cipher(self.cipher_key)
        self.settings[conn_name][pass_field] = cipher.encrypt_str(self.settings[conn_name][pass_field], cipher_)

    def decrypt_password(self, conn_name: str, pass_field: str ='db_pass', ck_fname: str = 'key.ck'):
        if not self.cipher_key:
            self.cipher_key = cipher.read_key(ck_fname)
        cipher_ = cipher.get_cipher(self.cipher_key)
        self.settings[conn_name][pass_field] = cipher.decrypt_str(self.settings[conn_name][pass_field], cipher_)

    def encode_password(self, conn_name: str, pass_field: str ='db_pass'):
        settings = self.get_settings().copy()
        settings[conn_name][pass_field] = cipher.encode_password(settings[conn_name][pass_field])
        self.set_settings(settings)

    def decode_password(self, conn_name: str, pass_field: str ='db_pass'):
        settings = self.get_settings().copy()
        settings[conn_name][pass_field] = cipher.decode_password(settings[conn_name][pass_field])
        self.set_settings(settings)

    def save_settings(self, file_: str = './settings.ini', encoding='utf-8', use_yaml=True):
        if use_yaml:
            c = main.Yaml(file_, encoding=encoding)
        else:
            c = main.Json(file_, encoding=encoding)
        c.set_data(self.get_settings())
        c.create()

    @staticmethod
    def convert_config(file_from: str = './settings.ini', file_to: str = './settings.ini',
                       encoding='utf-8', use_yaml=True):
        if use_yaml:
            j = main.Json(file_from, encoding=encoding)
            y = main.Yaml(file_to, encoding=encoding)
            j.parse()
            y.set_data(j.get_data())
            y.create()
        else:
            y = main.Yaml(file_from, encoding=encoding)
            j = main.Json(file_to, encoding=encoding)
            y.parse()
            j.set_data(y.get_data())
            j.create()

    @staticmethod
    def get_version(fname=None):
        if not fname:
            fname = sys.argv[0]
        filename = main.get_list_files(os.path.dirname(fname), filter=os.path.basename(fname), add_path=True)[-1]
        version = datetime.fromtimestamp(os.path.getmtime(filename))
        return datetime.strftime(version, '%y%m%d')


if __name__ == '__main__':
    pass
