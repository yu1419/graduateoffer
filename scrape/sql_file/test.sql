select result, ranking, clean_university,major_cate,degree,under_school_type,gpa,toefl, gre,gre_aw, received_date, total_count, person.person_id, offer.url from offer, person, offer_count where (person.version, person.person_id) in (select max(version), person_id from person group by person_id) and offer.person_id = person.person_id and offer_count.person_id= person.person_id  and offer.ranking>=1 and offer.ranking<=78 order by ISNULL(received_date) , received_date DESC  limit 0,10

ALTER TABLE person ADD INDEX (person_id);
