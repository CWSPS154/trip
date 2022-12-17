/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - trip
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`trip` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `trip`;

/*Table structure for table `account` */

DROP TABLE IF EXISTS `account`;

CREATE TABLE `account` (
  `ac_id` int(11) NOT NULL AUTO_INCREMENT,
  `login_id` int(11) DEFAULT NULL,
  `surename` varchar(50) DEFAULT NULL,
  `ac_no` varchar(100) DEFAULT NULL,
  `ifsc` varchar(100) DEFAULT NULL,
  `mob` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `adrs` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state` varchar(100) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `balance` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ac_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `account` */

insert  into `account`(`ac_id`,`login_id`,`surename`,`ac_no`,`ifsc`,`mob`,`email`,`adrs`,`city`,`state`,`pin`,`balance`) values (1,1,'Admin','1234567891234567','ADS1234','9685741230','admin@mail.com','kannur, ulikkal','kannur','Kerala',670705,'40869.19'),(2,48,'Sanoop Ps','12458963784512025','FDS1234','09685741230','dwarakha@mail.com','kannur, ulikkal','kannur','Kerala',670705,'738552.6099999999'),(3,50,'Hiran Joseph','7896541236987452','AXS123','09685741230','finekerala@mail.com','kannur, ulikkal','kannur','Kerala',670705,'0'),(4,51,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0'),(5,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(6,55,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0'),(7,55,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0'),(8,56,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0'),(9,57,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'0');

/*Table structure for table `ad` */

DROP TABLE IF EXISTS `ad`;

CREATE TABLE `ad` (
  `ad_id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` int(11) DEFAULT NULL,
  `ad` varchar(200) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ad_id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;

/*Data for the table `ad` */

insert  into `ad`(`ad_id`,`agency_id`,`ad`,`date`,`type`) values (21,48,'20200223_163052.jpg','2020-02-23','Posted'),(22,50,'20200223_221350.jpg','2020-02-23','Posted'),(23,51,'20200224_123238.jpg','2020-02-24','Posted');

/*Table structure for table `agency` */

DROP TABLE IF EXISTS `agency`;

CREATE TABLE `agency` (
  `agency_id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_name` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `postoffice` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `mob_no` varchar(50) DEFAULT NULL,
  `lic_no` varchar(50) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `cover` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`agency_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;

/*Data for the table `agency` */

insert  into `agency`(`agency_id`,`agency_name`,`place`,`postoffice`,`pin`,`email`,`mob_no`,`lic_no`,`photo`,`cover`) values (48,'Dwaraka Holidays & Travels','City Center, Iritty','Iritty',670703,'dwarakaholidays@shopatkerala.com','9745362626','DW3454784662','20200223_141203.jpg','20200404_162339.jpg'),(50,'Fine Kerala Tours And Travels','Keezhpalli, Kannur','Keezhpalli',670704,'finekeralatours@gmail.com','9947386505','FT5447097434','20200223_212717.jpg','20200404_162424.jpg'),(51,'Sanchari Holidays','1st Floor, CK Bhaskaran Memmorial Building',' Kannur',670595,'sanjarijithesh@gmail.com','9846453886','SH1246434623','20200223_231159.jpg','20200404_150759.jpg'),(56,'Travel Arround','Kozhikode','Kozhikode',456466,'travelaround@gmail.com','7896526852','854596317896','20200601_221215.jpg','20200601_221215.jpg'),(57,'Dwaraka Holidays & Travels','kannur','67001',670633,'dwaraks98@gmail.om','0968574534','123456789012','20200605_102533.jpg','20200605_102533.jpg');

/*Table structure for table `allocate_guide` */

DROP TABLE IF EXISTS `allocate_guide`;

CREATE TABLE `allocate_guide` (
  `alct_id` int(11) NOT NULL AUTO_INCREMENT,
  `guide_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`alct_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `allocate_guide` */

insert  into `allocate_guide`(`alct_id`,`guide_id`,`user_id`) values (7,0,49),(8,17,53);

/*Table structure for table `bank` */

DROP TABLE IF EXISTS `bank`;

CREATE TABLE `bank` (
  `bank_id` int(11) NOT NULL AUTO_INCREMENT,
  `card_no` varchar(50) DEFAULT NULL,
  `cvc` int(11) DEFAULT NULL,
  `mm` int(11) DEFAULT NULL,
  `yy` int(11) DEFAULT NULL,
  `amt` float DEFAULT NULL,
  PRIMARY KEY (`bank_id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=latin1;

/*Data for the table `bank` */

insert  into `bank`(`bank_id`,`card_no`,`cvc`,`mm`,`yy`,`amt`) values (80,'1478956320157234',432,12,2023,999),(81,'5874123698520123',432,12,2023,999),(84,'1234567890123456',432,12,2023,198350),(86,'1234567890123456',432,12,2023,171843);

/*Table structure for table `booking` */

DROP TABLE IF EXISTS `booking`;

CREATE TABLE `booking` (
  `bk_id` int(11) NOT NULL AUTO_INCREMENT,
  `package_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `adults` varchar(100) DEFAULT NULL,
  `kids` varchar(100) DEFAULT NULL,
  `bk_date` date DEFAULT NULL,
  `details` varchar(500) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`bk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `booking` */

insert  into `booking`(`bk_id`,`package_id`,`user_id`,`date`,`adults`,`kids`,`bk_date`,`details`,`status`) values (3,53,49,'2020-04-01','53','2','2020-04-23','fghfj','Payed'),(4,55,53,'2020-04-01','53','12','2020-05-01','fdh','Payed'),(5,71,53,'2020-06-01','10','12','2020-06-28','dfgfdg','Booking'),(8,53,54,'2020-06-02','345','43','2020-06-26','fdgfg','Booking');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `cmplt_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `cmplt` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `reply` varchar(100) DEFAULT NULL,
  `rdate` date DEFAULT NULL,
  `agency_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`cmplt_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

insert  into `complaint`(`cmplt_id`,`user_id`,`cmplt`,`date`,`reply`,`rdate`,`agency_id`) values (3,49,'not good','2020-02-26','pending','0000-00-00',48),(4,49,'not well','2020-02-26','Sorry for that\r\n','2020-03-25',50),(5,49,'wrost','2020-02-26','sorry  for that','2020-02-26',48);

/*Table structure for table `enquiry` */

DROP TABLE IF EXISTS `enquiry`;

CREATE TABLE `enquiry` (
  `eid` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `name` varchar(60) DEFAULT NULL,
  `mail` varchar(60) DEFAULT NULL,
  `phno` varchar(60) DEFAULT NULL,
  `adult` int(11) DEFAULT NULL,
  `kids` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `details` varchar(60) DEFAULT NULL,
  `status` varchar(60) DEFAULT NULL,
  `created_at` date DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`eid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `enquiry` */

insert  into `enquiry`(`eid`,`pid`,`name`,`mail`,`phno`,`adult`,`kids`,`date`,`details`,`status`,`created_at`,`user_id`) values (4,55,'Hiran Joseph','hiranjoe46@gmail.com','+91 7559876583',10,12,'2020-03-31','dgfgdf','pending','2020-03-26',49);

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `fdbk_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `fdbk` varchar(100) DEFAULT NULL,
  `agency_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`fdbk_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`fdbk_id`,`user_id`,`date`,`fdbk`,`agency_id`) values (8,49,'2020-02-26','good',48),(9,49,'2020-02-26','nice',50),(10,49,'2020-02-26','hi',50),(11,49,'2020-02-26','supper',48);

/*Table structure for table `guide` */

DROP TABLE IF EXISTS `guide`;

CREATE TABLE `guide` (
  `guide_id` int(11) NOT NULL AUTO_INCREMENT,
  `guide_name` varchar(50) DEFAULT NULL,
  `agency_id` int(50) DEFAULT NULL,
  `email_id` varchar(50) DEFAULT NULL,
  `mob_no` varchar(50) DEFAULT NULL,
  `G_exp` varchar(50) DEFAULT NULL,
  `Kn_lng` varchar(50) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `package_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`guide_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

/*Data for the table `guide` */

insert  into `guide`(`guide_id`,`guide_name`,`agency_id`,`email_id`,`mob_no`,`G_exp`,`Kn_lng`,`photo`,`status`,`package_id`) values (17,'Nandhakumar',48,'nadhakumar85@gmail.com','7567564534','4','English,Malayalam,Hindi,Tamil,Telung','20200223_160351.jpg','free',NULL),(18,'Ramdas',50,'ramdaskr@gmail.com','7686754534','8','Hindi,English','20200223_220419.jpg','free',NULL),(19,'Shaji paulose',50,'shajipls@gmail.com','7895373212','4','Malayalam,Hindi,Tamil','20200223_220741.jpg','Requested',71),(20,'Sandra',48,'sadafdsf@fdfs','7895373212','5','English,Malayalam,Hindi,Tamil,Telung','20200325_125213.jpg','Requested',55);

/*Table structure for table `location` */

DROP TABLE IF EXISTS `location`;

CREATE TABLE `location` (
  `loc_id` int(11) NOT NULL AUTO_INCREMENT,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `package_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`loc_id`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=latin1;

/*Data for the table `location` */

insert  into `location`(`loc_id`,`latitude`,`longitude`,`package_id`) values (106,15.4507,73.80272,53),(107,9.81699,77.24625,55),(117,11.26596,76.20634,70),(118,9.51099,76.35365,69),(119,32.24707,77.18874,71),(120,12.30514,76.65515,72),(121,10.23438,77.48646,73),(122,17.36156,78.47466,74),(123,8.48324,76.94344,75),(124,11.78457,76.16311,76);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `Login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`Login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`Login_id`,`username`,`password`,`type`) values (1,'admin','admin','admin'),(48,'dwarakaholidays@shopatkerala.com','dwaraka123','agency'),(49,'hiranjoe46@gmail.com','alian46@','user'),(50,'finekeralatours@gmail.com','finekerala123','agency'),(51,'sanjarijithesh@gmail.com','sanchari098','agency'),(53,'sanoopsahadevan9990@gmail.com','sanoop@123','user'),(54,'amal689itga@gmail.com','amalptomy','user'),(56,'travelaround@gmail.com','travel2123','pending'),(57,'dwaraks98@gmail.om','dwaraka123','pending');

/*Table structure for table `notification` */

DROP TABLE IF EXISTS `notification`;

CREATE TABLE `notification` (
  `notfcn_id` int(11) NOT NULL AUTO_INCREMENT,
  `notfcn_ctnt` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `Login_id` int(50) DEFAULT NULL,
  `Type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`notfcn_id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=latin1;

/*Data for the table `notification` */

insert  into `notification`(`notfcn_id`,`notfcn_ctnt`,`date`,`Login_id`,`Type`) values (1,'Welcome to tripio','2020-02-26',1,'All'),(19,'Your package -Ramakkalmedu - Vagamon 2 Days Trip - is removed from trending ','2020-03-25',1,'48'),(20,'Your package -Ramakkalmedu - Vagamon 2 Days Trip - is now on trending ','2020-03-25',1,'48'),(21,'Admin is gived the reply for the user complaint','2020-03-25',1,'50'),(22,'Your Advertisement is removed','2020-03-25',1,'48'),(23,'Your Advertisement is posted','2020-03-25',1,'48'),(24,'Your Enquiry is checked and we will contact you soon','2020-03-25',48,'49'),(25,'Your Enquiry is deleted','2020-03-25',48,'49'),(33,'You Booked Ramakkalmedu - Vagamon 2 Days Trip is Rejected by the agency due to some reasons,Please book again the package with proper arguments for your trip','2020-04-01',48,'49'),(34,'You Booked Goa - Dandeli 3 Days 2 Nights Package is accepted and now you can pay the amount for the package through card payment','2020-04-01',48,'49'),(35,'You Booked Ramakkalmedu - Vagamon 2 Days Trip is accepted and now you can pay the amount for the package through card payment','2020-04-01',48,'53'),(36,'Null Tech is payed for Ramakkalmedu - Vagamon 2 Days Trip','2020-04-01',53,'48'),(37,'Null Tech is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-04-01',53,'48'),(38,'Hiran Joseph is payed amount for Goa - Dandeli 3 Days 2 Nights Package','2020-04-02',49,'48'),(40,'Null Tech is payed for Ramakkalmedu - Vagamon 2 Days Trip','2020-04-03',53,'48'),(41,'Your Advertisement is removed','2020-06-01',1,'51'),(42,'Your Advertisement is posted','2020-06-01',1,'51'),(43,'Your package -Ramakkalmedu - Vagamon 2 Days Trip - is removed from trending ','2020-06-01',1,'48'),(44,'Your package -Ramakkalmedu - Vagamon 2 Days Trip - is now on trending ','2020-06-01',1,'48'),(45,'Your Enquiry is deleted','2020-06-02',48,'0'),(47,'Amal P Tomy is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',54,'48'),(48,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(49,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(50,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(51,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(52,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(53,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(54,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(55,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(56,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(57,'Hiran Joseph is canceled  Goa - Dandeli 3 Days 2 Nights Package','2020-06-02',49,'48'),(58,'Amal P Tomy is canceled  Ramakkalmedu - Vagamon 2 Days Trip','2020-06-02',54,'48');

/*Table structure for table `package` */

DROP TABLE IF EXISTS `package`;

CREATE TABLE `package` (
  `package_id` int(11) NOT NULL AUTO_INCREMENT,
  `package_name` varchar(50) DEFAULT NULL,
  `ctgory` varchar(50) DEFAULT NULL,
  `Decptn` varchar(1000) DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `photo` varchar(1000) DEFAULT NULL,
  `agencyid` int(11) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`package_id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=latin1;

/*Data for the table `package` */

insert  into `package`(`package_id`,`package_name`,`ctgory`,`Decptn`,`amount`,`photo`,`agencyid`,`type`) values (53,'Goa - Dandeli 3 Days 2 Nights Package','College','4 people share a room,\r\n   Mineral water,\r\n   Tour guide,\r\n   DJ party,\r\n   Accommodation at standard Hotel,\r\n   Entry ticket','3999','20200223_143122.jpg',48,'Approved'),(55,'Ramakkalmedu - Vagamon 2 Days Trip','Family','4 people share a room,   All food,    Mineral water,   Tour guide,    Entry ticket,    Traveling in ac bus','2999','20200223_144205.jpg',48,'Approved'),(69,'Alappuzha Houseboat Stay 2Days','Honeymoon','All meals Veg and Non Veg\r\n   All transfers in  AC Cab','5999','20200223_220042.jpg',50,'Approved'),(70,'1 Day Nilambur Trip','Family','  All transfers in  AC Cab\r\n   All food','3999','20200223_223921.jpg',50,'Approved'),(71,'2 Nights 3 Days Manali Holiday Packages','College','5 percentage GST,\r\n   All meals Breakfast and Dinner','9499','20200223_225002.jpg',50,'Approved'),(73,'Kodaikanal 2 Days 2 Nights Package','College','   All meals Veg and Non Veg,\r\n   All transfers in deluxe Non AC bus,\r\n   All vehicle expense','3999','20200223_233708.jpg',51,'Approved'),(74,'Hyderabad Package 4 Nights 5 Days','College',' All meals Veg and Non Veg,\r\n   Tour guide,\r\n   Accommodation at standard Hotel,\r\n   Activities','5599','20200223_234110.jpg',51,'Approved'),(75,'Thiruvananthapuram 1 Night - 2 Days Package','College','All transfers in deluxe Non AC bus,\r\n   Mineral water,\r\n   Tour guide,\r\n   Entry ticket','2349','20200223_234404.jpg',51,'Approved'),(76,'Agra - Delhi Tour','Family','hdgkeugl','4546','20200605_102946.jpg',48,'pending');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `amount` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `package_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=87 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`amount`,`date`,`user_id`,`package_id`) values (84,'198350.4','2020-04-02',49,53),(86,'171842.69999999998','2020-04-03',53,55);

/*Table structure for table `rating` */

DROP TABLE IF EXISTS `rating`;

CREATE TABLE `rating` (
  `rtg_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(50) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `package_id` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`rtg_id`)
) ENGINE=InnoDB AUTO_INCREMENT=131 DEFAULT CHARSET=latin1;

/*Data for the table `rating` */

insert  into `rating`(`rtg_id`,`user_id`,`rating`,`date`,`package_id`,`status`) values (46,49,4,'2020-02-23',57,'post'),(47,49,4,'2020-02-23',57,'post'),(48,49,3,'2020-02-23',53,'post'),(49,49,4,'2020-02-24',53,'post'),(50,52,4,'2020-02-24',70,'post'),(51,49,4,'2020-02-26',53,'post'),(52,49,3,'2020-02-26',53,'post'),(53,49,4,'2020-03-01',53,'post'),(54,49,4,'2020-03-01',53,'post'),(55,49,4,'2020-03-01',55,'post'),(56,49,4,'2020-03-01',53,'post'),(57,49,4,'2020-03-02',55,'post'),(58,49,3,'2020-03-02',71,'post'),(59,49,4,'2020-03-14',70,'post'),(60,49,4,'2020-03-14',71,'post'),(61,49,5,'2020-03-14',55,'post'),(62,49,5,'2020-03-14',55,'post'),(63,49,4,'2020-03-14',55,'post'),(64,49,4,'2020-03-14',55,'post'),(65,49,5,'2020-03-15',70,'post'),(66,49,4,'2020-03-15',55,'post'),(67,49,5,'2020-03-15',53,'post'),(68,49,5,'2020-03-15',53,'post'),(69,49,5,'2020-03-16',55,'post'),(70,49,4,'2020-03-18',53,'post'),(71,49,5,'2020-03-19',53,'post'),(72,49,5,'2020-03-22',70,'post'),(73,54,4,'2020-03-23',70,'post'),(74,50,0,'2020-03-23',69,'pending'),(75,50,0,'2020-03-23',72,'pending'),(76,51,0,'2020-03-23',73,'pending'),(77,51,0,'2020-03-23',74,'pending'),(78,51,0,'2020-03-23',75,'pending'),(79,49,5,'2020-03-24',55,'post'),(80,49,5,'2020-03-24',71,'post'),(82,49,5,'2020-03-24',55,'post'),(83,49,3,'2020-03-24',70,'post'),(85,49,2,'2020-03-24',55,'post'),(86,49,4,'2020-03-24',55,'post'),(89,49,4,'2020-03-24',55,'post'),(90,49,3,'2020-03-24',71,'post'),(98,49,3,'2020-03-24',53,'post'),(99,48,0,'2020-03-25',76,'pending'),(100,48,0,'2020-03-25',77,'pending'),(101,48,0,'2020-03-25',78,'pending'),(102,48,0,'2020-03-25',79,'pending'),(103,48,0,'2020-03-25',80,'pending'),(104,48,0,'2020-03-25',81,'pending'),(105,48,0,'2020-03-25',82,'pending'),(106,48,0,'2020-03-25',83,'pending'),(107,49,3,'2020-03-26',55,'post'),(108,49,5,'2020-03-26',53,'pending'),(109,49,5,'2020-04-01',55,'post'),(110,49,4,'2020-04-01',53,'pending'),(111,53,5,'2020-04-01',55,'post'),(112,53,4,'2020-04-01',53,'pending'),(113,53,4,'2020-06-01',71,'pending'),(114,48,0,'2020-06-02',76,'pending'),(115,48,0,'2020-06-02',77,'pending'),(116,54,4,'2020-06-02',53,'pending'),(117,54,4,'2020-06-02',53,'pending'),(118,54,4,'2020-06-02',53,'pending'),(119,54,3,'2020-06-02',55,'pending'),(120,49,4,'2020-06-02',53,'pending'),(121,49,4,'2020-06-02',53,'pending'),(122,49,5,'2020-06-02',53,'pending'),(123,49,4,'2020-06-02',53,'pending'),(124,49,3,'2020-06-02',53,'pending'),(125,49,3,'2020-06-02',53,'pending'),(126,49,3,'2020-06-02',53,'pending'),(127,49,4,'2020-06-02',53,'pending'),(128,49,4,'2020-06-02',53,'pending'),(129,49,4,'2020-06-02',53,'pending'),(130,48,0,'2020-06-05',76,'pending');

/*Table structure for table `trending` */

DROP TABLE IF EXISTS `trending`;

CREATE TABLE `trending` (
  `trd_id` int(11) NOT NULL AUTO_INCREMENT,
  `package_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`trd_id`)
) ENGINE=InnoDB AUTO_INCREMENT=76 DEFAULT CHARSET=latin1;

/*Data for the table `trending` */

insert  into `trending`(`trd_id`,`package_id`) values (67,70),(68,53),(69,71),(75,55);

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `userid` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) DEFAULT NULL,
  `place` varchar(50) DEFAULT NULL,
  `postoffice` varchar(50) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `dob` varchar(50) DEFAULT NULL,
  `mail` varchar(50) DEFAULT NULL,
  `mobile_number` varchar(50) DEFAULT NULL,
  `profile_pic` varchar(100) DEFAULT NULL,
  `login_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`userid`,`username`,`place`,`postoffice`,`pin`,`dob`,`mail`,`mobile_number`,`profile_pic`,`login_id`) values (49,'Hiran Joseph','Kudiyanmala','Kudiyanmala',670582,'22','hiranjoe46@gmail.com','7559876583','20200326_195202.jpg',49),(53,'Null Tech','kannur','Iritty',670705,'20','sanoopsahadevan9990@gmail.com','6734545433','20200401_003143.jpg',53),(54,'Amal P Tomy','Nellikkampoil','Ulikkal',670705,'20','amal689itga@gmail.com','6282370799','20200602_151544.jpg',54);

/*Table structure for table `validity` */

DROP TABLE IF EXISTS `validity`;

CREATE TABLE `validity` (
  `val_id` int(11) NOT NULL AUTO_INCREMENT,
  `agency_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `exp_date` date DEFAULT NULL,
  `amount` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`val_id`)
) ENGINE=InnoDB AUTO_INCREMENT=86 DEFAULT CHARSET=latin1;

/*Data for the table `validity` */

insert  into `validity`(`val_id`,`agency_id`,`date`,`exp_date`,`amount`,`status`) values (3,51,NULL,NULL,NULL,'Not Payed'),(80,48,'2020-03-17','2021-03-17','999','Payed'),(81,50,'2020-03-17','2021-03-17','999','Payed'),(82,55,NULL,NULL,NULL,'Not Payed'),(83,55,NULL,NULL,NULL,'Not Payed'),(84,56,NULL,NULL,NULL,'Not Payed'),(85,57,NULL,NULL,NULL,'Not Payed');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
