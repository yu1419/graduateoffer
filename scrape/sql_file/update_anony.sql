drop trigger if exists update_anony ;
DELIMITER $$

CREATE
    TRIGGER update_anony before update
    ON offer_count
    FOR EACH ROW 
    BEGIN
    	IF NEW.person_id = "gter_" then
    		set NEW.total_count = 1;
    	END if;
	END$$

DELIMITER ;
