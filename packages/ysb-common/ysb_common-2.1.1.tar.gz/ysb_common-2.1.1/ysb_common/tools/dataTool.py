

class DataTool():
    # 印花税新报表数据格式装换 add by zlf
    @staticmethod
    def yhs_format(sdata):
        fdata = {}
        v = '1'
        for obj in sdata:
            for key in obj:
                new_key = key + "_" + v
                fdata[new_key] = obj[key]
            v = str(int(v) + 1)
        print("格式转换完成")
        return fdata

    # 新报表数据格式转换 add by zlf
    @staticmethod
    def line_format(sdata):
        fdata = {}
        for i, ii in sdata.items():
            for key, val in ii.items():
                new_key = key + "_" + i
                fdata[new_key] = val
        print("格式转换完成")
        return fdata
        # 新报表铺数方法 add by zlf

    @staticmethod
    def ybnsr_set_value(browser, sdata, mapping):
        fdata = DataTool.line_format(sdata)
        for key in mapping:
            if key in fdata.keys():
                id = mapping[key]
                value = str(fdata[key])
                SeleniumTool.ybnsr_set_value_by_js(browser, id, value)
            print("填充完成")