wMachine - MyCrawel 文档
========
Very Disappointed...

分析执行流程及参数
--------
注意：所有流程涉及文件夹的部分必须手动建立相应文件夹
### 进入MyCrawel文件夹
### python MyCrawel2.py  [cookies.txt相对路径]  [uids.txt相对路径]  [数据类别字符串]
	功能：自动抓取列表中所有uid对应的所有微博并进行有效内容简易过滤并存档
	参数说明
		cookies.txt：存放手动登陆微博之后提取HTTP头的Cookie字段内容
		uids.txt：存放需要抓取的一类微博用户id，每个id一行，不要用用户名
		数据类别字符串：自定义的分类标签
	输出说明
		抓取数据为对应uid微博用户所有经过简易处理的微博内容，去除了大多数内容无关的元素，如html标签等
		抓取数据输出路径为“data/类别/”，文件名为“用户uid.txt”，文本类型可直接查看
### python CalcFreq.py  [数据类别字符串]
	功能：调用词库（测试默认为IT词库）对每个uid的数据进行分词并统计词频后进行序列化
	参数说明
	输出说明
		每个uid对应的原始抓取数据将被分词并统计词频后输出到“freqs/类别/”，文件名为“用户uid.seq”，作为序列化处理，使用python的cPickle可以反序列化读取
### python MergeFreq.py  [数据类别字符串]
	功能：合并所有单独的词频文件并输出到一个文件
	参数说明
	输出说明
		存放于“freqs/类别/”中的所有.seq文件被反序列化并合并成一个词典，存放在“freqs/”根路径中，命名为“类别.seq”
### python Filter.py  [数据类别字符串]  [提取维度数目]
	功能：对合并后的词频词典进行过滤，去除无关维度，并最后提取出词频最高的若干维度关键词
	参数说明
	输出说明
		存放于“freq/”根路径中的“类别.seq”被序列化读取后进行相关操作，最终结果序列化存储于“freq/”根路径中，命名为“类别_filtered.seq”，文件可以被反序列化查看
### python GenerateTrainSet.py  [来源数据类别字符串]  [特征维度定义文件相对路径]  [统一值，即LABEL值]
	功能：将过滤后并进行维度提取后的词频文件应用于来源类别下的所有单个词频文件，进行匹配后生成部分具有相同LABEL值的libsvm输入格式文档
	参数说明
		来源数据类别字符串：程序将访问“freqs/来源类别/”目录下所有CalcFilter.py生成的单个以“用户uid.seq”命名的文件作为输入处理
		特征维度定义文件相对路径：程序将访问“freqs/特征_filtered.seq”文件将其作为标准的维度提取模板
		LABEL值：指明从来源数据类别文件夹输入的所有数据的学习值是多少，建议显示加上正负符号
	输出说明
		程序将在“input_parts/特征/”路径生成命名为“特征_on_来源_part_LABEL.txt”的文件，表明以特征维度为标准提取来源数据中的对应维度词频并标记为LABEL值的文件
### python MergeTrainSet.py  [数据类别字符串]
	功能：将具有不同LABEL值的生成数据片段合成一份
	参数说明
		数据类别字符串
	输出说明
		程序将在”input_parts/类别/”路径中的所有文件简单地合并在一起，形成一个有效的libsvm输入文件，存放于“input_full/”路径，命名为“类别_input.txt”
### python TrainModel.py  [数据类别字符串]  [训练维度数目]
	功能：训练出指定类别维度的libsvm适用模型
	参数说明
		数据类别字符串
		训练维度数目：指明使用libsvm训练从维度1到指定维度的数目，即维度上界
	输出说明
		程序将在“models/”路径中生成“类别.model”的模型文件，可被libsvm加载执行预测
### python GenerateTestcase.py  [来源数据类别字符串]  [目标数据类别字符串]
	功能：根据来源数据，在目标维度空间上提取特征维度，生成测试输入数据
	参数说明
		来源数据类别字符串
		目标数据类别字符串：提供特征维度空间的类别，使用其_filtered.seq识别
	输出说明
		程序将在“testcases/”目录中生成“来源_on_目标_predict_0.txt”文件
		输出的LABEL默认均为0，暂时没有参数可以调整
### python SVMPredict.py  [模型名称（数据类别字符串）]  [测试数据名]  [预测点数目]
	功能：将制定测试数据应用于预测模型上进行预测判断并输出结果
	参数说明
		模型名称：即数据类别字符串，程序将在“models/”目录寻找相应模型并加载
		测试数据名：需要手动完全指定，省略后缀名，程序将在“testcases/”目录中寻找并加载
		预测点数目：指定测试数据中从第一个点开始将被预测的点的数目，即指定数目上界
	输出说明
		直接在屏幕输出带有最终预测值的一个列表的字符串化可读打印结果

执行示例
--------
进入MyCrawel文件夹
	cd MyCrawel/

使用根目录的cookies.txt抓取“uids/meishi.txt”中的所有uid的微博，结果存入“data/meishi/”目录中
	python MyCrawel2.py cookies.txt meishi.txt meishi

计算“data/meishi/”目录中每个数据文件的词频，将结果写入到“freqs/meishi/”目录中
	python CalcFreq.py meishi

将“freqs/meishi/”目录中的所有词频文件合并成一个文件并存放于“freqs/”目录中，命名为“meishi.seq”
	python MergeFreq.py meishi

将“freqs/meishi.seq”进行过滤，抽取其中前10000维的数据，生成“freqs/”目录中命名为“freqs/meishi_filtered.seq”文件
	python Filter.py meishi 10000

将“freqs/meishi/”中的所有数据计算其在由“freqs/meishi_filtered.seq”定义的维度上的值，并赋予其标签，存入“input_parts/meishi/”目录中，命名为“meishi_on_meishi_part_1.txt”
	python GenerateTrainSet.py meishi meishi 1

相同步骤完成一个叫caijing的类别，再次生成部分输入数据（省略前序代码），存入“input_parts/meishi/”目录，命名“caijing_on_meishi_part_-1.txt”
	python GenerateTrainSet.py caijing meishi -1

接着可以将两个文件合并，生成“input_full/”目录下的“类别_input.txt”文件
	python MergeTrainSet.py meishi

接着对meishi种类的合成的判定训练数据进行训练，“input_full/类别_input.txt”文件默认作为输入源，默认生成了“models/类别.model”文件
	python TrainModel.py meishi 10000

然后重复上述步骤准备好即将输入接受预测的数据，直到生成了_filtered.seq文件，运行以下脚本生成mates数据在meishi特征维度上的各点数值，得到脚本返回的生成文件名为“testcases/mates_on_meishi_predict_0.txt”文件，记住文件名
	python GenerateTestcase.py mates meishi

最后，进行预测，将mates（包含5个点）全部点在meishi的模型上进行预测，得到输出的预测值列表
	python SVMPredict.py mates meishi 5

