-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 17, 2020 at 05:43 PM
-- Server version: 8.0.13-4
-- PHP Version: 7.2.24-0ubuntu0.18.04.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `DHomcPe4Ay`
--

-- --------------------------------------------------------

--
-- Table structure for table `auditapp_user`
--

CREATE TABLE `auditapp_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_partner` tinyint(1) NOT NULL,
  `is_manager` tinyint(1) NOT NULL,
  `is_auditorclerk` tinyint(1) NOT NULL,
  `is_articleholder` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auditapp_user`
--

INSERT INTO `auditapp_user` (`id`, `password`, `last_login`, `username`, `email`, `first_name`, `last_name`, `is_admin`, `is_partner`, `is_manager`, `is_auditorclerk`, `is_articleholder`, `is_active`) VALUES
(1, 'pbkdf2_sha256$150000$a6t4RzTDIQNM$KzehPNSxEcXA/5XUrundmnkfoSuYf6cgG6Fs6ibgUQw=', '2020-05-14 10:31:00.861014', 'admin', '', NULL, NULL, 1, 0, 0, 0, 0, 1),
(2, 'pbkdf2_sha256$150000$mi4lnbgCrP7d$i8s8TPRJPRlitv/V4yvj+SPsn+o9Z2228xxPshUIrVE=', '2020-05-16 11:24:12.805139', 'partner1', NULL, NULL, NULL, 0, 1, 0, 0, 0, 1),
(3, 'pbkdf2_sha256$150000$ZAslMP0WVLTm$oVYm/Dxh6AD1ZYMUjzEgsNL7Yxg5GcR6PjozW6cquOk=', '2020-05-17 08:06:17.653847', 'manager1', NULL, NULL, NULL, 0, 0, 1, 0, 0, 1),
(4, 'pbkdf2_sha256$150000$jeEG85vtdrsf$UHWqdF2ZMSk+yAi90M/xv8oj3ml9Zr7kxU1QjucDj4U=', '2020-05-15 20:56:32.830825', 'auditor1', NULL, NULL, NULL, 0, 0, 0, 1, 0, 1),
(5, 'pbkdf2_sha256$150000$NYkJiXc11HXc$zUasEutU+hdAfChqxfVH1PupcinSIJZ6HOPZFtkc0ow=', '2020-05-16 10:34:03.345968', 'article1', 'article1@yopmail.com', NULL, NULL, 0, 0, 0, 0, 1, 1),
(6, 'pbkdf2_sha256$150000$FYxruFVdpANC$leGXuQgGFqN22rWOXpc1d2VmuR9DozURNzCdVbVfAVQ=', '2020-05-16 10:38:45.888885', 'manager2', NULL, NULL, NULL, 0, 0, 1, 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add user', 6, 'add_user'),
(22, 'Can change user', 6, 'change_user'),
(23, 'Can delete user', 6, 'delete_user'),
(24, 'Can view user', 6, 'view_user'),
(25, 'Can add regulation', 7, 'add_regulation'),
(26, 'Can change regulation', 7, 'change_regulation'),
(27, 'Can delete regulation', 7, 'delete_regulation'),
(28, 'Can view regulation', 7, 'view_regulation'),
(29, 'Can add industry', 8, 'add_industry'),
(30, 'Can change industry', 8, 'change_industry'),
(31, 'Can delete industry', 8, 'delete_industry'),
(32, 'Can view industry', 8, 'view_industry'),
(33, 'Can add audit type', 9, 'add_audittype'),
(34, 'Can change audit type', 9, 'change_audittype'),
(35, 'Can delete audit type', 9, 'delete_audittype'),
(36, 'Can view audit type', 9, 'view_audittype'),
(37, 'Can add entity', 10, 'add_entity'),
(38, 'Can change entity', 10, 'change_entity'),
(39, 'Can delete entity', 10, 'delete_entity'),
(40, 'Can view entity', 10, 'view_entity'),
(41, 'Can add act', 11, 'add_act'),
(42, 'Can change act', 11, 'change_act'),
(43, 'Can delete act', 11, 'delete_act'),
(44, 'Can view act', 11, 'view_act'),
(45, 'Can add activity', 12, 'add_activity'),
(46, 'Can change activity', 12, 'change_activity'),
(47, 'Can delete activity', 12, 'delete_activity'),
(48, 'Can view activity', 12, 'view_activity'),
(49, 'Can add task', 13, 'add_task'),
(50, 'Can change task', 13, 'change_task'),
(51, 'Can delete task', 13, 'delete_task'),
(52, 'Can view task', 13, 'view_task'),
(53, 'Can add client', 14, 'add_client'),
(54, 'Can change client', 14, 'change_client'),
(55, 'Can delete client', 14, 'delete_client'),
(56, 'Can view client', 14, 'view_client'),
(57, 'Can add client task', 15, 'add_clienttask'),
(58, 'Can change client task', 15, 'change_clienttask'),
(59, 'Can delete client task', 15, 'delete_clienttask'),
(60, 'Can view client task', 15, 'view_clienttask'),
(61, 'Can add client activities', 16, 'add_clientactivities'),
(62, 'Can change client activities', 16, 'change_clientactivities'),
(63, 'Can delete client activities', 16, 'delete_clientactivities'),
(64, 'Can view client activities', 16, 'view_clientactivities'),
(65, 'Can add audit plan', 17, 'add_auditplan'),
(66, 'Can change audit plan', 17, 'change_auditplan'),
(67, 'Can delete audit plan', 17, 'delete_auditplan'),
(68, 'Can view audit plan', 17, 'view_auditplan'),
(69, 'Can add area', 18, 'add_area'),
(70, 'Can change area', 18, 'change_area'),
(71, 'Can delete area', 18, 'delete_area'),
(72, 'Can view area', 18, 'view_area'),
(73, 'Can add b_ activity', 19, 'add_b_activity'),
(74, 'Can change b_ activity', 19, 'change_b_activity'),
(75, 'Can delete b_ activity', 19, 'delete_b_activity'),
(76, 'Can view b_ activity', 19, 'view_b_activity'),
(77, 'Can add f_ area', 20, 'add_f_area'),
(78, 'Can change f_ area', 20, 'change_f_area'),
(79, 'Can delete f_ area', 20, 'delete_f_area'),
(80, 'Can view f_ area', 20, 'view_f_area'),
(81, 'Can add f_ activity', 21, 'add_f_activity'),
(82, 'Can change f_ activity', 21, 'change_f_activity'),
(83, 'Can delete f_ activity', 21, 'delete_f_activity'),
(84, 'Can view f_ activity', 21, 'view_f_activity');

-- --------------------------------------------------------

--
-- Table structure for table `business_area`
--

CREATE TABLE `business_area` (
  `id` int(11) NOT NULL,
  `area_name` varchar(255) NOT NULL,
  `industry_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `business_b_activity`
--

CREATE TABLE `business_b_activity` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) NOT NULL,
  `b_activity_description` varchar(255) NOT NULL,
  `area_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2020-04-29 14:51:55.275799', '2', 'partner1', 1, '[{\"added\": {}}]', 6, 1),
(2, '2020-04-29 14:52:02.303794', '2', 'partner1', 2, '[]', 6, 1),
(3, '2020-04-29 14:52:16.542793', '3', 'manager1', 1, '[{\"added\": {}}]', 6, 1),
(4, '2020-04-29 14:52:29.914792', '4', 'auditor1', 1, '[{\"added\": {}}]', 6, 1),
(5, '2020-04-29 14:52:40.545793', '5', 'article1', 1, '[{\"added\": {}}]', 6, 1),
(6, '2020-04-29 14:59:16.774436', '37', 'Computer Hardware', 2, '[{\"changed\": {\"fields\": [\"regulation\"]}}]', 8, 1),
(7, '2020-04-29 14:59:47.099438', '23', 'TELECOM', 2, '[{\"changed\": {\"fields\": [\"regulation\"]}}]', 8, 1),
(8, '2020-04-29 15:00:11.301433', '1', 'Statutory', 1, '[{\"added\": {}}]', 9, 1),
(9, '2020-04-29 15:00:24.403441', '2', 'Internal', 1, '[{\"added\": {}}]', 9, 1),
(10, '2020-04-29 15:00:46.023433', '14', 'Company-Private Limited-Unlimited', 2, '[{\"changed\": {\"fields\": [\"audit_type\"]}}]', 10, 1),
(11, '2020-04-29 15:01:02.089440', '1', 'Company-Public Limited', 2, '[{\"changed\": {\"fields\": [\"audit_type\"]}}]', 10, 1),
(12, '2020-04-29 15:01:30.924436', '1', 'Income Tax Act 1961', 2, '[{\"changed\": {\"fields\": [\"entity\"]}}]', 11, 1),
(13, '2020-04-29 15:01:48.805436', '7', 'The Companies Act, 2013', 2, '[{\"changed\": {\"fields\": [\"entity\"]}}]', 11, 1),
(14, '2020-04-29 15:02:05.496433', '1', 'Test Activity 1', 1, '[{\"added\": {}}]', 12, 1),
(15, '2020-04-29 15:02:13.771433', '2', 'Test Activity 2', 1, '[{\"added\": {}}]', 12, 1),
(16, '2020-04-29 15:02:44.776436', '1', 'Finance Activity', 2, '[{\"changed\": {\"fields\": [\"activity_name\"]}}]', 12, 1),
(17, '2020-04-29 15:02:57.423434', '2', 'Company Activity', 2, '[{\"changed\": {\"fields\": [\"activity_name\"]}}]', 12, 1),
(18, '2020-04-29 15:03:25.763435', '1', 'Task 1', 1, '[{\"added\": {}}]', 13, 1),
(19, '2020-04-29 15:03:37.075435', '1', 'Finance Task 1', 2, '[{\"changed\": {\"fields\": [\"task_name\"]}}]', 13, 1),
(20, '2020-04-29 15:03:56.104435', '2', 'Finance Task 2', 1, '[{\"added\": {}}]', 13, 1),
(21, '2020-04-29 15:23:40.857433', '1', 'Client 1', 1, '[{\"added\": {}}]', 14, 1),
(22, '2020-04-29 15:24:14.668439', '2', 'Client 2', 1, '[{\"added\": {}}]', 14, 1),
(23, '2020-04-29 15:26:02.694431', '1', 'ClientTask object (1)', 1, '[{\"added\": {}}]', 15, 1),
(24, '2020-04-30 10:45:45.764359', '3', 'Client 2', 3, '', 14, 1),
(25, '2020-04-30 10:47:11.715360', '5', 'Nachiket', 3, '', 14, 1),
(26, '2020-04-30 10:47:11.849356', '4', 'Nachiket', 3, '', 14, 1),
(27, '2020-04-30 10:59:01.018359', '6', 'manager2', 1, '[{\"added\": {}}]', 6, 1),
(28, '2020-04-30 10:59:03.651361', '1', 'Client 1', 2, '[{\"changed\": {\"fields\": [\"assigned_user\"]}}]', 14, 1),
(29, '2020-04-30 10:59:11.325357', '1', 'Client 1', 2, '[{\"changed\": {\"fields\": [\"assigned_user\"]}}]', 14, 1),
(30, '2020-04-30 12:00:46.394839', '5', 'article1', 2, '[{\"changed\": {\"fields\": [\"email\"]}}]', 6, 1),
(31, '2020-04-30 12:00:46.451839', '5', 'article1', 2, '[]', 6, 1),
(32, '2020-05-01 11:19:38.649433', '221', 'Task 1', 1, '[{\"added\": {}}]', 15, 1),
(33, '2020-05-01 11:59:39.646428', '223', 'Company Task 1', 1, '[{\"added\": {}}]', 15, 1),
(34, '2020-05-01 12:04:32.873434', '224', 'Company Task 1', 1, '[{\"added\": {}}]', 15, 1),
(35, '2020-05-01 12:07:39.081435', '223', 'Company Task 1', 2, '[]', 15, 1),
(36, '2020-05-01 12:12:06.314433', '7', 'New CLient', 3, '', 14, 1),
(37, '2020-05-02 20:07:38.152970', '6', 'Nachiket', 3, '', 14, 1),
(38, '2020-05-02 20:28:52.868963', '8', 'New Client', 2, '[{\"changed\": {\"fields\": [\"assigned_user\"]}}]', 14, 1),
(39, '2020-05-02 20:30:59.239958', '2', 'Client 2', 3, '', 14, 1),
(40, '2020-05-02 20:30:59.282959', '1', 'Client 1', 3, '', 14, 1),
(41, '2020-05-03 10:50:28.219389', '37', 'Computer Hardware', 3, '', 8, 1),
(42, '2020-05-03 10:50:28.290388', '36', 'IT/ITES', 3, '', 8, 1),
(43, '2020-05-03 10:50:28.363387', '35', 'Logistics-Others', 3, '', 8, 1),
(44, '2020-05-03 10:50:28.400385', '34', 'Logistics-Transporters', 3, '', 8, 1),
(45, '2020-05-03 10:50:28.414388', '33', 'Movie Production', 3, '', 8, 1),
(46, '2020-05-03 10:50:28.451384', '32', 'Movie Exhibition', 3, '', 8, 1),
(47, '2020-05-03 10:50:28.465386', '31', 'Manpower Services', 3, '', 8, 1),
(48, '2020-05-03 10:50:28.503784', '30', 'Manufacturing', 3, '', 8, 1),
(49, '2020-05-03 10:50:28.525382', '29', 'Engineering', 3, '', 8, 1),
(50, '2020-05-03 10:50:28.572716', '28', 'Hotels/Resorts', 3, '', 8, 1),
(51, '2020-05-03 10:50:28.611389', '27', 'Trading', 3, '', 8, 1),
(52, '2020-05-03 10:50:28.682382', '26', 'Oil and Gas', 3, '', 8, 1),
(53, '2020-05-03 10:50:28.696385', '25', 'Power', 3, '', 8, 1),
(54, '2020-05-03 10:50:28.708382', '24', 'Forest Products', 3, '', 8, 1),
(55, '2020-05-03 10:50:28.739387', '23', 'TELECOM', 3, '', 8, 1),
(56, '2020-05-03 10:50:28.751383', '22', 'CEMENT & CEMENT PRODUCTS', 3, '', 8, 1),
(57, '2020-05-03 10:50:28.781387', '21', 'TEXTILES', 3, '', 8, 1),
(58, '2020-05-03 10:50:28.794391', '20', 'FERTILISERS & PESTICIDES', 3, '', 8, 1),
(59, '2020-05-03 10:50:28.807385', '19', 'Metals and Mining', 3, '', 8, 1),
(60, '2020-05-03 10:50:28.820386', '18', 'Metals', 3, '', 8, 1),
(61, '2020-05-03 10:50:28.833382', '17', 'Healthcare-Diagnostic Centers', 3, '', 8, 1),
(62, '2020-05-03 10:50:28.846386', '16', 'Healthcare-Hospitals', 3, '', 8, 1),
(63, '2020-05-03 10:50:28.860388', '15', 'Pharma', 3, '', 8, 1),
(64, '2020-05-03 10:50:28.873391', '14', 'Construction-Commercial', 3, '', 8, 1),
(65, '2020-05-03 10:50:28.884382', '13', 'Construction-Housing', 3, '', 8, 1),
(66, '2020-05-03 10:50:28.898385', '12', 'Advertising', 3, '', 8, 1),
(67, '2020-05-03 10:50:28.910387', '11', 'Consumer Durables', 3, '', 8, 1),
(68, '2020-05-03 10:50:28.924387', '10', 'FMCG-Food', 3, '', 8, 1),
(69, '2020-05-03 10:50:28.936382', '9', 'Houing Finance-Non FD accepting', 3, '', 8, 1),
(70, '2020-05-03 10:50:28.950384', '8', 'Housing Finance-FD Accepting', 3, '', 8, 1),
(71, '2020-05-03 10:50:28.979383', '7', 'NBFC-FD accepting', 3, '', 8, 1),
(72, '2020-05-03 10:50:28.994382', '6', 'NBFC-Non FD accepting', 3, '', 8, 1),
(73, '2020-05-03 10:50:29.031385', '5', 'Banks-Private Sector', 3, '', 8, 1),
(74, '2020-05-03 10:50:29.044388', '4', 'Banks-Public Sector', 3, '', 8, 1),
(75, '2020-05-03 10:50:29.057390', '3', 'Chemicals', 3, '', 8, 1),
(76, '2020-05-03 10:50:29.086381', '2', 'Automobiles', 3, '', 8, 1),
(77, '2020-05-03 10:50:29.123387', '1', 'Marketing', 3, '', 8, 1),
(78, '2020-05-03 10:51:26.179390', '38', 'My Industry', 1, '[{\"added\": {}}]', 8, 1),
(79, '2020-05-03 10:51:42.323390', '8', 'The Limited Liability Partnership Act, 2008', 3, '', 11, 1),
(80, '2020-05-03 10:51:42.336388', '7', 'The Companies Act, 2013', 3, '', 11, 1),
(81, '2020-05-03 10:51:42.349390', '6', 'The Insolvency and Bankruptcy Code, 2016', 3, '', 11, 1),
(82, '2020-05-03 10:51:42.395387', '5', 'The Pension Fund Regulatory and Development Authority Act, 2013', 3, '', 11, 1),
(83, '2020-05-03 10:51:42.415390', '4', 'The Union Territory Goods and Services Tax Act, 2017', 3, '', 11, 1),
(84, '2020-05-03 10:51:42.427387', '3', 'The Integrated Goods and Services Tax Act, 2017', 3, '', 11, 1),
(85, '2020-05-03 10:51:42.440383', '2', 'The Central Goods and Services Tax Act, 2017', 3, '', 11, 1),
(86, '2020-05-03 10:51:42.452386', '1', 'Income Tax Act 1961', 3, '', 11, 1),
(87, '2020-05-03 10:51:51.723390', '2', 'Internal', 3, '', 9, 1),
(88, '2020-05-03 10:51:51.778386', '1', 'Statutory', 3, '', 9, 1),
(89, '2020-05-03 10:52:05.104390', '370', 'Company Task 23', 3, '', 15, 1),
(90, '2020-05-03 10:52:05.146389', '369', 'Company Task 22', 3, '', 15, 1),
(91, '2020-05-03 10:52:05.158387', '368', 'Company Task 21', 3, '', 15, 1),
(92, '2020-05-03 10:52:05.172387', '367', 'Company Task 20', 3, '', 15, 1),
(93, '2020-05-03 10:52:05.192384', '366', 'Company Task 19', 3, '', 15, 1),
(94, '2020-05-03 10:52:05.231386', '365', 'Company Task 18', 3, '', 15, 1),
(95, '2020-05-03 10:52:05.256390', '364', 'Company Task 17', 3, '', 15, 1),
(96, '2020-05-03 10:52:05.299393', '363', 'Company Task 16', 3, '', 15, 1),
(97, '2020-05-03 10:52:05.311387', '362', 'Company Task 15', 3, '', 15, 1),
(98, '2020-05-03 10:52:05.326389', '361', 'Company Task 14', 3, '', 15, 1),
(99, '2020-05-03 10:52:05.345386', '360', 'Company Task 13', 3, '', 15, 1),
(100, '2020-05-03 10:52:05.376390', '359', 'Company Task 12', 3, '', 15, 1),
(101, '2020-05-03 10:52:05.414385', '358', 'Company Task 11', 3, '', 15, 1),
(102, '2020-05-03 10:52:05.427393', '357', 'Company Task 10', 3, '', 15, 1),
(103, '2020-05-03 10:52:05.460389', '356', 'Company Task 9', 3, '', 15, 1),
(104, '2020-05-03 10:52:05.478394', '355', 'Company Task 8', 3, '', 15, 1),
(105, '2020-05-03 10:52:05.491383', '354', 'Company Task 7', 3, '', 15, 1),
(106, '2020-05-03 10:52:05.504390', '353', 'Company Task 6', 3, '', 15, 1),
(107, '2020-05-03 10:52:05.517382', '352', 'Company Task 5', 3, '', 15, 1),
(108, '2020-05-03 10:52:05.530388', '351', 'Company Task 4', 3, '', 15, 1),
(109, '2020-05-03 10:52:05.543388', '350', 'Company Task 3', 3, '', 15, 1),
(110, '2020-05-03 10:52:05.557388', '349', 'Company Task 2', 3, '', 15, 1),
(111, '2020-05-03 10:52:05.596389', '348', 'Company Task 1', 3, '', 15, 1),
(112, '2020-05-03 10:52:05.621382', '347', 'Finance Task 48', 3, '', 15, 1),
(113, '2020-05-03 10:52:05.634384', '346', 'Finance Task 47', 3, '', 15, 1),
(114, '2020-05-03 10:52:05.673389', '345', 'Finance Task 46', 3, '', 15, 1),
(115, '2020-05-03 10:52:05.687387', '344', 'Finance Task 45', 3, '', 15, 1),
(116, '2020-05-03 10:52:05.707387', '343', 'Finance Task 44', 3, '', 15, 1),
(117, '2020-05-03 10:52:05.719387', '342', 'Finance Task 43', 3, '', 15, 1),
(118, '2020-05-03 10:52:05.751390', '341', 'Finance Task 42', 3, '', 15, 1),
(119, '2020-05-03 10:52:05.762387', '340', 'Finance Task 41', 3, '', 15, 1),
(120, '2020-05-03 10:52:05.810391', '339', 'Finance Task 40', 3, '', 15, 1),
(121, '2020-05-03 10:52:05.821382', '338', 'Finance Task 39', 3, '', 15, 1),
(122, '2020-05-03 10:52:05.835386', '337', 'Finance Task 38', 3, '', 15, 1),
(123, '2020-05-03 10:52:05.856387', '336', 'Finance Task 37', 3, '', 15, 1),
(124, '2020-05-03 10:52:05.870388', '335', 'Finance Task 36', 3, '', 15, 1),
(125, '2020-05-03 10:52:05.882387', '334', 'Finance Task 35', 3, '', 15, 1),
(126, '2020-05-03 10:52:05.895382', '333', 'Finance Task 34', 3, '', 15, 1),
(127, '2020-05-03 10:52:05.908390', '332', 'Finance Task 33', 3, '', 15, 1),
(128, '2020-05-03 10:52:05.921382', '331', 'Finance Task 32', 3, '', 15, 1),
(129, '2020-05-03 10:52:05.934386', '330', 'Finance Task 31', 3, '', 15, 1),
(130, '2020-05-03 10:52:05.947382', '329', 'Finance Task 30', 3, '', 15, 1),
(131, '2020-05-03 10:52:05.960387', '328', 'Finance Task 29', 3, '', 15, 1),
(132, '2020-05-03 10:52:05.991390', '327', 'Finance Task 28', 3, '', 15, 1),
(133, '2020-05-03 10:52:06.011390', '326', 'Finance Task 27', 3, '', 15, 1),
(134, '2020-05-03 10:52:06.075382', '325', 'Finance Task 26', 3, '', 15, 1),
(135, '2020-05-03 10:52:06.123797', '324', 'Finance Task 25', 3, '', 15, 1),
(136, '2020-05-03 10:52:06.135386', '323', 'Finance Task 24', 3, '', 15, 1),
(137, '2020-05-03 10:52:06.165384', '322', 'Finance Task 23', 3, '', 15, 1),
(138, '2020-05-03 10:52:06.194385', '321', 'Finance Task 22', 3, '', 15, 1),
(139, '2020-05-03 10:52:06.224382', '320', 'Finance Task 21', 3, '', 15, 1),
(140, '2020-05-03 10:52:06.255393', '319', 'Finance Task 20', 3, '', 15, 1),
(141, '2020-05-03 10:52:06.267386', '318', 'Finance Task 19', 3, '', 15, 1),
(142, '2020-05-03 10:52:06.296389', '317', 'Finance Task 18', 3, '', 15, 1),
(143, '2020-05-03 10:52:06.343389', '316', 'Finance Task 17', 3, '', 15, 1),
(144, '2020-05-03 10:52:06.364388', '315', 'Finance Task 16', 3, '', 15, 1),
(145, '2020-05-03 10:52:06.394387', '314', 'Finance Task 15', 3, '', 15, 1),
(146, '2020-05-03 10:52:06.424391', '313', 'Finance Task 14', 3, '', 15, 1),
(147, '2020-05-03 10:52:06.453383', '312', 'Finance Task 13', 3, '', 15, 1),
(148, '2020-05-03 10:52:06.482385', '311', 'Finance Task 12', 3, '', 15, 1),
(149, '2020-05-03 10:52:06.513388', '310', 'Finance Task 11', 3, '', 15, 1),
(150, '2020-05-03 10:52:06.525387', '309', 'Finance Task 10', 3, '', 15, 1),
(151, '2020-05-03 10:52:06.556389', '308', 'Finance Task 9', 3, '', 15, 1),
(152, '2020-05-03 10:52:06.568390', '307', 'Finance Task 8', 3, '', 15, 1),
(153, '2020-05-03 10:52:06.590389', '306', 'Finance Task 7', 3, '', 15, 1),
(154, '2020-05-03 10:52:06.628385', '305', 'Finance Task 6', 3, '', 15, 1),
(155, '2020-05-03 10:52:06.686382', '304', 'Finance Task 5', 3, '', 15, 1),
(156, '2020-05-03 10:52:06.719387', '303', 'Finance Task 4', 3, '', 15, 1),
(157, '2020-05-03 10:52:06.732387', '302', 'Finance Task 3', 3, '', 15, 1),
(158, '2020-05-03 10:52:06.773390', '301', 'Finance Task 2', 3, '', 15, 1),
(159, '2020-05-03 10:52:06.793389', '300', 'Finance Task 1', 3, '', 15, 1),
(160, '2020-05-03 10:52:06.823386', '299', 'Finance Task 2 old', 3, '', 15, 1),
(161, '2020-05-03 10:52:06.860389', '298', 'Finance Task 1 old', 3, '', 15, 1),
(162, '2020-05-03 10:52:15.185388', '8', 'New Client', 3, '', 14, 1),
(163, '2020-05-03 10:52:24.156393', '2', 'Company Activity', 3, '', 12, 1),
(164, '2020-05-03 10:52:24.207382', '1', 'Finance Activity', 3, '', 12, 1),
(165, '2020-05-03 10:52:37.639390', '75', 'Company Task 24', 3, '', 13, 1),
(166, '2020-05-03 10:52:37.793382', '74', 'Company Task 23', 3, '', 13, 1),
(167, '2020-05-03 10:52:37.826387', '73', 'Company Task 22', 3, '', 13, 1),
(168, '2020-05-03 10:52:37.839382', '72', 'Company Task 21', 3, '', 13, 1),
(169, '2020-05-03 10:52:37.852386', '71', 'Company Task 20', 3, '', 13, 1),
(170, '2020-05-03 10:52:37.867386', '70', 'Company Task 19', 3, '', 13, 1),
(171, '2020-05-03 10:52:37.881390', '69', 'Company Task 18', 3, '', 13, 1),
(172, '2020-05-03 10:52:37.901388', '68', 'Company Task 17', 3, '', 13, 1),
(173, '2020-05-03 10:52:37.914389', '67', 'Company Task 16', 3, '', 13, 1),
(174, '2020-05-03 10:52:37.926383', '66', 'Company Task 15', 3, '', 13, 1),
(175, '2020-05-03 10:52:37.955386', '65', 'Company Task 14', 3, '', 13, 1),
(176, '2020-05-03 10:52:37.992387', '64', 'Company Task 13', 3, '', 13, 1),
(177, '2020-05-03 10:52:38.039391', '63', 'Company Task 12', 3, '', 13, 1),
(178, '2020-05-03 10:52:38.051390', '62', 'Company Task 11', 3, '', 13, 1),
(179, '2020-05-03 10:52:38.064393', '61', 'Company Task 10', 3, '', 13, 1),
(180, '2020-05-03 10:52:38.076388', '60', 'Company Task 9', 3, '', 13, 1),
(181, '2020-05-03 10:52:38.089382', '59', 'Company Task 8', 3, '', 13, 1),
(182, '2020-05-03 10:52:38.131389', '58', 'Company Task 7', 3, '', 13, 1),
(183, '2020-05-03 10:52:38.219396', '57', 'Company Task 6', 3, '', 13, 1),
(184, '2020-05-03 10:52:38.389382', '56', 'Company Task 5', 3, '', 13, 1),
(185, '2020-05-03 10:52:38.456384', '55', 'Company Task 4', 3, '', 13, 1),
(186, '2020-05-03 10:52:38.468386', '54', 'Company Task 3', 3, '', 13, 1),
(187, '2020-05-03 10:52:38.499389', '53', 'Company Task 2', 3, '', 13, 1),
(188, '2020-05-03 10:52:38.519387', '52', 'Company Task 1', 3, '', 13, 1),
(189, '2020-05-03 10:52:38.545390', '51', 'Finance Task 49', 3, '', 13, 1),
(190, '2020-05-03 10:52:38.569387', '50', 'Finance Task 48', 3, '', 13, 1),
(191, '2020-05-03 10:52:38.583392', '49', 'Finance Task 47', 3, '', 13, 1),
(192, '2020-05-03 10:52:38.596392', '48', 'Finance Task 46', 3, '', 13, 1),
(193, '2020-05-03 10:52:38.616388', '47', 'Finance Task 45', 3, '', 13, 1),
(194, '2020-05-03 10:52:38.628382', '46', 'Finance Task 44', 3, '', 13, 1),
(195, '2020-05-03 10:52:38.640381', '45', 'Finance Task 43', 3, '', 13, 1),
(196, '2020-05-03 10:52:38.662389', '44', 'Finance Task 42', 3, '', 13, 1),
(197, '2020-05-03 10:52:38.674382', '43', 'Finance Task 41', 3, '', 13, 1),
(198, '2020-05-03 10:52:38.695387', '42', 'Finance Task 40', 3, '', 13, 1),
(199, '2020-05-03 10:52:38.709382', '41', 'Finance Task 39', 3, '', 13, 1),
(200, '2020-05-03 10:52:38.753382', '40', 'Finance Task 38', 3, '', 13, 1),
(201, '2020-05-03 10:52:38.766385', '39', 'Finance Task 37', 3, '', 13, 1),
(202, '2020-05-03 10:52:38.796393', '38', 'Finance Task 36', 3, '', 13, 1),
(203, '2020-05-03 10:52:38.808382', '37', 'Finance Task 35', 3, '', 13, 1),
(204, '2020-05-03 10:52:38.820382', '36', 'Finance Task 34', 3, '', 13, 1),
(205, '2020-05-03 10:52:38.834388', '35', 'Finance Task 33', 3, '', 13, 1),
(206, '2020-05-03 10:52:38.846388', '34', 'Finance Task 32', 3, '', 13, 1),
(207, '2020-05-03 10:52:38.858387', '33', 'Finance Task 31', 3, '', 13, 1),
(208, '2020-05-03 10:52:38.871383', '32', 'Finance Task 30', 3, '', 13, 1),
(209, '2020-05-03 10:52:38.883386', '31', 'Finance Task 29', 3, '', 13, 1),
(210, '2020-05-03 10:52:38.896382', '30', 'Finance Task 28', 3, '', 13, 1),
(211, '2020-05-03 10:52:38.908382', '29', 'Finance Task 27', 3, '', 13, 1),
(212, '2020-05-03 10:52:38.922386', '28', 'Finance Task 26', 3, '', 13, 1),
(213, '2020-05-03 10:52:38.934389', '27', 'Finance Task 25', 3, '', 13, 1),
(214, '2020-05-03 10:52:38.947384', '26', 'Finance Task 24', 3, '', 13, 1),
(215, '2020-05-03 10:52:38.959386', '25', 'Finance Task 23', 3, '', 13, 1),
(216, '2020-05-03 10:52:38.971382', '24', 'Finance Task 22', 3, '', 13, 1),
(217, '2020-05-03 10:52:38.984388', '23', 'Finance Task 21', 3, '', 13, 1),
(218, '2020-05-03 10:52:38.996384', '22', 'Finance Task 20', 3, '', 13, 1),
(219, '2020-05-03 10:52:39.011392', '21', 'Finance Task 19', 3, '', 13, 1),
(220, '2020-05-03 10:52:39.030389', '20', 'Finance Task 18', 3, '', 13, 1),
(221, '2020-05-03 10:52:39.044392', '19', 'Finance Task 17', 3, '', 13, 1),
(222, '2020-05-03 10:52:39.072390', '18', 'Finance Task 16', 3, '', 13, 1),
(223, '2020-05-03 10:52:39.090395', '17', 'Finance Task 15', 3, '', 13, 1),
(224, '2020-05-03 10:52:39.106392', '16', 'Finance Task 14', 3, '', 13, 1),
(225, '2020-05-03 10:52:39.118389', '15', 'Finance Task 13', 3, '', 13, 1),
(226, '2020-05-03 10:52:39.174390', '14', 'Finance Task 12', 3, '', 13, 1),
(227, '2020-05-03 10:52:39.218389', '13', 'Finance Task 11', 3, '', 13, 1),
(228, '2020-05-03 10:52:39.238395', '12', 'Finance Task 10', 3, '', 13, 1),
(229, '2020-05-03 10:52:39.255391', '11', 'Finance Task 9', 3, '', 13, 1),
(230, '2020-05-03 10:52:39.275389', '10', 'Finance Task 8', 3, '', 13, 1),
(231, '2020-05-03 10:52:39.319389', '9', 'Finance Task 7', 3, '', 13, 1),
(232, '2020-05-03 10:52:39.332388', '8', 'Finance Task 6', 3, '', 13, 1),
(233, '2020-05-03 10:52:39.344391', '7', 'Finance Task 5', 3, '', 13, 1),
(234, '2020-05-03 10:52:39.364387', '6', 'Finance Task 4', 3, '', 13, 1),
(235, '2020-05-03 10:52:39.407387', '5', 'Finance Task 3', 3, '', 13, 1),
(236, '2020-05-03 10:52:39.446389', '4', 'Finance Task 2', 3, '', 13, 1),
(237, '2020-05-03 10:52:39.500389', '3', 'Finance Task 1', 3, '', 13, 1),
(238, '2020-05-03 10:52:39.536385', '2', 'Finance Task 2 old', 3, '', 13, 1),
(239, '2020-05-03 10:52:39.583389', '1', 'Finance Task 1 old', 3, '', 13, 1),
(240, '2020-05-03 10:53:12.207395', '3', 'Statutory Audit', 1, '[{\"added\": {}}]', 9, 1),
(241, '2020-05-03 10:53:12.565390', '4', 'Statutory Audit', 1, '[{\"added\": {}}]', 9, 1),
(242, '2020-05-03 10:53:20.838387', '5', 'Internal Audit', 1, '[{\"added\": {}}]', 9, 1),
(243, '2020-05-03 10:53:28.819391', '6', 'Certification Audit', 1, '[{\"added\": {}}]', 9, 1),
(244, '2020-05-03 10:53:46.206391', '7', 'Taxation Audit', 1, '[{\"added\": {}}]', 9, 1),
(245, '2020-05-03 10:54:13.210390', '8', 'Investigation Assigment Audit', 1, '[{\"added\": {}}]', 9, 1),
(246, '2020-05-03 10:54:26.207389', '4', 'Statutory Audit', 3, '', 9, 1),
(247, '2020-05-03 10:55:04.541388', '9', 'HFC Act 1882', 1, '[{\"added\": {}}]', 11, 1),
(248, '2020-05-03 10:55:29.106391', '10', 'Income Tax Act 1961', 1, '[{\"added\": {}}]', 11, 1),
(249, '2020-05-03 10:56:30.457388', '3', 'Bank Reconciliation', 1, '[{\"added\": {}}]', 12, 1),
(250, '2020-05-03 10:56:54.052389', '76', 'Task 1', 1, '[{\"added\": {}}]', 13, 1),
(251, '2020-05-03 10:57:09.402390', '77', 'Task 2', 1, '[{\"added\": {}}]', 13, 1),
(252, '2020-05-03 10:58:26.066393', '9', 'Nachiket', 1, '[{\"added\": {}}]', 14, 1),
(253, '2020-05-03 18:42:12.063968', '39', 'Agro', 1, '[{\"added\": {}}]', 8, 1),
(254, '2020-05-03 18:42:16.472968', '12', 'Test Act 2', 1, '[{\"added\": {}}]', 11, 1),
(255, '2020-05-03 18:42:39.514968', '5', 'Nachiket 123', 2, '[{\"changed\": {\"fields\": [\"act\"]}}]', 12, 1),
(256, '2020-05-03 18:44:37.105969', '79', 'Task 4', 1, '[{\"added\": {}}]', 13, 1),
(257, '2020-05-03 18:47:33.133968', '6', 'Test Activity 1', 1, '[{\"added\": {}}]', 12, 1),
(258, '2020-05-03 18:49:56.548963', '80', 'Task 5', 1, '[{\"added\": {}}]', 13, 1),
(259, '2020-05-03 18:52:31.282970', '7', 'Test Activity 2', 1, '[{\"added\": {}}]', 12, 1),
(260, '2020-05-03 18:52:45.118968', '8', 'Test Activity 3', 1, '[{\"added\": {}}]', 12, 1),
(261, '2020-05-03 18:53:37.141964', '81', 'Task 6', 1, '[{\"added\": {}}]', 13, 1),
(262, '2020-05-03 18:53:55.805968', '82', 'Task 7', 1, '[{\"added\": {}}]', 13, 1),
(263, '2020-05-03 18:57:47.675976', '78', 'Task 3', 2, '[{\"changed\": {\"fields\": [\"activity\"]}}]', 13, 1),
(264, '2020-05-03 18:57:58.323971', '76', 'Task 1', 2, '[{\"changed\": {\"fields\": [\"task_name\", \"activity\"]}}]', 13, 1),
(265, '2020-05-03 19:09:26.386969', '11', 'New Client', 3, '', 14, 1),
(266, '2020-05-03 19:09:33.084968', '10', 'New Client', 3, '', 14, 1),
(267, '2020-05-03 19:09:33.113971', '9', 'Nachiket', 3, '', 14, 1),
(268, '2020-05-03 19:23:08.045969', '12', 'Client 1', 3, '', 14, 1),
(269, '2020-05-03 20:07:28.837969', '13', 'Client 1', 3, '', 14, 1),
(270, '2020-05-04 12:13:13.938814', '14', 'Client 2', 2, '[{\"changed\": {\"fields\": [\"industry\"]}}]', 14, 1),
(271, '2020-05-04 12:13:14.390813', '14', 'Client 2', 2, '[]', 14, 1),
(272, '2020-05-04 12:16:25.705813', '14', 'Client 2', 2, '[{\"changed\": {\"fields\": [\"industry\"]}}]', 14, 1),
(273, '2020-05-04 12:24:36.018810', '79', 'Task 4', 2, '[]', 13, 1),
(274, '2020-05-04 12:24:47.207810', '388', 'Task 2', 2, '[{\"changed\": {\"fields\": [\"is_completed\"]}}]', 15, 1),
(275, '2020-05-04 12:25:06.581809', '390', 'Task 4', 2, '[{\"changed\": {\"fields\": [\"is_completed\"]}}]', 15, 1),
(276, '2020-05-04 12:26:59.428811', '15', 'Nachiket', 3, '', 14, 1),
(277, '2020-05-04 12:58:20.259817', '16', 'Nachiket', 2, '[{\"changed\": {\"fields\": [\"audit_type\"]}}]', 14, 1),
(278, '2020-05-09 12:05:58.702416', '17', 'Client 3', 1, '[{\"added\": {}}]', 14, 1),
(279, '2020-05-09 12:06:33.985423', '17', 'Client 3', 3, '', 14, 1),
(280, '2020-05-09 12:08:38.698422', '18', 'Client 3', 3, '', 14, 1),
(281, '2020-05-09 12:32:38.161422', '20', 'Client 3', 2, '[{\"changed\": {\"fields\": [\"assigned_user\"]}}]', 14, 1),
(282, '2020-05-09 12:39:00.621422', '416', 'Task 1', 2, '[{\"changed\": {\"fields\": [\"user\"]}}]', 15, 1),
(283, '2020-05-09 12:40:55.672425', '416', 'Task 1', 2, '[{\"changed\": {\"fields\": [\"task_end_date\"]}}]', 15, 1),
(284, '2020-05-09 13:18:39.440422', '417', 'Task 2', 2, '[{\"changed\": {\"fields\": [\"user\"]}}]', 15, 1),
(285, '2020-05-09 13:52:15.131421', '417', 'Task 2', 2, '[{\"changed\": {\"fields\": [\"user\"]}}]', 15, 1),
(286, '2020-05-09 18:43:04.760691', '21', 'Client 3', 3, '', 14, 1),
(287, '2020-05-13 09:22:21.241125', '23', 'Test Client', 3, '', 14, 1),
(288, '2020-05-13 09:22:21.279117', '22', 'Client 3', 3, '', 14, 1),
(289, '2020-05-13 09:32:55.465123', '24', 'Test Client', 1, '[{\"added\": {}}]', 14, 1),
(290, '2020-05-13 09:33:03.772131', '24', 'Test Client', 3, '', 14, 1),
(291, '2020-05-13 10:21:13.492125', '35', 'Agro Client', 3, '', 14, 1),
(292, '2020-05-13 10:21:13.547121', '34', 'Agro Client', 3, '', 14, 1),
(293, '2020-05-13 10:21:13.585122', '33', 'Agro Client', 3, '', 14, 1),
(294, '2020-05-13 10:21:13.613118', '32', 'Agro Client', 3, '', 14, 1),
(295, '2020-05-13 10:21:13.644124', '31', 'Agro Client', 3, '', 14, 1),
(296, '2020-05-13 10:21:13.672125', '30', 'Agro Client', 3, '', 14, 1),
(297, '2020-05-13 10:21:13.685123', '29', 'Agro Client', 3, '', 14, 1),
(298, '2020-05-13 10:21:13.705123', '28', 'Agro Client', 3, '', 14, 1),
(299, '2020-05-13 10:21:13.717123', '27', 'Agro Client', 3, '', 14, 1),
(300, '2020-05-13 10:21:13.730122', '26', 'Agro Client', 3, '', 14, 1),
(301, '2020-05-13 10:21:13.742123', '25', 'Agro Client', 3, '', 14, 1),
(302, '2020-05-13 10:31:16.587123', '437', 'Agro Task 1', 2, '[]', 15, 1),
(303, '2020-05-13 10:32:36.640124', '437', 'Agro Task 1', 2, '[{\"changed\": {\"fields\": [\"activity\"]}}]', 15, 1),
(304, '2020-05-13 10:56:44.318976', '20', 'Client 3', 3, '', 14, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(6, 'auditapp', 'user'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(18, 'business', 'area'),
(19, 'business', 'b_activity'),
(4, 'contenttypes', 'contenttype'),
(21, 'finance', 'f_activity'),
(20, 'finance', 'f_area'),
(11, 'partner', 'act'),
(12, 'partner', 'activity'),
(17, 'partner', 'auditplan'),
(9, 'partner', 'audittype'),
(14, 'partner', 'client'),
(16, 'partner', 'clientactivities'),
(15, 'partner', 'clienttask'),
(10, 'partner', 'entity'),
(8, 'partner', 'industry'),
(7, 'partner', 'regulation'),
(13, 'partner', 'task'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-04-29 14:47:03.864793'),
(2, 'auditapp', '0001_initial', '2020-04-29 14:47:04.105796'),
(3, 'admin', '0001_initial', '2020-04-29 14:47:04.363787'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-04-29 14:47:05.552788'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-04-29 14:47:05.586792'),
(6, 'contenttypes', '0002_remove_content_type_name', '2020-04-29 14:47:06.658794'),
(7, 'auth', '0001_initial', '2020-04-29 14:47:07.476794'),
(8, 'auth', '0002_alter_permission_name_max_length', '2020-04-29 14:47:11.786792'),
(9, 'auth', '0003_alter_user_email_max_length', '2020-04-29 14:47:11.820793'),
(10, 'auth', '0004_alter_user_username_opts', '2020-04-29 14:47:11.871793'),
(11, 'auth', '0005_alter_user_last_login_null', '2020-04-29 14:47:11.946792'),
(12, 'auth', '0006_require_contenttypes_0002', '2020-04-29 14:47:11.966794'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2020-04-29 14:47:12.007793'),
(14, 'auth', '0008_alter_user_username_max_length', '2020-04-29 14:47:12.065794'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2020-04-29 14:47:12.115791'),
(16, 'auth', '0010_alter_group_name_max_length', '2020-04-29 14:47:12.375791'),
(17, 'auth', '0011_update_proxy_permissions', '2020-04-29 14:47:12.523786'),
(18, 'sessions', '0001_initial', '2020-04-29 14:47:13.133794'),
(19, 'partner', '0001_initial', '2020-04-29 14:49:36.568793'),
(20, 'partner', '0002_auto_20200430_1509', '2020-04-30 09:39:13.401351'),
(21, 'partner', '0003_auto_20200430_1558', '2020-04-30 10:28:46.429357'),
(22, 'partner', '0004_auto_20200430_1602', '2020-04-30 10:32:42.622357'),
(23, 'partner', '0005_auto_20200501_1644', '2020-05-01 11:14:27.592430'),
(24, 'partner', '0006_auto_20200501_1706', '2020-05-01 11:36:18.913431'),
(25, 'partner', '0007_auto_20200501_1708', '2020-05-01 11:38:50.555432'),
(26, 'partner', '0008_auto_20200503_0129', '2020-05-02 19:59:26.376960'),
(27, 'partner', '0009_auto_20200503_1618', '2020-05-03 10:48:16.921390'),
(28, 'business', '0001_initial', '2020-05-03 10:49:38.718387'),
(29, 'finance', '0001_initial', '2020-05-03 10:49:48.616391'),
(30, 'partner', '0010_auto_20200504_0004', '2020-05-03 18:34:59.510963'),
(31, 'partner', '0011_auto_20200504_0109', '2020-05-03 19:39:35.696968'),
(32, 'partner', '0012_auto_20200504_0111', '2020-05-03 19:41:50.870969'),
(33, 'partner', '0013_auto_20200504_0116', '2020-05-03 19:46:44.282964'),
(34, 'partner', '0014_auto_20200504_0126', '2020-05-03 19:56:38.623969'),
(35, 'partner', '0015_auto_20200504_0132', '2020-05-03 20:02:29.318971'),
(36, 'partner', '0016_auto_20200509_1727', '2020-05-09 11:57:50.353422'),
(37, 'partner', '0017_clienttask_task_master', '2020-05-09 12:02:24.127422'),
(38, 'partner', '0018_remove_clienttask_task_master', '2020-05-09 12:08:50.249419'),
(39, 'partner', '0019_auto_20200513_1415', '2020-05-13 08:45:58.546082'),
(40, 'partner', '0020_remove_clienttask_audit_type', '2020-05-13 10:17:02.907123'),
(41, 'partner', '0021_clienttask_reject_task', '2020-05-15 20:16:39.135170'),
(42, 'partner', '0022_auto_20200516_0148', '2020-05-15 20:18:18.450851');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('07uqy0s079yxc6igp33nh9amaut1n6e0', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-30 11:07:13.886605'),
('0vyk0lh0av1jyjwssyfkej5uvyn0fxqg', 'NjBhNTIzMmJhOTQ5NzJiNDUwMmI5YTNiNGYyNGViNzU0MjgxNmMxNTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YWRjNTZkZDYyNWNkMzc3YmM3ODIyNjAwYTAxOWFhMTkyZGRkMDFlIn0=', '2020-05-29 16:16:03.639393'),
('28ujnoy4o8gacse7xuof8pubxuh7rghi', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-27 08:47:34.794095'),
('3gegnohksrg8o82wn7o02363lfv6mkbu', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-27 14:36:54.069796'),
('5edignl9buai0kr4qx9l5z4f68zi77hh', 'ZjgzNmE2OTJmNTMwMzg5NTk5OTJjOGY3ZmRjOTlhNjRiM2VmYjdiODp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwZmU1Y2FmNGJjNmFlNTNiMDJlOTliYzg1ZmU2YmVkMzQ2ZWM0OTQ5In0=', '2020-05-29 18:19:41.631792'),
('65ntqe1cecjyzuncdwakkjnpkvys9k2j', 'NjBhNTIzMmJhOTQ5NzJiNDUwMmI5YTNiNGYyNGViNzU0MjgxNmMxNTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YWRjNTZkZDYyNWNkMzc3YmM3ODIyNjAwYTAxOWFhMTkyZGRkMDFlIn0=', '2020-05-31 08:06:17.849858'),
('7wipvgbtgks5apz1ts7vzsq3yfj1zp3j', 'NjBhNTIzMmJhOTQ5NzJiNDUwMmI5YTNiNGYyNGViNzU0MjgxNmMxNTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YWRjNTZkZDYyNWNkMzc3YmM3ODIyNjAwYTAxOWFhMTkyZGRkMDFlIn0=', '2020-05-16 20:31:28.505966'),
('96020mt65tgvtoj60bdl0jij6hprmjx2', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-14 10:10:14.458359'),
('9t207q6cgddw26j7wyqgro4eg04pj0f5', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-28 10:31:00.892381'),
('abmoajn0jofbzvytof1l3brbuvv9an1j', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-16 20:06:51.714962'),
('fzjhpbbt21mfh7hwv84m4w9vz2mqndc0', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-17 10:48:59.828382'),
('h3u70kqgd1539vk885nxdmi7gdeisv4t', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-13 14:51:32.159793'),
('h3x3rn7ytzrdtev17vnmem0xez562dzw', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-18 11:34:42.429940'),
('hvhfvsp114frhmtgbob93pl4be1psjab', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-23 12:01:18.045418'),
('iytx9cf87fercppsm7njr8fdhn8zajm2', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-16 20:27:07.076962'),
('j2mkovind5e3kx0wg0eumuzgrvmyjwvw', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-30 11:24:12.850217'),
('k4cgltw7y6bsnn7lqi6ei3agdtvr7le6', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-27 12:13:01.478393'),
('l3nann9mxh2caov7sx4bvgespin1z9uq', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-17 18:41:56.662974'),
('lwvl272cu0le8wesp6jt6h1x4id84b55', 'NjBhNTIzMmJhOTQ5NzJiNDUwMmI5YTNiNGYyNGViNzU0MjgxNmMxNTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YWRjNTZkZDYyNWNkMzc3YmM3ODIyNjAwYTAxOWFhMTkyZGRkMDFlIn0=', '2020-05-28 08:02:10.585772'),
('npkihh0tbxi8fpdd754d0fk1cs0uodqu', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-15 11:18:38.214431'),
('nurbf7c180zm6eb3lfrrn6wvpw0pxuqm', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-27 09:59:33.574127'),
('r3imn5ogi77ik5z9u1d09zg296kexfwd', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-27 09:21:41.998125'),
('uh1l1r04cgx8t7u5357x7tiqpaejmcig', 'NjBhNTIzMmJhOTQ5NzJiNDUwMmI5YTNiNGYyNGViNzU0MjgxNmMxNTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YWRjNTZkZDYyNWNkMzc3YmM3ODIyNjAwYTAxOWFhMTkyZGRkMDFlIn0=', '2020-05-16 19:39:47.684964'),
('w9hjaoaynvxxwmloyxv85nkrz5ocj4h0', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-15 10:13:29.145433'),
('yksq2jxhq1wkgw0p8i9kiwr8fgsx3yl3', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-29 05:13:57.367228'),
('ynzlg75ts4zw4yx5gc0h6navdu7j0c8f', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-17 18:25:56.481969'),
('zkdrobqisay9bor32po8ca8fitha9a4e', 'Y2Y4MmZmNjZlOGUxOTkzMWIyMWYwYjY0Y2ZlZGRkODlmMzY2MjVjMjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDdmYjVjN2I5ZjhkZjdkMjkwNDFhZGQzNzc1MGZhNGU1ODc1ZGU5In0=', '2020-05-28 10:17:26.636337');

-- --------------------------------------------------------

--
-- Table structure for table `finance_f_activity`
--

CREATE TABLE `finance_f_activity` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) NOT NULL,
  `f_activity_description` varchar(255) NOT NULL,
  `area_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `finance_f_area`
--

CREATE TABLE `finance_f_area` (
  `id` int(11) NOT NULL,
  `area_name` varchar(255) NOT NULL,
  `f_industry_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `partner_act`
--

CREATE TABLE `partner_act` (
  `id` int(11) NOT NULL,
  `act_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_act`
--

INSERT INTO `partner_act` (`id`, `act_name`) VALUES
(9, 'HFC Act 1882'),
(10, 'Income Tax Act 1961'),
(12, 'Test Act 2'),
(13, 'MGN'),
(14, 'SEBI MF Reg 1996');

-- --------------------------------------------------------

--
-- Table structure for table `partner_activity`
--

CREATE TABLE `partner_activity` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) NOT NULL,
  `activity_description` varchar(255) NOT NULL,
  `act_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_activity`
--

INSERT INTO `partner_activity` (`id`, `activity_name`, `activity_description`, `act_id`) VALUES
(3, 'Bank Reconciliation', 'HDSJKH', 9),
(5, 'Nachiket 123', 'hdjkashdsakhdkjhdsjhsa', 12),
(6, 'Test Activity 1', 'This is a test activity', 10),
(7, 'Test Activity 2', 'This is a test activity', 12),
(8, 'Test Activity 3', 'This is a test activity', 9),
(9, 'TEST 1', 'HDSJKH', 12),
(10, 'TEST 2', 'HDJSHJDS', 10),
(11, 'Check 20-25 rule', 'Check 20-25 rule', 13),
(12, 'Cash Vouching', 'Cash Vouching', 14);

-- --------------------------------------------------------

--
-- Table structure for table `partner_activity_audit_type`
--

CREATE TABLE `partner_activity_audit_type` (
  `id` int(11) NOT NULL,
  `activity_id` int(11) NOT NULL,
  `audittype_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_activity_audit_type`
--

INSERT INTO `partner_activity_audit_type` (`id`, `activity_id`, `audittype_id`) VALUES
(5, 3, 3),
(6, 3, 6),
(7, 3, 8),
(4, 9, 3),
(8, 10, 3),
(9, 10, 6),
(10, 10, 7),
(11, 11, 3),
(12, 12, 3),
(13, 12, 5);

-- --------------------------------------------------------

--
-- Table structure for table `partner_activity_entities`
--

CREATE TABLE `partner_activity_entities` (
  `id` int(11) NOT NULL,
  `activity_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_activity_entities`
--

INSERT INTO `partner_activity_entities` (`id`, `activity_id`, `entity_id`) VALUES
(28, 3, 1),
(29, 3, 3),
(30, 3, 5),
(31, 3, 6),
(9, 5, 1),
(10, 5, 3),
(11, 5, 5),
(12, 5, 12),
(13, 5, 14),
(14, 5, 16),
(16, 6, 7),
(15, 6, 8),
(17, 7, 6),
(18, 8, 6),
(24, 9, 1),
(25, 9, 3),
(26, 9, 5),
(27, 9, 12),
(32, 10, 4),
(33, 10, 6),
(34, 10, 8),
(35, 10, 9),
(36, 10, 11),
(37, 10, 13),
(38, 11, 2),
(39, 12, 1),
(40, 12, 6);

-- --------------------------------------------------------

--
-- Table structure for table `partner_act_industry`
--

CREATE TABLE `partner_act_industry` (
  `id` int(11) NOT NULL,
  `act_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_act_industry`
--

INSERT INTO `partner_act_industry` (`id`, `act_id`, `industry_id`) VALUES
(1, 9, 38),
(2, 10, 38),
(4, 12, 39),
(6, 14, 38),
(7, 14, 40);

-- --------------------------------------------------------

--
-- Table structure for table `partner_audittype`
--

CREATE TABLE `partner_audittype` (
  `id` int(11) NOT NULL,
  `audit_type_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_audittype`
--

INSERT INTO `partner_audittype` (`id`, `audit_type_name`) VALUES
(3, 'Statutory Audit'),
(5, 'Internal Audit'),
(6, 'Certification Audit'),
(7, 'Taxation Audit'),
(8, 'Investigation Assigment Audit');

-- --------------------------------------------------------

--
-- Table structure for table `partner_client`
--

CREATE TABLE `partner_client` (
  `id` int(11) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `pan_no` varchar(10) NOT NULL,
  `tan_no` varchar(10) NOT NULL,
  `gst_no` varchar(255) NOT NULL,
  `assigned_user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_client`
--

INSERT INTO `partner_client` (`id`, `client_name`, `pan_no`, `tan_no`, `gst_no`, `assigned_user_id`) VALUES
(36, 'Agro Client', 'GDSHDGS7', 'TAN23321', 'GSTIN432', 3),
(37, 'My Industry Client', 'GDSHDGS7', 'TAN23321', 'GSTIN4324', 6),
(38, 'Both industry client', 'GDSHDGS73', 'TAN23321', 'GSTIN4324', 3),
(39, 'MGN Mutual Fund', '123456', '123456', '12345', 3),
(40, 'MGN Housing Solutions', '', '', '', 3),
(41, 'MGN Caterers', '123456', '123456', '', 3);

-- --------------------------------------------------------

--
-- Table structure for table `partner_clientactivities`
--

CREATE TABLE `partner_clientactivities` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) DEFAULT NULL,
  `activity_description` varchar(255) NOT NULL,
  `task_start_date` date DEFAULT NULL,
  `task_end_date` date DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `partner_clienttask`
--

CREATE TABLE `partner_clienttask` (
  `id` int(11) NOT NULL,
  `task_start_date` date DEFAULT NULL,
  `task_end_date` date DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `attachment_file` varchar(100) DEFAULT NULL,
  `remark` varchar(255) DEFAULT NULL,
  `is_rejected` tinyint(1) NOT NULL,
  `is_completed` tinyint(1) NOT NULL,
  `is_start` tinyint(1) NOT NULL,
  `is_reject` tinyint(1) NOT NULL,
  `rejection_remark` varchar(255) DEFAULT NULL,
  `client_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `act_id` int(11) DEFAULT NULL,
  `activity_id` int(11) DEFAULT NULL,
  `task_auditing_standard` varchar(255) DEFAULT NULL,
  `task_estimated_days` varchar(255) DEFAULT NULL,
  `task_international_auditing_standard` varchar(255) DEFAULT NULL,
  `task_name` varchar(255) DEFAULT NULL,
  `reject_task_remark` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_clienttask`
--

INSERT INTO `partner_clienttask` (`id`, `task_start_date`, `task_end_date`, `status`, `is_approved`, `attachment_file`, `remark`, `is_rejected`, `is_completed`, `is_start`, `is_reject`, `rejection_remark`, `client_id`, `user_id`, `act_id`, `activity_id`, `task_auditing_standard`, `task_estimated_days`, `task_international_auditing_standard`, `task_name`, `reject_task_remark`) VALUES
(434, NULL, NULL, 1, 1, '', NULL, 0, 0, 0, 0, 'nooo noo no', 36, 5, 12, 5, 'MY', '43', 'WHO', 'Task 4', NULL),
(435, NULL, NULL, 1, 1, '', NULL, 0, 0, 0, 0, 'same ', 36, 5, 12, 7, 'OSI', '30', 'DCN', 'Task 3', NULL),
(436, NULL, NULL, 0, 0, '', NULL, 1, 0, 1, 0, 'no no no', 36, 5, 12, 7, 'PIIU', '54', 'KSJCE', 'Task 6', NULL),
(437, '2020-05-13', NULL, 0, 0, 'task_submission/437/credentials.yml', 'done', 0, 0, 0, 0, NULL, 36, 5, 10, 9, 'OSI', '20', 'ISO', 'Agro Task 1', NULL),
(438, '2020-05-16', NULL, 1, 0, 'task_submission/438/.gitconfig_oP7Jott', '', 1, 0, 1, 1, 'nai\r\n', 37, 4, 9, 8, 'INS', '2000', 'IETE', 'Task 1', 'trail'),
(439, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 1, 'ofverload', 37, 4, 9, 3, 'OSI', '100', 'IFTF', 'Task 2', NULL),
(440, NULL, '2020-05-15', 0, 0, '', NULL, 0, 0, 0, 1, NULL, 37, 4, 10, 6, 'MY', '432', 'OJI', 'Task 5', NULL),
(441, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 1, NULL, 37, 4, 9, 8, 'KJSCETI', '09', 'KJARTS', 'Task 7', NULL),
(442, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 1, NULL, 38, 4, 9, 8, 'INS', '2000', 'IETE', 'Task 1', NULL),
(443, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 38, NULL, 9, 3, 'OSI', '100', 'IFTF', 'Task 2', NULL),
(444, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 38, NULL, 12, 7, 'OSI', '30', 'DCN', 'Task 3', NULL),
(445, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 38, NULL, 12, 5, 'MY', '43', 'WHO', 'Task 4', NULL),
(446, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 38, NULL, 10, 6, 'MY', '432', 'OJI', 'Task 5', NULL),
(447, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 38, NULL, 12, 7, 'PIIU', '54', 'KSJCE', 'Task 6', NULL),
(448, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 38, NULL, 9, 8, 'KJSCETI', '09', 'KJARTS', 'Task 7', NULL),
(449, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 1, NULL, 39, NULL, 13, 11, 'AAS-1(i)', '1', 'IAS 26', 'Obtain Holding report from R&T', NULL),
(450, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 1, NULL, 40, NULL, 13, 11, 'AAS-1(i)', '1', 'IAS 26', 'Obtain Holding report from R&T', NULL),
(451, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 40, NULL, 13, 11, '', '1', 'IAS 1', 'Check financial reports made from Underlying books', NULL),
(452, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 41, NULL, 9, 3, 'OSI', '100', 'IFTF', 'Task 2', NULL),
(453, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 41, NULL, 9, 8, 'INS', '2000', 'IETE', 'Task 1', NULL),
(454, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 41, NULL, 9, 8, 'KJSCETI', '09', 'KJARTS', 'Task 7', NULL),
(455, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 41, NULL, 10, 6, 'MY', '432', 'OJI', 'Task 5', NULL),
(456, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 41, NULL, 10, 6, 'ISO', '2', 'ISO', 'wed task 1', NULL),
(457, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 41, NULL, 14, 12, 'IAS2', '1', '', 'Check Cash Balance', NULL),
(458, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 37, NULL, 9, 8, 'HJHDS', '21', 'UIYREU', 'Test task 2', NULL),
(459, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 38, NULL, 9, 8, 'HJHDS', '21', 'UIYREU', 'Test task 2', NULL),
(460, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 41, NULL, 9, 8, 'HJHDS', '21', 'UIYREU', 'Test task 2', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `partner_client_audit_type`
--

CREATE TABLE `partner_client_audit_type` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `audittype_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_client_audit_type`
--

INSERT INTO `partner_client_audit_type` (`id`, `client_id`, `audittype_id`) VALUES
(72, 36, 3),
(73, 36, 6),
(74, 36, 8),
(75, 37, 3),
(76, 37, 6),
(77, 37, 8),
(78, 38, 3),
(79, 38, 7),
(80, 38, 8),
(81, 39, 3),
(82, 40, 3),
(83, 41, 3),
(84, 41, 5);

-- --------------------------------------------------------

--
-- Table structure for table `partner_client_entities`
--

CREATE TABLE `partner_client_entities` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_client_entities`
--

INSERT INTO `partner_client_entities` (`id`, `client_id`, `entity_id`) VALUES
(134, 36, 1),
(135, 36, 3),
(136, 36, 5),
(137, 36, 7),
(138, 36, 9),
(139, 37, 1),
(140, 37, 3),
(141, 37, 5),
(142, 37, 9),
(143, 37, 11),
(144, 37, 13),
(145, 37, 14),
(146, 37, 15),
(147, 37, 16),
(148, 38, 1),
(149, 38, 3),
(150, 38, 5),
(151, 38, 6),
(152, 38, 7),
(153, 38, 8),
(154, 38, 10),
(155, 39, 1),
(156, 40, 1),
(157, 41, 1);

-- --------------------------------------------------------

--
-- Table structure for table `partner_client_industry`
--

CREATE TABLE `partner_client_industry` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_client_industry`
--

INSERT INTO `partner_client_industry` (`id`, `client_id`, `industry_id`) VALUES
(59, 36, 39),
(60, 37, 38),
(61, 38, 38),
(62, 38, 39),
(63, 39, 40),
(64, 40, 40),
(65, 41, 38),
(66, 41, 40);

-- --------------------------------------------------------

--
-- Table structure for table `partner_entity`
--

CREATE TABLE `partner_entity` (
  `id` int(11) NOT NULL,
  `entity_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_entity`
--

INSERT INTO `partner_entity` (`id`, `entity_name`) VALUES
(1, 'Company-Public Limited'),
(2, 'Company-Deemed Public Limited'),
(3, 'Coopertaive Housing Society'),
(4, 'Trust-Public'),
(5, 'Trust-Private'),
(6, 'Partnership Firm'),
(7, 'Association of Persons'),
(8, 'Sole properitor'),
(9, 'Cooperative Society-Deposit Accepting'),
(10, 'Coopertaive Society-Non Deposit Accepting'),
(11, 'Limited Liability Partnerships ( LLP)'),
(12, 'Company-Private Limited-Limited by Shares'),
(13, 'Company-Private Limited-Limited by gurantee'),
(14, 'Company-Private Limited-Unlimited'),
(15, 'Hindu Undivided Family-HUF'),
(16, 'Individual');

-- --------------------------------------------------------

--
-- Table structure for table `partner_industry`
--

CREATE TABLE `partner_industry` (
  `id` int(11) NOT NULL,
  `industry_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_industry`
--

INSERT INTO `partner_industry` (`id`, `industry_name`) VALUES
(38, 'My Industry'),
(39, 'Agro'),
(40, 'ABCD');

-- --------------------------------------------------------

--
-- Table structure for table `partner_industry_regulation`
--

CREATE TABLE `partner_industry_regulation` (
  `id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL,
  `regulation_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_industry_regulation`
--

INSERT INTO `partner_industry_regulation` (`id`, `industry_id`, `regulation_id`) VALUES
(10, 38, 1),
(11, 39, 2),
(12, 39, 3),
(13, 40, 2);

-- --------------------------------------------------------

--
-- Table structure for table `partner_regulation`
--

CREATE TABLE `partner_regulation` (
  `id` int(11) NOT NULL,
  `regulation_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_regulation`
--

INSERT INTO `partner_regulation` (`id`, `regulation_name`) VALUES
(1, 'RBI – Reserve Bank of India'),
(2, 'SEBI – Securities and Exchange Board of India'),
(3, 'IRDAI – Insurance Regulatory and Development Authority of India'),
(4, 'PFRDA – Pension Fund Regulatory & Development Authority'),
(5, 'NABARD – National Bank for Agriculture and Rural Development'),
(6, 'SIDBI – Small Industries Development Bank of India'),
(7, 'NHB - National Housing Bank'),
(8, 'TRAI – Telecom Regulatory Authority of India'),
(9, 'CBFC – Central Board of Film Certification'),
(10, 'FSDC – Financial Stability and Development Council'),
(11, 'FSSAI – Food Safety and Standards Authority of India'),
(12, 'BIS – Bureau of Indian Standards'),
(13, 'ASCI – Advertising Standards Council of India'),
(14, 'BCCI – Board of Control for Cricket in India'),
(15, 'AMFI – Association of Mutual Funds in India'),
(16, 'EEPC – Engineering Export Promotional Council of India'),
(17, 'EICI – Express Industry Council of India'),
(18, 'FIEO – Federation of Indian Export Organisation'),
(19, 'INSA – Indian National Shipowners’ Association'),
(20, 'ICC – Indian Chemical Council'),
(21, 'ISSDA – Indian Stainless Steel Development Association'),
(22, 'MAIT – Manufacturers’ Association for Information Technology'),
(23, 'NASSCOM – National Association of Software and Service Companies'),
(24, 'OPPI – Organisation Of Plastic Processors of India'),
(25, ' PEPC – Project Exports Promotion Council of India'),
(26, 'CDSCO – Central Drugs Standard Control Organisation'),
(27, 'Inland Waterways Authority of India'),
(28, 'National Highways Authority of India'),
(29, 'ICAI-Institute of Chartered Accountants of India'),
(30, 'DGMS-Directorate General of Mines Safety'),
(31, 'Airports Economic Regulatory Authority'),
(32, 'ROC-Registrar of Companies'),
(33, 'Competition Commission of India'),
(34, 'Central Electricity Regulatory Commission'),
(35, 'Warehousing Development and Regulatory Authority'),
(36, 'Atomic Energy Regulatory Board'),
(37, 'NHB-National Housing Bank'),
(38, 'Central Drug standardisation and control organisation'),
(39, 'Government of India'),
(40, 'International Accounting Standards'),
(41, 'Test'),
(42, 'Income tax'),
(43, 'Central Board of Excise and Customs'),
(44, 'The Fugitive Economic Offenders Act, 2018.'),
(45, 'Other');

-- --------------------------------------------------------

--
-- Table structure for table `partner_task`
--

CREATE TABLE `partner_task` (
  `id` int(11) NOT NULL,
  `task_name` varchar(255) DEFAULT NULL,
  `task_estimated_days` varchar(255) DEFAULT NULL,
  `task_auditing_standard` varchar(255) DEFAULT NULL,
  `task_international_auditing_standard` varchar(255) DEFAULT NULL,
  `activity_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `partner_task`
--

INSERT INTO `partner_task` (`id`, `task_name`, `task_estimated_days`, `task_auditing_standard`, `task_international_auditing_standard`, `activity_id`) VALUES
(76, 'Task 1', '2000', 'INS', 'IETE', 8),
(77, 'Task 2', '100', 'OSI', 'IFTF', 3),
(78, 'Task 3', '30', 'OSI', 'DCN', 7),
(79, 'Task 4', '43', 'MY', 'WHO', 5),
(80, 'Task 5', '432', 'MY', 'OJI', 6),
(81, 'Task 6', '54', 'PIIU', 'KSJCE', 7),
(82, 'Task 7', '09', 'KJSCETI', 'KJARTS', 8),
(83, 'Obtain Holding report from R&T', '1', 'AAS-1(i)', 'IAS 26', 11),
(84, 'Check financial reports made from Underlying books', '1', '', 'IAS 1', 11),
(85, 'wed task 1', '2', 'ISO', 'ISO', 6),
(86, 'Check Cash Balance', '1', 'IAS2', '', 12),
(87, 'Test task 2', '21', 'HJHDS', 'UIYREU', 8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auditapp_user`
--
ALTER TABLE `auditapp_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `business_area`
--
ALTER TABLE `business_area`
  ADD PRIMARY KEY (`id`),
  ADD KEY `business_area_industry_id_f38f0b37_fk_partner_industry_id` (`industry_id`);

--
-- Indexes for table `business_b_activity`
--
ALTER TABLE `business_b_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `business_b_activity_area_id_8ac53f31_fk_business_area_id` (`area_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auditapp_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `finance_f_activity`
--
ALTER TABLE `finance_f_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `finance_f_activity_area_id_384998a2_fk_finance_f_area_id` (`area_id`);

--
-- Indexes for table `finance_f_area`
--
ALTER TABLE `finance_f_area`
  ADD PRIMARY KEY (`id`),
  ADD KEY `finance_f_area_f_industry_id_b1a15a34_fk_partner_industry_id` (`f_industry_id`);

--
-- Indexes for table `partner_act`
--
ALTER TABLE `partner_act`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_activity`
--
ALTER TABLE `partner_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_activity_act_id_bbed62e5_fk_partner_act_id` (`act_id`);

--
-- Indexes for table `partner_activity_audit_type`
--
ALTER TABLE `partner_activity_audit_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_activity_audit_t_activity_id_audittype_id_ee46747b_uniq` (`activity_id`,`audittype_id`),
  ADD KEY `partner_activity_aud_audittype_id_c2da18f4_fk_partner_a` (`audittype_id`);

--
-- Indexes for table `partner_activity_entities`
--
ALTER TABLE `partner_activity_entities`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_activity_entities_activity_id_entity_id_ef97a4b1_uniq` (`activity_id`,`entity_id`),
  ADD KEY `partner_activity_ent_entity_id_94b9dcd7_fk_partner_e` (`entity_id`);

--
-- Indexes for table `partner_act_industry`
--
ALTER TABLE `partner_act_industry`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_act_industry_act_id_industry_id_9de9c93e_uniq` (`act_id`,`industry_id`),
  ADD KEY `partner_act_industry_industry_id_593b587f_fk_partner_industry_id` (`industry_id`);

--
-- Indexes for table `partner_audittype`
--
ALTER TABLE `partner_audittype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_client`
--
ALTER TABLE `partner_client`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_client_assigned_user_id_544465d2_fk_auditapp_user_id` (`assigned_user_id`);

--
-- Indexes for table `partner_clientactivities`
--
ALTER TABLE `partner_clientactivities`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_clientactivities_user_id_ed58b20c_fk_auditapp_user_id` (`user_id`);

--
-- Indexes for table `partner_clienttask`
--
ALTER TABLE `partner_clienttask`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_clienttask_user_id_a1b44cc3_fk_auditapp_user_id` (`user_id`),
  ADD KEY `partner_clienttask_client_id_cfdaefeb_fk_partner_client_id` (`client_id`),
  ADD KEY `partner_clienttask_act_id_05f0ffb6_fk_partner_act_id` (`act_id`),
  ADD KEY `partner_clienttask_activity_id_d9928643_fk_partner_activity_id` (`activity_id`);

--
-- Indexes for table `partner_client_audit_type`
--
ALTER TABLE `partner_client_audit_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_client_audit_type_client_id_audittype_id_5a19f6f5_uniq` (`client_id`,`audittype_id`),
  ADD KEY `partner_client_audit_audittype_id_43cc84f6_fk_partner_a` (`audittype_id`);

--
-- Indexes for table `partner_client_entities`
--
ALTER TABLE `partner_client_entities`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_client_entities_client_id_entity_id_891d6685_uniq` (`client_id`,`entity_id`),
  ADD KEY `partner_client_entities_entity_id_db3abc8f_fk_partner_entity_id` (`entity_id`);

--
-- Indexes for table `partner_client_industry`
--
ALTER TABLE `partner_client_industry`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_client_industry_client_id_industry_id_fc485afc_uniq` (`client_id`,`industry_id`),
  ADD KEY `partner_client_indus_industry_id_5dd54e18_fk_partner_i` (`industry_id`);

--
-- Indexes for table `partner_entity`
--
ALTER TABLE `partner_entity`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_industry`
--
ALTER TABLE `partner_industry`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_industry_regulation`
--
ALTER TABLE `partner_industry_regulation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_industry_regulat_industry_id_regulation_i_79b6cf34_uniq` (`industry_id`,`regulation_id`),
  ADD KEY `partner_industry_reg_regulation_id_ceba0ca7_fk_partner_r` (`regulation_id`);

--
-- Indexes for table `partner_regulation`
--
ALTER TABLE `partner_regulation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_task`
--
ALTER TABLE `partner_task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_task_activity_id_d5347460_fk_partner_activity_id` (`activity_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auditapp_user`
--
ALTER TABLE `auditapp_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `business_area`
--
ALTER TABLE `business_area`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `business_b_activity`
--
ALTER TABLE `business_b_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=305;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `finance_f_activity`
--
ALTER TABLE `finance_f_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `finance_f_area`
--
ALTER TABLE `finance_f_area`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `partner_act`
--
ALTER TABLE `partner_act`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `partner_activity`
--
ALTER TABLE `partner_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `partner_activity_audit_type`
--
ALTER TABLE `partner_activity_audit_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `partner_activity_entities`
--
ALTER TABLE `partner_activity_entities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `partner_act_industry`
--
ALTER TABLE `partner_act_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `partner_audittype`
--
ALTER TABLE `partner_audittype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `partner_client`
--
ALTER TABLE `partner_client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;

--
-- AUTO_INCREMENT for table `partner_clientactivities`
--
ALTER TABLE `partner_clientactivities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `partner_clienttask`
--
ALTER TABLE `partner_clienttask`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=461;

--
-- AUTO_INCREMENT for table `partner_client_audit_type`
--
ALTER TABLE `partner_client_audit_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=85;

--
-- AUTO_INCREMENT for table `partner_client_entities`
--
ALTER TABLE `partner_client_entities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=158;

--
-- AUTO_INCREMENT for table `partner_client_industry`
--
ALTER TABLE `partner_client_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;

--
-- AUTO_INCREMENT for table `partner_entity`
--
ALTER TABLE `partner_entity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `partner_industry`
--
ALTER TABLE `partner_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `partner_industry_regulation`
--
ALTER TABLE `partner_industry_regulation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `partner_regulation`
--
ALTER TABLE `partner_regulation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `partner_task`
--
ALTER TABLE `partner_task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=88;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `business_area`
--
ALTER TABLE `business_area`
  ADD CONSTRAINT `business_area_industry_id_f38f0b37_fk_partner_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`);

--
-- Constraints for table `business_b_activity`
--
ALTER TABLE `business_b_activity`
  ADD CONSTRAINT `business_b_activity_area_id_8ac53f31_fk_business_area_id` FOREIGN KEY (`area_id`) REFERENCES `business_area` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `finance_f_activity`
--
ALTER TABLE `finance_f_activity`
  ADD CONSTRAINT `finance_f_activity_area_id_384998a2_fk_finance_f_area_id` FOREIGN KEY (`area_id`) REFERENCES `finance_f_area` (`id`);

--
-- Constraints for table `finance_f_area`
--
ALTER TABLE `finance_f_area`
  ADD CONSTRAINT `finance_f_area_f_industry_id_b1a15a34_fk_partner_industry_id` FOREIGN KEY (`f_industry_id`) REFERENCES `partner_industry` (`id`);

--
-- Constraints for table `partner_activity`
--
ALTER TABLE `partner_activity`
  ADD CONSTRAINT `partner_activity_act_id_bbed62e5_fk_partner_act_id` FOREIGN KEY (`act_id`) REFERENCES `partner_act` (`id`);

--
-- Constraints for table `partner_activity_audit_type`
--
ALTER TABLE `partner_activity_audit_type`
  ADD CONSTRAINT `partner_activity_aud_activity_id_270f5717_fk_partner_a` FOREIGN KEY (`activity_id`) REFERENCES `partner_activity` (`id`),
  ADD CONSTRAINT `partner_activity_aud_audittype_id_c2da18f4_fk_partner_a` FOREIGN KEY (`audittype_id`) REFERENCES `partner_audittype` (`id`);

--
-- Constraints for table `partner_activity_entities`
--
ALTER TABLE `partner_activity_entities`
  ADD CONSTRAINT `partner_activity_ent_activity_id_083deed9_fk_partner_a` FOREIGN KEY (`activity_id`) REFERENCES `partner_activity` (`id`),
  ADD CONSTRAINT `partner_activity_ent_entity_id_94b9dcd7_fk_partner_e` FOREIGN KEY (`entity_id`) REFERENCES `partner_entity` (`id`);

--
-- Constraints for table `partner_act_industry`
--
ALTER TABLE `partner_act_industry`
  ADD CONSTRAINT `partner_act_industry_act_id_fc6314c0_fk_partner_act_id` FOREIGN KEY (`act_id`) REFERENCES `partner_act` (`id`),
  ADD CONSTRAINT `partner_act_industry_industry_id_593b587f_fk_partner_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`);

--
-- Constraints for table `partner_client`
--
ALTER TABLE `partner_client`
  ADD CONSTRAINT `partner_client_assigned_user_id_544465d2_fk_auditapp_user_id` FOREIGN KEY (`assigned_user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `partner_clientactivities`
--
ALTER TABLE `partner_clientactivities`
  ADD CONSTRAINT `partner_clientactivities_user_id_ed58b20c_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `partner_clienttask`
--
ALTER TABLE `partner_clienttask`
  ADD CONSTRAINT `partner_clienttask_act_id_05f0ffb6_fk_partner_act_id` FOREIGN KEY (`act_id`) REFERENCES `partner_act` (`id`),
  ADD CONSTRAINT `partner_clienttask_activity_id_d9928643_fk_partner_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `partner_activity` (`id`),
  ADD CONSTRAINT `partner_clienttask_client_id_cfdaefeb_fk_partner_client_id` FOREIGN KEY (`client_id`) REFERENCES `partner_client` (`id`),
  ADD CONSTRAINT `partner_clienttask_user_id_a1b44cc3_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `partner_client_audit_type`
--
ALTER TABLE `partner_client_audit_type`
  ADD CONSTRAINT `partner_client_audit_audittype_id_43cc84f6_fk_partner_a` FOREIGN KEY (`audittype_id`) REFERENCES `partner_audittype` (`id`),
  ADD CONSTRAINT `partner_client_audit_client_id_e975b576_fk_partner_c` FOREIGN KEY (`client_id`) REFERENCES `partner_client` (`id`);

--
-- Constraints for table `partner_client_entities`
--
ALTER TABLE `partner_client_entities`
  ADD CONSTRAINT `partner_client_entities_client_id_f455a129_fk_partner_client_id` FOREIGN KEY (`client_id`) REFERENCES `partner_client` (`id`),
  ADD CONSTRAINT `partner_client_entities_entity_id_db3abc8f_fk_partner_entity_id` FOREIGN KEY (`entity_id`) REFERENCES `partner_entity` (`id`);

--
-- Constraints for table `partner_client_industry`
--
ALTER TABLE `partner_client_industry`
  ADD CONSTRAINT `partner_client_indus_industry_id_5dd54e18_fk_partner_i` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`),
  ADD CONSTRAINT `partner_client_industry_client_id_589fdd31_fk_partner_client_id` FOREIGN KEY (`client_id`) REFERENCES `partner_client` (`id`);

--
-- Constraints for table `partner_industry_regulation`
--
ALTER TABLE `partner_industry_regulation`
  ADD CONSTRAINT `partner_industry_reg_industry_id_e2d4fa50_fk_partner_i` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`),
  ADD CONSTRAINT `partner_industry_reg_regulation_id_ceba0ca7_fk_partner_r` FOREIGN KEY (`regulation_id`) REFERENCES `partner_regulation` (`id`);

--
-- Constraints for table `partner_task`
--
ALTER TABLE `partner_task`
  ADD CONSTRAINT `partner_task_activity_id_d5347460_fk_partner_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `partner_activity` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
