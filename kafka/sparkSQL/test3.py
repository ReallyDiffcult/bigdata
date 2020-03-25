from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession,Row
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

def get_spark(master="yarn", memory="1g", local_dir="/tmp", app_name="preporcess", queue="default", engine_id="asdf"):

    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL basic example") \
        .config("spark.some.config.option", "some-value") \
        .master("local[*]") \
        .getOrCreate()
    return spark
def get_sc():
    conf = SparkConf().setAppName("miniProject").setMaster("local[2]")
    sc = SparkContext.getOrCreate(conf)
    return sc
def split_(dict_count):
    # dict_count = {u'www.xmsyj.moa.gov.cn': 1, u'www.xmsyj.moa.gov.cn/jcyj': 1}
    path_list = []
    for key in dict_count.keys():
        path_list.append((key,dict_count[key]))
    return path_list
def remove_port(url):
    return url.split(":")[0]
def remove_port_main():
    spark = get_spark()
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    sc = get_sc()
    test_rdd = sc.parallelize([{u'www.xmsyj.moa.gov.cn': 1, u'www.xmsyj.moa.gov.cn/jcyj': 1},
                               {u'www.yyj.moa.gov.cn': 1, u'www.yyj.moa.gov.cn/zcjd': 1}])
    # print(test_rdd.collect())
    # print(test_rdd.flatMap(lambda x: split_(x)).collect())
    gov_port_list = [["video.mwr.gov.cn:8030"], ["www.nqs.gov.cn:81"], ["xxgk.zjzs.spb.gov.cn:80"]]
    # gov_port_rdd = sc.parallelize(gov_port_list)
    # print(gov_port_rdd.collect())
    gov_port_df = spark.createDataFrame(gov_port_list, ["Host"])
    # gov_port_df.show(3,False)
    # gov_port_df.show()
    remove_port_udf = udf(remove_port, StringType())
    remove_port_df = gov_port_df.select(remove_port_udf(gov_port_df.Host)).withColumnRenamed("remove_port(Host)",
                                                                                             "Host")
    # remove_port_df.show()
    gov_port_merger = gov_port_df.unionAll(remove_port_df)
    # gov_port_merger.show()
    gov_port_merger.select(remove_port_udf(gov_port_merger.Host)).show(6, False)
    spark.stop()
def get_rdd():
    spark = get_spark()
    sc = get_sc()
    return  sc.parallelize([{'wsdj.saic.gov.cn': {'saicreg': {'register': {'verifycodesend': {}}}}},{'wsdj.saic.gov.cn': {'saicreg': {'register': {'verifycodesend': {}}}}}])
    # print(sc.collect())
def convert_dict(dicts={}):
    dicts = {'wsdj.saic.gov.cn': {'saicreg': {'register': {'verifycodesend': {}}}}}
    keys = list(dicts.keys())
    key = keys[0]
    return (key,str(dicts[key]))
def save_main():
    testRDD = get_rdd().map(lambda x: convert_dict(x))
    Path = Row("gov_url", "gov_tree")
    ov_rdd = testRDD.map(lambda r: Path(*r))
    # print(ov_rdd.collect())
    spark = get_spark()
    df1 = spark.createDataFrame(ov_rdd)
    df1.show()
    df1.select("*").write.mode("overwrite").json("C:/Users/yangkun/Desktop/file")
def read_file():
    spark = get_spark()
    df = spark.read.option("mode","DROPMALFORMED").json('C:/Users/yangkun/Desktop/file')
    return df
def get_path_tup(path_tup = ()):
    gov_url = path_tup[0]
    path_list = path_tup[1]
    dir_tup_list = []
    for i in range(len(path_list)):
        paths = path_list[i]
        dir = ""
        for j in range(len(paths)):
            path = paths[j]
            dir = dir + "/"+path if dir != "" else dir + path
            dir_tup_list.append((dir,1))
    return dir_tup_list
def get_path_tup_main():
    path_tup = ('www.csh.moe.gov.cn',
  [['moetc', 'images', 'left_bg1.jpg'],
   ['moetc', 'images', 'cog_edit.png'],
   ['moetc', 'images', 'logo_bg_left.jpg'],
   ['moetc', 'images', 'ftp-alt-2.png'],
   ['moetc', 'images', 'anniu_left.png'],
   ['moetc', 'login', 'loginaction!leftmenu.action']])
    print(get_path_tup(path_tup=path_tup))
if __name__ == '__main__':
    # get_path_tup_main()
    # print(testRDD.collect())
    # print(convert_dict({}))
    # df = read_file()
    # df.select("gov_tree").show(10,False)
    print(["1","s"].reverse())
    print("a".endswith("b"))