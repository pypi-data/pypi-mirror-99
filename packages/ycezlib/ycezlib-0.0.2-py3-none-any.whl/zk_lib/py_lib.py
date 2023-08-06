import pandas as pd
import numpy as np
import re
import os
import glob

def process_index(k):
    lst=k.split("|")
    return tuple((lst[-1],"".join(lst[0:-1])))

def equal_df(df):
    # print(df.shape, len(df))
    for i in range(len(df)):
        pass

def astype_str_notna(df):
    '''
    传入参数：数据框里面一列  Series
    return：转换后的一列  Series
    '''
    t = []
    for i in df:
        if type(i) == float:
            if not np.isnan(i):
                i = str(int(i))
        if type(i) == int:
            i = str(i)

        t.append(i)
    return pd.Series(t)

import logging
import os
from logging.handlers import RotatingFileHandler #
import colorlog # 控制台日志输入颜色

log_colors_config = {
  'DEBUG': 'blue',
  'INFO': 'black',
  'WARNING': 'purple',
  'ERROR': 'red',
  'CRITICAL': 'red',
}

class Log:
    def __init__(self, logname='log.log'):
        self.logname = os.path.join(os.getcwd(), '%s' % logname)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
            log_colors=log_colors_config) # 日志输出格式
        self.info_formatter = colorlog.ColoredFormatter(
            '%(log_color)s[%(filename)s:%(lineno)d] [%(levelname)s]- %(message)s',log_colors=log_colors_config) # 日志输出格式

    def console(self, level, message):
    # 创建一个FileHandler，用于写到本地
        fh = logging.handlers.TimedRotatingFileHandler(self.logname, when='MIDNIGHT', interval=1, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.info_formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 这两行代码是为了避免日志输出重复问题
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        fh.close() # 关闭打开的文件

    def debug(self, message):
        self.console('debug', message)

    def info(self, message):
        self.console('info', message)

    def warning(self, message):
        self.console('warning', message)

    def error(self, message):
        self.console('error', message)

def export_dfs_to_xls(d,xls_file_dst,sht):
    d.to_excel(xls_file_dst, sheet_name=sht)

def find_total_row(df,str_xj="小计"):
    row=df.shape[0]
    row=max(-1 * row,-8)

    for i in range(-1,row,-1):
        if df.iloc[i, 0:-2].astype(str).str.contains(str_xj, na=False).any():
            return i
    return 0

def xls_auto_skip_rows(xls_file_src):
    dfs = pd.read_excel(xls_file_src, sheet_name=None, header=None, index_col=None, skiprows=None)
    # df_merge = pd.DataFrame(data=None, columns=["姓名"])
    df_merge = pd.DataFrame(data=None, columns=["姓名", "年级", "合计"])
    df_concat = pd.DataFrame(data=None, columns=[])
    df_tail_dict_drop= {}

    print("\n%s\n当前操作的工作簿为:%s\n%s" % ('-'*100,xls_file_src,'-'*100))
    for sht_name, df in dfs.items():
        # 仅仅读取 XXXX.XX格式的工作表
        if re.match(r"\d{4}\.[\dz]{1,2}", sht_name):
            # first_row = (df.count(axis=1) >= df.shape[1]).idxmax()                #查找列名所在行数的一种方法，处理10,11月份没有问题，9月份出现问题
            first_row = (df.count(axis=1) >= df.count(axis=1).max()).idxmax()  # 查找列名所在行数的另一种办法
            df.columns = df.loc[first_row]  # 更改当前df的列索引名称
            df.rename(columns=lambda x: str(x).strip("\r\n\t ."), inplace=True)  # 去掉列名首位的空白字符
            df = df.loc[first_row + 1:]
            df=df.apply(lambda x:x.str.strip("\r\n\t .") if x.name=="姓名" else x)    # 去掉列中的空白字符

            row_total=find_total_row(df)        #定位最后几行中,小计所在行
            if row_total < -1:
                row_tail_drop = row_total * -1 - 1          #准备删除小计行以下的所有行
                # lg.debug("has drop these last row ：{}".format(df.tail(row_tail_drop).index))
                df_tail_dict_drop[sht_name]=df.tail(row_tail_drop)          #将小计行以下的所有行保存到字典中以备查证
                df=df.drop(df.tail(row_tail_drop).index)
            else:
                row_tail_drop = 0

            #检查该列是否存在重复值，如果存在则进行输出。
            if df.duplicated("姓名", keep=False).any() == True:
                # print("\n%s: workboot:%10s ,found below duplicated rows !!!!!!!!!" % (xls_file_src,sht_name))
                lg.warning("\n{:^10}: workboot:{:^10} ,found below duplicated rows !!!!!!!!!".format(xls_file_src,sht_name))
                # 准备显示重复行内容
                flag_dup = df.loc[df.duplicated("姓名", keep=False)]
                lg.info(flag_dup)
                # print(flag_dup)
                #如果重复值含有空白单元格，则保留末尾的空白单元格，删除前面的重复空白单元格
                flag_dup_na = df.loc[df.duplicated("姓名", keep="last") & (pd.isnull(df["姓名"]))]
                if len(flag_dup_na)>0:
                    drop_list = flag_dup_na.index.tolist()
                    # print("has drop these index row ：" ,drop_list)
                    lg.debug("has drop these above row ：{}".format(drop_list))
                    df=df.drop(drop_list)

            df_tmp=df[["姓名", "年级", "合计"]]
            df_tmp=df_tmp.add_suffix('|'+ sht_name)
            # df_tmp.columns=df_tmp.columns.map(lambda x: str(x) +'|'+ sht_name if x!="姓名" else x)
            # tmp = (lambda x: str(x) + '|' + sht_name for x in df_tmp.columns if x.name!="姓名" else x)
            # print(df_tmp,df_tmp.columns)
            df_merge = pd.merge(df_merge, df[["姓名", "年级", "合计"]], how="outer", on="姓名",suffixes=("", "|" + sht_name))  # 以姓名作为公共列，对多个df数据集进行连接。
            df_concat = pd.concat([df_concat,df_tmp],axis=1,join="outer")  # 对两个数据集进行横向堆叠

            # print("workbook:<%10s>,df.shape:(%3d,%2d),auto skip %2d rows,"
            #       "df_merge：(%d,%d)"
            #       "df_concat：(%d,%d)" %
            #       (sht_name, df.shape[0], df.shape[1], first_row,df_merge.shape[0], df_merge.shape[1],df_concat.shape[0], df_concat.shape[1]))
            lg.info("workbook:{:^10},df.shape:({:>3d},{:>3d}),skip head-tail:({:>d},{:>d}),"
                  "df_merge：({},{}),"
                  "df_concat：({},{})".format(
                sht_name, df.shape[0], df.shape[1], first_row, row_tail_drop ,df_merge.shape[0], df_merge.shape[1], df_concat.shape[0],
                df_concat.shape[1]
                )
            )

        else:
            # print("workbook:<%10s> is ignored" % sht_name)
            lg.info("workbook:{:^10} is ignored".format(sht_name))

    df_merge.columns = df_merge.columns.map(lambda x: str(x).replace("合计","小计"))
    col_xj=df_merge.columns[df_merge.columns.str.find("小计")>-1]                                 #定位小计所在列
    df_merge.loc["pd_sum",col_xj]=df_merge.loc[pd.notnull(df_merge["姓名"]),col_xj].fillna(0).sum()       #对小计列进行垂直合计
    df_merge["合计"]=df_merge[col_xj].fillna(0).sum(axis=1)                                       #对每行进行水平合计
    df_merge = df_merge.drop([ "年级", "小计"],axis=1)
    # df_merge.columns=df_merge.columns.map(lambda x:process_index(x))

    # col_xm=df_concat.columns[df_concat.columns.str.find("姓名") > -1]
    # df_base=df_concat[col_xm]
    # df_base=df_concat.loc[:,col_xm]
    # print(df_concat.columns.str.find("姓名") > -1,df_base.shape,df_concat.shape)

    # df_base=df_concat["姓名"].fillna("")
    #对包含姓名的所有列进行比对，将比对结果追加到最后列
    # df_base=df_concat.filter(like="姓名").fillna("")
    df_base=df_concat.loc[:,df_concat.columns[df_concat.columns.str.find("姓名") > -1]].fillna("")
    df_base_pre=df_base.iloc[:, 0:-1]
    df_base_suf=df_base.iloc[:, 1:]
    df_base_suf.columns=df_base_pre.columns
    df_base_comp=df_base_pre.eq(df_base_suf)
    df_concat=pd.concat([df_concat,df_base_comp],axis=1)

    df_concat.columns = df_concat.columns.map(lambda x: str(x).replace("合计","小计"))
    # col_xj=df_concat.columns[df_concat.columns.str.find("小计")>-1]                                 #定位小计所在列
    # df_concat["合计"] = df_concat[col_xj].fillna(0).sum(axis=1)    # 对每行进行水平合计
    df_concat["合计"] = df_concat.filter(like="小计").fillna("").sum(axis=1)    # 对每行进行水平合计的第二种办法
    # df_concat.loc["", col_xj] = df_concat.loc[pd.notnull(df_concat["姓名"]), col_xj].fillna(0).sum()  # 对小计列进行垂直合计

    if len(df_tail_dict_drop)>0:
        lg.info("workbook {} has drop {} sheet tail data:".format(xls_file_src,len(df_tail_dict_drop)))
        for k,v in df_tail_dict_drop.items():
            lg.info("worksheet {:^10}\n{}".format(k,v))

    return df_merge,df_concat

def get_all_files_by_walk(path, pattern=".*.*"):
    file_list = []
    path = os.path.expanduser(path)
    for (dirname, subdir, subfile) in os.walk(path):
        # print('dirname is %s, subdir is %s, subfile is %s' % (dirname, subdir, subfile))
        for f in subfile:
            # print(os.path.join(dirname, f))
            if re.match(pattern, f):
                # print(os.path.join(dirname, f))
                file_list.append(os.path.join(dirname, f))
    return file_list

def get_all_files_by_glob(path, pattern="*.*"):
    file_list = []
    for f in glob.glob(path + '\\' + pattern):
        # print(os.path.join(path, f))
        # lg.debug(os.path.join(path, f))
        file_list.append(os.path.join(path, f))
    return file_list

def get_all_files_by_listdir(path, pattern="*.*",sub_mode=False):
    file_list = []
    files=os.listdir(path)
    for item in files:
        path_tmp=os.path.join(path,item)
        if os.path.isfile(path_tmp):
            if re.match(pattern,item,re.IGNORECASE):
                file_list.append(path_tmp)
        elif sub_mode and os.path.isdir(path_tmp):
            get_all_files_by_listdir(path_tmp)
    return file_list

def out_log(fl):
    import logging

    # 创建Logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建Handler
    # 终端Handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # 文件Handler
    fileHandler = logging.FileHandler(fl, mode='w', encoding='UTF-8')
    fileHandler.setLevel(logging.NOTSET)

    # Formatter
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 添加到Logger中
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    # 打印日志
    # logger.debug('debug 信息')
    # logger.info('info 信息')
    # logger.warning('warn 信息')
    # logger.error('error 信息')
    # logger.critical('critical 信息')
    # logger.debug('%s 是自定义信息' % '这些东西')
    return  logger

def print_me():
    print("%s\n        Hello,this is zk's lib for python.\n%s" %('-'*70 ,'-'*70))

if __name__=="__main__":
    lg=Log()
    lg.debug("\n{}\n        Hello,this is zk's lib for python.\n{}".format('-'*70 ,'-'*70))
else:
    lg = Log()

# list = get_all_files_by_glob(r"F:\ZK\jwc\绩效\源文件", "[gc][123z]_*.xls")
# with pd.ExcelWriter(r".\wage_dst.xls") as writer:
#     for f in list:
#         xls_auto_skip_rows(f, writer, f.split('\\')[-1][0:2])
#         pass
#     # xls_auto_skip_rows(r"F:\ZK\jwc\绩效\源文件\g3_2020.9-2021.1.xls",writer,"test")