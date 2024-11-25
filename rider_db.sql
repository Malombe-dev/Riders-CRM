-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 24, 2024 at 09:08 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rider_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `contact_form`
--

CREATE TABLE `contact_form` (
  `id` int(11) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact_form`
--

INSERT INTO `contact_form` (`id`, `user_name`, `email`, `phone`, `subject`, `message`, `created_at`) VALUES
(1, 'test@gmail.com', 'vincentmutinda560@gmail.com', '+254793830795', 'dcdcv', 'sysfcuyasgcjas', '2024-11-09 10:11:13'),
(2, 'test@gmail.com', 'vincentmutinda560@gmail.com', '+25479830795', 'dcdcv', 'guyu', '2024-11-09 10:52:35'),
(3, 'test@gmail.com', 'vincentmutinda560@gmail.com', '+25479830795', 'dcdcv', 'guyu', '2024-11-09 10:54:36'),
(4, 'test@gmail.com', 'vincentmutinda560@gmail.com', '+254793830795', 'dcdcv', 'kaclalvcadc', '2024-11-09 10:54:59'),
(5, 'test@gmail.com', 'vincentmutinda560@gmail.com', '+254793830795', 'dcdcv', 'bjgiug', '2024-11-09 11:01:35'),
(6, 'test@gmail.com', 'vincentmutinda560@gmail.com', '+25479830795', 'dcdcv', ';ochjaosdihcv', '2024-11-09 11:06:01'),
(7, 'tes@gmail.com', 'vincentmutida560@gmail.com', '+254793830795', 'dcdcv', 'xzxc z', '2024-11-12 09:47:31'),
(8, 'vmalombe', 'vincentutinda560@gmail.com', '+254793830795', 'dcdcv', 'ascasc', '2024-11-13 08:28:36');

-- --------------------------------------------------------

--
-- Table structure for table `deals`
--

CREATE TABLE `deals` (
  `deal_id` int(11) NOT NULL,
  `rider_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `deals`
--

INSERT INTO `deals` (`deal_id`, `rider_id`, `product_id`, `created_at`) VALUES
(6, 7, 3, '2024-10-26 15:25:08'),
(7, 1, 1, '2024-10-27 17:33:22'),
(8, 4, 11, '2024-10-31 09:54:50'),
(9, 8, 3, '2024-11-04 09:47:45'),
(10, 4, 14, '2024-11-05 08:10:12'),
(11, 15, 3, '2024-11-06 09:18:47'),
(12, 5, 4, '2024-11-06 12:19:57'),
(13, 4, 15, '2024-11-08 09:19:57'),
(14, 25, 3, '2024-11-15 09:58:19'),
(15, 1, 4, '2024-11-22 06:47:24');

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `product_description` text NOT NULL,
  `product_image` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`product_id`, `product_name`, `product_description`, `product_image`, `created_at`) VALUES
(1, 'Grilled Chicken Salad ', 'qwertyuiop[poiuh', 'QVZmM0lUUUg4Q045RVpVRQ.jpeg', '2024-10-23 16:00:54'),
(2, 'Grilled Chicken Salad ', 'qwertyu', 'QVZmM0lUUUg4Q045RVpVRQ.jpeg', '2024-10-24 06:15:51'),
(3, 'spark sport bike ', 'blue , 400w motor', 'QVZmNV91bGpOTGRxdElFNw.jpeg', '2024-10-25 05:27:42'),
(4, 'Chicken Caesar Wrap', 'asdasdfhjkgfhf', 'QVZmNV91bGpOTGRxdElFNw.jpeg', '2024-10-25 09:15:15'),
(5, 'Grilled Chicken Salad ', 'ddegvdfg', 'QVZmNV91bGpOTGRxdElFNw.jpeg', '2024-10-25 09:22:38'),
(6, 'Grilled Chicken Salad ', 'qwreytjy', 'QVZmM0lUUUg4Q045RVpVRQ.jpeg', '2024-10-25 09:25:27'),
(7, 'Grilled Chicken Salad ', 'zvxcvxcvbxcvvxcvxcvxc', 'h1.jpg', '2024-10-31 08:47:48'),
(8, 'Grilled Chicken Salad ', 'earddhytfuyuy', 'h3.jpg', '2024-10-31 08:48:07'),
(9, 'Grilled Chicken Salad ', 'hyfytdytdtydytd', 'h4.jpg', '2024-10-31 08:48:18'),
(10, 'Grilled Chicken Salad ', 'dydhiulgkyu', 'h6.jpg', '2024-10-31 08:48:33'),
(11, 'Grilled Chicken Salad ', 'hyytcjhyfi t', 'h5.jpg', '2024-10-31 08:49:00'),
(12, 'Grilled Chicken Salad ', 'hyytcjhyfi t', 'h5.jpg', '2024-10-31 08:49:00'),
(13, 'Grilled Chicken Salad ', 'fythdytuyguy', 'h6.jpg', '2024-10-31 08:49:17'),
(14, 'Grilled Chicken Salad ', 'hgchytfytfytf', 'h5.jpg', '2024-10-31 08:49:28'),
(15, 'Grilled Chicken Salad ', 'werfwef', 'h2.jpg', '2024-10-31 09:37:19'),
(16, 'Grilled Chicken Salad ', 'chgchghy', '136464644_237184877807880_177296533134027139_n.jpg', '2024-11-11 10:01:33'),
(17, 'Grilled Chicken Salad ', 'LCNSA', 'f1.jpg', '2024-11-14 19:22:59'),
(18, ',cbj skj,nsdcja', 'ac, abkjcka', 'f5.jpg', '2024-11-14 19:42:04'),
(19, 'Grilled Chicken Salad ', '.navlkkn', 'f5.jpg', '2024-11-14 19:46:03'),
(20, 'Grilled Chicken Salad ', '.navlkkn', 'f5.jpg', '2024-11-14 19:48:50'),
(21, 'mjbvjkadbv', ',bckjabdcj', 'f2.jpg', '2024-11-14 19:50:18'),
(22, '.knavldvnalkklanbcv', 'knalvkna', 'f2.jpg', '2024-11-14 19:53:49'),
(23, 'Grilled Chicken Salad ', ',sbckbja', 'f2.jpg', '2024-11-14 19:56:55'),
(24, 'Grilled Chicken Salad ', ',sbckbja', 'f2.jpg', '2024-11-14 20:00:27'),
(25, 'Grilled Chicken Salad ', ',kbnaclka', 'f2.jpg', '2024-11-14 20:06:54'),
(26, 'Grilled Chicken Salad ', ',kbnaclka', 'f2.jpg', '2024-11-14 20:11:37'),
(27, 'Grilled Chicken Salad ', 'mbkjvbj', 'f3.jpg', '2024-11-14 20:12:19'),
(28, 'Grilled Chicken Salad ', 'mbkjvbj', 'f3.jpg', '2024-11-14 20:14:58'),
(29, 'Chicken Caesar Wrap', ',,n z,z z', 'f2.jpg', '2024-11-14 20:16:27'),
(30, 'Beef Burrito Bowl ', 'lkbvbm,ln', 'f6.jpg', '2024-11-14 20:18:22'),
(31, 'Beef Burrito Bowl ', ',lkn zlk nlz', 'f2.jpg', '2024-11-14 20:20:31');

-- --------------------------------------------------------

--
-- Table structure for table `riders`
--

CREATE TABLE `riders` (
  `rider_id` int(11) NOT NULL,
  `customername` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `work_location` varchar(100) DEFAULT NULL,
  `current_motorbike` varchar(100) DEFAULT NULL,
  `fuel_consumption_per_day` float DEFAULT NULL,
  `any_pending_loan` tinyint(1) DEFAULT NULL,
  `lead_classification` varchar(50) DEFAULT NULL,
  `any_comments` text DEFAULT NULL,
  `submitted_by` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `riders`
--

INSERT INTO `riders` (`rider_id`, `customername`, `phone_number`, `work_location`, `current_motorbike`, `fuel_consumption_per_day`, `any_pending_loan`, `lead_classification`, `any_comments`, `submitted_by`, `created_at`) VALUES
(1, 'malombe vincent', '12123342', 'voi', 'kmgf260a', 0.01, 1, 'warm', 'rttwtyywywgdhjski', 'malombe', '2024-10-23 11:45:12'),
(3, 'precy', '0712345', 'lavvie ', 'kmgf260a', 0.02, 1, 'hot', 'weilljdhjd', 'malombe', '2024-10-24 06:55:39'),
(4, 'rider 1', '0793830795', 'nairobi', 'hobda125', 0.03, 1, 'hot', 'qwqdedfdffff', 'officer 1', '2024-10-25 05:24:56'),
(5, 'rider 3', '0793830795', 'ruiru', 'kmgf260a', 0.02, 1, 'cold', 'dwdscsdcscsd', 'officer 3', '2024-10-25 05:26:24'),
(7, 'tush', '1233435', 'machakos', 'boxer150', 0.02, 1, 'warm', 'dewrtyuiklkjhg', 'tanui', '2024-10-26 07:41:36'),
(8, 'ysysy', '12123342', 'voi', 'kmgf260a', 0.03, 1, 'warm', 'fghjklm;', 'malombe', '2024-10-26 15:11:06'),
(15, 'skisa', '637889494', 'kawangware', 'boxer150', 2, 0, 'warm', 'sdhidshiydsvodsv;odsv\'dl;vb', 'malombe', '2024-11-04 12:26:28'),
(22, 'malombe vincent', '1233435', 'lavvie ', 'sczcz', 4, 1, 'cold', 'fbfdvbdf', 'malombe', '2024-11-15 09:26:33'),
(23, 'b dbd', '12123342', 'fdb', 'kmgf260a', 0.01, 0, 'cold', 'fdbbdf', 'qwer', '2024-11-15 09:26:57'),
(24, 'fdbd', '1233435', 'kawangware', 'zss', 0.02, 1, 'warm', 'z  zx', 'sdfg', '2024-11-15 09:27:26'),
(25, 'x xc x', '12123342', 'sc', 'boxer150', 0.02, 1, 'cold', 'dvsvsd', 'sdfg', '2024-11-15 09:27:47'),
(26, 'malombe vincent', '12123342', 'machakos', 'kmgf260a', 0.02, 0, 'hot', 'ffbdfn', 'tanui', '2024-11-15 09:57:24'),
(27, ',ab ckj b', '1233435', 'machakos', 'Boxer 150', 0.02, 0, 'warm', ',xm ,', 'sdfg', '2024-11-16 19:39:06'),
(28, 'malombe vincent', ',lkanb cklj', 'voi', ' caa', 4, 1, 'hot', ',lkb naklsb', 'tanui', '2024-11-17 13:14:51'),
(29, 'ysysy', '12123342', 'kawangware', 'qdfg', 4, 1, 'cold', 'gxgfxgfx', 'tanui', '2024-11-18 20:00:43'),
(30, 'ysysy', '12123342', 'voi', 'boxer150', 5, 1, 'warm', 'vjhvjh', 'sdfg', '2024-11-18 20:01:26'),
(31, 'malombe vincent', '0793830795', 'kawangware', '23', 3, 1, 'hot', 'dgdg', 'malombe', '2024-11-21 07:04:47'),
(32, 'ysysy', '12123342', 'voi', 'boxer150', 4, 1, 'cold', 'jhhvhhghghg', 'officer 4', '2024-11-22 06:48:15');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'malombe', 'vincentmutinda560@gmail.com', 'scrypt:32768:8:1$Otbh1bwSMEoZLZD9$a0cb51f6b92151f18cf1e66552314aa30a4632f97026c6fa778e734fb06f2d5bc28ea65574af0752c3a1b7d38b10005c0e4d6a42772782abf3ae3074ac75a743', 'user', '2024-11-12 09:59:51'),
(2, 'vinny', 'test2@gmail.com', 'scrypt:32768:8:1$WBWLWTQk2pMIuclV$29e160cff886411dc3df172a5606eed97e64f2ec401b4f1b8d2d145ca5a33d6655b8cd01e234ad8d4eb6b7b6ab7a8f01f9a8d66ee9486e76895da8888b100e3b', 'admin', '2024-11-13 09:49:16'),
(3, 'user', 'test3@gmail.com', 'scrypt:32768:8:1$Z52xBF4qyQ6bFuBD$e6476cd711fac419021ff9e94990b1cd022da7d866a75d3fcc56e082180bf111f52c003361c608785dc9ed21e8b897adea33c21d60cfef00f435f3cd97d17ff0', 'user', '2024-11-13 14:28:12');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contact_form`
--
ALTER TABLE `contact_form`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `deals`
--
ALTER TABLE `deals`
  ADD PRIMARY KEY (`deal_id`),
  ADD KEY `rider_id` (`rider_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `riders`
--
ALTER TABLE `riders`
  ADD PRIMARY KEY (`rider_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contact_form`
--
ALTER TABLE `contact_form`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `deals`
--
ALTER TABLE `deals`
  MODIFY `deal_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `riders`
--
ALTER TABLE `riders`
  MODIFY `rider_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `deals`
--
ALTER TABLE `deals`
  ADD CONSTRAINT `deals_ibfk_1` FOREIGN KEY (`rider_id`) REFERENCES `riders` (`rider_id`),
  ADD CONSTRAINT `deals_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;