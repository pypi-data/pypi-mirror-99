class Constant:
    # 纳税人信息字典表
    nsrxx_dict = {'KYSLRQ': 'slrq',  # 开业设立日期
                  'DJXH': 'djxh',  # 登记序号
                  'YXBZ': 'yxbz',  # 有效标志
                  'SHXYDM': 'shxydm',  # 社会信用代码
                  'ZGSWJ_DM': 'zgswjDm',  # 主管税务局代码
                  'ZGSWJ_MC': 'zgswjMc',  # 主管税务局名称
                  'ZGSWSKFJ_DM': 'zgswskfjDm',  # 主管税务所（科、分局）代码
                  'SSGLY_DM': 'ssglyDm',  # 税收管理员代码
                  'FJMQYBZ': 'fjmqybz',  # 非居民企业标志
                  'SWDJBLBZ': 'swdjblbz',  # 税务登记补录标志
                  'SJTB_SJ': 'sjtbSj',  # 数据同步时间
                  'NSRBM': '',  # 纳税人编号
                  'GDSLX_DM': 'gdslxDm',  # 国地税类型代码
                  'SSDABH': 'ssdabh',  # 税收档案编号
                  'NSRSBH': 'nsrsbh',  # 纳税人识别号
                  'NSRMC': 'nsrmc',  # 纳税人名称
                  'KZZTDJLX_DM': 'kzztdjlxDm',  # 课征主体登记类型代码
                  'DJZCLX_DM': 'djzclxDm',  # 登记注册类型代码
                  'FDDBRXM': 'fddbrxm',  # 法定代表人姓名
                  'FDDBRSFZJLX_DM': 'fddbrsfzjlxDm',  # 法定代表人身份证件类型代码
                  'SCJYDZ': 'scjydz',  # 生产经营地址
                  'FDDBRSFZJHM': 'fddbrsfzjhm',  # 法定代表人身份证号码
                  'SCJYDZXZQHSZ_DM': 'scjydzxzqhszDm',  # 生产经营地址行政区划数字代码
                  'NSRZT_DM': 'nsrztDm',  # 纳税人状态代码
                  'HY_DM': 'hyDm',  # 行业代码
                  'ZCDZ': 'zcdz',  # 注册地址
                  'ZCDZXZQHSZ_DM': 'zcdzxzqhszDm',  # 注册地址行政区划数字代码
                  'JDXZ_DM': 'jdxzDm',  # 街道乡镇代码
                  'DWLSGX_DM': 'dwlsgxDm',  # 单位隶属关系代码
                  'GDGHLX_DM': 'gdghlxDm',  # 国地管户类型代码
                  'DJJG_DM': 'djjgDm',  # 登记机关代码
                  'DJRQ': 'djrq',  # 登记日期
                  'ZZJG_DM': 'zzjgDm',  # 组织机构代码
                  'KQCCSZTDJBZ': 'kqccsztdjbz',  # 跨区财产税主体登记标志
                  'LRR_DM': 'lrrDm',  # 录入人代码
                  'LRRQ': 'lrrq',  # 录入日期
                  'XGR_DM': 'xgrDm',  # 修改人代码
                  'XGRQ': 'xgrq',  # 修改日期
                  'SJGSDQ': 'sjgsdq',  # 数据归属地区
                  'HJSZD': 'hjszd',  # 户籍所在地
                  'JYFW': 'jyfw',  # 经营范围
                  'ZCDLXDH': 'zcdlxdh',  # 注册地联系电话
                  'ZCDYZBM': 'zcdyzbm',  # 注册地邮政编码
                  'SCJYDLXDH': 'scjydlxdh',  # 生产经营地联系电话
                  'SCJYDYZBM': 'scjydyzbm',  # 生产经营地邮政编码
                  'HSFS_DM': 'hsfsDm',  # 核算方式代码
                  'CYRS': 'cyrs',  # 从业人数
                  'WJCYRS': 'wjcyrs',  # 外籍从业人数
                  'HHRS': 'hhrs',  # 合伙人数
                  'GGRS': 'ggrs',  # 雇工人数
                  'GDGRS': 'gdgrs',  # 固定工人数
                  'ZZJGLX_DM': 'zzjglxDm',  # 组织机构类型代码
                  'KJZDZZ_DM': 'kjzdzzDm',  # 会计制度（准则）代码
                  'WZ': 'wz',  # 网址
                  # 'SWDLRLXDH': 'swdlrlxdh',  # 税务代理人联系电话
                  'SWDLRDZXX': 'swdlrdzxx',  # 税务代理人电子信箱
                  'ZCZB': 'zczb',  # 注册资本
                  'TZZE': 'tzze',  # 投资总额
                  'ZRRTZBL': 'zrrtzbl',  # 自然人投资比例
                  'WZTZBL': 'wztzbl',  # 外资投资比例
                  'GYTZBL': 'gytzbl',  # 国有投资比例
                  'GYKGLX_DM': 'gykglxDm',  # 国有控股类型代码
                  'ZFJGLX_DM': 'zfjglxDm',  # 总分机构类型代码
                  'BZFS_DM': 'bzfsDm',  # 办证方式代码
                  'FDDBRGDDH': 'fddbrgddh',  # 法定代表人固定电话
                  'FDDBRYDDH': 'fddbryddh',  # 法定代表人移动电话
                  'FDDBRDZXX': 'fddbrdzxx',  # 法定代表人电子信箱
                  'CWFZRXM': 'cwfzrxm',  # 财务负责人姓名
                  'CWFZRSFZJZL_DM': 'cwfzrsfzjzlDm',  # 财务负责人身份证件种类代码
                  'CWFZRSFZJHM': 'cwfzrsfzjhm',  # 财务负责人身份证件号码
                  'CWFZRGDDH': 'cwfzrgddh',  # 财务负责人固定电话
                  'CWFZRYDDH': 'cwfzryddh',  # 财务负责人移动电话
                  'CWFZRDZXX': 'cwfzrdzxx',  # 财务负责人电子信箱
                  'BSRXM': 'bsrxm',  # 办税人姓名
                  'BSRSFZJZL_DM': 'bsrsfzjzlDm',  # 办税人身份证件种类代码
                  'BSRSFZJHM': 'bsrsfzjhm',  # 办税人身份证件号码
                  'BSRGDDH': 'bsrgddh',  # 办税人固定电话
                  'BSRYDDH': 'bsryddh',  # 办税人移动电话
                  'BSRDZXX': 'bsrdzxx',  # 办税人电子信箱
                  'LSSWDJYXQQ': 'lsswdjyxqq',  # 临时税务登记有效期起
                  'LSSWDJYXQZ': 'lsswdjyxqz',  # 临时税务登记有效期止
                  'SWDLRNSRSBH': 'swdlrnsrsbh',  # 税务代理人纳税人识别号
                  'SWDLRMC': 'swdlrmc',  # 税务代理人名称
                  'QYGLCJBH': '',  # 企业管理层级编号
                  'QYSSJT_DM': '',  # 企业所属集团代码
                  'NSRYWMC': '',  # 纳税人英文名称
                  'YWZCDZ': '',  # 英文注册地址
                  'WHSYJSFJFXXDJBZ': 'whsyjsfjfxxdjbz',  # 文化事业建设费缴费信息登记标志
                  'ZZSJYLB': 'zzsjylb',  # 增值税经营类别
                  'YHSJNFS_DM': 'yhsjnfsDm',  # 印花税缴纳方式代码
                  'ZSXMCXBZ_DM': 'zsxmcxbzDm',  # 征收项目城乡标志代码
                  'ZZSQYLX_DM': 'zzsqylxDm',  # 增值税企业类型代码
                  'GJHDQSZ_DM': 'gjhdqszDm',  # 国家或地区数字代码
                  'YGZNSRLX_DM': 'ygznsrlxDm'  # 营改增纳税人类型代码
                  }
    # 纳税人信息表含有默认值的字段
    nsrxx_default_dict = {'YXBZ': 'Y',
                          'KZZTDJLX_DM': '1000',
                          'FDDBRSFZJLX_DM': '201',
                          'NSRZT_DM': '03',
                          'CWFZRSFZJZL_DM': '201',
                          'BSRSFZJZL_DM': '201'}

    # 纳税人存款账户账号信息字典表
    nsrck_dict = {
        'BGRQ': 'bgrq',  # 变更日期
        'BZ': 'bz',  # 备注
        'CKTSZHBZ': 'cktszhbz',  # 出口退税账户标志
        'CKZHUUID': 'ckzhuuid',  # 存款账号uuid
        'DJKSKZHBZ': 'djkskzhbz',  # 待缴库税款账户标志
        'DJXH': 'djxh',  # 登记序号
        'FFRQ': 'ffrq',  # 发放日期
        'KHRQ': 'khrq',  # 开户日期
        'LCSLID': 'lcslid',  # 流程实例id
        'LRRQ': 'lrrq',  # 录入日期
        'SBBM': 'sbbm',  # 社保编码
        'SBDJXH': 'sbdjxh',  # 社保登记序号
        'SBFZHBZ': 'sbfzhbz',  # 社保费账户标志
        'SBJBJG': 'sbjbjg',  # 社保经办机构
        'SJGSDQ': 'sjgsdq',  # 数据归属地区
        'SXJFZHBZ': 'sxjfzhbz',  # 首选缴费账户标志
        'SXJSZHBZ': 'sxjszhbz',  # 首选缴税账户标志
        'TFZHBZ': 'tfzhbz',  # 退费账户标志
        'TSZHBZ': 'tszhbz',  # 退税账户标志
        'XGRQ': 'xgrq',  # 修改日期
        'YHKHDJZH': 'yhkhdjzh',  # 银行开户登记证号
        'YHZH': 'yhzh',  # 银行账号
        'YXBZ': 'yxbz',  # 有效标志
        'YXQQ': 'yxqq',  # 有效期起
        'YXQZ': 'yxqz',  # 有效期止
        'ZHMC': 'zhmc',  # 账户名称
        'ZXRQ': 'zxrq',  # 注销日期
        'KHYHHH': 'yhzh',  # 开户行行号
        'QSYHHH': '',  # 清算行行号
        'YHZHXZ_DM': 'yhzhxzDm',  # 银行账户性质代码
        'XZQHSZ_DM': 'xzqhszDm',  # 行政区划数字代码
        'YHHB_DM': 'yhhbDm',  # 银行行别代码
        'HBSZ_DM': 'hbszDm',  # 货币数字代码
        'YHYYWD_DM': 'yhyywdDm',  # 银行营业网点代码
        'LRR_DM': 'lrrDm',  # 录入人代码
        'XGR_DM': 'xgrDm',  # 修改人代码
        'SJTB_SJ': 'sjtbSj',  # 数据同步时间
    }
    # 纳税人存款账户账号信息含有默认的字段
    nsrck_default_dict = {'YXBZ': 'Y'}

    # 汇总纳税企业信息备案表
    hznsqyxxbab_dict = {
        'HZNSUUID': 'hznsuuid',  # 汇总纳税UUID
        'DJXH': 'djxh',  # 登记序号
        'ZFJGLX_DM': 'zfjglxDm',  # 总分机构类型代码
        'YXQQ': 'yxqq',  # 有效期起
        'YXQZ': 'yxqz',  # 有效期止
        'FZJGCJ_DM': 'fzjgcjDm',  # 分支机构层级代码
        'ZFBZ_1': 'zfbz1',  # 作废标志
        'FZJGJXFPBZ': 'fzjgjxfpbz',  # 分支机构继续分配标志
        'JDJNBS': 'jdjnbs',  # 就地缴纳标识
        'HJQYLX_DM': 'hjqylxDm',  # 汇缴企业类型代码
        'YJDYJYSKM_DM': 'yjdyjyskmDm',  # 月（季）度预缴预算科目
        'YJDYJYSJC_DM': 'yjdyjysjcDm',  # 月（季）度预缴预算级次
        'NDHSQJYSKM_DM': 'ndhsqjyskmDm',  # 年度汇算清缴预算科目
        'CYNDHQJBZ': 'cyndhqjbz',  # 参与年度汇算清缴标识
        'NDHSQJYSJC_DM': 'ndhsqjysjcDm',  # 年度汇算清缴预算级次
        'YJDYJYSFPBL_DM': 'yjdyjysfpblDm',  # 月（季）度预缴预算分配比例代码
        'NDHSQJYSFPBL_DM': 'ndhsqjysfpblDm',  # 年度汇算清缴预算分配比例代码
    }
    # 汇总纳税企业信息备案表默认字段
    hznsqyxxbab_default_dict = {}

    # 财务会计制度及核算软件备案报告书信息字典表
    cwkjzdjhsrjbabgs_dict = {
        'DJXH': 'djxh',  # 登记序号
        'KCYQZYQYKFZCZJFF_DM': 'kcyqzyqykfzczjffDm',  # 开采油（气）资源企业开发资产折旧方法代码
        'CBZRJG': 'cbzrjg',  # 催报责任机关
        'QYCWZD_DM': 'qycwzdDm',  # 企业财务制度代码
        'CWZDBZ': 'cwzdbz',  # 财务制度备注
        'CWKJZDBAUUID': 'cwkjzdbauuid',  # 财务会计制度备案UUID
        'CWKJZDBZ': 'cwkjzdbz',  # 财务会计制度备注
        'DZYHPTXFF_DM': 'dzyhptxffDm',  # 低值易耗品摊销方法代码
        'DZYHPTXFFBZ': 'dzyhptxffbz',  # 低值易耗品摊销方法备注
        'ZJFFBZ': 'zjffbz',  # 折旧方法备注
        'CBHSFFBZ': 'cbhsffbz',  # 成本核算方法备注
        'KJHSRJMC': 'kjhsrjmc',  # 会计核算软件名称
        'KJHSRJBZ': 'kjhsrjbz',  # 会计核算软件备注
        'KJHSRJBBH': 'kjhsrjbbh',  # 会计核算软件版本号
        'KJHSRJQYSJ': 'kjhsrjqysj',  # 会计核算软件启用时间
        'KJHSRJSJKLXMC': 'kjhsrjsjklxmc',  # 会计核算软件数据库类型名称
        'LRR_DM': '',  # 录入人代码
        'LRRQ': 'lrrq',  # 录入日期
        'XGR_DM': 'xgrDm',  # 修改人代码
        'XGRQ': 'xgrq',  # 修改日期
        'SJGSDQ': 'sjgsdq',  # 数据归属地区
        'CBHSFF_DM': 'cbhsffDm',  # 成本核算方法代码
        'ZJFSDL_DM': 'zjfsdlDm',  # 折旧方式大类代码
        'ZJFSXL_DM': 'zjfsxlDm',  # 折旧方式小类代码
        'LCSLID': 'lcslid',  # 流程实例ID
        'ZLBSXL_DM': 'zlbsxlDm',  # 资料报送小类代码
        'SJTB_SJ': '',  # 数据同步时间
        'YXQQ': 'yxqq',  # 有效期起
        'YXQZ': 'yxqz',  # 有效期止
        'KJZDZZ_DM': 'kjzdzzDm',  # 会计制度（准则）代码
        'KCYQZYQYKTZCTXFF_DM': 'kcyqzyqyktzctxffDm',  # 开采油（气）资源企业勘探支出摊销方法代码
        'KCYQZYQYKQQYZCZHFF_DM': 'kcyqzyqykqqyzczhffDm',  # 开采油（气）资源企业矿区权益支出折耗方法代码
    }
    # 财务会计制度及核算软件备案报告书信息含有默认的字段
    cwkjzdjhsrjbabgs_default_dict = {
        'YXBZ': 'Y',  # 有效标志
    }
    # 财务会计制度备案信息字典表
    cwkjzdba_dict = {
        'DJXH': 'djxh',  # 登记序号
        'KJBBBZ': 'kjbbbz',  # 会计报表备注
        'CWKJZDBAUUID': 'cwkjzdbauuid',  # 财务会计制度备案UUID
        'SJTB_SJ': '',  # 数据同步时间
        'KJBBBSQX_DM': 'kjbbbsqxDm',  # 会计报表报送期限代码
        'SJGSDQ': 'sjgsdq',  # 数据归属地区
        'XGRQ': 'xgrq',  # 修改日期
        'XGR_DM': 'xgrDm',  # 修改人代码
        'LRRQ': 'lrrq',  # 录入日期
        'LRR_DM': 'lrrDm',  # 录入人代码
        'BBBSQ_DM': 'bbbsqDm',  # 报表报送期代码
        'CWBBZL_DM': 'cwbbzlDm',  # 报表报送期代码
        'LCSLID': 'lcslid',  # 流程实例ID
        'KJBBMCUUID': 'kjbbmcuuid',  # 会计报表名称UUID
        'CWKJBBLX_DM': 'cwkjbblxDm',  # 财务会计报表类型代码
    }
    # 财务会计制度备案信息含有默认的字段
    cwkjzdba_default_dict = {
        'YXBZ': 'Y',  # 有效标志
    }
    # 发票票种核定信息字典表
    fp_pzhdxx_dict = {
        'DJXH': 'djxh',  # 登记序号
        'SJTB_SJ': '',  # 数据同步时间
        'WTDKBZ': '',  # 委托代开标志(否的话传N，是的话传Y)
        'LXKPLJXE': '',  # 离线开票累计限额
        'LXKPSX': '',  # 离线开票时限
        'XGRQ': '',  # 修改日期
        'XGR_DM': '',  # 修改人代码
        'LRRQ': '',  # 录入日期
        'LRR_DM': '',  # 录入人代码
        'SWJG_DM': 'swjgDm',  # 税务机关代码
        'YXQZ': 'yxqz',  # 有效期止
        'YXQQ': 'yxqq',  # 有效期起
        'FPGPFS_DM': '',  # 发票购票方式代码
        'CPZGSL': 'cpzgsl',  # 持票最高数量
        'MCZGGPSL': 'mczggpsl',  # 每次最高购票数量
        'MYZGGPSL': 'myzggpsl',  # 每月最高购票数量
        'DFFPZGKPXE': 'dffpzgkpxe',  # 单份发票最高开票限额
        'DFFPZGKPXE_DM': 'dffpzgkpxeDm',  # 单份发票最高开票限额代码
        'SJGSDQ': '',  # 数据归属地区
        'HDQCUUID': '',  # 票种清册UUID
        'FPZL_DM': 'fpzlDm',  # 发票种类代码(可传名称)
    }
    fp_pzhdxx_default_dict = {
        'YXBZ': 'Y',  # 有效标志
    }
    # 纳税人资格信息结果字典表
    nsrzgxx_jgb_dict = {
        'DJXH': 'djxh',  # 登记序号
        'SJTB_SJ': '',  # 数据同步时间
        'RDPZUUID': 'rdpzuuid',  # 认定凭证UUID
        'LCSLID': 'lcslid',  # 流程实例ID
        'NSRZGLX_DM': 'nsrzglxDm',  # 纳税人资格类型代码(可传名称)
        'YXQQ': 'yxqq',  # 有效期起
        'YXQZ': 'yxqz',  # 有效期止
        'SJZZRQ': 'sjzzrq',  # 数据中止日期
        'QXBZ': 'qxbz',  # 取消标志
        'WSZG': 'wszg',  # 文书字轨
        'ZFBZ_1': 'zfbz1',  # 作废标志
        'ZFR_DM': '',  # 作废人代码
        'ZFRQ_1': '',  # 作废日期
        'LRR_DM': 'lrrDm',  # 录入人代码
        'LRRQ': 'lrrq',  # 录入日期
        'XGR_DM': 'xgrDm',  # 修改人代码
        'XGRQ': 'xgrq',  # 修改日期
        'SJGSDQ': 'sjgsdq',  # 数据归属地区
    }
    # 税（费）种认定信息字典表
    sfzrdxxb_dict = {
        'DJXH': 'djxh',  # 登记序号
        'SJTB_SJ': '',  # 数据同步时间
        'GFJBJG_DM': '',  # 规费经办机构代码
        'ZSXMCXBZ_DM': '',  # 征收项目城乡标志代码
        'JFJC_DM': '',  # 缴费级次
        'RDPZUUID': '',  # 认定凭证UUID
        'ZFSBZ': 'zfsbz',  # 主附税标志||0：主税，1：附税，2：增值税附税，3：消费税附税 （后期需要做進一步的判斷）
        'RDZSUUID': '',  # 主税uuid
        'ZSXM_DM': 'zsxmMc',  # 征收项目代码(可传名称)
        'ZSPM_DM': 'zspmMc',  # 征收品目代码(可传名称)
        'ZSZM_DM': '',  # 征收子目代码
        'RDYXQQ': 'zsxmyxqQ',  # 认定有效期起
        'RDYXQZ': 'zsxmyxqZ',  # 认定有效期止
        'HY_DM': 'hymc',  # 行业代码(可传名称)
        'SBQX_DM': 'sbqx',  # 申报期限代码 （后期需要进行判断处理）
        'NSQX_DM': 'sbqy',  # 纳税期限代码  （后期需要进行判断处理）
        'SLHDWSE': 'slhdwse',  # 税率或单位税额
        'YSKM_DM': '',  # 预算科目代码
        'ZSL': 'zsl',  # 征收率
        'YSFPBL_DM': '',  # 预算分配比例代码
        'SKGK_DM': 'skgkDm',  # 收款国库代码
        'JKQX_DM': 'jkqxmc',  # 缴款期限代码  （后期需要进行判断处理）
        'ZSDLFS_DM': 'zsdlfsmc',  # 征收代理方式代码 （后期需要进行判断处理）
        'ZGSWSKFJ_DM': '',  # 主管税务所（科、分局）代码
        'LRR_DM': '',  # 录入人代码
        'LRRQ': '',  # 录入日期
        'XGR_DM': '',  # 修改人代码
        'XGRQ': '',  # 修改日期
        'SJGSDQ': '',  # 数据归属地区
    }
    sfzrdxxb_default_dict = {
        'YXBZ': 'Y',  # 有效标志
    }
    # 定期定额(增值税)核定结果字典表
    dqdehd_jg_dict = {
        'DJXH': 'djxh',  # 登记序号
        'YWPZUUID': '',  # 业务凭证uuid
        'JYXM_DM': '',  # 经营项目代码
        'SJTB_SJ': '',  # 数据同步时间
        'SSKCS': '',  # 速算扣除数
        'SJGSDQ': '',  # 数据归属地区
        'XGRQ': '',  # 修改日期
        'XGR_DM': '',  # 修改人代码修改人代码
        'LRRQ': '',  # 录入日期
        'LRR_DM': '',  # 录入人代码
        'ZGSWSKFJ_DM': 'gsSwjgDm',  # 主管税务所（科、分局）代码
        'SJZXQZ': 'sjzxqz',  # 实际执行期止
        'HDZXQZ': 'hdqxz',  # 核定执行期止
        'HDZXQQ': 'hdqxq',  # 核定执行期起
        'HDSE': 'hdse',  # 核定税额
        'SL_1': 'sl',  # 税率
        'YNSJYE': 'ynssde',  # 应纳税经营额
        'ZSPM_DM': '',  # 征收品目代码(可传名称)
        'LCSLID': '',  # 流程实例ID
        'HDJGUUID': '',  # 核定结果UUID
        'ZFR_DM': '',  # 作废人代码
        'ZFRQ_1': '',  # 作废日期
        'ZFBZ_1': '',  # 作废标志
        'WDQZDBZ': '',  # 未达起征点标志
        'YNSE': 'hdse',  # 应纳税额
        'DEXM_DM': '',  # 定额项目代码
        'HY_DM': '',  # 行业代码(可传名称)
        'JSBZ_1': '',  # 计税标志
        'YSSDL': '',  # 应税所得率
        'JSYJ': '',  # 计税依据
        'ZXHDBZ': '',  # 最新核定标志0
    }
    dqdehd_jg_default_dict = {
        'ZSXM_DM': '10101',  # 征收项目代码(可传名称)
    }
    # 企业所得税核定结果字典表
    qysdshd_jg_dict = {
        'DJXH': 'djxh',  # 登记序号
        'HDQXQ': 'hdqxq',  # 核定期限起
        'HDQXZ': 'hdqxz',  # 核定期限止
        'SJZXQZ': 'sjzxqz',  # 实际执行期止
        'NHDYNSSDE': '',  # 年核定应纳税所得额
        'NHDSDSE': '',  # 年核定所得税额
        'YSSDL': '',  # 应税所得率
        'LRL': '',  # 利润率
        'QYSDSYJQX_DM': '',  # 企业所得税预缴期限代码
        'QYSDSYJFS_DM': '',  # 企业所得税预缴方式代码
        'ZGSWSKFJ_DM': 'gsSwjgDm',  # 主管税务所（科、分局）代码
        'SNSDSE': '',  # 上年所得税额
        'SNYCLXHLE': '',  # 上年原材料耗费量（额）
        'SNZSFS_DM': '',  # 上年征收方式代码
        'SNZGRS': '',  # 上年职工人数
        'SNZCZB': '',  # 上年注册资本
        'SX': '',  # 上限
        'SL_1': 'sl',  # 税率
        'XX': '',  # 下限
        'ZBSZQK': '',  # 账簿设置情况
        'ZSZM_DM': '',  # 征收子目代码
        'BQYNSSDEHYNSEYSQHDEBDQK': '',  # 本期应纳税所得额或应纳税额与上期核定额变动情况
        'SCJYFWBDQK': '',  # 生产经营范围变动情况
        'FJMQYHY_DM': '',  # 非居民企业行业代码
        'FJMQYYWMC': '',  # 非居民企业英文名称
        'SNCBFYE': '',  # 上年成本费用额
        'SNGDZCYZ': '',  # 上年固定资产原值
        'SNRLDLHFLE': '',  # 上年燃料（动力）耗费量（额）
        'SNSPXSLE': '',  # 上年商品销售量（额）
        'SNSRZE': '',  # 上年收入总额
    }
    qysdshd_jg_default_dict = {
        'ZSFS_DM': '400',  # 征收方式代码
    }
    # 三方协议等级信息字典表
    sfxy_dict = {
        'DJXH': 'djxh',  # 登记序号
        'KHYHHH': 'khyhhh',  # 开户行行号
        'JKZH': 'jkzh',  # 缴款帐号
        'JKZHMC': 'jkzhmc',  # 缴款账户名称
        'SFXYZT_DM': 'sfxyztDm',  # 三方协议状态代码
        'SFXYYZTG_RQ': '',  # 三方协议验证通过日期
        'XZQHSZ_DM': '',  # 行政区划数字代码
        'YHYYWDMC': 'yhyywdMc',  # 银行营业网点名称
        'YHYYWD_DM': '',  # 银行营业网点代码
        'NSRSBH': 'nsrsbh',  # 纳税人识别号
        'SJTB_SJ': '',  # 数据同步时间
        'PKBZ': 'pkbz',  # 批扣标志
        'SFXYYZXX': '',  # 三方协议验证信息
        'SJGSDQ': '',  # 数据归属地区
        'SFXYDJUUID': 'sfxydjuuid',  # 三方协议uuid
        'SKSSSWJG_DM': '',  # 税款所属税务机构代码
        'SFXYH': 'sfxyh',  # 三方协议号
        'YHHB_DM': 'yhhbDm',  # 银行行别代码
        'YHHBMC': '',  # 银行行别名称
        'QSYHHH': 'qsyhhh',  # 清算行行号
    }

    tm_data = ['fddbrsfzjhm', 'zcdlxdh', 'scjydlxdh', 'fddbrgddh', 'fddbryddh', 'cwfzrsfzjhm', 'cwfzrgddh', 'cwfzryddh',
               'bsrsfzjhm', 'bsrgddh', 'bsryddh', 'yhzh']


    BucketName_Ysb = "ysbpt"
    MAX_RETRY_TIME = 3
