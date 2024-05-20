-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-05-2024 a las 07:53:50
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `flask_login`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calendar`
--

CREATE TABLE `calendar` (
  `id` int(11) NOT NULL,
  `task_id` int(11) DEFAULT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `task`
--

CREATE TABLE `task` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `task_info` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `password` text CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `fullname` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `email`, `password`, `fullname`) VALUES
(1, 'ddd333@gmail.com', 'pbkdf2:sha256:600000$W5XgTSUdJcXojUyy$ef721ccfc4d235a7389f2490a2f68a1409012a760ddaeccb5a81508c24c89fbc', 'Rodrigo Martinez'),
(5, 'nando@hotmail.com', 'pbkdf2:sha256:260000$wGsd5hjKbweX1ibn$43ae147366164a17f15156182f28ac53f7e0500dd9f6fcc00a635d5fc4d1af93', 'firula nando'),
(6, 'javid@hotmail.com', 'pbkdf2:sha256:260000$5YJO8WjO2z5weYQv$b2b71055f842a9e0f93cc0651091742d732780dc25a2a3fcb19fe6ba8b4e0b3f', 'javid diaz'),
(8, 'cristian@gmail.com', 'scrypt:32768:8:1$m1XXXPE02dNO8Jwb$2883954601f2a242b7d576045e71739804d343675185dd90fd04e6e24ddcf9efd2d3de8505cdddbc2597d36808004f3703be17119a8e1cb345da3ee356a6e1ee', 'cristian diaz'),
(9, 'andresescobarlopez2004@gmail.com', 'pbkdf2:sha256:600000$EEc9bZSlrkf4w6sK$a3899bdd0990cbc48b2c4fe1f17923ae57331db755af7b20d23c1eb165800ab8', 'Andres Felipe Escobar Lopez'),
(10, 'marinenyer19@gmail.com', 'pbkdf2:sha256:600000$GiAaO7WOtLcrL1Sm$2025a74e9256e9012de3113993edf49c102a59ef0dffd4b3eb05e40b4d588bca', 'Enyerbe Antuan'),
(11, 'akolacronic@gmail.com', 'pbkdf2:sha256:600000$RsXYerxI7UgbApUW$1ac1fdecd1cdf9fe1de34bee4a5d540079c339d1730eb878f64dd7e70da5124b', 'fsdfs fddsaf'),
(12, 'luis@hotmail.com', 'pbkdf2:sha256:600000$oPFbWnI9mbo1aPYG$dfe63b0f8b9c46fc2e1a93267e3ae3772d166033f2f9f2f451d1e1dc0b441e88', 'luis suarez');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `calendar`
--
ALTER TABLE `calendar`
  ADD PRIMARY KEY (`id`),
  ADD KEY `task_id` (`task_id`);

--
-- Indices de la tabla `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `calendar`
--
ALTER TABLE `calendar`
  ADD CONSTRAINT `calendar_ibfk_1` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`);

--
-- Filtros para la tabla `task`
--
ALTER TABLE `task`
  ADD CONSTRAINT `task_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
