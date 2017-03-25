import re


def clean_string(content):
    special = ['\n', '\'', '\"', '\\', '\t']
    if content:
        content = content.strip()
        for item in special:
            content = content.replace(item, " ")
        pattern = re.compile("\ +")
        return re.sub(pattern, " ", content)
    else:
        return None


def clean_school(school_name):
    if school_name:
        school_name = school_name.replace("-", " ")
        school_name = re.findall("[a-zA-z\ ]", school_name)
        school_name = "".join(school_name)
        return school_name
    else:
        return None


def clean_result(result):
    if "拒" in result or "rej" in result or "Rej" in result:
        return "Rejection"
    elif "AD" in result or "ad" in result:
        return "AD"
    elif "list" in result:
        return "Wait_list"
    elif "offer" in result or "Offer" in result:
        return "Offer"
    else:
        return None


def clean_degree(degree):
    degree = re.findall("[a-zA-Z]", degree)
    result = ("".join(degree)).lower()
    if "mar" in result:
        return "Master"
    elif "jd" in result or "llm" in result:
        return "JD/LLM"
    elif "msw" in result:
        return "Master"
    elif "mfa" in result:
        return "Master"
    elif "mba" in result:
        return "Master"
    elif "mph" in result:
        return "Master"
    elif "mpa" in result:
        return "Master"
    elif "ms" in result or "meng" in result or "master" in result:
        return "Master"
    elif "phd" in result:
        return "PhD"
    else:
        return "other"


def under_cate(under):
    eight_list = ["清华", "北大", "科大", "浙大", "浙江大学", "中国科学技术",
                  "中国科技大学", "上海交通", "北京大学", "复旦", "华科", "华中科技",
                  "中国人民大学", "人大", "北京航空航天", "北航", "北京理工大学", "北理",
                  "中国农业", "北京师范", "北师", "民族", "南开", "天津大学", "大连理工",
                  "东北大学", "吉林大学", "哈尔滨工业", "同济", "华东师范", "南京大学",
                  "南大", "华师", "东南", "厦门大学", "厦大", "山东大", "山大", "海洋",
                  "武汉大学", "武大", "湖南大学", "中南", "国防科学技术", "国防科技",
                  "中山大", "中大", "华南理工", "四川大学", "川大", "电子科技",
                  "重庆大学", "西安交通", "西交", "西北工业", "西北农林", "兰州大学"]

    abroad = ["College", "college", "UC", "美国", "US", "美本", "海外", "海本",
              "国外", "Uni", "uni", "港", "澳"]
    if under:
        if "非" in under or "其他" in under:
            return "other"
        for item in abroad:
            if item in under:
                return "Abroad"
        if "985" in under:
            return "985"
        for item in eight_list:
            if item in under:
                return "985"
        return "211"
        return "other"
    else:
        return "other"


def is_grad(grad):
    if grad:
        return True
    else:
        return False


def major_category(major):
    if "法" in major:
        return "Law"
    major = re.findall("[a-zA-Z\ ]", major)
    major = ("".join(major)).lower()
    if "llm" in major or "law" in major:
        return "Law"
    if "account" in major:
        return "Accounting"
    elif "fin" in major:
        return "MFE/FinMath"
    elif "math" in major:
        return "Math"
    elif "geo" in major:
        return "Geo"
    elif "phys" in major:
        return "Physics"
    elif "stat" in major:
        return "Stat"
    elif "electri" in major or (len(major)<5 and "ee" in major) or "ece" in major:
        return "EE"
    elif "envir" in major:
        return "Environment/EnvirEngi"
    elif "bio" in major or "bme" in major:
        return "Bio/BioEngi"
    elif "info" in major:
        return "Information"
    elif "material" in major or "mse" in major:
        return "Material"
    elif "edu" in major:
        return "Education"
    elif "chem" in major:
        return "Chem/ChemEngi"
    elif "art" in major and "earth" not in major:
        return "Art"
    elif "econ" in major:
        return "Econ"
    elif "health" in major:
        return "Health"
    elif "arc" in major and "research" not in major:
        return "Architecture"
    elif "lang" in major or "edu" in major or "stud" in major or "teach" in major:
        return "Teaching/Edu"
    elif "design" in major:
        return "Design"
    elif "phar" in major:
        return "Pharm"
    elif "psych" in major:
        return "Psych"
    elif "public" in major:
        return "Public"
    elif "journ" in major:
        return "Journalism"
    elif "urban" in major:
        return "Urban"
    elif "advert" in major:
        return "Advertise"
    elif "social" in major or "sociol" in major:
        return "Social"
    elif "commu" in major:
        return "Communication"
    elif "tesol" in major:
        return "TESOL"
    elif (len(major) < 5 and"me" in major) or "mecha" in major:
        return "ME"
    elif "computer" in major or (len(major)<5 and "cs" in major) or (len(major)<5 and "ce" in major) or "cis" in major:
        return "CS"
    elif "mis" in major:
        return "MIS"
    elif "eng" in major:
        return "OtherEngin"
    elif "ieor" in major:
        return "IEOR"
    else:
        return "Other"
