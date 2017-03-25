def get_school_rank(dic, school):
    school = school.lower()
    for key in dic:
        name_list = dic[key]
        for name in name_list:
            if name in school:
                cleaned_school = key
                ranking = list(dic.keys()).index(key) + 1
                return cleaned_school, ranking
    return None, None
