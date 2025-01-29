-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Jan 26, 2025 at 03:29 PM
-- Server version: 10.1.13-MariaDB
-- PHP Version: 7.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `car_dealership`
--

-- --------------------------------------------------------

--
-- Table structure for table `blog_posts`
--

CREATE TABLE `blog_posts` (
  `id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `blog_posts`
--

INSERT INTO `blog_posts` (`id`, `title`, `content`, `created_at`) VALUES
(1, 'How to Choose the Right Car for You', 'Choosing a car can be overwhelming, but here are some tips to help you decide...', '2025-01-20 17:14:50'),
(2, 'Top 5 Electric Cars of 2025', 'Electric cars are becoming more popular, and here are the top 5 to consider...', '2025-01-20 17:14:50'),
(3, 'Why You Should Consider Buying a Used Car', 'Buying a used car can save you a lot of money, and here are some tips to find the best deals...', '2025-01-20 17:14:50'),
(4, 'The Future of Autonomous Vehicles', 'Self-driving cars are on the rise, and here''s what you need to know about them...', '2025-01-20 17:14:50');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `id` int(11) NOT NULL,
  `customer_name` varchar(100) DEFAULT NULL,
  `customer_email` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `car_id` int(11) DEFAULT NULL,
  `booking_date` date DEFAULT NULL,
  `booking_time` time DEFAULT NULL,
  `status` enum('pending','confirmed','cancelled') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`id`, `customer_name`, `customer_email`, `phone_number`, `car_id`, `booking_date`, `booking_time`, `status`, `created_at`) VALUES
(1, 'Ahmed Ali', 'ahmed@example.com', '1234567890', 1, '2025-01-25', '10:00:00', 'confirmed', '2025-01-20 17:14:31'),
(2, 'Sara Hassan', 'sara@example.com', '0987654321', 3, '2025-01-26', '14:30:00', 'confirmed', '2025-01-20 17:14:31'),
(4, 'Mona Farouk', 'mona@example.com', '6677889900', 2, '2025-01-28', '11:00:00', 'confirmed', '2025-01-20 17:14:31');

-- --------------------------------------------------------

--
-- Table structure for table `cars`
--

CREATE TABLE `cars` (
  `id` int(11) NOT NULL,
  `brand` varchar(100) DEFAULT NULL,
  `model` varchar(100) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `fuel_type` varchar(50) DEFAULT NULL,
  `engine_power` int(11) DEFAULT NULL,
  `fuel_efficiency` decimal(5,2) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `is_new` tinyint(1) DEFAULT NULL,
  `description` text,
  `category` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `cars`
--

INSERT INTO `cars` (`id`, `brand`, `model`, `year`, `price`, `fuel_type`, `engine_power`, `fuel_efficiency`, `image_url`, `is_new`, `description`, `category`) VALUES
(1, 't', 'Camry', 2024, '25000.00', 'Gasoline', 200, '12.50', 'car1.jpg', 1, 'A reliable sedan with great fuel efficiency.', 'Sedan'),
(2, 'Ford', 'Mustang', 2023, '45000.00', 'Gasoline', 350, '9.00', 'car2.jpg', 1, 'A powerful sports car for enthusiasts.', 'Sports'),
(3, 'Tesla', 'Model 3', 2023, '55000.00', 'Electric', 283, '15.00', 'car3.jpg', 1, 'An electric car with cutting-edge technology.', 'Electric'),
(7, 'heonday', 'yyyyy', 1999, '20000.00', 'Gasoline', 200, '12.00', 'photo_2_2024-01-02_01-52-14.jpg', NULL, 'kjsdkkjsdfkjshkjsd', 'Sedan');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `car_id` int(11) DEFAULT NULL,
  `user_name` varchar(100) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `review_text` text,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`id`, `car_id`, `user_name`, `rating`, `review_text`, `created_at`) VALUES
(1, 1, 'John Doe', 4, 'Great car with excellent fuel efficiency.', '2025-01-20 17:14:14'),
(2, 1, 'Jane Smith', 5, 'I love this car, it''s super reliable and comfortable!', '2025-01-20 17:14:14'),
(3, 2, 'Alex Johnson', 3, 'A bit too expensive for my liking, but good performance.', '2025-01-20 17:14:14'),
(4, 3, 'Emily Davis', 5, 'Tesla Model 3 is a game changer in electric cars.', '2025-01-20 17:14:14');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `created_at`) VALUES
(1, 'admin', 'admin@example.com', 'admin123', '2025-01-20 17:15:09'),
(2, 'john_doe', 'john@example.com', 'password123', '2025-01-20 17:15:09'),
(3, 'sara_smith', 'sara@example.com', 'securepassword', '2025-01-20 17:15:09'),
(4, 'alex_johnson', 'alex@example.com', 'alexpassword', '2025-01-20 17:15:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `blog_posts`
--
ALTER TABLE `blog_posts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `car_id` (`car_id`);

--
-- Indexes for table `cars`
--
ALTER TABLE `cars`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `car_id` (`car_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `blog_posts`
--
ALTER TABLE `blog_posts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `cars`
--
ALTER TABLE `cars`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`);

--
-- Constraints for table `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`car_id`) REFERENCES `cars` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
