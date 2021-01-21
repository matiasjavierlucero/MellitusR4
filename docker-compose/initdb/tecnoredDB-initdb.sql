-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: plan-management-db:3306
-- Generation Time: Jan 21, 2021 at 08:51 PM
-- Server version: 5.7.32
-- PHP Version: 7.4.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tecnoredDB`
--

-- --------------------------------------------------------

--
-- Table structure for table `ab_permission`
--

CREATE TABLE IF NOT EXISTS `ab_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ab_permission`
--

INSERT INTO `ab_permission` (`id`, `name`) VALUES
(22, 'can_add'),
(45, 'can_chart'),
(49, 'can_chartDigestores'),
(7, 'can_delete'),
(13, 'can_download'),
(19, 'can_edit'),
(46, 'can_get'),
(25, 'can_list'),
(47, 'can_method3'),
(16, 'can_show'),
(1, 'can_this_form_get'),
(4, 'can_this_form_post'),
(10, 'can_userinfo'),
(43, 'copyrole'),
(28, 'down_excel'),
(40, 'menu_access'),
(31, 'resetmypassword'),
(34, 'resetpasswords'),
(37, 'userinfoedit');

-- --------------------------------------------------------

--
-- Table structure for table `ab_permission_view`
--

CREATE TABLE IF NOT EXISTS `ab_permission_view` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_id` int(11) DEFAULT NULL,
  `view_menu_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission_id` (`permission_id`,`view_menu_id`),
  KEY `view_menu_id` (`view_menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=995 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ab_permission_view`
--

INSERT INTO `ab_permission_view` (`id`, `permission_id`, `view_menu_id`) VALUES
(2, NULL, 12),
(3, NULL, 12),
(4, NULL, 12),
(6, NULL, 12),
(18, NULL, 21),
(19, NULL, 21),
(21, NULL, 21),
(22, NULL, 21),
(24, NULL, 21),
(25, NULL, 21),
(27, NULL, 21),
(28, NULL, 21),
(30, NULL, 21),
(31, NULL, 21),
(33, NULL, 21),
(34, NULL, 21),
(35, NULL, 21),
(37, NULL, 21),
(39, NULL, 21),
(40, NULL, 21),
(42, NULL, 21),
(43, NULL, 21),
(45, NULL, 21),
(46, NULL, 21),
(48, NULL, 21),
(49, NULL, 21),
(51, NULL, 24),
(52, NULL, 24),
(69, NULL, 29),
(531, NULL, 169),
(1, 1, 12),
(7, 1, 15),
(12, 1, 18),
(5, 4, 12),
(10, 4, 15),
(15, 4, 18),
(17, 7, 21),
(56, 7, 29),
(95, 7, 54),
(110, 7, 57),
(126, 7, 60),
(146, 7, 66),
(158, 7, 69),
(170, 7, 72),
(187, 7, 76),
(202, 7, 79),
(215, 7, 82),
(234, 7, 88),
(250, 7, 92),
(263, 7, 95),
(280, 7, 101),
(294, 7, 105),
(308, 7, 109),
(322, 7, 113),
(337, 7, 118),
(353, 7, 122),
(373, 7, 128),
(390, 7, 132),
(406, 7, 136),
(422, 7, 140),
(438, 7, 144),
(454, 7, 149),
(469, 7, 153),
(486, 7, 157),
(501, 7, 161),
(514, 7, 165),
(538, 7, 174),
(555, 7, 177),
(571, 7, 182),
(595, 7, 192),
(611, 7, 197),
(626, 7, 201),
(641, 7, 205),
(660, 7, 213),
(675, 7, 217),
(692, 7, 221),
(707, 7, 225),
(721, 7, 229),
(736, 7, 233),
(753, 7, 238),
(770, 7, 248),
(793, 7, 256),
(808, 7, 261),
(821, 7, 265),
(835, 7, 269),
(850, 7, 275),
(865, 7, 279),
(880, 7, 283),
(895, 7, 288),
(910, 7, 293),
(924, 7, 298),
(936, 7, 302),
(951, 7, 307),
(966, 7, 311),
(981, 7, 315),
(20, 10, 21),
(23, 13, 21),
(58, 13, 29),
(98, 13, 54),
(113, 13, 57),
(128, 13, 60),
(148, 13, 66),
(160, 13, 69),
(172, 13, 72),
(190, 13, 76),
(204, 13, 79),
(217, 13, 82),
(236, 13, 88),
(253, 13, 92),
(265, 13, 95),
(281, 13, 101),
(296, 13, 105),
(311, 13, 109),
(325, 13, 113),
(339, 13, 118),
(355, 13, 122),
(376, 13, 128),
(392, 13, 132),
(409, 13, 136),
(425, 13, 140),
(441, 13, 144),
(456, 13, 149),
(471, 13, 153),
(488, 13, 157),
(503, 13, 161),
(517, 13, 165),
(540, 13, 174),
(557, 13, 177),
(573, 13, 182),
(597, 13, 192),
(614, 13, 197),
(629, 13, 201),
(644, 13, 205),
(663, 13, 213),
(678, 13, 217),
(693, 13, 221),
(708, 13, 225),
(724, 13, 229),
(739, 13, 233),
(755, 13, 238),
(773, 13, 248),
(795, 13, 256),
(810, 13, 261),
(823, 13, 265),
(837, 13, 269),
(852, 13, 275),
(867, 13, 279),
(882, 13, 283),
(896, 13, 288),
(911, 13, 293),
(926, 13, 298),
(939, 13, 302),
(953, 13, 307),
(968, 13, 311),
(983, 13, 315),
(26, 16, 21),
(59, 16, 29),
(100, 16, 54),
(115, 16, 57),
(129, 16, 60),
(149, 16, 66),
(161, 16, 69),
(173, 16, 72),
(192, 16, 76),
(205, 16, 79),
(218, 16, 82),
(237, 16, 88),
(255, 16, 92),
(266, 16, 95),
(282, 16, 101),
(297, 16, 105),
(313, 16, 109),
(327, 16, 113),
(340, 16, 118),
(356, 16, 122),
(378, 16, 128),
(393, 16, 132),
(411, 16, 136),
(427, 16, 140),
(443, 16, 144),
(457, 16, 149),
(472, 16, 153),
(489, 16, 157),
(504, 16, 161),
(519, 16, 165),
(542, 16, 174),
(558, 16, 177),
(574, 16, 182),
(598, 16, 192),
(616, 16, 197),
(631, 16, 201),
(646, 16, 205),
(665, 16, 213),
(680, 16, 217),
(696, 16, 221),
(710, 16, 225),
(726, 16, 229),
(741, 16, 233),
(756, 16, 238),
(775, 16, 248),
(796, 16, 256),
(811, 16, 261),
(824, 16, 265),
(838, 16, 269),
(853, 16, 275),
(868, 16, 279),
(883, 16, 283),
(899, 16, 288),
(913, 16, 293),
(927, 16, 298),
(941, 16, 302),
(954, 16, 307),
(969, 16, 311),
(984, 16, 315),
(29, 19, 21),
(62, 19, 29),
(101, 19, 54),
(117, 19, 57),
(132, 19, 60),
(152, 19, 66),
(164, 19, 69),
(176, 19, 72),
(193, 19, 76),
(208, 19, 79),
(221, 19, 82),
(240, 19, 88),
(256, 19, 92),
(268, 19, 95),
(285, 19, 101),
(300, 19, 105),
(314, 19, 109),
(328, 19, 113),
(343, 19, 118),
(359, 19, 122),
(379, 19, 128),
(396, 19, 132),
(412, 19, 136),
(428, 19, 140),
(444, 19, 144),
(459, 19, 149),
(475, 19, 153),
(491, 19, 157),
(506, 19, 161),
(520, 19, 165),
(544, 19, 174),
(560, 19, 177),
(577, 19, 182),
(601, 19, 192),
(617, 19, 197),
(632, 19, 201),
(647, 19, 205),
(666, 19, 213),
(681, 19, 217),
(698, 19, 221),
(712, 19, 225),
(727, 19, 229),
(743, 19, 233),
(757, 19, 238),
(776, 19, 248),
(798, 19, 256),
(813, 19, 261),
(826, 19, 265),
(841, 19, 269),
(854, 19, 275),
(869, 19, 279),
(884, 19, 283),
(901, 19, 288),
(914, 19, 293),
(929, 19, 298),
(942, 19, 302),
(955, 19, 307),
(970, 19, 311),
(986, 19, 315),
(32, 22, 21),
(64, 22, 29),
(104, 22, 54),
(120, 22, 57),
(134, 22, 60),
(154, 22, 66),
(166, 22, 69),
(178, 22, 72),
(196, 22, 76),
(210, 22, 79),
(223, 22, 82),
(242, 22, 88),
(259, 22, 92),
(269, 22, 95),
(288, 22, 101),
(302, 22, 105),
(316, 22, 109),
(331, 22, 113),
(345, 22, 118),
(361, 22, 122),
(382, 22, 128),
(398, 22, 132),
(414, 22, 136),
(430, 22, 140),
(447, 22, 144),
(460, 22, 149),
(476, 22, 153),
(492, 22, 157),
(507, 22, 161),
(523, 22, 165),
(546, 22, 174),
(562, 22, 177),
(579, 22, 182),
(603, 22, 192),
(619, 22, 197),
(634, 22, 201),
(648, 22, 205),
(668, 22, 213),
(684, 22, 217),
(699, 22, 221),
(714, 22, 225),
(729, 22, 229),
(744, 22, 233),
(760, 22, 238),
(779, 22, 248),
(799, 22, 256),
(814, 22, 261),
(827, 22, 265),
(843, 22, 269),
(857, 22, 275),
(872, 22, 279),
(887, 22, 283),
(902, 22, 288),
(917, 22, 293),
(930, 22, 298),
(945, 22, 302),
(958, 22, 307),
(973, 22, 311),
(987, 22, 315),
(36, 25, 21),
(65, 25, 29),
(79, 25, 38),
(84, 25, 42),
(88, 25, 46),
(106, 25, 54),
(122, 25, 57),
(135, 25, 60),
(155, 25, 66),
(167, 25, 69),
(179, 25, 72),
(198, 25, 76),
(213, 25, 79),
(224, 25, 82),
(243, 25, 88),
(261, 25, 92),
(272, 25, 95),
(290, 25, 101),
(303, 25, 105),
(317, 25, 109),
(333, 25, 113),
(346, 25, 118),
(362, 25, 122),
(384, 25, 128),
(399, 25, 132),
(415, 25, 136),
(431, 25, 140),
(449, 25, 144),
(463, 25, 149),
(478, 25, 153),
(495, 25, 157),
(510, 25, 161),
(525, 25, 165),
(549, 25, 174),
(565, 25, 177),
(580, 25, 182),
(604, 25, 192),
(620, 25, 197),
(635, 25, 201),
(651, 25, 205),
(669, 25, 213),
(686, 25, 217),
(701, 25, 221),
(716, 25, 225),
(730, 25, 229),
(747, 25, 233),
(762, 25, 238),
(781, 25, 248),
(802, 25, 256),
(815, 25, 261),
(830, 25, 265),
(844, 25, 269),
(859, 25, 275),
(874, 25, 279),
(889, 25, 283),
(904, 25, 288),
(919, 25, 293),
(933, 25, 298),
(947, 25, 302),
(960, 25, 307),
(975, 25, 311),
(990, 25, 315),
(38, 28, 21),
(107, 28, 54),
(123, 28, 57),
(138, 28, 60),
(182, 28, 72),
(199, 28, 76),
(227, 28, 82),
(246, 28, 88),
(262, 28, 92),
(349, 28, 118),
(365, 28, 122),
(385, 28, 128),
(402, 28, 132),
(418, 28, 136),
(434, 28, 140),
(450, 28, 144),
(465, 28, 149),
(480, 28, 153),
(497, 28, 157),
(526, 28, 165),
(551, 28, 174),
(567, 28, 177),
(583, 28, 182),
(607, 28, 192),
(623, 28, 197),
(638, 28, 201),
(653, 28, 205),
(672, 28, 213),
(687, 28, 217),
(702, 28, 221),
(718, 28, 225),
(733, 28, 229),
(749, 28, 233),
(763, 28, 238),
(782, 28, 248),
(804, 28, 256),
(817, 28, 261),
(832, 28, 265),
(846, 28, 269),
(860, 28, 275),
(875, 28, 279),
(890, 28, 283),
(905, 28, 288),
(920, 28, 293),
(961, 28, 307),
(976, 28, 311),
(992, 28, 315),
(41, 31, 21),
(44, 34, 21),
(47, 37, 21),
(50, 40, 24),
(53, 40, 27),
(71, 40, 32),
(76, 40, 37),
(81, 40, 41),
(86, 40, 45),
(91, 40, 49),
(140, 40, 63),
(143, 40, 64),
(184, 40, 75),
(229, 40, 84),
(231, 40, 85),
(248, 40, 91),
(274, 40, 98),
(277, 40, 99),
(291, 40, 103),
(305, 40, 108),
(319, 40, 112),
(334, 40, 116),
(351, 40, 121),
(367, 40, 125),
(370, 40, 126),
(387, 40, 131),
(404, 40, 135),
(420, 40, 139),
(436, 40, 143),
(451, 40, 147),
(466, 40, 152),
(483, 40, 156),
(498, 40, 160),
(512, 40, 164),
(528, 40, 168),
(534, 40, 172),
(536, 40, 173),
(552, 40, 176),
(568, 40, 180),
(585, 40, 185),
(590, 40, 189),
(592, 40, 191),
(625, 40, 200),
(640, 40, 204),
(654, 40, 208),
(659, 40, 212),
(674, 40, 216),
(690, 40, 220),
(705, 40, 224),
(719, 40, 227),
(735, 40, 232),
(750, 40, 236),
(764, 40, 241),
(769, 40, 247),
(785, 40, 251),
(790, 40, 254),
(805, 40, 259),
(818, 40, 264),
(833, 40, 268),
(847, 40, 272),
(862, 40, 278),
(877, 40, 282),
(893, 40, 286),
(908, 40, 291),
(921, 40, 296),
(935, 40, 301),
(948, 40, 305),
(963, 40, 310),
(978, 40, 314),
(993, 40, 318),
(68, 43, 29),
(74, 45, 34),
(94, 46, 51),
(532, 47, 169),
(609, 47, 195),
(657, 47, 209),
(767, 47, 244),
(587, 49, 186),
(787, 49, 253);

-- --------------------------------------------------------

--
-- Table structure for table `ab_permission_view_role`
--

CREATE TABLE IF NOT EXISTS `ab_permission_view_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `permission_view_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `permission_view_id` (`permission_view_id`,`role_id`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=945 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ab_permission_view_role`
--

INSERT INTO `ab_permission_view_role` (`id`, `permission_view_id`, `role_id`) VALUES
(2, 1, 1),
(1, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1),
(6, 6, 1),
(7, 7, 1),
(8, 10, 1),
(10, 12, 1),
(11, 15, 1),
(13, 17, 1),
(15, 18, 1),
(14, 19, 1),
(16, 20, 1),
(18, 21, 1),
(17, 22, 1),
(20, 23, 1),
(21, 24, 1),
(19, 25, 1),
(24, 26, 1),
(23, 27, 1),
(22, 28, 1),
(27, 29, 1),
(26, 30, 1),
(25, 31, 1),
(30, 32, 1),
(28, 33, 1),
(29, 34, 1),
(31, 35, 1),
(33, 36, 1),
(32, 37, 1),
(34, 38, 1),
(35, 39, 1),
(36, 40, 1),
(37, 41, 1),
(39, 42, 1),
(38, 43, 1),
(41, 44, 1),
(42, 45, 1),
(40, 46, 1),
(43, 47, 1),
(45, 48, 1),
(44, 49, 1),
(47, 50, 1),
(46, 51, 1),
(48, 52, 1),
(49, 53, 1),
(50, 56, 1),
(52, 58, 1),
(55, 59, 1),
(56, 62, 1),
(58, 64, 1),
(61, 65, 1),
(62, 68, 1),
(63, 69, 1),
(64, 71, 1),
(65, 74, 1),
(67, 76, 1),
(68, 79, 1),
(70, 81, 1),
(71, 84, 1),
(73, 86, 1),
(75, 88, 1),
(76, 91, 1),
(77, 94, 1),
(80, 95, 1),
(81, 98, 1),
(83, 100, 1),
(86, 101, 1),
(87, 104, 1),
(89, 106, 1),
(92, 107, 1),
(93, 110, 1),
(94, 113, 1),
(96, 115, 1),
(98, 117, 1),
(99, 120, 1),
(101, 122, 1),
(104, 123, 1),
(105, 126, 1),
(107, 128, 1),
(110, 129, 1),
(111, 132, 1),
(113, 134, 1),
(116, 135, 1),
(117, 138, 1),
(119, 140, 1),
(120, 143, 1),
(121, 146, 1),
(123, 148, 1),
(126, 149, 1),
(127, 152, 1),
(129, 154, 1),
(132, 155, 1),
(133, 158, 1),
(135, 160, 1),
(138, 161, 1),
(139, 164, 1),
(141, 166, 1),
(144, 167, 1),
(145, 170, 1),
(147, 172, 1),
(150, 173, 1),
(151, 176, 1),
(153, 178, 1),
(156, 179, 1),
(157, 182, 1),
(159, 184, 1),
(160, 187, 1),
(161, 190, 1),
(163, 192, 1),
(166, 193, 1),
(167, 196, 1),
(169, 198, 1),
(172, 199, 1),
(173, 202, 1),
(175, 204, 1),
(178, 205, 1),
(179, 208, 1),
(180, 210, 1),
(181, 213, 1),
(183, 215, 1),
(185, 217, 1),
(188, 218, 1),
(189, 221, 1),
(191, 223, 1),
(194, 224, 1),
(195, 227, 1),
(197, 229, 1),
(199, 231, 1),
(200, 234, 1),
(202, 236, 1),
(205, 237, 1),
(206, 240, 1),
(208, 242, 1),
(211, 243, 1),
(212, 246, 1),
(214, 248, 1),
(216, 250, 1),
(217, 253, 1),
(219, 255, 1),
(221, 256, 1),
(222, 259, 1),
(223, 261, 1),
(225, 262, 1),
(228, 263, 1),
(229, 265, 1),
(232, 266, 1),
(234, 268, 1),
(237, 269, 1),
(238, 272, 1),
(240, 274, 1),
(242, 277, 1),
(241, 280, 1),
(243, 281, 1),
(244, 282, 1),
(245, 285, 1),
(246, 288, 1),
(248, 290, 1),
(251, 291, 1),
(252, 294, 1),
(254, 296, 1),
(257, 297, 1),
(258, 300, 1),
(260, 302, 1),
(263, 303, 1),
(265, 305, 1),
(266, 308, 1),
(267, 311, 1),
(269, 313, 1),
(272, 314, 1),
(274, 316, 1),
(277, 317, 1),
(279, 319, 1),
(280, 322, 1),
(281, 325, 1),
(283, 327, 1),
(286, 328, 1),
(287, 331, 1),
(289, 333, 1),
(292, 334, 1),
(293, 337, 1),
(295, 339, 1),
(298, 340, 1),
(299, 343, 1),
(301, 345, 1),
(304, 346, 1),
(305, 349, 1),
(307, 351, 1),
(309, 353, 1),
(311, 355, 1),
(314, 356, 1),
(315, 359, 1),
(317, 361, 1),
(319, 362, 1),
(320, 365, 1),
(322, 367, 1),
(323, 370, 1),
(324, 373, 1),
(325, 376, 1),
(327, 378, 1),
(330, 379, 1),
(331, 382, 1),
(333, 384, 1),
(335, 385, 1),
(337, 387, 1),
(338, 390, 1),
(340, 392, 1),
(343, 393, 1),
(344, 396, 1),
(346, 398, 1),
(349, 399, 1),
(350, 402, 1),
(352, 404, 1),
(354, 406, 1),
(355, 409, 1),
(357, 411, 1),
(360, 412, 1),
(362, 414, 1),
(365, 415, 1),
(366, 418, 1),
(368, 420, 1),
(370, 422, 1),
(371, 425, 1),
(373, 427, 1),
(376, 428, 1),
(378, 430, 1),
(381, 431, 1),
(382, 434, 1),
(384, 436, 1),
(386, 438, 1),
(387, 441, 1),
(389, 443, 1),
(391, 444, 1),
(392, 447, 1),
(394, 449, 1),
(397, 450, 1),
(400, 451, 1),
(401, 454, 1),
(403, 456, 1),
(406, 457, 1),
(408, 459, 1),
(411, 460, 1),
(412, 463, 1),
(414, 465, 1),
(417, 466, 1),
(418, 469, 1),
(420, 471, 1),
(423, 472, 1),
(424, 475, 1),
(426, 476, 1),
(427, 478, 1),
(429, 480, 1),
(430, 483, 1),
(431, 486, 1),
(433, 488, 1),
(435, 489, 1),
(437, 491, 1),
(440, 492, 1),
(441, 495, 1),
(443, 497, 1),
(446, 498, 1),
(447, 501, 1),
(449, 503, 1),
(452, 504, 1),
(454, 506, 1),
(457, 507, 1),
(458, 510, 1),
(460, 512, 1),
(462, 514, 1),
(463, 517, 1),
(465, 519, 1),
(467, 520, 1),
(468, 523, 1),
(470, 525, 1),
(473, 526, 1),
(475, 528, 1),
(476, 531, 1),
(477, 532, 1),
(478, 534, 1),
(479, 536, 1),
(481, 538, 1),
(482, 540, 1),
(484, 542, 1),
(485, 544, 1),
(488, 546, 1),
(489, 549, 1),
(491, 551, 1),
(494, 552, 1),
(495, 555, 1),
(496, 557, 1),
(498, 558, 1),
(499, 560, 1),
(502, 562, 1),
(503, 565, 1),
(505, 567, 1),
(507, 568, 1),
(508, 571, 1),
(510, 573, 1),
(513, 574, 1),
(514, 577, 1),
(516, 579, 1),
(519, 580, 1),
(520, 583, 1),
(522, 585, 1),
(524, 587, 1),
(525, 590, 1),
(527, 592, 1),
(528, 595, 1),
(530, 597, 1),
(533, 598, 1),
(534, 601, 1),
(536, 603, 1),
(538, 604, 1),
(539, 607, 1),
(541, 609, 1),
(543, 611, 1),
(544, 614, 1),
(546, 616, 1),
(548, 617, 1),
(550, 619, 1),
(553, 620, 1),
(554, 623, 1),
(556, 625, 1),
(559, 626, 1),
(560, 629, 1),
(562, 631, 1),
(564, 632, 1),
(566, 634, 1),
(569, 635, 1),
(570, 638, 1),
(572, 640, 1),
(575, 641, 1),
(576, 644, 1),
(578, 646, 1),
(581, 647, 1),
(584, 648, 1),
(585, 651, 1),
(587, 653, 1),
(590, 654, 1),
(591, 657, 1),
(593, 659, 1),
(596, 660, 1),
(597, 663, 1),
(599, 665, 1),
(601, 666, 1),
(603, 668, 1),
(606, 669, 1),
(607, 672, 1),
(609, 674, 1),
(612, 675, 1),
(613, 678, 1),
(614, 680, 1),
(617, 681, 1),
(618, 684, 1),
(620, 686, 1),
(622, 687, 1),
(623, 690, 1),
(625, 692, 1),
(628, 693, 1),
(629, 696, 1),
(631, 698, 1),
(633, 699, 1),
(635, 701, 1),
(638, 702, 1),
(639, 705, 1),
(641, 707, 1),
(643, 708, 1),
(644, 710, 1),
(646, 712, 1),
(647, 714, 1),
(650, 716, 1),
(652, 718, 1),
(655, 719, 1),
(657, 721, 1),
(658, 724, 1),
(660, 726, 1),
(662, 727, 1),
(664, 729, 1),
(667, 730, 1),
(668, 733, 1),
(670, 735, 1),
(673, 736, 1),
(674, 739, 1),
(675, 741, 1),
(677, 743, 1),
(680, 744, 1),
(681, 747, 1),
(683, 749, 1),
(685, 750, 1),
(686, 753, 1),
(688, 755, 1),
(691, 756, 1),
(694, 757, 1),
(695, 760, 1),
(697, 762, 1),
(700, 763, 1),
(703, 764, 1),
(706, 767, 1),
(708, 769, 1),
(711, 770, 1),
(712, 773, 1),
(714, 775, 1),
(716, 776, 1),
(717, 779, 1),
(719, 781, 1),
(722, 782, 1),
(723, 785, 1),
(725, 787, 1),
(726, 790, 1),
(727, 793, 1),
(729, 795, 1),
(731, 796, 1),
(733, 798, 1),
(736, 799, 1),
(737, 802, 1),
(739, 804, 1),
(741, 805, 1),
(742, 808, 1),
(744, 810, 1),
(746, 811, 1),
(747, 813, 1),
(750, 814, 1),
(753, 815, 1),
(755, 817, 1),
(758, 818, 1),
(759, 821, 1),
(761, 823, 1),
(763, 824, 1),
(765, 826, 1),
(768, 827, 1),
(769, 830, 1),
(770, 832, 1),
(772, 833, 1),
(774, 835, 1),
(775, 837, 1),
(778, 838, 1),
(779, 841, 1),
(781, 843, 1),
(784, 844, 1),
(786, 846, 1),
(789, 847, 1),
(790, 850, 1),
(792, 852, 1),
(795, 853, 1),
(798, 854, 1),
(799, 857, 1),
(801, 859, 1),
(803, 860, 1),
(805, 862, 1),
(806, 865, 1),
(808, 867, 1),
(811, 868, 1),
(814, 869, 1),
(815, 872, 1),
(817, 874, 1),
(819, 875, 1),
(821, 877, 1),
(822, 880, 1),
(824, 882, 1),
(827, 883, 1),
(830, 884, 1),
(831, 887, 1),
(833, 889, 1),
(835, 890, 1),
(836, 893, 1),
(838, 895, 1),
(841, 896, 1),
(842, 899, 1),
(844, 901, 1),
(846, 902, 1),
(848, 904, 1),
(851, 905, 1),
(852, 908, 1),
(854, 910, 1),
(857, 911, 1),
(859, 913, 1),
(862, 914, 1),
(863, 917, 1),
(865, 919, 1),
(868, 920, 1),
(871, 921, 1),
(872, 924, 1),
(874, 926, 1),
(876, 927, 1),
(878, 929, 1),
(881, 930, 1),
(882, 933, 1),
(884, 935, 1),
(887, 936, 1),
(888, 939, 1),
(890, 941, 1),
(891, 942, 1),
(892, 945, 1),
(894, 947, 1),
(896, 948, 1),
(897, 951, 1),
(899, 953, 1),
(902, 954, 1),
(905, 955, 1),
(906, 958, 1),
(908, 960, 1),
(910, 961, 1),
(912, 963, 1),
(913, 966, 1),
(915, 968, 1),
(918, 969, 1),
(921, 970, 1),
(922, 973, 1),
(924, 975, 1),
(926, 976, 1),
(928, 978, 1),
(929, 981, 1),
(931, 983, 1),
(933, 984, 1),
(935, 986, 1),
(938, 987, 1),
(939, 990, 1),
(941, 992, 1),
(943, 993, 1);

-- --------------------------------------------------------

--
-- Table structure for table `ab_register_user`
--

CREATE TABLE IF NOT EXISTS `ab_register_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `email` varchar(64) NOT NULL,
  `registration_date` datetime DEFAULT NULL,
  `registration_hash` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ab_role`
--

CREATE TABLE IF NOT EXISTS `ab_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ab_role`
--

INSERT INTO `ab_role` (`id`, `name`) VALUES
(1, 'Admin'),
(2, 'Public');

-- --------------------------------------------------------

--
-- Table structure for table `ab_user`
--

CREATE TABLE IF NOT EXISTS `ab_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(64) NOT NULL,
  `last_name` varchar(64) NOT NULL,
  `username` varchar(64) NOT NULL,
  `password` varchar(256) DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `email` varchar(64) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `login_count` int(11) DEFAULT NULL,
  `fail_login_count` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `changed_on` datetime DEFAULT NULL,
  `created_by_fk` int(11) DEFAULT NULL,
  `changed_by_fk` int(11) DEFAULT NULL,
  `idTdni` int(11) NOT NULL,
  `idPais` int(11) NOT NULL,
  `idProfesion` int(11) NOT NULL,
  `numerodniUser` varchar(50) NOT NULL,
  `celUser` varchar(50) DEFAULT NULL,
  `fnacimientoUser` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `numerodniUser` (`numerodniUser`),
  KEY `created_by_fk` (`created_by_fk`),
  KEY `changed_by_fk` (`changed_by_fk`),
  KEY `idTdni` (`idTdni`),
  KEY `idPais` (`idPais`),
  KEY `idProfesion` (`idProfesion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ab_user_role`
--

CREATE TABLE IF NOT EXISTS `ab_user_role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`role_id`),
  KEY `role_id` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `ab_view_menu`
--

CREATE TABLE IF NOT EXISTS `ab_view_menu` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=320 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `ab_view_menu`
--

INSERT INTO `ab_view_menu` (`id`, `name`) VALUES
(118, 'Agitador16View'),
(121, 'Agitadores'),
(125, 'Analisis quimico'),
(122, 'AnalisisquimicoView'),
(131, 'Analizadores de gas'),
(128, 'Analizadorgas17View'),
(132, 'Antorcha11View'),
(135, 'Antorchas'),
(126, 'Área/Planta'),
(108, 'Áreas'),
(76, 'AreaView'),
(105, 'Area_PlanView'),
(20, 'AuthDBView'),
(41, 'Base Permissions'),
(136, 'Bomba5View'),
(139, 'Bombas'),
(143, 'Caldera'),
(140, 'Caldera6View'),
(147, 'Campaña'),
(144, 'CampaniaView'),
(156, 'carga-merma'),
(253, 'CargaMasivastsvView'),
(186, 'CargaMasivaView'),
(153, 'CargamermaView'),
(149, 'Caudalimetro26View'),
(152, 'Caudalimetros'),
(173, 'Charts'),
(195, 'ChartView'),
(157, 'Chiller13View'),
(160, 'Chillers'),
(164, 'Combusibles'),
(161, 'CombustibleView'),
(168, 'Compresor de aire'),
(165, 'Compresoraire22View'),
(99, 'Conf. Planta'),
(64, 'Consultor'),
(63, 'Consultora'),
(60, 'ConsultoraView'),
(174, 'Deposito14View'),
(176, 'Depósitos'),
(180, 'Desulfurizador'),
(177, 'Desulfurizador18View'),
(182, 'Digestor1View'),
(185, 'Digestores'),
(85, 'Equipos'),
(116, 'Estado equipos'),
(113, 'EstadoqView'),
(197, 'Filtrobiogas19View'),
(200, 'Filtros Biogas'),
(191, 'Fos/Tac'),
(189, 'FosTac Carga Masiva'),
(192, 'FostacView'),
(172, 'Inca'),
(169, 'incaView'),
(201, 'Intdecalor7View'),
(204, 'Intercambiador de calor'),
(32, 'List Roles'),
(24, 'List Users'),
(6, 'LocaleView'),
(57, 'LocalidadView'),
(112, 'Marcas'),
(109, 'MarcaView'),
(51, 'MenuApi'),
(247, 'Merma'),
(244, 'mermaView'),
(103, 'Mis Plantas'),
(101, 'MisPlantasView'),
(212, 'Motor'),
(205, 'Motor2View'),
(208, 'Motores'),
(209, 'motoresView'),
(1, 'MyIndexView'),
(21, 'MyUserDBModelView'),
(66, 'PaisView'),
(213, 'Palacargadora24View'),
(216, 'Palas cargadoras'),
(49, 'Permission on Views/Menus'),
(38, 'PermissionModelView'),
(46, 'PermissionViewModelView'),
(92, 'PlantaequipoView'),
(98, 'Plantas'),
(95, 'PlantaView'),
(79, 'PlanUsuaView'),
(75, 'Profesiones'),
(72, 'ProfesionView'),
(54, 'ProvinciaView'),
(217, 'Regador3View'),
(220, 'Regadores'),
(224, 'Relacion Equipos'),
(221, 'RelacionequipoView'),
(15, 'ResetMyPasswordView'),
(12, 'ResetPasswordView'),
(29, 'RoleModelView'),
(27, 'Security'),
(9, 'SecurityApi'),
(225, 'Separador9View'),
(227, 'Separadores'),
(229, 'sopbiogas8View'),
(233, 'Sopdetecho15View'),
(236, 'Soplador de techo'),
(232, 'Sopladora Biogas'),
(251, 'Stsv'),
(254, 'stsvCargaMasiva'),
(248, 'StsvView'),
(91, 'Super equipos'),
(88, 'SuperequipoView'),
(241, 'Sustrato'),
(238, 'SustratoView'),
(259, 'Tablero eléctrico'),
(256, 'Tableroelectrico21View'),
(283, 'TbombaView'),
(69, 'TdniView'),
(278, 'Tipo Agitador'),
(286, 'Tipo Bombas'),
(282, 'Tipo Cámaras'),
(291, 'Tipo caudal'),
(296, 'Tipo construcción'),
(275, 'TipoagitadorView'),
(279, 'TipocamaraView'),
(288, 'TipocaudalView'),
(293, 'TipoconstruccionView'),
(82, 'TipoequipoView'),
(84, 'Tipos equipo'),
(301, 'Tipos tablero'),
(298, 'TipotableroView'),
(268, 'Tolva'),
(265, 'Tolva23View'),
(261, 'Tractor4View'),
(264, 'Tractores'),
(269, 'Transformador20View'),
(272, 'Transformadores'),
(305, 'Unidades de Medida Sustrato'),
(302, 'UnidadmedidaView'),
(37, 'User\'s Statistics'),
(18, 'UserInfoEditView'),
(34, 'UserStatsChartView'),
(4, 'UtilView'),
(315, 'Valtresvias25View'),
(311, 'Valvdepresion12View'),
(314, 'Válvulas de presión'),
(318, 'Valvulas tres vias'),
(307, 'Vehiculo10View'),
(310, 'Vehículos'),
(42, 'ViewMenuModelView'),
(45, 'Views/Menus');

-- --------------------------------------------------------

--
-- Table structure for table `agitador16`
--

CREATE TABLE IF NOT EXISTS `agitador16` (
  `idAgitador16` int(11) NOT NULL AUTO_INCREMENT,
  `potenciaAgitador16` float DEFAULT NULL,
  `idSuperequipo` int(11) NOT NULL,
  `idTipoagitador` int(11) NOT NULL,
  PRIMARY KEY (`idAgitador16`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idTipoagitador` (`idTipoagitador`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `analisisquimico`
--

CREATE TABLE IF NOT EXISTS `analisisquimico` (
  `idAnalisisquimico` int(11) NOT NULL AUTO_INCREMENT,
  `fechaAnalisisquimico` date NOT NULL,
  `tipoAnalisisquimico` tinyint(1) NOT NULL,
  `nitorgAnalisisquimico` float NOT NULL,
  `penfosAnalisisquimico` float NOT NULL,
  `diopotAnalisisquimico` float NOT NULL,
  `matorgAnalisisquimico` float NOT NULL,
  `obsAnalisisquimico` varchar(250) DEFAULT NULL,
  `idUsuarioM` int(11) NOT NULL,
  `fcargaAnalisisquimico` date NOT NULL,
  `idPlanta` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idAnalisisquimico`),
  KEY `idUsuarioM` (`idUsuarioM`),
  KEY `idPlanta` (`idPlanta`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `analizadorgas17`
--

CREATE TABLE IF NOT EXISTS `analizadorgas17` (
  `idAnalizadorgas17` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `canalesAnalizadorgas17` int(11) NOT NULL,
  PRIMARY KEY (`idAnalizadorgas17`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `antorcha11`
--

CREATE TABLE IF NOT EXISTS `antorcha11` (
  `idAntorcha11` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `capacidadAntorcha11` float NOT NULL,
  PRIMARY KEY (`idAntorcha11`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `area`
--

CREATE TABLE IF NOT EXISTS `area` (
  `idArea` int(11) NOT NULL AUTO_INCREMENT,
  `nombreArea` varchar(100) NOT NULL,
  `descripcionArea` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`idArea`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `area_plan`
--

CREATE TABLE IF NOT EXISTS `area_plan` (
  `idArea_plan` int(11) NOT NULL AUTO_INCREMENT,
  `idPlanta` int(11) NOT NULL,
  `idArea` int(11) NOT NULL,
  `fechacargaArea_plan` date DEFAULT NULL,
  PRIMARY KEY (`idArea_plan`),
  KEY `idPlanta` (`idPlanta`),
  KEY `idArea` (`idArea`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `bomba5`
--

CREATE TABLE IF NOT EXISTS `bomba5` (
  `idBomba5` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperEquipo` int(11) NOT NULL,
  `idTbomba` int(11) NOT NULL,
  `caudalBomba5` float NOT NULL,
  `cansolidoBomba5` float NOT NULL,
  PRIMARY KEY (`idBomba5`),
  KEY `idSuperEquipo` (`idSuperEquipo`),
  KEY `idTbomba` (`idTbomba`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `caldera6`
--

CREATE TABLE IF NOT EXISTS `caldera6` (
  `idCaldera6` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `potenciaCaldera6` decimal(10,0) NOT NULL,
  `tempsalidaCaldera6` decimal(10,0) NOT NULL,
  `tipocaldera6` varchar(50) NOT NULL,
  PRIMARY KEY (`idCaldera6`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `campania`
--

CREATE TABLE IF NOT EXISTS `campania` (
  `idCampania` int(11) NOT NULL AUTO_INCREMENT,
  `nombreCampania` varchar(100) NOT NULL,
  `idUsuarioM` int(11) NOT NULL,
  `fechaCampania` date DEFAULT NULL,
  `fcreacionCampania` date NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `idPlanta` int(11) NOT NULL,
  PRIMARY KEY (`idCampania`),
  KEY `idUsuarioM` (`idUsuarioM`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idPlanta` (`idPlanta`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `cargamerma`
--

CREATE TABLE IF NOT EXISTS `cargamerma` (
  `idCargamerma` int(11) NOT NULL AUTO_INCREMENT,
  `fechaCargamerma` date NOT NULL,
  `idSustrato` int(11) NOT NULL,
  `idUsuarioM` int(11) NOT NULL,
  `dispdiarioCargamerma` int(11) NOT NULL,
  `valorCargamerma` float NOT NULL,
  `cargateoricaCargamerma` int(11) NOT NULL,
  `fcargaCargamerma` date NOT NULL,
  `idPlanta` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idCargamerma`),
  KEY `idSustrato` (`idSustrato`),
  KEY `idUsuarioM` (`idUsuarioM`),
  KEY `idPlanta` (`idPlanta`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `caudalimetro26`
--

CREATE TABLE IF NOT EXISTS `caudalimetro26` (
  `idCaudalimetro26` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `idTipocaudal` int(11) DEFAULT NULL,
  `idTipoconstruccion` int(11) DEFAULT NULL,
  `cmaxCaudalimetro26` float DEFAULT NULL,
  `cminCaudalimetro26` float DEFAULT NULL,
  `diametroCaudalimetro26` float DEFAULT NULL,
  PRIMARY KEY (`idCaudalimetro26`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idTipocaudal` (`idTipocaudal`),
  KEY `idTipoconstruccion` (`idTipoconstruccion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `chiller13`
--

CREATE TABLE IF NOT EXISTS `chiller13` (
  `idChiller13` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `volumenChiller13` float NOT NULL,
  `tempinChiller13` float NOT NULL,
  `tempoutChiller13` float NOT NULL,
  PRIMARY KEY (`idChiller13`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `combcald`
--

CREATE TABLE IF NOT EXISTS `combcald` (
  `idCombcald` int(11) NOT NULL AUTO_INCREMENT,
  `idCombustible` int(11) NOT NULL,
  `idCaldera6` int(11) NOT NULL,
  PRIMARY KEY (`idCombcald`),
  KEY `idCombustible` (`idCombustible`),
  KEY `idCaldera6` (`idCaldera6`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `combustible`
--

CREATE TABLE IF NOT EXISTS `combustible` (
  `idCombustible` int(11) NOT NULL AUTO_INCREMENT,
  `nombreCombustible` varchar(200) NOT NULL,
  PRIMARY KEY (`idCombustible`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `compresoraire22`
--

CREATE TABLE IF NOT EXISTS `compresoraire22` (
  `idCompresoraire22` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `capacidadCompresoraire22` decimal(10,0) NOT NULL,
  PRIMARY KEY (`idCompresoraire22`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `consultora`
--

CREATE TABLE IF NOT EXISTS `consultora` (
  `idConsultora` int(11) NOT NULL AUTO_INCREMENT,
  `nombreConsultora` varchar(250) NOT NULL,
  `cuitConsultora` varchar(15) NOT NULL,
  `idSfiscal` int(11) NOT NULL,
  `mailConsultora` varchar(100) DEFAULT NULL,
  `telFijoConsultora` varchar(100) DEFAULT NULL,
  `celConsultora` varchar(100) DEFAULT NULL,
  `direccionConsultora` varchar(100) DEFAULT NULL,
  `idLoc` int(11) NOT NULL,
  `fCargaConsultora` date DEFAULT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idConsultora`),
  KEY `idSfiscal` (`idSfiscal`),
  KEY `idLoc` (`idLoc`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `deposito14`
--

CREATE TABLE IF NOT EXISTS `deposito14` (
  `idDeposito14` int(11) NOT NULL AUTO_INCREMENT,
  `largoDeposito14` float DEFAULT NULL,
  `anchoDeposito14` float DEFAULT NULL,
  `idSuperequipo` int(11) NOT NULL,
  `profmaxDeposito14` float DEFAULT NULL,
  `idTipocamara` int(11) NOT NULL,
  `capacidadDeposito14` float DEFAULT NULL,
  `agitadoDeposito14` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`idDeposito14`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idTipocamara` (`idTipocamara`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `desulfurizador18`
--

CREATE TABLE IF NOT EXISTS `desulfurizador18` (
  `idDesulfurizador18` int(11) NOT NULL AUTO_INCREMENT,
  `caudalDesulfurizador18` float DEFAULT NULL,
  `presionDesulfurizador18` float DEFAULT NULL,
  `idSuperequipo` int(11) NOT NULL,
  PRIMARY KEY (`idDesulfurizador18`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `digestor1`
--

CREATE TABLE IF NOT EXISTS `digestor1` (
  `idDigestor1` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `voltotalDigestor1` decimal(10,0) NOT NULL,
  `volutilDigestor1` decimal(10,0) NOT NULL,
  `volgasometroDigestor1` decimal(10,0) NOT NULL,
  PRIMARY KEY (`idDigestor1`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `estadoq`
--

CREATE TABLE IF NOT EXISTS `estadoq` (
  `idEstadoq` int(11) NOT NULL AUTO_INCREMENT,
  `nombreEstadoq` varchar(100) NOT NULL,
  PRIMARY KEY (`idEstadoq`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `filtrobiogas19`
--

CREATE TABLE IF NOT EXISTS `filtrobiogas19` (
  `idFiltrobiogas19` int(11) NOT NULL AUTO_INCREMENT,
  `volumenFiltrobiogas19` float DEFAULT NULL,
  `idSuperequipo` int(11) NOT NULL,
  `idTipofiltro` int(11) NOT NULL,
  PRIMARY KEY (`idFiltrobiogas19`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idTipofiltro` (`idTipofiltro`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `fostac`
--

CREATE TABLE IF NOT EXISTS `fostac` (
  `idFostac` int(11) NOT NULL AUTO_INCREMENT,
  `idPlantaequipo` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `phcFostac` float NOT NULL,
  `fosFostac` int(11) NOT NULL,
  `tacFostac` int(11) NOT NULL,
  `fostacFostac` float NOT NULL,
  `tempFostac` float NOT NULL,
  `fmedicionFostac` date NOT NULL,
  `fcargaFostac` date NOT NULL,
  `obsFostac` varchar(255) DEFAULT NULL,
  `idUsuarioM` int(11) NOT NULL,
  PRIMARY KEY (`idFostac`),
  KEY `idPlantaequipo` (`idPlantaequipo`),
  KEY `idUsuario` (`idUsuario`),
  KEY `idUsuarioM` (`idUsuarioM`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `intdecalor7`
--

CREATE TABLE IF NOT EXISTS `intdecalor7` (
  `idIntdecalor7` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `potenciaIntdecalor7` decimal(2,0) NOT NULL,
  `areaintIntdecalor7` decimal(2,0) NOT NULL,
  PRIMARY KEY (`idIntdecalor7`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `localidad`
--

CREATE TABLE IF NOT EXISTS `localidad` (
  `idLocalidad` int(11) NOT NULL AUTO_INCREMENT,
  `nomLocalidad` varchar(45) NOT NULL,
  `idProvincia` int(11) NOT NULL,
  PRIMARY KEY (`idLocalidad`),
  KEY `idProvincia` (`idProvincia`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `marca`
--

CREATE TABLE IF NOT EXISTS `marca` (
  `idMarca` int(11) NOT NULL AUTO_INCREMENT,
  `nombreMarca` varchar(200) NOT NULL,
  PRIMARY KEY (`idMarca`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `motor2`
--

CREATE TABLE IF NOT EXISTS `motor2` (
  `idMotor2` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `idCombustible` int(11) DEFAULT NULL,
  `potenciaMotor2` float DEFAULT NULL,
  PRIMARY KEY (`idMotor2`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idCombustible` (`idCombustible`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `pais`
--

CREATE TABLE IF NOT EXISTS `pais` (
  `idPais` int(11) NOT NULL AUTO_INCREMENT,
  `nomPais` varchar(45) NOT NULL,
  `parentId` int(11) NOT NULL,
  PRIMARY KEY (`idPais`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `palacargadora24`
--

CREATE TABLE IF NOT EXISTS `palacargadora24` (
  `idPalacargadora24` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `tambaldePalacargadora24` float DEFAULT NULL,
  PRIMARY KEY (`idPalacargadora24`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `planta`
--

CREATE TABLE IF NOT EXISTS `planta` (
  `idPlanta` int(11) NOT NULL AUTO_INCREMENT,
  `idConsultora` int(11) NOT NULL,
  `razonsocialPlanta` varchar(200) NOT NULL,
  `nombrePlanta` varchar(250) NOT NULL,
  `cuitPlanta` varchar(15) NOT NULL,
  `idSfiscal` int(11) NOT NULL,
  `telfijocontactoPlanta` varchar(100) DEFAULT NULL,
  `celcontactoPlanta` varchar(100) DEFAULT NULL,
  `cargocontactoPlanta` varchar(100) NOT NULL,
  `potinstaladaPlanta` decimal(10,0) DEFAULT NULL,
  `potadjudicadaPlanta` decimal(10,0) DEFAULT NULL,
  `idLocf` int(11) DEFAULT NULL,
  `direccionfiscalPlanta` varchar(200) DEFAULT NULL,
  `ubicacionPlanta` varchar(200) NOT NULL,
  `idLoc` int(11) DEFAULT NULL,
  `mailPlanta` varchar(100) DEFAULT NULL,
  `contactoPlanta` varchar(150) NOT NULL,
  `fcargaPlanta` date NOT NULL,
  `activoPlanta` tinyint(1) DEFAULT NULL,
  `logoPlanta` text,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idPlanta`),
  KEY `idConsultora` (`idConsultora`),
  KEY `idSfiscal` (`idSfiscal`),
  KEY `idLocf` (`idLocf`),
  KEY `idLoc` (`idLoc`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `plantaequipo`
--

CREATE TABLE IF NOT EXISTS `plantaequipo` (
  `idPlantaequipo` int(11) NOT NULL AUTO_INCREMENT,
  `idEstadoq` int(11) NOT NULL,
  `idSuperequipo` int(11) NOT NULL,
  `nombrePlantaequipo` varchar(100) NOT NULL,
  `idPlanta` int(11) NOT NULL,
  `nroseriePlantaequipo` varchar(200) DEFAULT NULL,
  `anioPlantaequipo` int(11) DEFAULT NULL,
  `nivelPlantaequipo` int(11) NOT NULL,
  `situacionPlantaequipo` enum('Indefinido','Primario','Secundario') DEFAULT NULL,
  `descripcionPlantaequipo` varchar(300) DEFAULT NULL,
  `fCargaPlantaequipo` date DEFAULT NULL,
  `activoPlantaequipo` tinyint(1) DEFAULT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idPlantaequipo`),
  KEY `idEstadoq` (`idEstadoq`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idPlanta` (`idPlanta`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `plan_usua`
--

CREATE TABLE IF NOT EXISTS `plan_usua` (
  `idPlan_usua` int(11) NOT NULL AUTO_INCREMENT,
  `idPlanta` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  `fcargaPlan_usua` date DEFAULT NULL,
  `finicioPlan_usua` date DEFAULT NULL,
  `activoPlan_usua` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`idPlan_usua`),
  KEY `idPlanta` (`idPlanta`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `profesion`
--

CREATE TABLE IF NOT EXISTS `profesion` (
  `idProfesion` int(11) NOT NULL AUTO_INCREMENT,
  `nomProfesion` varchar(255) NOT NULL,
  PRIMARY KEY (`idProfesion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `provincia`
--

CREATE TABLE IF NOT EXISTS `provincia` (
  `idProvincia` int(11) NOT NULL AUTO_INCREMENT,
  `nomProvincia` varchar(45) NOT NULL,
  `idPais` int(11) NOT NULL,
  PRIMARY KEY (`idProvincia`),
  KEY `idPais` (`idPais`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `regador3`
--

CREATE TABLE IF NOT EXISTS `regador3` (
  `idRegador3` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `tipoRegador3` enum('Solido','Liquido') DEFAULT NULL,
  `volcargaRegador3` float NOT NULL,
  PRIMARY KEY (`idRegador3`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `relacionequipo`
--

CREATE TABLE IF NOT EXISTS `relacionequipo` (
  `idRelacionequipo` int(11) NOT NULL AUTO_INCREMENT,
  `idPlantaequipoprimario` int(11) NOT NULL,
  `idPlantaequiposecundario` int(11) NOT NULL,
  `activoRelacionequipo` tinyint(1) DEFAULT NULL,
  `finicioRelacionequipo` date DEFAULT NULL,
  `ffinalRelacionequipo` date DEFAULT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idRelacionequipo`),
  KEY `idPlantaequipoprimario` (`idPlantaequipoprimario`),
  KEY `idPlantaequiposecundario` (`idPlantaequiposecundario`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `separador9`
--

CREATE TABLE IF NOT EXISTS `separador9` (
  `idSeparador9` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `caudalSeparador9` float DEFAULT NULL,
  `porcsolidoSeparador9` float DEFAULT NULL,
  PRIMARY KEY (`idSeparador9`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sfiscal`
--

CREATE TABLE IF NOT EXISTS `sfiscal` (
  `idSfiscal` int(11) NOT NULL AUTO_INCREMENT,
  `nombreSfiscal` varchar(255) NOT NULL,
  PRIMARY KEY (`idSfiscal`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sopbiogas8`
--

CREATE TABLE IF NOT EXISTS `sopbiogas8` (
  `idSopbiogas8` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `presionSopbiogas8` decimal(10,0) NOT NULL,
  `caudalSopbiogas8` decimal(10,0) NOT NULL,
  `tipoSopbiogas8` varchar(50) NOT NULL,
  PRIMARY KEY (`idSopbiogas8`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sopdetecho15`
--

CREATE TABLE IF NOT EXISTS `sopdetecho15` (
  `idSopdetecho15` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `potenciaSopdetecho15` float NOT NULL,
  `presionSopdetecho15` float NOT NULL,
  PRIMARY KEY (`idSopdetecho15`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `stsv`
--

CREATE TABLE IF NOT EXISTS `stsv` (
  `idStsv` int(11) NOT NULL AUTO_INCREMENT,
  `fechaStsv` date NOT NULL,
  `valorstStsv` float NOT NULL,
  `valorsvStsv` float NOT NULL,
  `obsStsv` varchar(150) DEFAULT NULL,
  `idPlantaequipo` int(11) NOT NULL,
  `fcargaStsv` date NOT NULL,
  `idUsuarioM` int(11) NOT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idStsv`),
  KEY `idPlantaequipo` (`idPlantaequipo`),
  KEY `idUsuarioM` (`idUsuarioM`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `superequipo`
--

CREATE TABLE IF NOT EXISTS `superequipo` (
  `idSuperequipo` int(11) NOT NULL AUTO_INCREMENT,
  `idTipoequipo` int(11) NOT NULL,
  `idMarca` int(11) NOT NULL,
  `modeloSuperequipo` varchar(150) DEFAULT NULL,
  `fcargaSuperequipo` date DEFAULT NULL,
  `activoSuperequipo` tinyint(1) DEFAULT NULL,
  `idUsuario` int(11) NOT NULL,
  PRIMARY KEY (`idSuperequipo`),
  KEY `idTipoequipo` (`idTipoequipo`),
  KEY `idMarca` (`idMarca`),
  KEY `idUsuario` (`idUsuario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sustrato`
--

CREATE TABLE IF NOT EXISTS `sustrato` (
  `idSustrato` int(11) NOT NULL AUTO_INCREMENT,
  `nombreSustrato` varchar(100) DEFAULT NULL,
  `descrpcionSustrato` varchar(100) DEFAULT NULL,
  `idUnidadmedida` int(11) DEFAULT NULL,
  PRIMARY KEY (`idSustrato`),
  KEY `idUnidadmedida` (`idUnidadmedida`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tableroelectrico21`
--

CREATE TABLE IF NOT EXISTS `tableroelectrico21` (
  `idTableroelectrico21` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `idTipodetablero` int(11) NOT NULL,
  PRIMARY KEY (`idTableroelectrico21`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idTipodetablero` (`idTipodetablero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tbomba`
--

CREATE TABLE IF NOT EXISTS `tbomba` (
  `idTbomba` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTbomba` varchar(200) NOT NULL,
  PRIMARY KEY (`idTbomba`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tdni`
--

CREATE TABLE IF NOT EXISTS `tdni` (
  `idTdni` int(11) NOT NULL AUTO_INCREMENT,
  `tipDni` varchar(20) NOT NULL,
  PRIMARY KEY (`idTdni`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tipoagitador`
--

CREATE TABLE IF NOT EXISTS `tipoagitador` (
  `idTipoagitador` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipoagitador` varchar(100) NOT NULL,
  PRIMARY KEY (`idTipoagitador`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tipocamara`
--

CREATE TABLE IF NOT EXISTS `tipocamara` (
  `idTipocamara` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipocamara` varchar(100) NOT NULL,
  PRIMARY KEY (`idTipocamara`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tipocaudal`
--

CREATE TABLE IF NOT EXISTS `tipocaudal` (
  `idTipocaudal` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipocaudal` varchar(200) NOT NULL,
  PRIMARY KEY (`idTipocaudal`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tipoconstruccion`
--

CREATE TABLE IF NOT EXISTS `tipoconstruccion` (
  `idTipoconstruccion` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipoconstruccion` varchar(200) NOT NULL,
  PRIMARY KEY (`idTipoconstruccion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tipoequipo`
--

CREATE TABLE IF NOT EXISTS `tipoequipo` (
  `idTipoequipo` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipoequipo` varchar(100) NOT NULL,
  PRIMARY KEY (`idTipoequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tipofiltro`
--

CREATE TABLE IF NOT EXISTS `tipofiltro` (
  `idTipofiltro` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipofiltro` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idTipofiltro`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tipotablero`
--

CREATE TABLE IF NOT EXISTS `tipotablero` (
  `idTipotablero` int(11) NOT NULL AUTO_INCREMENT,
  `nombreTipotablero` varchar(100) NOT NULL,
  PRIMARY KEY (`idTipotablero`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tolva23`
--

CREATE TABLE IF NOT EXISTS `tolva23` (
  `idTolva23` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `capacidadTolva23` float NOT NULL,
  `capdescargaTolva23` float NOT NULL,
  PRIMARY KEY (`idTolva23`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `tractor4`
--

CREATE TABLE IF NOT EXISTS `tractor4` (
  `idTractor4` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `idCombustible` int(11) NOT NULL,
  `potenciaTractor4` float DEFAULT NULL,
  PRIMARY KEY (`idTractor4`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idCombustible` (`idCombustible`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `transformador20`
--

CREATE TABLE IF NOT EXISTS `transformador20` (
  `idTransformador20` int(11) NOT NULL AUTO_INCREMENT,
  `potenciaTransformador20` float DEFAULT NULL,
  `idSuperequipo` int(11) NOT NULL,
  PRIMARY KEY (`idTransformador20`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `unidadmedida`
--

CREATE TABLE IF NOT EXISTS `unidadmedida` (
  `idUnidadmedida` int(11) NOT NULL AUTO_INCREMENT,
  `abrevUnidadmedida` varchar(45) NOT NULL,
  `descricpion` varchar(45) NOT NULL,
  PRIMARY KEY (`idUnidadmedida`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `valtresvias25`
--

CREATE TABLE IF NOT EXISTS `valtresvias25` (
  `idValvulatresvias25` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `diametroValvulatresvias25` float DEFAULT NULL,
  PRIMARY KEY (`idValvulatresvias25`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `valvdepresion12`
--

CREATE TABLE IF NOT EXISTS `valvdepresion12` (
  `idValvdepresion12` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `maxpValvdepresion12` float NOT NULL,
  PRIMARY KEY (`idValvdepresion12`),
  KEY `idSuperequipo` (`idSuperequipo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `vehiculo10`
--

CREATE TABLE IF NOT EXISTS `vehiculo10` (
  `idVehiculo10` int(11) NOT NULL AUTO_INCREMENT,
  `idSuperequipo` int(11) NOT NULL,
  `idCombustible` int(11) NOT NULL,
  `descripcionVehiculo10` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`idVehiculo10`),
  KEY `idSuperequipo` (`idSuperequipo`),
  KEY `idCombustible` (`idCombustible`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ab_permission_view`
--
ALTER TABLE `ab_permission_view`
  ADD CONSTRAINT `ab_permission_view_ibfk_1` FOREIGN KEY (`permission_id`) REFERENCES `ab_permission` (`id`),
  ADD CONSTRAINT `ab_permission_view_ibfk_2` FOREIGN KEY (`view_menu_id`) REFERENCES `ab_view_menu` (`id`);

--
-- Constraints for table `ab_permission_view_role`
--
ALTER TABLE `ab_permission_view_role`
  ADD CONSTRAINT `ab_permission_view_role_ibfk_1` FOREIGN KEY (`permission_view_id`) REFERENCES `ab_permission_view` (`id`),
  ADD CONSTRAINT `ab_permission_view_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `ab_role` (`id`);

--
-- Constraints for table `ab_user`
--
ALTER TABLE `ab_user`
  ADD CONSTRAINT `ab_user_ibfk_1` FOREIGN KEY (`created_by_fk`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `ab_user_ibfk_2` FOREIGN KEY (`changed_by_fk`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `ab_user_ibfk_3` FOREIGN KEY (`idTdni`) REFERENCES `tdni` (`idTdni`),
  ADD CONSTRAINT `ab_user_ibfk_4` FOREIGN KEY (`idPais`) REFERENCES `pais` (`idPais`),
  ADD CONSTRAINT `ab_user_ibfk_5` FOREIGN KEY (`idProfesion`) REFERENCES `profesion` (`idProfesion`);

--
-- Constraints for table `ab_user_role`
--
ALTER TABLE `ab_user_role`
  ADD CONSTRAINT `ab_user_role_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `ab_user_role_ibfk_2` FOREIGN KEY (`role_id`) REFERENCES `ab_role` (`id`);

--
-- Constraints for table `agitador16`
--
ALTER TABLE `agitador16`
  ADD CONSTRAINT `agitador16_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `agitador16_ibfk_2` FOREIGN KEY (`idTipoagitador`) REFERENCES `tipoagitador` (`idTipoagitador`);

--
-- Constraints for table `analisisquimico`
--
ALTER TABLE `analisisquimico`
  ADD CONSTRAINT `analisisquimico_ibfk_1` FOREIGN KEY (`idUsuarioM`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `analisisquimico_ibfk_2` FOREIGN KEY (`idPlanta`) REFERENCES `planta` (`idPlanta`),
  ADD CONSTRAINT `analisisquimico_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `analizadorgas17`
--
ALTER TABLE `analizadorgas17`
  ADD CONSTRAINT `analizadorgas17_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `antorcha11`
--
ALTER TABLE `antorcha11`
  ADD CONSTRAINT `antorcha11_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `area_plan`
--
ALTER TABLE `area_plan`
  ADD CONSTRAINT `area_plan_ibfk_1` FOREIGN KEY (`idPlanta`) REFERENCES `planta` (`idPlanta`),
  ADD CONSTRAINT `area_plan_ibfk_2` FOREIGN KEY (`idArea`) REFERENCES `area` (`idArea`);

--
-- Constraints for table `bomba5`
--
ALTER TABLE `bomba5`
  ADD CONSTRAINT `bomba5_ibfk_1` FOREIGN KEY (`idSuperEquipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `bomba5_ibfk_2` FOREIGN KEY (`idTbomba`) REFERENCES `tbomba` (`idTbomba`);

--
-- Constraints for table `caldera6`
--
ALTER TABLE `caldera6`
  ADD CONSTRAINT `caldera6_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `campania`
--
ALTER TABLE `campania`
  ADD CONSTRAINT `campania_ibfk_1` FOREIGN KEY (`idUsuarioM`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `campania_ibfk_2` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `campania_ibfk_3` FOREIGN KEY (`idPlanta`) REFERENCES `planta` (`idPlanta`);

--
-- Constraints for table `cargamerma`
--
ALTER TABLE `cargamerma`
  ADD CONSTRAINT `cargamerma_ibfk_1` FOREIGN KEY (`idSustrato`) REFERENCES `sustrato` (`idSustrato`),
  ADD CONSTRAINT `cargamerma_ibfk_2` FOREIGN KEY (`idUsuarioM`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `cargamerma_ibfk_3` FOREIGN KEY (`idPlanta`) REFERENCES `planta` (`idPlanta`),
  ADD CONSTRAINT `cargamerma_ibfk_4` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `caudalimetro26`
--
ALTER TABLE `caudalimetro26`
  ADD CONSTRAINT `caudalimetro26_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `caudalimetro26_ibfk_2` FOREIGN KEY (`idTipocaudal`) REFERENCES `tipocaudal` (`idTipocaudal`),
  ADD CONSTRAINT `caudalimetro26_ibfk_3` FOREIGN KEY (`idTipoconstruccion`) REFERENCES `tipoconstruccion` (`idTipoconstruccion`);

--
-- Constraints for table `chiller13`
--
ALTER TABLE `chiller13`
  ADD CONSTRAINT `chiller13_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `combcald`
--
ALTER TABLE `combcald`
  ADD CONSTRAINT `combcald_ibfk_1` FOREIGN KEY (`idCombustible`) REFERENCES `combustible` (`idCombustible`),
  ADD CONSTRAINT `combcald_ibfk_2` FOREIGN KEY (`idCaldera6`) REFERENCES `caldera6` (`idCaldera6`);

--
-- Constraints for table `compresoraire22`
--
ALTER TABLE `compresoraire22`
  ADD CONSTRAINT `compresoraire22_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `consultora`
--
ALTER TABLE `consultora`
  ADD CONSTRAINT `consultora_ibfk_1` FOREIGN KEY (`idSfiscal`) REFERENCES `sfiscal` (`idSfiscal`),
  ADD CONSTRAINT `consultora_ibfk_2` FOREIGN KEY (`idLoc`) REFERENCES `localidad` (`idLocalidad`),
  ADD CONSTRAINT `consultora_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `deposito14`
--
ALTER TABLE `deposito14`
  ADD CONSTRAINT `deposito14_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `deposito14_ibfk_2` FOREIGN KEY (`idTipocamara`) REFERENCES `tipocamara` (`idTipocamara`);

--
-- Constraints for table `desulfurizador18`
--
ALTER TABLE `desulfurizador18`
  ADD CONSTRAINT `desulfurizador18_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `digestor1`
--
ALTER TABLE `digestor1`
  ADD CONSTRAINT `digestor1_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `filtrobiogas19`
--
ALTER TABLE `filtrobiogas19`
  ADD CONSTRAINT `filtrobiogas19_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `filtrobiogas19_ibfk_2` FOREIGN KEY (`idTipofiltro`) REFERENCES `tipofiltro` (`idTipofiltro`);

--
-- Constraints for table `fostac`
--
ALTER TABLE `fostac`
  ADD CONSTRAINT `fostac_ibfk_1` FOREIGN KEY (`idPlantaequipo`) REFERENCES `plantaequipo` (`idPlantaequipo`),
  ADD CONSTRAINT `fostac_ibfk_2` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `fostac_ibfk_3` FOREIGN KEY (`idUsuarioM`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `intdecalor7`
--
ALTER TABLE `intdecalor7`
  ADD CONSTRAINT `intdecalor7_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `localidad`
--
ALTER TABLE `localidad`
  ADD CONSTRAINT `localidad_ibfk_1` FOREIGN KEY (`idProvincia`) REFERENCES `provincia` (`idProvincia`);

--
-- Constraints for table `motor2`
--
ALTER TABLE `motor2`
  ADD CONSTRAINT `motor2_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `motor2_ibfk_2` FOREIGN KEY (`idCombustible`) REFERENCES `combustible` (`idCombustible`);

--
-- Constraints for table `palacargadora24`
--
ALTER TABLE `palacargadora24`
  ADD CONSTRAINT `palacargadora24_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `planta`
--
ALTER TABLE `planta`
  ADD CONSTRAINT `planta_ibfk_1` FOREIGN KEY (`idConsultora`) REFERENCES `consultora` (`idConsultora`),
  ADD CONSTRAINT `planta_ibfk_2` FOREIGN KEY (`idSfiscal`) REFERENCES `sfiscal` (`idSfiscal`),
  ADD CONSTRAINT `planta_ibfk_3` FOREIGN KEY (`idLocf`) REFERENCES `localidad` (`idLocalidad`),
  ADD CONSTRAINT `planta_ibfk_4` FOREIGN KEY (`idLoc`) REFERENCES `localidad` (`idLocalidad`),
  ADD CONSTRAINT `planta_ibfk_5` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `plantaequipo`
--
ALTER TABLE `plantaequipo`
  ADD CONSTRAINT `plantaequipo_ibfk_1` FOREIGN KEY (`idEstadoq`) REFERENCES `estadoq` (`idEstadoq`),
  ADD CONSTRAINT `plantaequipo_ibfk_2` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `plantaequipo_ibfk_3` FOREIGN KEY (`idPlanta`) REFERENCES `planta` (`idPlanta`),
  ADD CONSTRAINT `plantaequipo_ibfk_4` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `plan_usua`
--
ALTER TABLE `plan_usua`
  ADD CONSTRAINT `plan_usua_ibfk_1` FOREIGN KEY (`idPlanta`) REFERENCES `planta` (`idPlanta`),
  ADD CONSTRAINT `plan_usua_ibfk_2` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `provincia`
--
ALTER TABLE `provincia`
  ADD CONSTRAINT `provincia_ibfk_1` FOREIGN KEY (`idPais`) REFERENCES `pais` (`idPais`);

--
-- Constraints for table `regador3`
--
ALTER TABLE `regador3`
  ADD CONSTRAINT `regador3_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `relacionequipo`
--
ALTER TABLE `relacionequipo`
  ADD CONSTRAINT `relacionequipo_ibfk_1` FOREIGN KEY (`idPlantaequipoprimario`) REFERENCES `plantaequipo` (`idPlantaequipo`),
  ADD CONSTRAINT `relacionequipo_ibfk_2` FOREIGN KEY (`idPlantaequiposecundario`) REFERENCES `plantaequipo` (`idPlantaequipo`),
  ADD CONSTRAINT `relacionequipo_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `separador9`
--
ALTER TABLE `separador9`
  ADD CONSTRAINT `separador9_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `sopbiogas8`
--
ALTER TABLE `sopbiogas8`
  ADD CONSTRAINT `sopbiogas8_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `sopdetecho15`
--
ALTER TABLE `sopdetecho15`
  ADD CONSTRAINT `sopdetecho15_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `stsv`
--
ALTER TABLE `stsv`
  ADD CONSTRAINT `stsv_ibfk_1` FOREIGN KEY (`idPlantaequipo`) REFERENCES `plantaequipo` (`idPlantaequipo`),
  ADD CONSTRAINT `stsv_ibfk_2` FOREIGN KEY (`idUsuarioM`) REFERENCES `ab_user` (`id`),
  ADD CONSTRAINT `stsv_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `superequipo`
--
ALTER TABLE `superequipo`
  ADD CONSTRAINT `superequipo_ibfk_1` FOREIGN KEY (`idTipoequipo`) REFERENCES `tipoequipo` (`idTipoequipo`),
  ADD CONSTRAINT `superequipo_ibfk_2` FOREIGN KEY (`idMarca`) REFERENCES `marca` (`idMarca`),
  ADD CONSTRAINT `superequipo_ibfk_3` FOREIGN KEY (`idUsuario`) REFERENCES `ab_user` (`id`);

--
-- Constraints for table `sustrato`
--
ALTER TABLE `sustrato`
  ADD CONSTRAINT `sustrato_ibfk_1` FOREIGN KEY (`idUnidadmedida`) REFERENCES `unidadmedida` (`idUnidadmedida`);

--
-- Constraints for table `tableroelectrico21`
--
ALTER TABLE `tableroelectrico21`
  ADD CONSTRAINT `tableroelectrico21_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `tableroelectrico21_ibfk_2` FOREIGN KEY (`idTipodetablero`) REFERENCES `tipotablero` (`idTipotablero`);

--
-- Constraints for table `tolva23`
--
ALTER TABLE `tolva23`
  ADD CONSTRAINT `tolva23_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `tractor4`
--
ALTER TABLE `tractor4`
  ADD CONSTRAINT `tractor4_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `tractor4_ibfk_2` FOREIGN KEY (`idCombustible`) REFERENCES `combustible` (`idCombustible`);

--
-- Constraints for table `transformador20`
--
ALTER TABLE `transformador20`
  ADD CONSTRAINT `transformador20_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `valtresvias25`
--
ALTER TABLE `valtresvias25`
  ADD CONSTRAINT `valtresvias25_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `valvdepresion12`
--
ALTER TABLE `valvdepresion12`
  ADD CONSTRAINT `valvdepresion12_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`);

--
-- Constraints for table `vehiculo10`
--
ALTER TABLE `vehiculo10`
  ADD CONSTRAINT `vehiculo10_ibfk_1` FOREIGN KEY (`idSuperequipo`) REFERENCES `superequipo` (`idSuperequipo`),
  ADD CONSTRAINT `vehiculo10_ibfk_2` FOREIGN KEY (`idCombustible`) REFERENCES `combustible` (`idCombustible`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
