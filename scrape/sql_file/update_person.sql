drop trigger if exists update_person ;
DELIMITER $$

CREATE
    TRIGGER update_person BEFORE INSERT
    ON person
    FOR EACH ROW 
    BEGIN

        DECLARE has INT;
        DECLARE old_toefl INT;
        DECLARE old_gre INT;
        DECLARE old_gre_aw decimal(2,1);
        DECLARE old_under_school_type enum('985','211','Abroad','other');
        DECLARE old_gpa decimal(4,2);
        DECLARE old_version INT;
        IF NEW.gpa =3 or NEW.gpa >5.0 or NEW.gpa <2.5 and NEW.gpa <70 or NEW.gpa >100 THEN
            set NEW.gpa = NULL;
        END IF;
        IF NEW.gre<300 or NEW.gre >340 THEN
            set NEW.gre = NULL;
        END IF;
        IF NEW.gre_aw <2.0 or NEW.gre_aw >6 THEN
            set NEW.gre_aw = NULL;
        END IF;
        IF NEW.toefl>120 or NEW.toefl <70 and NEW.toefl >9 THEN
            set NEW.toefl = NULL;
        END IF;
        select count(*) into has from person where person.person_id = New.person_id and person.person_id<>"gter_" and person.person_id<>"point_";
        IF has THEN
            select toefl, gre, gre_aw, under_school_type, gpa, version into old_toefl, old_gre, old_gre_aw, old_under_school_type, old_gpa, old_version from person where person.person_id = New.person_id and person.person_id<>"gter_" and person.person_id<>"point_" order by version desc limit 1;
            IF not old_toefl THEN
                set NEW.toefl = old_toefl;
            END IF;
            IF not old_gre THEN
                set NEW.gre = old_gre;
            END IF;
            IF not old_gre_aw THEN
                set NEW.gre_aw = old_gre_aw;
            END IF;
            IF old_under_school_type <> "211" THEN
                set NEW.under_school_type = old_under_school_type;
            END IF;
            IF not old_gpa THEN
                set NEW.gpa = old_gpa;
            END IF;
                set NEW.version = old_version + 1;
        END IF;

    END$$

DELIMITER ;
