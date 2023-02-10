-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 30, 2020 at 02:33 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `auditapp`
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `auditapp_user`
--

INSERT INTO `auditapp_user` (`id`, `password`, `last_login`, `username`, `email`, `first_name`, `last_name`, `is_admin`, `is_partner`, `is_manager`, `is_auditorclerk`, `is_articleholder`, `is_active`) VALUES
(1, 'pbkdf2_sha256$150000$a6t4RzTDIQNM$KzehPNSxEcXA/5XUrundmnkfoSuYf6cgG6Fs6ibgUQw=', '2020-04-30 10:10:14.389360', 'admin', '', NULL, NULL, 1, 0, 0, 0, 0, 1),
(2, 'pbkdf2_sha256$150000$mi4lnbgCrP7d$i8s8TPRJPRlitv/V4yvj+SPsn+o9Z2228xxPshUIrVE=', '2020-04-30 08:49:20.111359', 'partner1', NULL, NULL, NULL, 0, 1, 0, 0, 0, 1),
(3, 'pbkdf2_sha256$150000$ZAslMP0WVLTm$oVYm/Dxh6AD1ZYMUjzEgsNL7Yxg5GcR6PjozW6cquOk=', '2020-04-30 10:54:26.518356', 'manager1', NULL, NULL, NULL, 0, 0, 1, 0, 0, 1),
(4, 'pbkdf2_sha256$150000$jeEG85vtdrsf$UHWqdF2ZMSk+yAi90M/xv8oj3ml9Zr7kxU1QjucDj4U=', NULL, 'auditor1', NULL, NULL, NULL, 0, 0, 0, 1, 0, 1),
(5, 'pbkdf2_sha256$150000$NYkJiXc11HXc$zUasEutU+hdAfChqxfVH1PupcinSIJZ6HOPZFtkc0ow=', NULL, 'article1', 'article1@yopmail.com', NULL, NULL, 0, 0, 0, 0, 1, 1),
(6, 'pbkdf2_sha256$150000$FYxruFVdpANC$leGXuQgGFqN22rWOXpc1d2VmuR9DozURNzCdVbVfAVQ=', NULL, 'manager2', NULL, NULL, NULL, 0, 0, 1, 0, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(31, '2020-04-30 12:00:46.451839', '5', 'article1', 2, '[]', 6, 1);

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(22, 'partner', '0004_auto_20200430_1602', '2020-04-30 10:32:42.622357');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('5xyi14sxjn6ewg8hbkmmc577wul5rsy8', 'NjBhNTIzMmJhOTQ5NzJiNDUwMmI5YTNiNGYyNGViNzU0MjgxNmMxNTp7Il9hdXRoX3VzZXJfaWQiOiIzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5YWRjNTZkZDYyNWNkMzc3YmM3ODIyNjAwYTAxOWFhMTkyZGRkMDFlIn0=', '2020-05-14 10:54:26.542366'),
('96020mt65tgvtoj60bdl0jij6hprmjx2', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-14 10:10:14.458359'),
('h3u70kqgd1539vk885nxdmi7gdeisv4t', 'NGM2YWQ2ZWIzNmZmNjI4NjliODU5NTE5ZGMzODFkY2JkNWQ1YTBlMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI2OWE2NWM3YzA3NjRmYzU4YTdhZjZkZDI2MzNlYWViOGQ2MmM5ZWQwIn0=', '2020-05-13 14:51:32.159793');

-- --------------------------------------------------------

--
-- Table structure for table `partner_act`
--

CREATE TABLE `partner_act` (
  `id` int(11) NOT NULL,
  `act_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_act`
--

INSERT INTO `partner_act` (`id`, `act_name`) VALUES
(1, 'Income Tax Act 1961'),
(2, 'The Central Goods and Services Tax Act, 2017'),
(3, 'The Integrated Goods and Services Tax Act, 2017'),
(4, 'The Union Territory Goods and Services Tax Act, 2017'),
(5, 'The Pension Fund Regulatory and Development Authority Act, 2013'),
(6, 'The Insolvency and Bankruptcy Code, 2016'),
(7, 'The Companies Act, 2013'),
(8, 'The Limited Liability Partnership Act, 2008');

-- --------------------------------------------------------

--
-- Table structure for table `partner_activity`
--

CREATE TABLE `partner_activity` (
  `id` int(11) NOT NULL,
  `activity_name` varchar(255) NOT NULL,
  `activity_description` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_activity`
--

INSERT INTO `partner_activity` (`id`, `activity_name`, `activity_description`) VALUES
(1, 'Finance Activity', 'This is a test activity'),
(2, 'Company Activity', 'This is a test activity 2');

-- --------------------------------------------------------

--
-- Table structure for table `partner_activity_act`
--

CREATE TABLE `partner_activity_act` (
  `id` int(11) NOT NULL,
  `activity_id` int(11) NOT NULL,
  `act_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_activity_act`
--

INSERT INTO `partner_activity_act` (`id`, `activity_id`, `act_id`) VALUES
(1, 1, 1),
(2, 2, 7);

-- --------------------------------------------------------

--
-- Table structure for table `partner_act_entity`
--

CREATE TABLE `partner_act_entity` (
  `id` int(11) NOT NULL,
  `act_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_act_entity`
--

INSERT INTO `partner_act_entity` (`id`, `act_id`, `entity_id`) VALUES
(1, 1, 1),
(2, 7, 1),
(3, 7, 14);

-- --------------------------------------------------------

--
-- Table structure for table `partner_auditplan`
--

CREATE TABLE `partner_auditplan` (
  `id` int(11) NOT NULL,
  `parent_company` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `client_name` varchar(255) NOT NULL,
  `industry_name` varchar(255) NOT NULL,
  `statutory_audit` tinyint(1) NOT NULL,
  `taxation_audit` tinyint(1) NOT NULL,
  `internal_audit` tinyint(1) NOT NULL,
  `certification_audit` tinyint(1) NOT NULL,
  `investigation_assignment_audit` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `partner_auditplan_entity`
--

CREATE TABLE `partner_auditplan_entity` (
  `id` int(11) NOT NULL,
  `auditplan_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `partner_audittype`
--

CREATE TABLE `partner_audittype` (
  `id` int(11) NOT NULL,
  `audit_type_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_audittype`
--

INSERT INTO `partner_audittype` (`id`, `audit_type_name`) VALUES
(1, 'Statutory'),
(2, 'Internal');

-- --------------------------------------------------------

--
-- Table structure for table `partner_audittype_industry`
--

CREATE TABLE `partner_audittype_industry` (
  `id` int(11) NOT NULL,
  `audittype_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_audittype_industry`
--

INSERT INTO `partner_audittype_industry` (`id`, `audittype_id`, `industry_id`) VALUES
(2, 1, 23),
(1, 1, 37),
(3, 2, 5);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_client`
--

INSERT INTO `partner_client` (`id`, `client_name`, `pan_no`, `tan_no`, `gst_no`, `assigned_user_id`) VALUES
(1, 'Client 1', 'AFHER4324H', 'TAN2132423', 'GSTIN4326723', 3),
(2, 'Client 2', 'HGSD42342P', 'TAN4237846', 'GSTIN478632746', NULL),
(6, 'Nachiket', 'GDshgad', '32dojdsaij', 'dsahdis324', 3);

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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  `task_master_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_clienttask`
--

INSERT INTO `partner_clienttask` (`id`, `task_start_date`, `task_end_date`, `status`, `is_approved`, `attachment_file`, `remark`, `is_rejected`, `is_completed`, `is_start`, `is_reject`, `rejection_remark`, `client_id`, `task_master_id`, `user_id`) VALUES
(1, '2020-04-29', '2020-04-30', 0, 0, '', NULL, 0, 0, 0, 0, NULL, 1, 3, 5),
(148, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 1, NULL),
(149, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 2, NULL),
(150, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 3, NULL),
(151, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 4, NULL),
(152, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 5, NULL),
(153, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 6, NULL),
(154, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 7, NULL),
(155, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 8, NULL),
(156, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 9, NULL),
(157, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 10, NULL),
(158, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 11, NULL),
(159, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 12, NULL),
(160, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 13, NULL),
(161, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 14, NULL),
(162, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 15, NULL),
(163, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 16, NULL),
(164, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 17, NULL),
(165, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 18, NULL),
(166, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 19, NULL),
(167, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 20, NULL),
(168, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 21, NULL),
(169, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 22, NULL),
(170, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 23, NULL),
(171, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 24, NULL),
(172, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 25, NULL),
(173, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 26, NULL),
(174, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 27, NULL),
(175, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 28, NULL),
(176, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 29, NULL),
(177, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 30, NULL),
(178, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 31, NULL),
(179, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 32, NULL),
(180, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 33, NULL),
(181, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 34, NULL),
(182, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 35, NULL),
(183, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 36, NULL),
(184, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 37, NULL),
(185, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 38, NULL),
(186, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 39, NULL),
(187, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 40, NULL),
(188, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 41, NULL),
(189, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 42, NULL),
(190, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 43, NULL),
(191, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 44, NULL),
(192, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 45, NULL),
(193, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 46, NULL),
(194, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 47, NULL),
(195, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 48, NULL),
(196, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 49, NULL),
(197, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 50, NULL),
(198, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 52, 5),
(199, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 53, NULL),
(200, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 54, NULL),
(201, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 55, NULL),
(202, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 56, NULL),
(203, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 57, NULL),
(204, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 58, NULL),
(205, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 59, NULL),
(206, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 60, NULL),
(207, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 61, 5),
(208, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 62, 5),
(209, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 63, 5),
(210, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 64, 5),
(211, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 65, 5),
(212, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 66, 5),
(213, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 67, 5),
(214, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 68, 5),
(215, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 69, NULL),
(216, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 70, NULL),
(217, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 71, NULL),
(218, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 72, NULL),
(219, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 73, NULL),
(220, NULL, NULL, 0, 0, '', NULL, 0, 0, 0, 0, NULL, 6, 74, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `partner_client_audit_type`
--

CREATE TABLE `partner_client_audit_type` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `audittype_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_client_audit_type`
--

INSERT INTO `partner_client_audit_type` (`id`, `client_id`, `audittype_id`) VALUES
(1, 1, 1),
(2, 2, 2),
(7, 6, 1),
(8, 6, 2);

-- --------------------------------------------------------

--
-- Table structure for table `partner_client_entities`
--

CREATE TABLE `partner_client_entities` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_client_entities`
--

INSERT INTO `partner_client_entities` (`id`, `client_id`, `entity_id`) VALUES
(1, 1, 14),
(2, 2, 1),
(7, 6, 1),
(8, 6, 7);

-- --------------------------------------------------------

--
-- Table structure for table `partner_client_industry`
--

CREATE TABLE `partner_client_industry` (
  `id` int(11) NOT NULL,
  `client_id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_client_industry`
--

INSERT INTO `partner_client_industry` (`id`, `client_id`, `industry_id`) VALUES
(2, 1, 23),
(1, 1, 37),
(3, 2, 37),
(9, 6, 23),
(10, 6, 37);

-- --------------------------------------------------------

--
-- Table structure for table `partner_entity`
--

CREATE TABLE `partner_entity` (
  `id` int(11) NOT NULL,
  `entity_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
-- Table structure for table `partner_entity_audit_type`
--

CREATE TABLE `partner_entity_audit_type` (
  `id` int(11) NOT NULL,
  `entity_id` int(11) NOT NULL,
  `audittype_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_entity_audit_type`
--

INSERT INTO `partner_entity_audit_type` (`id`, `entity_id`, `audittype_id`) VALUES
(2, 1, 2),
(1, 14, 1);

-- --------------------------------------------------------

--
-- Table structure for table `partner_industry`
--

CREATE TABLE `partner_industry` (
  `id` int(11) NOT NULL,
  `industry_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_industry`
--

INSERT INTO `partner_industry` (`id`, `industry_name`) VALUES
(1, 'Marketing'),
(2, 'Automobiles'),
(3, 'Chemicals'),
(4, 'Banks-Public Sector'),
(5, 'Banks-Private Sector'),
(6, 'NBFC-Non FD accepting'),
(7, 'NBFC-FD accepting'),
(8, 'Housing Finance-FD Accepting'),
(9, 'Houing Finance-Non FD accepting'),
(10, 'FMCG-Food'),
(11, 'Consumer Durables'),
(12, 'Advertising'),
(13, 'Construction-Housing'),
(14, 'Construction-Commercial'),
(15, 'Pharma'),
(16, 'Healthcare-Hospitals'),
(17, 'Healthcare-Diagnostic Centers'),
(18, 'Metals'),
(19, 'Metals and Mining'),
(20, 'FERTILISERS & PESTICIDES'),
(21, 'TEXTILES'),
(22, 'CEMENT & CEMENT PRODUCTS'),
(23, 'TELECOM'),
(24, 'Forest Products'),
(25, 'Power'),
(26, 'Oil and Gas'),
(27, 'Trading'),
(28, 'Hotels/Resorts'),
(29, 'Engineering'),
(30, 'Manufacturing'),
(31, 'Manpower Services'),
(32, 'Movie Exhibition'),
(33, 'Movie Production'),
(34, 'Logistics-Transporters'),
(35, 'Logistics-Others'),
(36, 'IT/ITES'),
(37, 'Computer Hardware');

-- --------------------------------------------------------

--
-- Table structure for table `partner_industry_regulation`
--

CREATE TABLE `partner_industry_regulation` (
  `id` int(11) NOT NULL,
  `industry_id` int(11) NOT NULL,
  `regulation_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_industry_regulation`
--

INSERT INTO `partner_industry_regulation` (`id`, `industry_id`, `regulation_id`) VALUES
(8, 23, 8),
(9, 23, 39),
(4, 37, 8),
(5, 37, 12),
(7, 37, 29),
(1, 37, 32),
(2, 37, 33),
(3, 37, 39),
(6, 37, 45);

-- --------------------------------------------------------

--
-- Table structure for table `partner_regulation`
--

CREATE TABLE `partner_regulation` (
  `id` int(11) NOT NULL,
  `regulation_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  `task_international_auditing_standard` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_task`
--

INSERT INTO `partner_task` (`id`, `task_name`, `task_estimated_days`, `task_auditing_standard`, `task_international_auditing_standard`) VALUES
(1, 'Finance Task 1 old', '100', 'RBI', 'OSI'),
(2, 'Finance Task 2 old', '10', 'SEBI', 'IETE'),
(3, 'Finance Task 1', '15', 'RIP', 'WHO'),
(4, 'Finance Task 2', '2', 'OIS', 'WHO'),
(5, 'Finance Task 3', '10', 'OIS', 'WHO'),
(6, 'Finance Task 4', '17', 'ISO', 'IETE'),
(7, 'Finance Task 5', '16', 'RIP', 'UNESCO'),
(8, 'Finance Task 6', '6', 'ISO', 'IETE'),
(9, 'Finance Task 7', '8', 'OIS', 'WHO'),
(10, 'Finance Task 8', '17', 'RIP', 'UNESCO'),
(11, 'Finance Task 9', '18', 'RIP', 'WHO'),
(12, 'Finance Task 10', '1', 'OIS', 'UNESCO'),
(13, 'Finance Task 11', '21', 'ISO', 'WHO'),
(14, 'Finance Task 12', '29', 'RIP', 'IETE'),
(15, 'Finance Task 13', '28', 'ISO', 'UNESCO'),
(16, 'Finance Task 14', '19', 'OIS', 'UNESCO'),
(17, 'Finance Task 15', '3', 'RIP', 'WHO'),
(18, 'Finance Task 16', '25', 'OIS', 'UNESCO'),
(19, 'Finance Task 17', '7', 'ISO', 'WHO'),
(20, 'Finance Task 18', '28', 'OIS', 'UNESCO'),
(21, 'Finance Task 19', '15', 'ISO', 'UNESCO'),
(22, 'Finance Task 20', '5', 'RIP', 'UNESCO'),
(23, 'Finance Task 21', '22', 'RIP', 'WHO'),
(24, 'Finance Task 22', '1', 'RIP', 'WHO'),
(25, 'Finance Task 23', '30', 'ISO', 'IETE'),
(26, 'Finance Task 24', '3', 'RIP', 'UNESCO'),
(27, 'Finance Task 25', '19', 'RIP', 'IETE'),
(28, 'Finance Task 26', '19', 'ISO', 'UNESCO'),
(29, 'Finance Task 27', '26', 'RIP', 'IETE'),
(30, 'Finance Task 28', '17', 'OIS', 'UNESCO'),
(31, 'Finance Task 29', '11', 'ISO', 'UNESCO'),
(32, 'Finance Task 30', '20', 'ISO', 'WHO'),
(33, 'Finance Task 31', '18', 'ISO', 'IETE'),
(34, 'Finance Task 32', '13', 'ISO', 'IETE'),
(35, 'Finance Task 33', '6', 'RIP', 'IETE'),
(36, 'Finance Task 34', '16', 'RIP', 'IETE'),
(37, 'Finance Task 35', '7', 'OIS', 'WHO'),
(38, 'Finance Task 36', '17', 'RIP', 'UNESCO'),
(39, 'Finance Task 37', '22', 'RIP', 'IETE'),
(40, 'Finance Task 38', '14', 'OIS', 'UNESCO'),
(41, 'Finance Task 39', '26', 'OIS', 'WHO'),
(42, 'Finance Task 40', '3', 'RIP', 'IETE'),
(43, 'Finance Task 41', '3', 'ISO', 'IETE'),
(44, 'Finance Task 42', '3', 'ISO', 'UNESCO'),
(45, 'Finance Task 43', '1', 'RIP', 'UNESCO'),
(46, 'Finance Task 44', '4', 'OIS', 'UNESCO'),
(47, 'Finance Task 45', '16', 'ISO', 'UNESCO'),
(48, 'Finance Task 46', '21', 'OIS', 'WHO'),
(49, 'Finance Task 47', '1', 'RIP', 'IETE'),
(50, 'Finance Task 48', '22', 'RIP', 'UNESCO'),
(51, 'Finance Task 49', '8', 'RIP', 'WHO'),
(52, 'Company Task 1', '17', 'RIP', 'WHO'),
(53, 'Company Task 2', '10', 'OIS', 'IETE'),
(54, 'Company Task 3', '16', 'RIP', 'UNESCO'),
(55, 'Company Task 4', '1', 'ISO', 'UNESCO'),
(56, 'Company Task 5', '4', 'OIS', 'IETE'),
(57, 'Company Task 6', '24', 'RIP', 'WHO'),
(58, 'Company Task 7', '26', 'OIS', 'UNESCO'),
(59, 'Company Task 8', '28', 'OIS', 'IETE'),
(60, 'Company Task 9', '30', 'ISO', 'UNESCO'),
(61, 'Company Task 10', '23', 'OIS', 'UNESCO'),
(62, 'Company Task 11', '12', 'OIS', 'UNESCO'),
(63, 'Company Task 12', '15', 'OIS', 'WHO'),
(64, 'Company Task 13', '1', 'ISO', 'UNESCO'),
(65, 'Company Task 14', '3', 'RIP', 'IETE'),
(66, 'Company Task 15', '16', 'RIP', 'WHO'),
(67, 'Company Task 16', '2', 'OIS', 'IETE'),
(68, 'Company Task 17', '22', 'ISO', 'IETE'),
(69, 'Company Task 18', '27', 'ISO', 'UNESCO'),
(70, 'Company Task 19', '19', 'OIS', 'IETE'),
(71, 'Company Task 20', '9', 'RIP', 'IETE'),
(72, 'Company Task 21', '5', 'OIS', 'UNESCO'),
(73, 'Company Task 22', '22', 'OIS', 'UNESCO'),
(74, 'Company Task 23', '15', 'RIP', 'UNESCO'),
(75, 'Company Task 24', '27', 'ISO', 'WHO');

-- --------------------------------------------------------

--
-- Table structure for table `partner_task_activity`
--

CREATE TABLE `partner_task_activity` (
  `id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL,
  `activity_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `partner_task_activity`
--

INSERT INTO `partner_task_activity` (`id`, `task_id`, `activity_id`) VALUES
(1, 1, 1),
(2, 2, 1),
(3, 3, 1),
(4, 4, 1),
(5, 5, 1),
(6, 6, 1),
(7, 7, 1),
(8, 8, 1),
(9, 9, 1),
(10, 10, 1),
(11, 11, 1),
(12, 12, 1),
(13, 13, 1),
(14, 14, 1),
(15, 15, 1),
(16, 16, 1),
(17, 17, 1),
(18, 18, 1),
(19, 19, 1),
(20, 20, 1),
(21, 21, 1),
(22, 22, 1),
(23, 23, 1),
(24, 24, 1),
(25, 25, 1),
(26, 26, 1),
(27, 27, 1),
(28, 28, 1),
(29, 29, 1),
(30, 30, 1),
(31, 31, 1),
(32, 32, 1),
(33, 33, 1),
(34, 34, 1),
(35, 35, 1),
(36, 36, 1),
(37, 37, 1),
(38, 38, 1),
(39, 39, 1),
(40, 40, 1),
(41, 41, 1),
(42, 42, 1),
(43, 43, 1),
(44, 44, 1),
(45, 45, 1),
(46, 46, 1),
(47, 47, 1),
(48, 48, 1),
(49, 49, 1),
(50, 50, 1),
(51, 52, 2),
(52, 53, 2),
(53, 54, 2),
(54, 55, 2),
(55, 56, 2),
(56, 57, 2),
(57, 58, 2),
(58, 59, 2),
(59, 60, 2),
(60, 61, 2),
(61, 62, 2),
(62, 63, 2),
(63, 64, 2),
(64, 65, 2),
(65, 66, 2),
(66, 67, 2),
(67, 68, 2),
(68, 69, 2),
(69, 70, 2),
(70, 71, 2),
(71, 72, 2),
(72, 73, 2),
(73, 74, 2);

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
-- Indexes for table `partner_act`
--
ALTER TABLE `partner_act`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_activity`
--
ALTER TABLE `partner_activity`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_activity_act`
--
ALTER TABLE `partner_activity_act`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_activity_act_activity_id_act_id_40ac8772_uniq` (`activity_id`,`act_id`),
  ADD KEY `partner_activity_act_act_id_bd7cd5a2_fk_partner_act_id` (`act_id`);

--
-- Indexes for table `partner_act_entity`
--
ALTER TABLE `partner_act_entity`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_act_entity_act_id_entity_id_21e98eb7_uniq` (`act_id`,`entity_id`),
  ADD KEY `partner_act_entity_entity_id_2e5c4ba6_fk_partner_entity_id` (`entity_id`);

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
-- Indexes for table `partner_audittype`
--
ALTER TABLE `partner_audittype`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_audittype_industry`
--
ALTER TABLE `partner_audittype_industry`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_audittype_indust_audittype_id_industry_id_9c881f0b_uniq` (`audittype_id`,`industry_id`),
  ADD KEY `partner_audittype_in_industry_id_7f8d0182_fk_partner_i` (`industry_id`);

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
  ADD KEY `partner_clienttask_client_id_cfdaefeb_fk_partner_client_id` (`client_id`),
  ADD KEY `partner_clienttask_user_id_a1b44cc3_fk_auditapp_user_id` (`user_id`),
  ADD KEY `partner_clienttask_task_master_id_a25d2ae5_fk_partner_task_id` (`task_master_id`);

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
-- Indexes for table `partner_entity_audit_type`
--
ALTER TABLE `partner_entity_audit_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_entity_audit_type_entity_id_audittype_id_1d1111c1_uniq` (`entity_id`,`audittype_id`),
  ADD KEY `partner_entity_audit_audittype_id_b4558431_fk_partner_a` (`audittype_id`);

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
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `partner_task_activity`
--
ALTER TABLE `partner_task_activity`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `partner_task_activity_task_id_activity_id_8fbe67bb_uniq` (`task_id`,`activity_id`),
  ADD KEY `partner_task_activit_activity_id_a5fc864d_fk_partner_a` (`activity_id`);

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
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `partner_act`
--
ALTER TABLE `partner_act`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `partner_activity`
--
ALTER TABLE `partner_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `partner_activity_act`
--
ALTER TABLE `partner_activity_act`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `partner_act_entity`
--
ALTER TABLE `partner_act_entity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
-- AUTO_INCREMENT for table `partner_audittype`
--
ALTER TABLE `partner_audittype`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `partner_audittype_industry`
--
ALTER TABLE `partner_audittype_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `partner_client`
--
ALTER TABLE `partner_client`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `partner_clientactivities`
--
ALTER TABLE `partner_clientactivities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `partner_clienttask`
--
ALTER TABLE `partner_clienttask`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=221;

--
-- AUTO_INCREMENT for table `partner_client_audit_type`
--
ALTER TABLE `partner_client_audit_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `partner_client_entities`
--
ALTER TABLE `partner_client_entities`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `partner_client_industry`
--
ALTER TABLE `partner_client_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `partner_entity`
--
ALTER TABLE `partner_entity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `partner_entity_audit_type`
--
ALTER TABLE `partner_entity_audit_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `partner_industry`
--
ALTER TABLE `partner_industry`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `partner_industry_regulation`
--
ALTER TABLE `partner_industry_regulation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `partner_regulation`
--
ALTER TABLE `partner_regulation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=46;

--
-- AUTO_INCREMENT for table `partner_task`
--
ALTER TABLE `partner_task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=76;

--
-- AUTO_INCREMENT for table `partner_task_activity`
--
ALTER TABLE `partner_task_activity`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;

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
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auditapp_user_id` FOREIGN KEY (`user_id`) REFERENCES `auditapp_user` (`id`);

--
-- Constraints for table `partner_activity_act`
--
ALTER TABLE `partner_activity_act`
  ADD CONSTRAINT `partner_activity_act_act_id_bd7cd5a2_fk_partner_act_id` FOREIGN KEY (`act_id`) REFERENCES `partner_act` (`id`),
  ADD CONSTRAINT `partner_activity_act_activity_id_07a255dc_fk_partner_activity_id` FOREIGN KEY (`activity_id`) REFERENCES `partner_activity` (`id`);

--
-- Constraints for table `partner_act_entity`
--
ALTER TABLE `partner_act_entity`
  ADD CONSTRAINT `partner_act_entity_act_id_1363a8b6_fk_partner_act_id` FOREIGN KEY (`act_id`) REFERENCES `partner_act` (`id`),
  ADD CONSTRAINT `partner_act_entity_entity_id_2e5c4ba6_fk_partner_entity_id` FOREIGN KEY (`entity_id`) REFERENCES `partner_entity` (`id`);

--
-- Constraints for table `partner_auditplan_entity`
--
ALTER TABLE `partner_auditplan_entity`
  ADD CONSTRAINT `partner_auditplan_en_auditplan_id_7e17e58b_fk_partner_a` FOREIGN KEY (`auditplan_id`) REFERENCES `partner_auditplan` (`id`),
  ADD CONSTRAINT `partner_auditplan_entity_entity_id_1112a3ae_fk_partner_entity_id` FOREIGN KEY (`entity_id`) REFERENCES `partner_entity` (`id`);

--
-- Constraints for table `partner_audittype_industry`
--
ALTER TABLE `partner_audittype_industry`
  ADD CONSTRAINT `partner_audittype_in_audittype_id_4a6e0f59_fk_partner_a` FOREIGN KEY (`audittype_id`) REFERENCES `partner_audittype` (`id`),
  ADD CONSTRAINT `partner_audittype_in_industry_id_7f8d0182_fk_partner_i` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`);

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
  ADD CONSTRAINT `partner_clienttask_client_id_cfdaefeb_fk_partner_client_id` FOREIGN KEY (`client_id`) REFERENCES `partner_client` (`id`),
  ADD CONSTRAINT `partner_clienttask_task_master_id_a25d2ae5_fk_partner_task_id` FOREIGN KEY (`task_master_id`) REFERENCES `partner_task` (`id`),
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
-- Constraints for table `partner_entity_audit_type`
--
ALTER TABLE `partner_entity_audit_type`
  ADD CONSTRAINT `partner_entity_audit_audittype_id_b4558431_fk_partner_a` FOREIGN KEY (`audittype_id`) REFERENCES `partner_audittype` (`id`),
  ADD CONSTRAINT `partner_entity_audit_entity_id_b070966d_fk_partner_e` FOREIGN KEY (`entity_id`) REFERENCES `partner_entity` (`id`);

--
-- Constraints for table `partner_industry_regulation`
--
ALTER TABLE `partner_industry_regulation`
  ADD CONSTRAINT `partner_industry_reg_industry_id_e2d4fa50_fk_partner_i` FOREIGN KEY (`industry_id`) REFERENCES `partner_industry` (`id`),
  ADD CONSTRAINT `partner_industry_reg_regulation_id_ceba0ca7_fk_partner_r` FOREIGN KEY (`regulation_id`) REFERENCES `partner_regulation` (`id`);

--
-- Constraints for table `partner_task_activity`
--
ALTER TABLE `partner_task_activity`
  ADD CONSTRAINT `partner_task_activit_activity_id_a5fc864d_fk_partner_a` FOREIGN KEY (`activity_id`) REFERENCES `partner_activity` (`id`),
  ADD CONSTRAINT `partner_task_activity_task_id_94f0baff_fk_partner_task_id` FOREIGN KEY (`task_id`) REFERENCES `partner_task` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
