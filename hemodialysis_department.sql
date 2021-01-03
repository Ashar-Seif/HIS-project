-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jan 03, 2021 at 01:10 PM
-- Server version: 8.0.18
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hemodialysis_department`
--

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `Fname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Mname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Lname` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `phone` int(11) NOT NULL,
  `Mail` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `BD` int(11) NOT NULL,
  `D.ID` int(14) NOT NULL,
  `Salary` int(11) NOT NULL,
  `gendre` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `Qualifications` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Syndicate_number` int(11) NOT NULL,
  `address` text COLLATE utf8mb4_general_ci NOT NULL,
  `Job_rank` varchar(255) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`Fname`, `Mname`, `Lname`, `phone`, `Mail`, `BD`, `D.ID`, `Salary`, `gendre`, `Qualifications`, `Syndicate_number`, `address`, `Job_rank`) VALUES
('Hussein', 'Khaiery', 'Ahmed', 1220985436, 'Husseinkgaiery@gmail.com', 1219973, 1234567889, 3000, 'male', 'PHD', 2345, 'Cairo university', 'Captian ');

-- --------------------------------------------------------

--
-- Table structure for table `nurses`
--

CREATE TABLE `nurses` (
  `Fname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Mname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Lname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `Mail` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `BD` int(11) DEFAULT NULL,
  `gender` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `IDN` int(14) DEFAULT NULL,
  `salary` int(255) DEFAULT NULL,
  `Years of Working` int(11) DEFAULT NULL,
  `address` text COLLATE utf8mb4_general_ci,
  `NSnum` int(150) DEFAULT NULL,
  `depnum` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nurses`
--

INSERT INTO `nurses` (`Fname`, `Mname`, `Lname`, `phone`, `Mail`, `BD`, `gender`, `IDN`, `salary`, `Years of Working`, `address`, `NSnum`, `depnum`) VALUES
('Soha', 'Mohamed ', 'Mahrous', 1220985436, 'Soha123@gmail.com ', 341997, 'female ', 29703045, 2000, 6, 'Kasr-Elainy ', 45678, 3);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `Fname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Mname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `Lname` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone` int(11) NOT NULL,
  `Mail` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `BD` int(11) NOT NULL,
  `Dry weight` int(11) NOT NULL,
  `Described drugs` text COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`Fname`, `Mname`, `Lname`, `phone`, `Mail`, `BD`, `Dry weight`, `Described drugs`) VALUES
('Ahmed', 'Mohamed', 'Youssif', 119845783, NULL, 341965, 80, 'Panadol \r\n');

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `Date` text COLLATE utf8mb4_general_ci,
  `Used device` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `Price` int(250) NOT NULL,
  `Who record` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `After weight` int(255) NOT NULL,
  `Numofhours` int(11) NOT NULL,
  `Taken drugs` text COLLATE utf8mb4_general_ci NOT NULL,
  `Complications` text COLLATE utf8mb4_general_ci NOT NULL,
  `Dealingwithcomplications` text COLLATE utf8mb4_general_ci NOT NULL,
  `BD(1,2,3,4)` text COLLATE utf8mb4_general_ci NOT NULL,
  `Pulse(1,2,3,4)` text COLLATE utf8mb4_general_ci NOT NULL,
  `Temp(1,2,3,4)` text COLLATE utf8mb4_general_ci NOT NULL,
  `Rrate(1,2,3,4)` text COLLATE utf8mb4_general_ci NOT NULL,
  `Comments` text COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `doctor`
--
ALTER TABLE `doctor`
  ADD UNIQUE KEY `Syndicate_number` (`Syndicate_number`);

--
-- Indexes for table `nurses`
--
ALTER TABLE `nurses`
  ADD UNIQUE KEY `NSnum` (`NSnum`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
