from collections import OrderedDict


def get_uni_rank():
    universities = OrderedDict()
    universities["Princeton"] = ["princeton"]
    universities["Harvard"] = ["harvard"]
    universities["UChicago"] = ["chicago"]
    universities["Yale"] = ["yale"]
    universities["Columbia"] = ["columbia"]
    universities["Stanford"] = ["stanford"]
    universities["MIT"] = ["massachusetts institute of technology", "mit"]
    universities["Duke"] = ["duke"]
    universities["UPenn"] = ["university of penn", "upenn", "u penn"]
    universities["JHU"] = ["johns hopkins", "jhu"]
    universities["Dartmouth"] = ["dartmouth"]
    universities["Caltech"] = ["california institute", "caltech"]
    universities["NWU"] = ["northwestern", "nwu"]
    universities["Brown"] = ["brown"]
    universities["Cornell"] = ["cornell"]
    universities["Rice"] = ["rice"]
    universities["Notre Dame"] = ["nd", "notre dame"]
    universities["Vanderbilt"] = ["vanderbilt"]
    universities["WUSTL"] = ["wustl", "saint louis", "st louis"]
    universities["Emory"] = ["emory"]
    universities["Georgetown"] = ["georgetown"]
    universities["Berkeley"] = ["berkeley", "ucb"]
    universities["USC"] = ["usc", "southern california", "south california"]
    universities["CMU"] = ["cmu", "carnegie"]
    universities["UCLA"] = ["ucla", "los angeles"]
    universities["UV"] = ["uv", "university of virginia"]
    universities["Tufts"] = ["tufts"]
    universities["UMich"] = ["umich", "ann arbor", "university of michi"]
    universities["WFU"] = ["wfu", "wake forest"]
    universities["UNC"] = ["unc", "chapel"]
    universities["Boston College"] = ["boston college", "bc"]
    universities["WM"] = ["wm", "william"]
    universities["Rochester"] = ["rochester"]
    universities["Brandeis"] = ["brandeis"]
    universities["GaTech"] = ["gate", "georgia institute"]
    universities["NYU"] = ["new york university", "nyu"]
    universities["CASE"] = ["case west", "cwru"]
    universities["UCSB"] = ["santa barbara", "ucsb"]
    universities["BU"] = ["boston u", "bu"]  # check buffalo
    universities["NEU"] = ["northeastern", "neu"]
    universities["RPI"] = ["rensselaer", "rpi"]
    universities["Tulane"] = ["tulane"]
    universities["UCI"] = ["uci", "irvine"]
    universities["Lehigh"] = ["lehigh"]
    universities["UCD"] = ["ucd", "davis"]
    universities["UCSD"] = ["ucsd", "san di"]
    universities["UIUC"] = ["uiuc", "champ"]
    universities["Miami"] = ["miami"]
    universities["WISC"] = ["wisc", "madison"]
    universities["PSU"] = ["psu", "pennsylvania state", "penn state"]
    universities["Pepperdine"] = ["pepperdine"]
    universities["UFL"] = ["ufl", "university of florida"]
    universities["villanova"] = ["villanova"]
    universities["OSU"] = ["osu", "ohio state"]
    universities["GWU"] = ["gwu", "george washington"]
    universities["Washington"] = ["washington", "uw"]
    # two washing check gwu first
    universities["SMU"] = ["methodist", "smu"]
    universities["UGA"] = ["university of georgia", "uga"]
    universities["UTexas"] = ["utexas", "austin"]
    universities["Fordham"] = ["fordham"]
    universities["Purdue"] = ["purdue"]
    universities["Syracuse"] = ["syracuse"]
    universities["UConn"] = ["ucon", "conn"]
    universities["UMD"] = ["maryland", "umd"]
    universities["WPI"] = ["wpi", "worcester"]
    universities["Clemson"] = ["clemson"]
    universities["Yeshiva"] = ["yeshiva"]
    universities["BYU"] = ["byu", "brigham"]
    universities["Pitt"] = ["pitt"]
    universities["Rugters"] = ["rutgers"]
    universities["Baylor"] = ["baylor"]
    universities["Stevens"] = ["steven"]
    universities["UMN"] = ["umn", "minne"]
    universities["American"] = ["american"]
    universities["Clark"] = ["clark"]
    universities["TAMU"] = ["tamu", "texas a"]
    universities["UMASS"] = ["umass", "amherst", "university of massachu"]
    universities["VT"] = ["vt", "virginia tech"]
    return universities

universities = get_uni_rank()


def get_school_rank(school, dic=universities):
    school = school.lower()
    for key in dic:
        name_list = dic[key]
        for name in name_list:
            if name in school:
                cleaned_school = key
                ranking = list(dic.keys()).index(key) + 1
                return cleaned_school, ranking
    return None, None
