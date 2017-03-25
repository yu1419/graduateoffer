drop trigger if exists update_offercount ;
DELIMITER $$

CREATE
    TRIGGER update_offercount after INSERT
    ON offer
    FOR EACH ROW 
    BEGIN
		DECLARE total_cnt INT;
        DECLARE has INT;
        select count(*) into total_cnt from offer where offer.person_id = New.person_id and ranking is not NULL;
        select count(*) into has from offer_count where person_id = New.person_id;
        IF has THEN
            update offer_count set total_count = total_cnt where person_id = New.person_id;
        ELSE
            insert into offer_count (total_count, person_id) values(total_cnt, New.person_id);
        END IF;

	END$$

DELIMITER ;
