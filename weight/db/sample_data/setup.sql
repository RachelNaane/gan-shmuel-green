--
-- Database: `Weight`
--

CREATE DATABASE IF NOT EXISTS `weight`;

-- --------------------------------------------------------

--
-- Table structure for table `containers-registered`
--

USE weight;


CREATE TABLE IF NOT EXISTS `containers_registered` (
  `container_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`container_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

CREATE TABLE IF NOT EXISTS `trucks_registered` (
  `truck_id` varchar(15) NOT NULL,
  `weight` int(12) DEFAULT NULL,
  `unit` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`truck_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;


-- --------------------------------------------------------

--
-- Table structure for table `transactions`
--

CREATE TABLE IF NOT EXISTS `transactions` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `sessionid` varchar(255) NOT NULL,
  `datetime` datetime DEFAULT NULL,
  `direction` varchar(10) DEFAULT NULL,
  `truck` varchar(50) DEFAULT NULL,
  `containers` varchar(10000) DEFAULT NULL,
  `bruto` int(12) DEFAULT NULL,
  `truckTara` int(12) DEFAULT NULL,
  --   "neto": <int> or "na" // na if some of containers unknown
  `neto` int(12) DEFAULT NULL,
  `produce` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=10001 ;

show tables;

describe containers_registered;
describe transactions;


-- DUMPING DATA TO THE DB
-- INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('1', '2022-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
-- INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('1', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

-- INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('22323', '2022-12-11', 'in', '123412315', '5423', '432', '300', '433', '431');
-- INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('22323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

-- INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('32323', '2021-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
-- INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('32323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

-- INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('42323', '2018-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
-- INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('52323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

-- INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('62323', '2022-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
-- INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('62323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

-- INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('72323', '2022-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
-- INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('72323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');


INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22323', '2022-12-11', 'In', 'T-12345', 'C-00123,C-00124', '1300',NULL , 'Navel');
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22323', '2022-12-11', 'Out', 'T-12345', NULL, NULL, 500, 'Navel');
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22324', '2022-12-12', 'In', 'T-12346', 'C-00125,C-00126', '1400',NULL , 'Navel');
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22324', '2022-12-12', 'Out', 'T-12346', NULL, NULL, 550, 'Navel');
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22325', '2022-12-08', 'In', 'T-12347', 'C-00127,C-00128', '1350', NULL, 'Navel');
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22325', '2022-12-08', 'Out', 'T-12347', NULL, 'NULL', 500, 'Navel');
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22326', '2022-12-08', 'In', 'T-12348', 'C-00123,C-00124', '1400', NULL, 'Navel')
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22326', '2022-12-08', 'Out', 'T-12348', 'C-00123,C-00124', NULL, 500, 'Navel');
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, produce) VALUES ('22323', '2022-12-11', 'None', NULL, 'C-0019', NULL,NULL, 'Navel');



-- Direction none


-- Containers
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-35434',296,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-73281',273,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-35537',292,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-49036',272,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-85957',274,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-57132',306,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-80015',285,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-40162',255,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-66667',238,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-65481',306,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-65816',270,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-38068',267,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-36882',286,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-38559',253,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-83754',247,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-40277',307,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-55516',260,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-45237',301,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-69828',269,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-44997',250,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-52273',308,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-63478',245,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-42418',286,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-86865',299,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-38552',266,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-81185',242,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-71151',300,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-78131',273,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-61969',289,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-82193',308,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-85358',259,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-47634',285,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-83570',278,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-45628',288,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-70986',251,'kg');
INSERT INTO containers_registered (container_id,weight,unit) VALUES ('C-54804',297,'kg');


--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa')



