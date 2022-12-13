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


--DUMPING DATA TO THE DB
INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('12323', '2022-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('12323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('22323', '2022-12-11', 'in', '123412315', '5423', '432', '300', '433', '431');
INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('22323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('32323', '2021-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('32323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('42323', '2018-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('52323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('62323', '2022-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('62323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

INSERT INTO transactions (sessionid, datetime, direction, truck, containers, bruto, truckTara, neto, produce) VALUES ('72323', '2022-11-11', 'in', '123412315', '5423', '432', '300', '433', '431');
INSERT INTO transactions (sessionid, datetime, direction, truck, bruto, truckTara, neto, produce) VALUES ('72323', '2022-11-11', 'out', '5423', '432', '300', '433', '431');

--Direction none
INSERT INTO transactions (sessionid, datetime, containers, bruto, truckTara, neto, produce) VALUES ('82323', '2022-11-11', '5423', '432', '300', '433', '431');


--
-- Dumping data for table `test`
--

-- INSERT INTO `test` (`id`, `aa`) VALUES
-- (1, 'aaaa')



