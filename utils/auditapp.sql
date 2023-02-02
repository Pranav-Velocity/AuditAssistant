-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 27, 2020 at 06:55 PM
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
  `password` varchar(128) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `is_partner` tinyint(1) NOT NULL,
  `is_manager` tinyint(1) NOT NULL,
  `is_auditorclerk` tinyint(1) NOT NULL,
  `is_articleholder` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `auditapp_user`
--

INSERT INTO `auditapp_user` (`id`, `password`, `last_login`, `username`, `email`, `first_name`, `last_name`, `is_admin`, `is_partner`, `is_manager`, `is_auditorclerk`, `is_articleholder`, `is_active`) VALUES
(1, 'pbkdf2_sha256$150000$YYApMFeglm2R$pQQFGSLUHg4uo9oZQUqak90hXdPMcOEAoAOPOWHutAA=', '2020-04-24 17:41:14.375390', 'admin', '', NULL, NULL, 1, 0, 0, 0, 0, 1),
(2, 'pbkdf2_sha256$150000$36Z2k4crS9aH$0e+NjyM2MCiHRpg5BwMiDl40zVjV/70tYZCeZrNzbh0=', '2020-04-27 11:59:10.861921', 'partner1', NULL, NULL, NULL, 0, 1, 0, 0, 0, 1),
(3, 'pbkdf2_sha256$150000$WBSdvcVVOJYe$n29KKjlMao6BKaujqs3oXH80TEOghkXDHZ/RKs9QP/E=', '2020-04-25 09:24:12.572367', 'manager1', NULL, NULL, NULL, 0, 0, 1, 0, 0, 1),
(4, 'pbkdf2_sha256$150000$h5mKso6voBg3$0x80rddW5Qm0toMgsXh4qppqN/CvfxIhj8DE5NXsE4A=', '2020-04-25 13:05:30.477300', 'auditor1', NULL, NULL, NULL, 0, 0, 0, 1, 0, 1),
(6, 'pbkdf2_sha256$150000$qyQOChtItTn4$z8SCkKcyQiIpjEBX++5Q+7GnDOUAl3wDlcRe/TLe81A=', '2020-04-27 09:01:56.975000', 'article1', 'article1@yopmail.com', 'Article', '1', 0, 0, 0, 0, 1, 1),
(7, 'pbkdf2_sha256$150000$AAUnHJPxUGLH$8658yunmrBXupEI818W5si2rsZ9xsD3XmRmNMomjdXU=', '2020-04-27 17:11:08.216131', 'yadav', 'yadavgagan143tcsc@gmail.com', 'y', 'd', 0, 0, 1, 0, 0, 1),
(8, 'pbkdf2_sha256$150000$9fbBXhGIFhoJ$6WB6c7FwFG9WWYwrM7qev9EMPUBu7EA/ZH+aq9DbOvo=', '2020-04-27 10:50:40.926818', 'gagan', 'gagansinghyadav676@gmail.com', 'g', 'y', 0, 0, 0, 1, 0, 1),
(14, 'pbkdf2_sha256$150000$vUJyZYJxPeIA$IZ/QDwUuwGWF5R/Ec5xcO1OShOvtZ1tdYZtTWg7/Sp8=', '2020-04-25 13:11:54.609921', 'g123', 'gag@gmail.com', NULL, NULL, 0, 0, 0, 0, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

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
(25, 'Can add act', 7, 'add_act'),
(26, 'Can change act', 7, 'change_act'),
(27, 'Can delete act', 7, 'delete_act'),
(28, 'Can view act', 7, 'view_act'),
(29, 'Can add client', 8, 'add_client'),
(30, 'Can change client', 8, 'change_client'),
(31, 'Can delete client', 8, 'delete_client'),
(32, 'Can view client', 8, 'view_client'),
(33, 'Can add entity', 9, 'add_entity'),
(34, 'Can change entity', 9, 'change_entity'),
(35, 'Can delete entity', 9, 'delete_entity'),
(36, 'Can view entity', 9, 'view_entity'),
(37, 'Can add industry', 10, 'add_industry'),
(38, 'Can change industry', 10, 'change_industry'),
(39, 'Can delete industry', 10, 'delete_industry'),
(40, 'Can view industry', 10, 'view_industry'),
(41, 'Can add regulation', 11, 'add_regulation'),
(42, 'Can change regulation', 11, 'change_regulation'),
(43, 'Can delete regulation', 11, 'delete_regulation'),
(44, 'Can view regulation', 11, 'view_regulation'),
(45, 'Can add task', 12, 'add_task'),
(46, 'Can change task', 12, 'change_task'),
(47, 'Can delete task', 12, 'delete_task'),
(48, 'Can view task', 12, 'view_task'),
(49, 'Can add activity', 13, 'add_activity'),
(50, 'Can change activity', 13, 'change_activity'),
(51, 'Can delete activity', 13, 'delete_activity'),
(52, 'Can view activity', 13, 'view_activity'),
(53, 'Can add area', 14, 'add_area'),
(54, 'Can change area', 14, 'change_area'),
(55, 'Can delete area', 14, 'delete_area'),
(56, 'Can view area', 14, 'view_area'),
(57, 'Can add b_ task', 15, 'add_b_task'),
(58, 'Can change b_ task', 15, 'change_b_task'),
(59, 'Can delete b_ task', 15, 'delete_b_task'),
(60, 'Can view b_ task', 15, 'view_b_task'),
(61, 'Can add b_ activity', 16, 'add_b_activity'),
(62, 'Can change b_ activity', 16, 'change_b_activity'),
(63, 'Can delete b_ activity', 16, 'delete_b_activity'),
(64, 'Can view b_ activity', 16, 'view_b_activity'),
(65, 'Can add f_ task', 17, 'add_f_task'),
(66, 'Can change f_ task', 17, 'change_f_task'),
(67, 'Can delete f_ task', 17, 'delete_f_task'),
(68, 'Can view f_ task', 17, 'view_f_task'),
(69, 'Can add f_ area', 18, 'add_f_area'),
(70, 'Can change f_ area', 18, 'change_f_area'),
(71, 'Can delete f_ area', 18, 'delete_f_area'),
(72, 'Can view f_ area', 18, 'view_f_area'),
(73, 'Can add f_ activity', 19, 'add_f_activity'),
(74, 'Can change f_ activity', 19, 'change_f_activity'),
(75, 'Can delete f_ activity', 19, 'delete_f_activity'),
(76, 'Can view f_ activity', 19, 'view_f_activity'),
(77, 'Can add Billing info', 20, 'add_billinginfo'),
(78, 'Can change Billing info', 20, 'change_billinginfo'),
(79, 'Can delete Billing info', 20, 'delete_billinginfo'),
(80, 'Can view Billing info', 20, 'view_billinginfo'),
(81, 'Can add Invoice', 21, 'add_invoice'),
(82, 'Can change Invoice', 21, 'change_invoice'),
(83, 'Can delete Invoice', 21, 'delete_invoice'),
(84, 'Can view Invoice', 21, 'view_invoice'),
(85, 'Can add Order', 22, 'add_order'),
(86, 'Can change Order', 22, 'change_order'),
(87, 'Can delete Order', 22, 'delete_order'),
(88, 'Can view Order', 22, 'view_order'),
(89, 'Can add Plan', 23, 'add_plan'),
(90, 'Can change Plan', 23, 'change_plan'),
(91, 'Can delete Plan', 23, 'delete_plan'),
(92, 'Can view Plan', 23, 'view_plan'),
(93, 'Can add Plan pricing', 24, 'add_planpricing'),
(94, 'Can change Plan pricing', 24, 'change_planpricing'),
(95, 'Can delete Plan pricing', 24, 'delete_planpricing'),
(96, 'Can view Plan pricing', 24, 'view_planpricing'),
(97, 'Can add Plan quota', 25, 'add_planquota'),
(98, 'Can change Plan quota', 25, 'change_planquota'),
(99, 'Can delete Plan quota', 25, 'delete_planquota'),
(100, 'Can view Plan quota', 25, 'view_planquota'),
(101, 'Can add Pricing', 26, 'add_pricing'),
(102, 'Can change Pricing', 26, 'change_pricing'),
(103, 'Can delete Pricing', 26, 'delete_pricing'),
(104, 'Can view Pricing', 26, 'view_pricing'),
(105, 'Can add Quota', 27, 'add_quota'),
(106, 'Can change Quota', 27, 'change_quota'),
(107, 'Can delete Quota', 27, 'delete_quota'),
(108, 'Can view Quota', 27, 'view_quota'),
(109, 'Can add User plan', 28, 'add_userplan'),
(110, 'Can change User plan', 28, 'change_userplan'),
(111, 'Can delete User plan', 28, 'delete_userplan'),
(112, 'Can view User plan', 28, 'view_userplan'),
(113, 'Can add g_ task', 29, 'add_g_task'),
(114, 'Can change g_ task', 29, 'change_g_task'),
(115, 'Can delete g_ task', 29, 'delete_g_task'),
(116, 'Can view g_ task', 29, 'view_g_task'),
(117, 'Can add assigned activities', 29, 'add_assignedactivities'),
(118, 'Can change assigned activities', 29, 'change_assignedactivities'),
(119, 'Can delete assigned activities', 29, 'delete_assignedactivities'),
(120, 'Can view assigned activities', 29, 'view_assignedactivities'),
(121, 'Can add company', 30, 'add_company'),
(122, 'Can change company', 30, 'change_company'),
(123, 'Can delete company', 30, 'delete_company'),
(124, 'Can view company', 30, 'view_company'),
(125, 'Can add audit plan', 31, 'add_auditplan'),
(126, 'Can change audit plan', 31, 'change_auditplan'),
(127, 'Can delete audit plan', 31, 'delete_auditplan'),
(128, 'Can view audit plan', 31, 'view_auditplan');

-- --------------------------------------------------------

--
-- Table structure for table `business_area`
--

CREATE TABLE `business_area` (
  `id` int(11) NOT NULL,
  `area_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `industry_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `business_b_activity`
--

CREATE TABLE `business_b_activity` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `b_activity_description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `area_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2020-03-13 10:39:49.381986', '2', 'partner1', 1, '[{\"added\": {}}]', 6, 1),
(2, '2020-03-13 10:40:11.581786', '3', 'manager1', 1, '[{\"added\": {}}]', 6, 1),
(3, '2020-03-13 10:40:26.104586', '3', 'manager1', 2, '[{\"changed\": {\"fields\": [\"is_manager\"]}}]', 6, 1),
(4, '2020-03-13 10:40:56.994186', '4', 'auditor1', 1, '[{\"added\": {}}]', 6, 1),
(5, '2020-03-16 08:31:22.903240', '5', 'gagan', 1, '[{\"added\": {}}]', 6, 1),
(6, '2020-03-16 13:02:41.068256', '6', 'gagan', 1, '[{\"added\": {}}]', 6, 1),
(7, '2020-03-16 16:37:03.358165', '6', 'article1', 2, '[{\"changed\": {\"fields\": [\"username\", \"email\", \"first_name\", \"last_name\"]}}]', 6, 1),
(8, '2020-03-16 17:38:16.010165', '6', 'article1', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1),
(9, '2020-03-16 17:38:27.057165', '6', 'article1', 2, '[]', 6, 1),
(10, '2020-03-17 07:51:28.375962', '7', 'yadav', 1, '[{\"added\": {}}]', 6, 1),
(11, '2020-03-17 07:51:40.745332', '7', 'yadav', 2, '[]', 6, 1),
(12, '2020-03-17 07:52:05.369669', '8', 'gagan', 1, '[{\"added\": {}}]', 6, 1),
(13, '2020-03-18 10:56:53.457900', '1', 'CHS', 1, '[{\"added\": {}}]', 9, 1),
(14, '2020-03-18 10:57:02.104382', '2', 'RTS', 1, '[{\"added\": {}}]', 9, 1),
(15, '2020-03-18 11:03:53.504723', '1', 'Company object (1)', 1, '[{\"added\": {}}]', 30, 1),
(16, '2020-03-18 11:41:31.305196', '3', 'CHS', 1, '[{\"added\": {}}]', 9, 1),
(17, '2020-03-18 11:43:57.795351', '16', 'Client 1', 1, '[{\"added\": {}}]', 8, 1),
(18, '2020-03-18 12:05:04.524714', '17', 'Client 2', 1, '[{\"added\": {}}]', 8, 1),
(19, '2020-03-19 13:48:31.868718', '14', 'g123', 1, '[{\"added\": {}}]', 6, 1),
(20, '2020-04-24 17:18:50.647285', '3', 'manager1', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(6, 'auditapp', 'user'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(14, 'business', 'area'),
(16, 'business', 'b_activity'),
(15, 'business', 'b_task'),
(4, 'contenttypes', 'contenttype'),
(19, 'finance', 'f_activity'),
(18, 'finance', 'f_area'),
(17, 'finance', 'f_task'),
(7, 'partner', 'act'),
(13, 'partner', 'activity'),
(29, 'partner', 'assignedactivities'),
(31, 'partner', 'auditplan'),
(8, 'partner', 'client'),
(30, 'partner', 'company'),
(9, 'partner', 'entity'),
(10, 'partner', 'industry'),
(11, 'partner', 'regulation'),
(12, 'partner', 'task'),
(20, 'plans', 'billinginfo'),
(21, 'plans', 'invoice'),
(22, 'plans', 'order'),
(23, 'plans', 'plan'),
(24, 'plans', 'planpricing'),
(25, 'plans', 'planquota'),
(26, 'plans', 'pricing'),
(27, 'plans', 'quota'),
(28, 'plans', 'userplan'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2020-03-13 10:35:50.729586'),
(2, 'auditapp', '0001_initial', '2020-03-13 10:35:53.303586'),
(3, 'admin', '0001_initial', '2020-03-13 10:35:55.037386'),
(4, 'admin', '0002_logentry_remove_auto_add', '2020-03-13 10:35:56.051786'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2020-03-13 10:35:56.316986'),
(6, 'contenttypes', '0002_remove_content_type_name', '2020-03-13 10:35:57.549386'),
(7, 'auth', '0001_initial', '2020-03-13 10:35:59.951786'),
(8, 'auth', '0002_alter_permission_name_max_length', '2020-03-13 10:36:02.151386'),
(9, 'auth', '0003_alter_user_email_max_length', '2020-03-13 10:36:02.432186'),
(10, 'auth', '0004_alter_user_username_opts', '2020-03-13 10:36:02.712986'),
(11, 'auth', '0005_alter_user_last_login_null', '2020-03-13 10:36:02.978186'),
(12, 'auth', '0006_require_contenttypes_0002', '2020-03-13 10:36:03.243386'),
(13, 'auth', '0007_alter_validators_add_error_messages', '2020-03-13 10:36:03.524186'),
(14, 'auth', '0008_alter_user_username_max_length', '2020-03-13 10:36:03.820586'),
(15, 'auth', '0009_alter_user_last_name_max_length', '2020-03-13 10:36:04.116986'),
(16, 'auth', '0010_alter_group_name_max_length', '2020-03-13 10:36:04.772186'),
(17, 'auth', '0011_update_proxy_permissions', '2020-03-13 10:36:05.442986'),
(18, 'partner', '0001_initial', '2020-03-13 10:36:12.197786'),
(19, 'business', '0001_initial', '2020-03-13 10:36:17.127386'),
(20, 'finance', '0001_initial', '2020-03-13 10:36:21.386186'),
(21, 'plans', '0001_initial', '2020-03-13 10:36:41.316786'),
(22, 'plans', '0002_auto_20200313_0828', '2020-03-13 10:36:51.831186'),
(23, 'sessions', '0001_initial', '2020-03-13 10:36:52.782786'),
(24, 'business', '0002_delete_b_task', '2020-03-13 16:04:45.123287'),
(25, 'finance', '0002_delete_f_task', '2020-03-13 16:04:45.562312'),
(26, 'partner', '0002_g_task', '2020-03-13 16:04:46.859386'),
(27, 'partner', '0003_auto_20200313_2146', '2020-03-13 16:16:39.049121'),
(28, 'partner', '0004_g_task_username', '2020-03-16 06:05:44.002648'),
(29, 'partner', '0005_auto_20200314_1231', '2020-03-16 06:05:45.338946'),
(30, 'plans', '0002_auto_20200305_1701', '2020-03-16 06:05:46.262748'),
(31, 'partner', '0006_auto_20200316_1526', '2020-03-16 09:56:45.304027'),
(32, 'plans', '0002_auto_20200307_1231', '2020-03-16 09:56:45.638223'),
(33, 'partner', '0007_activity_user', '2020-03-16 09:57:41.402970'),
(34, 'partner', '0008_remove_activity_user', '2020-03-16 10:09:22.968355'),
(35, 'partner', '0006_auto_20200316_1719', '2020-03-16 11:51:31.126165'),
(36, 'partner', '0007_auto_20200316_1720', '2020-03-16 11:51:31.716165'),
(37, 'partner', '0008_auto_20200316_2256', '2020-03-16 17:27:04.210165'),
(38, 'partner', '0009_task_user', '2020-03-17 09:25:56.851906'),
(39, 'plans', '0002_auto_20200317_0224', '2020-03-17 09:25:57.712402'),
(40, 'partner', '0010_auto_20200318_1533', '2020-03-18 10:04:20.308636'),
(41, 'plans', '0002_auto_20200318_1533', '2020-03-18 10:04:22.148956'),
(42, 'partner', '0011_auto_20200318_1552', '2020-03-18 10:22:31.494660'),
(43, 'partner', '0012_auto_20200319_1612', '2020-03-19 10:43:11.471917'),
(44, 'partner', '0013_auto_20200319_1706', '2020-03-19 11:36:07.057917'),
(45, 'partner', '0012_task_status', '2020-03-19 11:58:02.034177'),
(46, 'plans', '0002_auto_20200319_0608', '2020-03-19 13:08:51.330904'),
(47, 'partner', '0014_task_status', '2020-03-19 13:21:32.594035'),
(48, 'partner', '0015_auto_20200320_1813', '2020-03-20 12:43:11.986110'),
(49, 'partner', '0002_task_is_approved', '2020-04-21 09:08:41.437347'),
(50, 'partner', '0003_task_is_rejected', '2020-04-22 09:07:24.561435'),
(51, 'partner', '0004_task_is_start', '2020-04-23 18:54:44.642765'),
(52, 'partner', '0005_task_is_reject', '2020-04-24 07:35:15.110599'),
(53, 'partner', '0006_task_rejection_remark', '2020-04-24 09:31:48.202406'),
(54, 'partner', '0007_client_assigned_users', '2020-04-26 11:56:36.225222');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0nmh8u6by8x78650ba41x6rr4phiuvvx', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-04-09 09:30:39.884214'),
('0qdbjfloximtumntc25ka45l0p23k34l', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-10 13:17:41.308602'),
('151ue1r8zq5zcea0bbq5ra4mpy1cu2g6', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-10 08:48:20.846383'),
('2xrqzb353u2m8i2jmcnces8rbgv99l6l', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-04-07 16:05:10.842205'),
('6nxmnzsm5njc9ph86zvtll6o2yshp24x', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-04-01 05:30:36.840985'),
('6uh7c8ww8owi76f0zwlmr9vvvak6bi7k', 'M2U5NzYzOWMxNWMxYWM4ZWZlNWNiZjU5ZmQ0ZGJhNjAzOTIzMjA4Mzp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3MGI3N2E2ZTFlM2Y3MTI5Njk1NzIxNDBlMTY0Y2ZkODk2MjhmNWUzIn0=', '2020-05-09 13:52:37.549819'),
('8y53rnee4f2vwnwypma1upneokqb0894', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-09 04:49:20.664748'),
('91j2v31053dob9ydpnd9melexjnztg25', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-03-31 18:46:47.894022'),
('ag93k5jjgkjzlko7ka15qsb61n9hzm6j', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-03-30 17:49:11.399165'),
('apotvxeoysi2s8yczsdyc8neiecnxqj2', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-05-10 17:33:31.982320'),
('by3enwss68c10ca7iiph56lyar56tl6v', 'MzkxZTA2OGQ4MTAxNDhlZWRlNjBkNjkwZTljMGMyMDQ2YjU4Yjk4NTp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5M2I0YTY0YThmNjNkM2M1MzdlMGJiNDMzOGE3NmViZDhjMDFmYzM2In0=', '2020-03-30 13:03:15.594108'),
('c17poa2vlp26w85rc2ryei0d03l10xac', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-08 08:51:29.340845'),
('c2hlv26ej5spmakwrsqzq0y9ukhuuu4d', 'MmZjYzNhOTRlMzc3YTVkYjVkM2U2MjNkNmZmMGU2MGJiNzY1N2RiOTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjZWI2OGQxNjI2ZjMyMzYzZWNlZTk1YWNjY2E5OGVjZGI2YjEyZDAxIn0=', '2020-03-30 08:30:48.261404'),
('c96zbabyt2verybez4qlmj7of084r2yf', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-10 13:22:17.992701'),
('cvm9aiqu69noszx6w05h9i703e8y1ppc', 'MmZjYzNhOTRlMzc3YTVkYjVkM2U2MjNkNmZmMGU2MGJiNzY1N2RiOTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjZWI2OGQxNjI2ZjMyMzYzZWNlZTk1YWNjY2E5OGVjZGI2YjEyZDAxIn0=', '2020-03-30 14:00:58.309165'),
('dkbns3ez73sir4a47y0q53ggfv5eardo', 'MmZjYzNhOTRlMzc3YTVkYjVkM2U2MjNkNmZmMGU2MGJiNzY1N2RiOTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjZWI2OGQxNjI2ZjMyMzYzZWNlZTk1YWNjY2E5OGVjZGI2YjEyZDAxIn0=', '2020-05-08 17:41:14.517405'),
('fzy6q60xflgesohi2re8ugk8q0845zcz', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-04-03 12:49:44.728068'),
('g6su574lhmqxkv87cfxjhc9x93lr89kn', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-10 17:15:59.700621'),
('gf4ctb2bz2thgj5zdb4owgphxrap26um', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-10 17:22:33.296261'),
('hetslrxejegz9q6uwdo1zx182akzvc93', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-04-02 07:09:21.721991'),
('htsoc5yj8p79hw5xe1erhkirq37o7vp7', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-04-01 11:39:45.162393'),
('igdov1b2lq3f2hyzzk6suj8fhyhxp90i', 'OTQwZTBmZTE0Y2I3ZmVjZTg2ZmQxOTAyOGZjZDk2YmY0ODY1OWUxOTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkYjI3YzM3NzU5ODAyMmU4MjgyNjM4NzZiYmNhN2QyYzFmNTA1ZWE2In0=', '2020-05-08 19:46:32.611924'),
('jle49yw8notrfg5a07w1xq3eq49ryl7f', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-08 09:16:10.979154'),
('jmlhvee68z5ivpne6xlstpzs2jvvbhuh', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-03-30 06:07:12.400649'),
('kv1qn0fenxme0yd6aqbb4oryi78w768y', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-03-31 10:50:40.452032'),
('kyxxwftho1m3io0tttt9pjjrcx3ncfqc', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-11 17:11:08.254137'),
('laagsa7vmqcn7vi1v5rcwi6xrce70pym', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-09 17:33:47.581243'),
('oo0hs16x4hsniajbwnjce0eb5nb72se3', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-05-08 19:37:38.915396'),
('pgzotp8u5chliwum3nlyhcy1i11jqr5g', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-11 13:50:40.993152'),
('plc1akb0b3fh2kahx4g0fkli3n0ih97c', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-04-22 15:16:01.938786'),
('pwz2s8zqgpj10cbau6gxckhe05vpzew3', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-08 19:13:18.348391'),
('pzjd23zcoo0xznq9hk0bga2f7tyagw4n', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-10 10:18:49.212748'),
('qf4yqvg23pj3tqjm4ksi2dcyrke1sb91', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-04-03 09:44:36.879565'),
('qkv18svxgrgjtp2p3vixqep8qyhaprhm', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-03-31 08:40:21.092522'),
('qn8h8dy02mac6wa81mepe3kuy0nmn63x', 'MmNlOWUwZTIzOTc2MGZmYWM3ODAyNmNlMjQ5YTlkYjMxNTI5NWJmZTp7Il9hdXRoX3VzZXJfaWQiOiI3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzQ5YjkzYjNkMGE1MDUwMzQyODcxMDljNWYxZWQ3YjgzZDNlM2VjIn0=', '2020-05-11 12:41:40.029730'),
('rf1x32z8vfkd7x1hic5wq7iw0qj4zffu', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-10 07:32:03.757143'),
('rkldjgq1r8ftx6c440eduuhd06pognve', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-04-02 09:18:01.368917'),
('u0z4i3i4exhgjh8s0kk1ci55sytg5ybu', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-04-03 10:12:33.349825'),
('ubu2issyuwavfujmbm6f2cjo35xkt3x8', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-04-07 16:07:42.689432'),
('uzqt758k079dxqd2w1bmwvq4aj99vu70', 'NmM3MzZlMzUzNjFhZmQ0YzIxMWQ5NmFjNjJlZmE3NDc2MDJiOTU1Yjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmMWY0OGQ1YjgwYjBmZjVmMjI4MTU0OWQwZjFjNjQ1MDUxM2M0MmJjIn0=', '2020-05-10 11:38:17.425870'),
('wt53whhoixdx7e9v42vq53n4kfw7nrix', 'OTQwZTBmZTE0Y2I3ZmVjZTg2ZmQxOTAyOGZjZDk2YmY0ODY1OWUxOTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkYjI3YzM3NzU5ODAyMmU4MjgyNjM4NzZiYmNhN2QyYzFmNTA1ZWE2In0=', '2020-05-08 19:34:57.518388'),
('x6nx0wt8epfb5bttuzhi2ly0tedo3gm7', 'MmZjYzNhOTRlMzc3YTVkYjVkM2U2MjNkNmZmMGU2MGJiNzY1N2RiOTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJjZWI2OGQxNjI2ZjMyMzYzZWNlZTk1YWNjY2E5OGVjZGI2YjEyZDAxIn0=', '2020-04-01 10:56:37.754278'),
('x8rky0nksrculylyh2egdsiowofn5gbe', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-05-08 08:51:33.365838'),
('yazcli49qfpfyvyiranc17atuprbatq9', 'OTQwZTBmZTE0Y2I3ZmVjZTg2ZmQxOTAyOGZjZDk2YmY0ODY1OWUxOTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJkYjI3YzM3NzU5ODAyMmU4MjgyNjM4NzZiYmNhN2QyYzFmNTA1ZWE2In0=', '2020-05-09 09:24:12.718370'),
('zt7c6fl6ycshm842oy7kk6cgmn3x5a9k', 'NzI2ZDM1Njc0ZjkwMDkyMGIzMGJjYTg3NWY5MzE1NTVhNDQ5NDFiYjp7Il9hdXRoX3VzZXJfaWQiOiI2IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxN2QyOWY5NDcyMWEyZGRlZTcwZmE0NTYwYjkwYTE3ZmYzNjMzMTIwIn0=', '2020-05-10 06:56:52.854476');

-- --------------------------------------------------------

--
-- Table structure for table `finance_f_activity`
--

CREATE TABLE `finance_f_activity` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `f_activity_description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `area_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `finance_f_area`
--

CREATE TABLE `finance_f_area` (
  `id` int(11) NOT NULL,
  `area_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `f_industry_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `partner_act`
--

CREATE TABLE `partner_act` (
  `id` int(11) NOT NULL,
  `act_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `industry_id` int(11) DEFAULT NULL,
  `regulation_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_act`
--

INSERT INTO `partner_act` (`id`, `act_name`, `industry_id`, `regulation_id`) VALUES
(11, 'Income Tax Act 1961', 3, 51),
(12, 'The Central Goods and Services Tax Act, 2017 ', 3, 52),
(13, 'The Integrated Goods and Services Tax Act, 2017', 3, 52),
(14, 'The Union Territory Goods and Services Tax Act, 2017', 3, 52),
(15, 'The Pension Fund Regulatory and Development Authority Act, 2013', 3, 11),
(16, 'The Insolvency and Bankruptcy Code, 2016 ', 3, 5),
(17, 'The Companies Act, 2013 ', 3, 40),
(18, 'The Limited Liability Partnership Act, 2008 ', 3, 54);

-- --------------------------------------------------------

--
-- Table structure for table `partner_activity`
--

CREATE TABLE `partner_activity` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `activity_description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `act_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_activity`
--

INSERT INTO `partner_activity` (`id`, `activity_name`, `activity_description`, `act_id`) VALUES
(6, 'activity 1 rbi', 'check records', NULL),
(7, 'activity 1 rbi 2', 'police report', NULL),
(8, 'activity 1 sebi 1', 'check', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `partner_assignedactivities`
--

CREATE TABLE `partner_assignedactivities` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `activity_description` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `task_start_date` date DEFAULT NULL,
  `task_end_date` date DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_assignedactivities`
--

INSERT INTO `partner_assignedactivities` (`id`, `activity_name`, `activity_description`, `task_start_date`, `task_end_date`, `user_id`) VALUES
(31, 'activity 1 rbi', 'check records', '2020-03-18', '2020-03-20', 6);

-- --------------------------------------------------------

--
-- Table structure for table `partner_auditplan`
--

CREATE TABLE `partner_auditplan` (
  `id` int(11) NOT NULL,
  `parent_company` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `client_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `industry_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `statutory_audit` tinyint(1) NOT NULL,
  `taxation_audit` tinyint(1) NOT NULL,
  `internal_audit` tinyint(1) NOT NULL,
  `certification_audit` tinyint(1) NOT NULL,
  `investigation_assignment_audit` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `partner_auditplan_entity`
--

CREATE TABLE `partner_auditplan_entity` (
  `id` int(11) NOT NULL,
  `auditplan_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `partner_client`
--

CREATE TABLE `partner_client` (
  `id` int(11) NOT NULL,
  `client_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `industry_id` int(11) DEFAULT NULL,
  `client_start_date` date DEFAULT NULL,
  `client_end_date` date DEFAULT NULL,
  `certification_audit` tinyint(1) NOT NULL,
  `gst_no` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `internal_audit` tinyint(1) NOT NULL,
  `investigation_assignment_audit` tinyint(1) NOT NULL,
  `pan_no` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `statutory_audit` tinyint(1) NOT NULL,
  `taxation_audit` tinyint(1) NOT NULL,
  `company_id` int(11) DEFAULT NULL,
  `assigned_users_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_client`
--

INSERT INTO `partner_client` (`id`, `client_name`, `industry_id`, `client_start_date`, `client_end_date`, `certification_audit`, `gst_no`, `internal_audit`, `investigation_assignment_audit`, `pan_no`, `statutory_audit`, `taxation_audit`, `company_id`, `assigned_users_id`) VALUES
(16, 'Client 1', NULL, '2020-03-18', '2020-03-31', 1, 'DHGDHSG321312', 0, 0, 'ABCDF1234F', 1, 1, NULL, 3),
(17, 'Client 2', 3, '2020-03-31', '2020-08-13', 1, 'ASDFGJKL2313', 1, 1, 'DGSHG3131I', 0, 0, NULL, NULL),
(24, 'gagan', 3, NULL, NULL, 0, 'QWERF1254T4', 1, 0, 'BSDEF4587R', 1, 0, NULL, 7),
(26, 'test1', 21, '2020-03-31', '2020-04-01', 0, 'testgst', 0, 0, 'testpan', 1, 0, NULL, 7);

-- --------------------------------------------------------

--
-- Table structure for table `partner_client_entities`
--

CREATE TABLE `partner_client_entities` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_client_entities`
--

INSERT INTO `partner_client_entities` (`id`, `client_id`, `entity_id`) VALUES
(6, 26, 6),
(7, 26, 7);

-- --------------------------------------------------------

--
-- Table structure for table `partner_company`
--

CREATE TABLE `partner_company` (
  `id` int(11) NOT NULL,
  `company_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `partner_entity`
--

CREATE TABLE `partner_entity` (
  `id` int(11) NOT NULL,
  `entity_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_entity`
--

INSERT INTO `partner_entity` (`id`, `entity_name`) VALUES
(6, 'Company-Public Limited'),
(7, 'Company-Deemed Public Limited'),
(9, 'Coopertaive Housing Society'),
(10, 'Trust-Public'),
(11, 'Trust-Private'),
(12, 'Partnership Firm'),
(13, 'Association of Persons'),
(14, 'Sole properitor'),
(15, 'Cooperative Society-Deposit Accepting'),
(16, 'Coopertaive Society-Non Deposit Accepting'),
(17, 'Limited Liability Partnerships ( LLP)'),
(21, 'Company-Private Limited-Limited by Shares'),
(22, 'Company-Private Limited-Limited by gurantee'),
(24, 'Company-Private Limited-Unlimited'),
(27, 'Hindu Undivided Family-HUF'),
(28, 'Individual');

-- --------------------------------------------------------

--
-- Table structure for table `partner_industry`
--

CREATE TABLE `partner_industry` (
  `id` int(11) NOT NULL,
  `industry_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_industry`
--

INSERT INTO `partner_industry` (`id`, `industry_name`) VALUES
(3, 'Marketing'),
(4, 'Automobiles'),
(7, 'Chemicals'),
(8, 'Banks-Public Sector'),
(9, 'Banks-Private Sector'),
(10, 'NBFC-Non FD accepting'),
(11, 'NBFC-FD accepting'),
(12, 'Housing Finance-FD Accepting'),
(14, 'Houing Finance-Non FD accepting'),
(15, 'FMCG-Food'),
(16, 'Consumer Durables'),
(17, 'Advertising'),
(18, 'Construction-Housing'),
(19, 'Construction-Commercial'),
(20, 'Pharma'),
(21, 'Healthcare-Hospitals'),
(22, 'Healthcare-Diagnostic Centers'),
(23, 'Metals'),
(24, 'Metals and Mining'),
(25, 'FERTILISERS & PESTICIDES'),
(26, 'TEXTILES'),
(27, 'CEMENT & CEMENT PRODUCTS'),
(28, 'TELECOM'),
(29, 'Forest Products'),
(30, 'Power'),
(31, 'Oil and Gas'),
(32, 'Trading'),
(33, 'Hotels/Resorts'),
(34, 'Engineering '),
(35, 'Manufacturing'),
(36, 'Manpower Services'),
(37, 'Movie Exhibition'),
(38, 'Movie Production'),
(39, 'Logistics-Transporters'),
(40, 'Logistics-Others'),
(41, 'IT/ITES'),
(42, 'Computer Hardware');

-- --------------------------------------------------------

--
-- Table structure for table `partner_regulation`
--

CREATE TABLE `partner_regulation` (
  `id` int(11) NOT NULL,
  `regulation_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_regulation`
--

INSERT INTO `partner_regulation` (`id`, `regulation_name`) VALUES
(5, 'RBI – Reserve Bank of India'),
(8, 'SEBI – Securities and Exchange Board of India'),
(10, 'IRDAI – Insurance Regulatory and Development Authority of India'),
(11, 'PFRDA – Pension Fund Regulatory & Development Authority'),
(12, 'NABARD – National Bank for Agriculture and Rural Development'),
(13, 'SIDBI – Small Industries Development Bank of India'),
(14, 'NHB - National Housing Bank'),
(15, 'TRAI – Telecom Regulatory Authority of India'),
(16, 'CBFC – Central Board of Film Certification'),
(17, 'FSDC – Financial Stability and Development Council'),
(18, 'FSSAI – Food Safety and Standards Authority of India'),
(19, 'BIS – Bureau of Indian Standards'),
(20, 'ASCI – Advertising Standards Council of India'),
(21, 'BCCI – Board of Control for Cricket in India'),
(22, 'AMFI – Association of Mutual Funds in India'),
(23, 'EEPC – Engineering Export Promotional Council of India'),
(24, 'EICI – Express Industry Council of India'),
(25, 'FIEO – Federation of Indian Export Organisation'),
(26, 'INSA – Indian National Shipowners’ Association'),
(27, 'ICC – Indian Chemical Council'),
(28, 'ISSDA – Indian Stainless Steel Development Association'),
(29, 'MAIT – Manufacturers’ Association for Information Technology'),
(30, 'NASSCOM – National Association of Software and Service Companies'),
(31, 'OPPI – Organisation Of Plastic Processors of India'),
(32, ' PEPC – Project Exports Promotion Council of India'),
(33, 'CDSCO – Central Drugs Standard Control Organisation'),
(34, 'Inland Waterways Authority of India'),
(35, 'National Highways Authority of India'),
(37, 'ICAI-Institute of Chartered Accountants of India'),
(38, 'DGMS-Directorate General of Mines Safety'),
(39, 'Airports Economic Regulatory Authority'),
(40, 'ROC-Registrar of Companies'),
(41, 'Competition Commission of India'),
(42, 'Central Electricity Regulatory Commission'),
(43, 'Warehousing Development and Regulatory Authority'),
(44, 'Atomic Energy Regulatory Board'),
(45, 'NHB-National Housing Bank'),
(46, 'Central Drug standardisation and control organisation'),
(47, 'Government of India'),
(48, 'International Accounting Standards'),
(50, 'Test'),
(51, 'Income tax'),
(52, 'Central Board of Excise and Customs'),
(53, 'The Fugitive Economic Offenders Act, 2018.'),
(54, 'Other');

-- --------------------------------------------------------

--
-- Table structure for table `partner_task`
--

CREATE TABLE `partner_task` (
  `id` int(11) NOT NULL,
  `task_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `task_regulation_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `task_act_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `task_activity_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `client_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `task_auditing_standard` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `task_estimated_date` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `task_international_auditing_standard` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `task_end_date` date DEFAULT NULL,
  `task_start_date` date DEFAULT NULL,
  `attachment_file` varchar(100) COLLATE utf8_unicode_ci DEFAULT NULL,
  `remark` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `status` varchar(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '0 - Not sent for approval 1 - Sent for approval',
  `is_completed` tinyint(1) NOT NULL,
  `is_approved` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `is_rejected` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `is_start` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `is_reject` varchar(1) COLLATE utf8_unicode_ci NOT NULL,
  `rejection_remark` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `partner_task`
--

INSERT INTO `partner_task` (`id`, `task_name`, `task_regulation_name`, `task_act_name`, `task_activity_name`, `client_id`, `user_id`, `task_auditing_standard`, `task_estimated_date`, `task_international_auditing_standard`, `task_end_date`, `task_start_date`, `attachment_file`, `remark`, `status`, `is_completed`, `is_approved`, `is_rejected`, `is_start`, `is_reject`, `rejection_remark`) VALUES
(18, 'Task 2', 'RBI', 'RBI 2', 'activity 1 rbi 2', 16, 6, 'ISO', '5', 'ISO 2', '2020-03-18', '2020-03-01', 'task_submission/18/students.xlsx', 'This is a test', '0', 0, '0', '0', '0', '1', 'vvgvgvgvg'),
(19, 'Task 1', 'SEBI', 'sebi 1', 'activity 1 sebi 1', 17, 8, 'ISO-2', '10', 'IOS', '2020-05-01', '2020-04-21', '', NULL, '1', 0, '0', '0', '0', '0', NULL),
(20, 'Task 3', 'RBI', 'RBI 1', 'activity 1 rbi', 16, 8, 'ISO', '20', 'KJS', '2020-04-22', '2020-03-28', 'task_submission/20/selection_sort.py', 'file upload', '0', 0, '0', '0', '1', '0', 'rejectes'),
(35, 'Task 3', 'RBI', 'RBI 1', 'Task 3', 16, 8, 'testing inline editing', '4', 'testing inline', '2020-03-18', '2020-03-31', 'task_submission/35/selection_sort.py', 'file uploaded again', '1', 0, '0', '1', '1', '0', NULL),
(53, 'Task 3', 'RBI', 'RBI 1', 'Task 3', 16, NULL, 'test', '400', 'test', '2020-04-26', '2020-04-22', '', NULL, '0', 0, '0', '0', '0', '1', NULL),
(59, 'G1', 'SEBI', 'RBI 1', 'activity 1 rbi 2', 24, NULL, 'updated RTF', '100', 'updated FTR', '2020-04-29', '2020-04-20', '', NULL, '0', 0, '0', '0', '0', '1', 'Too much work'),
(60, 'testtask1', 'PFRDA – Pension Fund Regulatory & Development Authority', 'The Central Goods and Services Tax Act, 2017 ', 'activity 1 rbi', 26, NULL, 'ee', '3', 'ede', '2020-04-01', '2020-04-09', 'task_submission/60/Screenshot_2020-04-25_at_9.37.56_PM.png', 'done something', '1', 0, '0', '1', '1', '0', NULL),
(61, 'gagan ka task', 'RBI – Reserve Bank of India', 'Income Tax Act 1961', 'activity 1 rbi', 16, 6, 'iso', '4', 'iso', '2020-04-01', '2020-04-02', 'task_submission/61/_media_task_submission_60_Screenshot_2020-04-25_at_9.37.56_PM.png', 'gfayudvhair\r\n', '1', 0, '1', '0', '1', '0', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `plans_billinginfo`
--

CREATE TABLE `plans_billinginfo` (
  `id` int(11) NOT NULL,
  `tax_number` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `street` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `zipcode` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `city` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `country` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_street` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_zipcode` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_city` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_invoice`
--

CREATE TABLE `plans_invoice` (
  `id` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `full_number` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `type` int(11) NOT NULL,
  `issued` date NOT NULL,
  `issued_duplicate` date DEFAULT NULL,
  `selling_date` date DEFAULT NULL,
  `payment_date` date NOT NULL,
  `unit_price_net` decimal(7,2) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_net` decimal(7,2) NOT NULL,
  `total` decimal(7,2) NOT NULL,
  `tax_total` decimal(7,2) NOT NULL,
  `tax` decimal(4,2) DEFAULT NULL,
  `rebate` decimal(4,2) NOT NULL,
  `currency` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `item_description` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `buyer_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `buyer_street` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `buyer_zipcode` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `buyer_city` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `buyer_country` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `buyer_tax_number` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_street` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_zipcode` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_city` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `shipping_country` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `require_shipment` tinyint(1) NOT NULL,
  `issuer_name` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `issuer_street` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `issuer_zipcode` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `issuer_city` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `issuer_country` varchar(2) COLLATE utf8_unicode_ci NOT NULL,
  `issuer_tax_number` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_order`
--

CREATE TABLE `plans_order` (
  `id` int(11) NOT NULL,
  `flat_name` varchar(200) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created` datetime(6) NOT NULL,
  `completed` datetime(6) DEFAULT NULL,
  `amount` decimal(7,2) NOT NULL,
  `tax` decimal(4,2) DEFAULT NULL,
  `currency` varchar(3) COLLATE utf8_unicode_ci NOT NULL,
  `status` int(11) NOT NULL,
  `plan_id` int(11) NOT NULL,
  `pricing_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_plan`
--

CREATE TABLE `plans_plan` (
  `id` int(11) NOT NULL,
  `order` int(10) UNSIGNED NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `default` tinyint(1) NOT NULL,
  `available` tinyint(1) NOT NULL,
  `visible` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `url` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `customized_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_planpricing`
--

CREATE TABLE `plans_planpricing` (
  `id` int(11) NOT NULL,
  `price` decimal(7,2) NOT NULL,
  `plan_id` int(11) NOT NULL,
  `pricing_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_planquota`
--

CREATE TABLE `plans_planquota` (
  `id` int(11) NOT NULL,
  `value` int(11) DEFAULT NULL,
  `plan_id` int(11) NOT NULL,
  `quota_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_pricing`
--

CREATE TABLE `plans_pricing` (
  `id` int(11) NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `period` int(10) UNSIGNED DEFAULT NULL,
  `url` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_quota`
--

CREATE TABLE `plans_quota` (
  `id` int(11) NOT NULL,
  `order` int(10) UNSIGNED NOT NULL,
  `codename` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `name` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `unit` varchar(100) COLLATE utf8_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8_unicode_ci NOT NULL,
  `is_boolean` tinyint(1) NOT NULL,
  `url` varchar(200) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `plans_userplan`
--

CREATE TABLE `plans_userplan` (
  `id` int(11) NOT NULL,
  `expire` date DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `plan_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

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
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_act_industry_id_7665184d_fk_partner_industry_id` (`industry_id`),
  ADD KEY `partner_act_regulation_id_187ea64e_fk_partner_regulation_id` (`regulation_id`);

--
-- Indexes for table `partner_activity`
--
ALTER TABLE `partner_activity`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_activity_act_id_bbed62e5_fk_partner_act_id` (`act_id`);

--
-- Indexes for table `partner_assignedactivities`
--
ALTER TABLE `partner_assignedactivities`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_g_task_user_id_7c39c70a_fk_auditapp_user_id` (`user_id`);

--
-- Indexes for table `partner_auditplan`
--
ALTER TABLE `partner_auditplan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_auditplan_entity`
--
ALTER TABLE `partner_auditplan_entity`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_auditplan_entity_auditplan_id_entity_id_255fc27f_uniq` (`auditplan_id`,`entity_id`),
  ADD KEY `partner_auditplan_entity_entity_id_1112a3ae_fk_partner_entity_id` (`entity_id`);

--
-- Indexes for table `partner_client`
--
ALTER TABLE `partner_client`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_client_industry_id_9d8d9e91_fk_partner_industry_id` (`industry_id`),
  ADD KEY `partner_client_company_id_fd950132_fk_partner_company_id` (`company_id`),
  ADD KEY `partner_client_assigned_users_id_d8c09e34_fk_auditapp_user_id` (`assigned_users_id`);

--
-- Indexes for table `partner_client_entities`
--
ALTER TABLE `partner_client_entities`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_client_entities_client_id_entity_id_891d6685_uniq` (`client_id`,`entity_id`),
  ADD KEY `partner_client_entities_entity_id_db3abc8f_fk_partner_entity_id` (`entity_id`);

--
-- Indexes for table `partner_company`
--
ALTER TABLE `partner_company`
  ADD PRIMARY KEY (`id`);

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
-- Indexes for table `partner_regulation`
--
ALTER TABLE `partner_regulation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_task`
--
ALTER TABLE `partner_task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `partner_task_client_id_b95dd0bb_fk_partner_client_id` (`client_id`),
  ADD KEY `partner_task_user_id_98c6be2a_fk_auditapp_user_id` (`user_id`);

--
-- Indexes for table `plans_billinginfo`
--
ALTER TABLE `plans_billinginfo`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `plans_billinginfo_tax_number_afb5dea3` (`tax_number`),
  ADD KEY `plans_billinginfo_name_e69c18c3` (`name`);

--
-- Indexes for table `plans_invoice`
--
ALTER TABLE `plans_invoice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plans_invoice_number_029c6241` (`number`),
  ADD KEY `plans_invoice_type_d48ee091` (`type`),
  ADD KEY `plans_invoice_issued_74955383` (`issued`),
  ADD KEY `plans_invoice_issued_duplicate_3993f4e4` (`issued_duplicate`),
  ADD KEY `plans_invoice_selling_date_a8bf61a5` (`selling_date`),
  ADD KEY `plans_invoice_payment_date_165bea35` (`payment_date`),
  ADD KEY `plans_invoice_tax_bbc119a4` (`tax`),
  ADD KEY `plans_invoice_require_shipment_6591adce` (`require_shipment`),
  ADD KEY `plans_invoice_order_id_85fdb39d_fk_plans_order_id` (`order_id`),
  ADD KEY `plans_invoice_user_id_2acf7921_fk_auditapp_user_id` (`user_id`);

--
-- Indexes for table `plans_order`
--
ALTER TABLE `plans_order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plans_order_created_643392c9` (`created`),
  ADD KEY `plans_order_completed_6c33dd84` (`completed`),
  ADD KEY `plans_order_amount_b26e68f2` (`amount`),
  ADD KEY `plans_order_tax_1ee29bf0` (`tax`),
  ADD KEY `plans_order_plan_id_a7d62a45_fk_plans_plan_id` (`plan_id`),
  ADD KEY `plans_order_pricing_id_0dbc53e8_fk_plans_pricing_id` (`pricing_id`),
  ADD KEY `plans_order_user_id_d59f4b51_fk_auditapp_user_id` (`user_id`);

--
-- Indexes for table `plans_plan`
--
ALTER TABLE `plans_plan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plans_plan_customized_id_a5e0e78b_fk_auditapp_user_id` (`customized_id`),
  ADD KEY `plans_plan_order_579f69c5` (`order`),
  ADD KEY `plans_plan_default_38b10231` (`default`),
  ADD KEY `plans_plan_available_a258855c` (`available`),
  ADD KEY `plans_plan_visible_f04f078b` (`visible`),
  ADD KEY `plans_plan_created_07bdbc3f` (`created`);

--
-- Indexes for table `plans_planpricing`
--
ALTER TABLE `plans_planpricing`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plans_planpricing_plan_id_4072d329_fk_plans_plan_id` (`plan_id`),
  ADD KEY `plans_planpricing_price_3d4f8940` (`price`),
  ADD KEY `plans_planpricing_pricing_id_2c2b0761_fk_plans_pricing_id` (`pricing_id`);

--
-- Indexes for table `plans_planquota`
--
ALTER TABLE `plans_planquota`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plans_planquota_plan_id_9d7fe141_fk_plans_plan_id` (`plan_id`),
  ADD KEY `plans_planquota_quota_id_72a65bec_fk_plans_quota_id` (`quota_id`);

--
-- Indexes for table `plans_pricing`
--
ALTER TABLE `plans_pricing`
  ADD PRIMARY KEY (`id`),
  ADD KEY `plans_pricing_period_db4f2428` (`period`);

--
-- Indexes for table `plans_quota`
--
ALTER TABLE `plans_quota`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codename` (`codename`),
  ADD KEY `plans_quota_order_dee24da3` (`order`);

--
-- Indexes for table `plans_userplan`
--
ALTER TABLE `plans_userplan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`),
  ADD KEY `plans_userplan_plan_id_0d1d0b4b_fk_plans_plan_id` (`plan_id`),
  ADD KEY `plans_userplan_expire_f939a8c9` (`expire`),
  ADD KEY `plans_userplan_active_d4023ffa` (`active`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `auditapp_user`
--
ALTER TABLE `auditapp_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT for table `business_area`
--
ALTER TABLE `business_area`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `business_b_activity`
--
ALTER TABLE `business_b_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `finance_f_activity`
--
ALTER TABLE `finance_f_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `finance_f_area`
--
ALTER TABLE `finance_f_area`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `partner_act`
--
ALTER TABLE `partner_act`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `partner_activity`
--
ALTER TABLE `partner_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `partner_assignedactivities`
--
ALTER TABLE `partner_assignedactivities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `partner_auditplan`
--
ALTER TABLE `partner_auditplan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `partner_auditplan_entity`
--
ALTER TABLE `partner_auditplan_entity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `partner_client`
--
ALTER TABLE `partner_client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `partner_client_entities`
--
ALTER TABLE `partner_client_entities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `partner_company`
--
ALTER TABLE `partner_company`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `partner_entity`
--
ALTER TABLE `partner_entity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `partner_industry`
--
ALTER TABLE `partner_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `partner_regulation`
--
ALTER TABLE `partner_regulation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `partner_task`
--
ALTER TABLE `partner_task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `plans_billinginfo`
--
ALTER TABLE `plans_billinginfo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_invoice`
--
ALTER TABLE `plans_invoice`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_order`
--
ALTER TABLE `plans_order`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_plan`
--
ALTER TABLE `plans_plan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_planpricing`
--
ALTER TABLE `plans_planpricing`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_planquota`
--
ALTER TABLE `plans_planquota`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_pricing`
--
ALTER TABLE `plans_pricing`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_quota`
--
ALTER TABLE `plans_quota`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `plans_userplan`
--
ALTER TABLE `plans_userplan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

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
-- Constraints for table `partner_act`
--
ALTER TABLE `partner_act`
  ADD CONSTRAINT `partner_act_industry_id_7665184d_fk_partner_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`),
  ADD CONSTRAINT `partner_act_regulation_id_187ea64e_fk_partner_regulation_id` FOREIGN KEY (`regulation_id`) REFERENCES `partner_regulation` (`id`);

--
-- Constraints for table `partner_activity`
--
ALTER TABLE `partner_activity`
  ADD CONSTRAINT `partner_activity_act_id_bbed62e5_fk_partner_act_id` FOREIGN KEY (`act_id`) REFERENCES `partner_act` (`id`);

--
-- Constraints for table `partner_assignedactivities`
--
ALTER TABLE `partner_assignedactivities`
  ADD CONSTRAINT `partner_g_task_user_id_7c39c70a_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `partner_auditplan_entity`
--
ALTER TABLE `partner_auditplan_entity`
  ADD CONSTRAINT `partner_auditplan_en_auditplan_id_7e17e58b_fk_partner_a` FOREIGN KEY (`auditplan_id`) REFERENCES `partner_auditplan` (`id`),
  ADD CONSTRAINT `partner_auditplan_entity_entity_id_1112a3ae_fk_partner_entity_id` FOREIGN KEY (`entity_id`) REFERENCES `partner_entity` (`id`);

--
-- Constraints for table `partner_client`
--
ALTER TABLE `partner_client`
  ADD CONSTRAINT `partner_client_assigned_users_id_d8c09e34_fk_auditapp_user_id` FOREIGN KEY (`assigned_users_id`) REFERENCES `auditapp_user` (`id`),
  ADD CONSTRAINT `partner_client_company_id_fd950132_fk_partner_company_id` FOREIGN KEY (`company_id`) REFERENCES `partner_company` (`id`),
  ADD CONSTRAINT `partner_client_industry_id_9d8d9e91_fk_partner_industry_id` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`);

--
-- Constraints for table `partner_client_entities`
--
ALTER TABLE `partner_client_entities`
  ADD CONSTRAINT `partner_client_entities_client_id_f455a129_fk_partner_client_id` FOREIGN KEY (`client_id`) REFERENCES `partner_client` (`id`),
  ADD CONSTRAINT `partner_client_entities_entity_id_db3abc8f_fk_partner_entity_id` FOREIGN KEY (`entity_id`) REFERENCES `partner_entity` (`id`);

--
-- Constraints for table `partner_task`
--
ALTER TABLE `partner_task`
  ADD CONSTRAINT `partner_task_client_id_b95dd0bb_fk_partner_client_id` FOREIGN KEY (`client_id`) REFERENCES `partner_client` (`id`),
  ADD CONSTRAINT `partner_task_user_id_98c6be2a_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `plans_billinginfo`
--
ALTER TABLE `plans_billinginfo`
  ADD CONSTRAINT `plans_billinginfo_user_id_4e590872_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `plans_invoice`
--
ALTER TABLE `plans_invoice`
  ADD CONSTRAINT `plans_invoice_order_id_85fdb39d_fk_plans_order_id` FOREIGN KEY (`order_id`) REFERENCES `plans_order` (`id`),
  ADD CONSTRAINT `plans_invoice_user_id_2acf7921_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `plans_order`
--
ALTER TABLE `plans_order`
  ADD CONSTRAINT `plans_order_plan_id_a7d62a45_fk_plans_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plans_plan` (`id`),
  ADD CONSTRAINT `plans_order_pricing_id_0dbc53e8_fk_plans_pricing_id` FOREIGN KEY (`pricing_id`) REFERENCES `plans_pricing` (`id`),
  ADD CONSTRAINT `plans_order_user_id_d59f4b51_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `plans_plan`
--
ALTER TABLE `plans_plan`
  ADD CONSTRAINT `plans_plan_customized_id_a5e0e78b_fk_auditapp_user_id` FOREIGN KEY (`customized_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `plans_planpricing`
--
ALTER TABLE `plans_planpricing`
  ADD CONSTRAINT `plans_planpricing_plan_id_4072d329_fk_plans_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plans_plan` (`id`),
  ADD CONSTRAINT `plans_planpricing_pricing_id_2c2b0761_fk_plans_pricing_id` FOREIGN KEY (`pricing_id`) REFERENCES `plans_pricing` (`id`);

--
-- Constraints for table `plans_planquota`
--
ALTER TABLE `plans_planquota`
  ADD CONSTRAINT `plans_planquota_plan_id_9d7fe141_fk_plans_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plans_plan` (`id`),
  ADD CONSTRAINT `plans_planquota_quota_id_72a65bec_fk_plans_quota_id` FOREIGN KEY (`quota_id`) REFERENCES `plans_quota` (`id`);

--
-- Constraints for table `plans_userplan`
--
ALTER TABLE `plans_userplan`
  ADD CONSTRAINT `plans_userplan_plan_id_0d1d0b4b_fk_plans_plan_id` FOREIGN KEY (`plan_id`) REFERENCES `plans_plan` (`id`),
  ADD CONSTRAINT `plans_userplan_user_id_80dd1e54_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
