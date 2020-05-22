    /*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
    /*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;


    --
    --  TABELA ALBUMÓW
    --
    DROP TABLE IF EXISTS `albumy`;
    CREATE TABLE `albumy` (
        `ida` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `nazwa` VARCHAR(50) NOT NULL,
        `data` DATE NOT NULL,
        `ocena` TINYINT DEFAULT NULL,
        PRIMARY KEY(`ida`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    --
    --  DODAWANIE ALBUMÓW
    --
    INSERT INTO albumy(albumy.nazwa, albumy.data, albumy.ocena)
        VALUES ('Master of Puppets','1986-03-03',10), ('Black Sabbath','1970-02-13',10), ('Paranoid','1970-10-18',10),('Exile on Main','1972-05-12', NULL), ('The Pale Emperor', '2015-01-5', NULL);

    --
    --  TABELA UTWORÓW
    --
    DROP TABLE IF EXISTS `UTWORY`;
    CREATE TABLE `utwory` (
        `idu` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `nazwa` VARCHAR(50) NOT NULL,
        `dlugosc` TIME NOT NULL,
        `ocena` TINYINT DEFAULT NULL,
        PRIMARY KEY(`idu`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    --
    --  DODAWANIE UTWORÓW
    --
    INSERT INTO utwory(utwory.nazwa,  utwory.dlugosc, utwory.ocena)
        VALUES('Battery', '00:05:12', 10),('The Thing That Should Not Be','00:06:36',6),('The Wizard', '00:04:24', 10),('The Mephistopheles Of Los Angeles', '00:04:58', 10),('Rocks OFF', '00:04:33', NULL),('Rip This Joint','00:02:23',NULL), ('Iron Man', '00:05:56',NULL);


    --
    --  RELACJA UTWÓR należy do ALBUM
    --
    DROP TABLE IF EXISTS `utwor_album`;
    CREATE TABLE `utwor_album` (
        `idua` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `a_id` int(10) unsigned NOT NULL,
        `u_id` int(10) unsigned NOT NULL,
        `numer` VARCHAR(5) NOT NULL,
        PRIMARY KEY(`idua`),
        FOREIGN KEY (`a_id`) REFERENCES `albumy`(`ida`) ON UPDATE CASCADE,
        FOREIGN KEY (`u_id`) REFERENCES `utwory`(`idu`) ON UPDATE CASCADE
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    --
    --  DODAWANIE UTWORÓW do ALBUMÓW
    --

    INSERT INTO utwor_album(utwor_album.a_id,utwor_album.u_id,utwor_album.numer)
        VALUES (1,1,1),(1,2,2),(2,3,2),(3,7,4),(4,5,1),(4,6,2),(5,4,4);


    --
    --  TABELA WYKONAWCÓW 
    --
    DROP TABLE IF EXISTS `wykonawca`;
    CREATE TABLE `wykonawca` (
    `idw` int(10) unsigned NOT NULL AUTO_INCREMENT,
    
    PRIMARY KEY (`idw`)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    --
    --  TABELA ZESPOŁÓW
    --

    DROP TABLE IF EXISTS `zespol`;
    CREATE TABLE `zespol` (
    `idz` int(10) unsigned NOT NULL,
    `nazwa` VARCHAR(50) NOT NULL,
    `data_utworzenia` DATE NOT NULL,
    `data_rozwiazania` DATE DEFAULT NULL,
    PRIMARY KEY (`idz`),
    FOREIGN KEY (`idz`) REFERENCES `wykonawca` (`idw`) ON DELETE CASCADE ON UPDATE CASCADE
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    --
    --  TABELA MUZYKÓW 
    --

    DROP TABLE IF EXISTS `muzyk`;
    CREATE TABLE `muzyk` (
    `idm` int(10) unsigned NOT NULL,
    `imie` VARCHAR(50) DEFAULT NULL,
    `nazwisko` VARCHAR(50) NOT NULL,
    `data_ur` DATE NOT NULL,
    `data_sm` DATE DEFAULT NULL,
    `rola` VARCHAR(200) NOT NULL,
    PRIMARY KEY (`idm`),
    FOREIGN KEY (`idm`) REFERENCES `wykonawca` (`idw`) ON DELETE CASCADE ON UPDATE CASCADE
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;


    --
    --  DODAWANIE ZESPOŁÓW I MUZYKÓW
    --
    INSERT INTO wykonawca VALUES (); 
        SET @last_id = LAST_INSERT_ID();
        INSERT INTO zespol(zespol.idz, zespol.nazwa,zespol.data_utworzenia) VALUES (@last_id, 'Metallica', '1981-10-28');
    INSERT INTO wykonawca VALUES (); 
        SET @last_id = LAST_INSERT_ID();
        INSERT INTO zespol(zespol.idz, zespol.nazwa,zespol.data_utworzenia,zespol.data_rozwiazania) VALUES (@last_id, 'Black Sabbath', '1968-01-01','2017-02-04');
    INSERT INTO wykonawca VALUES (); 
        SET @last_id = LAST_INSERT_ID();
        INSERT INTO zespol(zespol.idz, zespol.nazwa,zespol.data_utworzenia) VALUES (@last_id, 'The Rolling Stones', '1962-07-12');
    INSERT INTO wykonawca VALUES();
        SET @last_id = LAST_INSERT_ID();
        INSERT INTO zespol(zespol.idz, zespol.nazwa,zespol.data_utworzenia) VALUES (@last_id, 'Motörhead', '1975-01-01');
    INSERT INTO wykonawca VALUES();
        SET @last_id = LAST_INSERT_ID();
        INSERT INTO zespol(zespol.idz, zespol.nazwa,zespol.data_utworzenia) VALUES (@last_id, 'Megadeth', '1983-04-01');

    INSERT INTO wykonawca values ();
        SET @last_id= LAST_INSERT_ID();
        INSERT INTO muzyk(muzyk.idm,muzyk.imie,muzyk.nazwisko,muzyk.data_ur,muzyk.rola) VALUES(@last_id,'Marilyn','Manson','1969-01-05','wokalista');
    INSERT INTO wykonawca values ();
        SET @last_id= LAST_INSERT_ID();
        INSERT INTO muzyk(muzyk.idm,muzyk.imie,muzyk.nazwisko,muzyk.data_ur,muzyk.rola) VALUES(@last_id,'Tony','Iommi','1948-02-19','gitarzysta');
    INSERT INTO wykonawca values ();
        SET @last_id= LAST_INSERT_ID();
        INSERT INTO muzyk(muzyk.idm,muzyk.imie,muzyk.nazwisko,muzyk.data_ur, muzyk.data_sm,muzyk.rola) VALUES(@last_id,'Lemmy','Kilmister','1945-12-24','2015-12-28','basista, wokalista');
    INSERT INTO wykonawca values ();
        SET @last_id= LAST_INSERT_ID();
        INSERT INTO muzyk(muzyk.idm,muzyk.imie,muzyk.nazwisko,muzyk.data_ur,muzyk.data_sm, muzyk.rola) VALUES(@last_id,'Cliff','Burton','1962-02-10','1986-10-27','basista');
    INSERT INTO wykonawca values ();
        SET @last_id= LAST_INSERT_ID();
        INSERT INTO muzyk(muzyk.idm,muzyk.imie,muzyk.nazwisko,muzyk.data_ur,muzyk.rola) VALUES(@last_id,'Dave','Mustaine','1961-10-13','gitarzysta, wolalista');

    --
    --  TABELA NALEZY
    --
    DROP TABLE IF EXISTS `nalezy`;
    CREATE TABLE `nalezy`(
        `idn` int(10)  unsigned NOT NULL AUTO_INCREMENT,
        `m_id` int(10) unsigned NOT NULL,
        `z_id` int(10) unsigned NOT NULL,
        `od` DATE NOT NULL,
        `do` DATE DEFAULT NULL,
        PRIMARY KEY(`idn`),
        FOREIGN KEY (`m_id`) REFERENCES `muzyk`(`idm`) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (`z_id`) REFERENCES `zespol`(`idz`) ON DELETE CASCADE ON UPDATE CASCADE

    )ENGINE=InnoDB DEFAULT CHARSET=utf8;


    --
    --  DODAWANIE MUZYKÓW do ZESPOŁÓW
    --

    INSERT INTO nalezy(nalezy.m_id,nalezy.z_id,nalezy.od, nalezy.do)
        VALUES(9,1,'1982-12-28','1986-10-27'),(8,4,'1975-01-01','2015-01-01'),(10,1,'1982-01-01', '1983-01-01'), (7,2,'1968-01-01',NULL), (10,5,'1983-01-01',NULL);


    DROP TABLE IF EXISTS `wydanie`;
    CREATE TABLE `wydanie`(
        `id_wydanie` int(10) unsigned NOT NULL AUTO_INCREMENT,
        `album_id` int(10) unsigned NOT NULL,
        `wykonawca_id` int(10) unsigned NOT NULL,
        PRIMARY KEY(`id_wydanie`),
        FOREIGN KEY (`album_id`) REFERENCES `albumy`(`ida`) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (`wykonawca_id`) REFERENCES `wykonawca`(`idw`) ON DELETE CASCADE ON UPDATE CASCADE
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;

    CREATE UNIQUE INDEX ind_wydanie ON wydanie(album_id,wykonawca_id);

    INSERT INTO wydanie(wydanie.album_id,wydanie.wykonawca_id)
        VALUES (1,1),(2,2),(3,2),(4,3),(5,6);


    /*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
    /*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
