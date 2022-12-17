--
-- Database: `billdb`
--

CREATE DATABASE IF NOT EXISTS `billdb`;
USE `billdb`;

-- --------------------------------------------------------

--
-- Table structure
--

CREATE TABLE IF NOT EXISTS `Provider` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  AUTO_INCREMENT=10001 ;

CREATE TABLE IF NOT EXISTS `Rates` (
  `product_id` varchar(50) NOT NULL,
  `rate` int(11) DEFAULT 0,
  `scope` varchar(50) DEFAULT NULL,
  FOREIGN KEY (scope) REFERENCES `Provider`(`id`)
) ENGINE=MyISAM ;

CREATE TABLE IF NOT EXISTS `Trucks` (
  `id` varchar(10) NOT NULL,
  `provider_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  FOREIGN KEY (`provider_id`) REFERENCES `Provider`(`id`)
) ENGINE=MyISAM ;
--
-- Dumping data
insert into Provider values ("10001","Roei");
insert into Provider values ("10002","Noam");
insert into Provider values ("10003","Or");
insert into Provider values ("10004","Dvir");
insert into Provider values ("10005","Yotam");
insert into Provider values ("10006","Rachel");
insert into Provider values ("10007","Elior");
insert into Provider values ("10008","Shoval");
insert into Provider values ("10009","Eduard");
insert into Provider values ("10010","Golan");

insert into Trucks values ("T-11111",10001);
insert into Trucks values ("T-22222",10002);     
insert into Trucks values ("T-33333",10003);     
insert into Trucks values ("T-12348",10002);    
insert into Trucks values ("T-12347",10002); 
insert into Trucks values ("T-12345",10006);   
insert into Trucks values ("T-12346",10007);
insert into Trucks values ("T-88888",10008);
insert into Trucks values ("T-99999",10009);   
insert into Trucks values ("T-11010",10001);                              

--

/*
INSERT INTO Provider (`name`) VALUES ('ALL'), ('pro1'),
(3, 'pro2');

INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES ('1', 2, 'ALL'),
(2, 4, 'pro1');

INSERT INTO Trucks (`id`, `provider_id`) VALUES ('134-33-443', 2),
('222-33-111', 1);
*/
