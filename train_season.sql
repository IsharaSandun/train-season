-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Aug 31, 2018 at 04:30 AM
-- Server version: 5.7.19
-- PHP Version: 5.6.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `train_season`
--
CREATE DATABASE IF NOT EXISTS `train_season` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `train_season`;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

DROP TABLE IF EXISTS `admin`;
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fname` varchar(50) NOT NULL,
  `lname` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `trash` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `fname`, `lname`, `email`, `password`, `trash`) VALUES
(1, 'admin', 'admin', 'admin@gmail.com', '$5$rounds=535000$ajAsKt0V6GPueU1m$Y7clRaaqAETrrpezNnzQrQhBQPAI7B1JMWNkpDkKeR1', 0);

-- --------------------------------------------------------

--
-- Table structure for table `locations`
--

DROP TABLE IF EXISTS `locations`;
CREATE TABLE IF NOT EXISTS `locations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `locations`
--

INSERT INTO `locations` (`id`, `name`) VALUES
(1, 'Abanpola'),
(2, 'Ambeypussa'),
(3, 'Agbopura'),
(4, 'Ahangama'),
(5, 'Ahungalle'),
(6, 'Akurala'),
(7, 'Alawatupitiya'),
(8, 'Alawwa'),
(9, 'Aluthgama'),
(10, 'Ambalangoda        '),
(11, 'Ambewela           '),
(12, 'Anawilundawa       '),
(13, 'Andadola           '),
(14, 'Angampitiya        '),
(15, 'Angulana           '),
(16, 'Anuradhapura       '),
(17, 'Anuradhapura Town  '),
(18, 'Arachchikattuwa    '),
(19, 'Arukkuwatte        '),
(20, 'Aukana             '),
(21, 'Avisawella         '),
(22, 'Badulla            '),
(23, 'Balana             '),
(24, 'Balapitiya         '),
(25, 'Bambalapitiya      '),
(26, 'Bandarawela        '),
(27, 'Bangadeniya        '),
(28, 'Baseline Road      '),
(29, 'Battaluoya         '),
(30, 'Batticaloa         '),
(31, 'Batuwatte          '),
(32, 'Bemmulla           '),
(33, 'Bentota            '),
(34, 'Beruwala           '),
(35, 'Bolawatte          '),
(36, 'Boossa             '),
(37, 'Bope               '),
(38, 'Borelessa          '),
(39, 'Botale             '),
(40, 'Bulugahagoda       '),
(41, 'Buthgamuwa         '),
(42, 'Chilaw             '),
(43, 'Chinabey           '),
(44, 'Colombo Fort       '),
(45, 'Cotta Road         '),
(46, 'Daraluwa           '),
(47, 'Dehiwala           '),
(48, 'Dematagoda         '),
(49, 'Demodara           '),
(50, 'Dewapuram          '),
(51, 'Diyatalawa         '),
(52, 'Dodanduwa          '),
(53, 'Egodauyana         '),
(54, 'Elle               '),
(55, 'Enderamulla        '),
(56, 'Eravur             '),
(57, 'Erittaperiyakulam  '),
(58, 'Erukkalam pendu    '),
(59, 'Galaboda           '),
(60, 'Galgamuwa          '),
(61, 'Gallalle           '),
(62, 'Galle              '),
(63, 'Galoya Junction    '),
(64, 'Gammana            '),
(65, 'Gampaha            '),
(66, 'Gampola            '),
(67, 'Ganegoda           '),
(68, 'Ganemulla          '),
(69, 'Ganewatte          '),
(70, 'Gangoda            '),
(71, 'Gelioya            '),
(72, 'Ginthota           '),
(73, 'Girambe            '),
(74, 'Godagama           '),
(75, 'Greatwestern       '),
(76, 'Habaraduwa         '),
(77, 'Habarana           '),
(78, 'Haliela            '),
(79, 'Haputale           '),
(80, 'Hataraskotuwa      '),
(81, 'Hatton             '),
(82, 'Heeloya            '),
(83, 'Heendeniya         '),
(84, 'Hettimulla         '),
(85, 'Hikkaduwa          '),
(86, 'Hingurakgoda       '),
(87, 'Hiriyala           '),
(88, 'Homagama           '),
(89, 'Homagama Hospital  '),
(90, 'Horape             '),
(91, 'Horiwiala          '),
(92, 'Hunupitiya         '),
(93, 'Idalgasinna        '),
(94, 'Ihalakotte         '),
(95, 'Ihalawatawala      '),
(96, 'Induruwa           '),
(97, 'Inguruoya          '),
(98, 'Jaela              '),
(99, 'Jayanthipura       '),
(100, 'adadasinagar  '),
(101, 'Kadigamuwa         '),
(102, 'Kadugannawa        '),
(103, 'Kadugoda           '),
(104, 'Kahawa             '),
(105, 'Kakkapalliya       '),
(106, 'Kalawewa           '),
(107, 'Kalkudah           '),
(108, 'Kalutara North     '),
(109, 'Kaluthara South    '),
(110, 'Kamburugamuwa      '),
(111, 'Kandana            '),
(112, 'Kandegoda          '),
(113, 'Kandy              '),
(114, 'Kantale            '),
(115, 'Kapuwatte          '),
(116, 'Karadipuwal        '),
(117, 'Kathaluwa          '),
(118, 'Kattuwa            '),
(119, 'Katugastota        '),
(120, 'Katugoda           '),
(121, 'Katukurunda        '),
(122, 'Katunayaka Airport '),
(123, 'Katunayake         '),
(124, 'Keenawala          '),
(125, 'Kekirawa           '),
(126, 'Kelaniya           '),
(127, 'Kinigama           '),
(128, 'Kirulapone         '),
(129, 'Kitalelle          '),
(130, 'Kochchikade        '),
(131, 'Koggala            '),
(132, 'Kollupitiya        '),
(133, 'Kompnnavidiya      '),
(134, 'Konwewa            '),
(135, 'Koralawella        '),
(136, 'Kosgama            '),
(137, 'Kosgoda            '),
(138, 'Koshinna           '),
(139, 'Kotagala           '),
(140, 'Kottawa            '),
(141, 'Kuda wawa          '),
(142, 'Kudahakapola       '),
(143, 'Kumarakanda        '),
(144, 'Kumbalgama         '),
(145, 'Kurana             '),
(146, 'Kurunegala         '),
(147, 'Laksauyana         '),
(148, 'Liyanagemulla      '),
(149, 'Lunawa             '),
(150, 'Lunuwaila          '),
(151, 'Madampagama        '),
(152, 'Madampe            '),
(153, 'Madurankuliya      '),
(154, 'Magelegoda         '),
(155, 'Maggona            '),
(156, 'Mahaiyawa          '),
(157, 'Maharagama         '),
(158, 'Maho               '),
(159, 'Malapalle          '),
(160, 'Manampitiya        '),
(161, 'Mangalaeliya       '),
(162, 'Manuwangama        '),
(163, 'Maradana           '),
(164, 'Matale             '),
(165, 'Matara             '),
(166, 'Medagama           '),
(167, 'Medawachchiya      '),
(168, 'Meegoda            '),
(169, 'Mha Induruwa       '),
(170, 'Midigama          '),
(171, 'Mihintale          '),
(172, 'Mihintale Junction '),
(173, 'Mihirigama         '),
(174, 'Minneriya          '),
(175, 'Mirissa            '),
(176, 'Mollipatana        '),
(177, 'Moragollagama      '),
(178, 'Morakele           '),
(179, 'Moratuwa           '),
(180, 'Mount Laviniya     '),
(181, 'Mundal             '),
(182, 'Muththettugala     '),
(183, 'Nagollagama        '),
(184, 'Nailiya            '),
(185, 'Nanuoya            '),
(186, 'Narahenpita        '),
(187, 'Nattandiya         '),
(188, 'Nawalapitiya       '),
(189, 'Nawinna            '),
(190, 'Negama             '),
(191, 'Negombo            '),
(192, 'Nelumpokuna        '),
(193, 'Nooranagar         '),
(194, 'Nugegoda           '),
(195, 'Ohiya              '),
(196, 'Padukka            '),
(197, 'Palavi             '),
(198, 'Pallewala          '),
(199, 'Palugaswewa        '),
(200, 'Panagoda           '),
(201, 'Panaleeya          '),
(202, 'Pannipitiya        '),
(203, 'Parakumpura        '),
(204, 'Parasangahawewa    '),
(205, 'Patagamgoda        '),
(206, 'Pathanpha          '),
(207, 'Pattipola          '),
(208, 'Payagala North     '),
(209, 'Payagala south     '),
(210, 'Peradeniya         '),
(211, 'Perakumpura        '),
(212, 'Peralanda          '),
(213, 'Periyanagavillu    '),
(214, 'Piliduwa           '),
(215, 'Pilimatalawa       '),
(216, 'Pinnawala          '),
(217, 'Pinwatte           '),
(218, 'Piyadigama         '),
(219, 'Piyagama           '),
(220, 'Plonnaruwa         '),
(221, 'Polgahawela        '),
(222, 'Polwathumodara     '),
(223, 'Poonewa            '),
(224, 'Potuhera           '),
(225, 'Pulachchikulam     '),
(226, 'Punani             '),
(227, 'Puttalam           '),
(228, 'Puwakpitiya        '),
(229, 'Radella            '),
(230, 'Ragama             '),
(231, 'Rambukkana         '),
(232, 'Ranamuggamuwa      '),
(233, 'Randenigama        '),
(234, 'Rathgama           '),
(235, 'Rathmalana         '),
(236, 'Richmond Hill      '),
(237, 'Rosella            '),
(238, 'Saliyapura         '),
(239, 'Sarasaviuyana      '),
(240, 'Sawarana           '),
(241, 'Secretartat Halt   '),
(242, 'Seeduwa            '),
(243, 'Seenigama          '),
(244, 'Senarathgama       '),
(245, 'Sevanapitiya       '),
(246, 'Sewanapitiya       '),
(247, 'Siyalangamuwa      '),
(248, 'Srawasthipura      '),
(249, 'Talawa             '),
(250, 'Talawakele         '),
(251, 'Talawattegedara    '),
(252, 'Tampalapopla       '),
(253, 'Taple              '),
(254, 'Telwatte           '),
(255, 'Tembligala         '),
(256, 'Thambuttegama      '),
(257, 'Thilladiya         '),
(258, 'Thiranagama        '),
(259, 'Timbiriyagedara    '),
(260, 'Tismalpola         '),
(261, 'Trade Zoone        '),
(262, 'Train Halt 01      '),
(263, 'Trincomalle        '),
(264, 'Tudella            '),
(265, 'Tummodara          '),
(266, 'Udatalawinna       '),
(267, 'Udaththawala       '),
(268, 'Udhamulla          '),
(269, 'Uduwara            '),
(270, 'Uggalla            '),
(271, 'Ukuwela            '),
(272, 'Ulapone            '),
(273, 'Unawatuna          '),
(274, 'Valachchenei       '),
(275, 'Vavuniya           '),
(276, 'Veyangoda          '),
(277, 'Wadduwa            '),
(278, 'Waga               '),
(279, 'Waikkala           '),
(280, 'Walahapitiya'),
(281, 'Walgama'),
(282, 'Walpola'),
(283, 'Wanawasala'),
(284, 'Wandurawa'),
(285, 'Watagoda'),
(286, 'Watareka'),
(287, 'Watawala'),
(288, 'Wattegama'),
(289, 'Weligama'),
(290, 'Welikanda'),
(291, 'Wellawa'),
(292, 'Wellawatte'),
(293, 'Wijayarajadahana'),
(294, 'Wilwatte'),
(295, 'Wlakubura'),
(296, 'Yagoda'),
(297, 'Yapahuwa'),
(298, 'Yatagama'),
(299, 'Yattalgoda');

-- --------------------------------------------------------

--
-- Table structure for table `season`
--

DROP TABLE IF EXISTS `season`;
CREATE TABLE IF NOT EXISTS `season` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `location_from` int(11) NOT NULL,
  `location_to` int(11) NOT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `amount` float DEFAULT NULL,
  `date_payment` datetime DEFAULT NULL,
  `class` int(1) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `season_id` varchar(10) DEFAULT NULL,
  `fname` varchar(20) NOT NULL,
  `lname` varchar(20) NOT NULL,
  `tp` varchar(15) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `pending` tinyint(1) DEFAULT '1',
  `trash` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `season_id` (`season_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
