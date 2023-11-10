DELIMITER //

CREATE PROCEDURE checkstatus(IN param VARCHAR)
BEGIN
    DECLARE a_id INT;
    DECLARE status VARCHAR(255);

   
    SELECT userid INTO a_id FROM cookie_jar where cookie=param


    SELECT voting_status INTO status FROM voted WHERE user_id = a_id;


    SELECT a_id AS A_ID, status AS Status;

END //

DELIMITER ;

CALL SelectEntriesFromAandB("cookie"); 

