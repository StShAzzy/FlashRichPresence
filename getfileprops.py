import win32api

def get_file_properties(fname):
    prop_names = ('Comments', 'InternalName', 'ProductName',
                  'CompanyName', 'LegalCopyright', 'ProductVersion',
                  'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                  'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None, 'FileDescription': None}

    fixed_info = win32api.GetFileVersionInfo(fname, '\\')
    props['FixedFileInfo'] = fixed_info
    props['FileVersion'] = "%d.%d.%d.%d" % (fixed_info['FileVersionMS'] / 65536,
                                                fixed_info['FileVersionMS'] % 65536,
                                                fixed_info['FileVersionLS'] / 65536,
                                                fixed_info['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
    lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

    str_info = {}
    for propName in prop_names:
        str_info_path = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
        str_info[propName] = win32api.GetFileVersionInfo(fname, str_info_path)

    props['StringFileInfo'] = str_info
   # except:
   #     pass

    return props