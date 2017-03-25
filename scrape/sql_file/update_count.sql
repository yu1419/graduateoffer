delete from offer_count where person_id is not NULL;
insert into offer_count (total_count, person_id) select count(*), person_id from offer where ranking is not NULL group by person_id;