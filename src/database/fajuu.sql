-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 31-08-2024 a las 23:51:11
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
-- Base de datos: `fajuu`
--

DELIMITER $$
--
-- Procedimientos
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `ActualizarEstadoUsuario` (IN `UsuarioID` INT(11), IN `NuevoEstado` VARCHAR(100))   BEGIN
    UPDATE Usuarios
    SET user_estado = NuevoEstado
    WHERE user_id = UsuarioID;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `Eliminar_Factura` (IN `FacturaID` INT(11))   BEGIN   

    IF EXISTS (SELECT 1 FROM Facturas WHERE fact_id = FacturaID) THEN 
        DELETE FROM Facturas WHERE fact_id = FacturaID;
        SELECT 'Factura eliminada correctamente' AS mensaje;
    ELSE
        SELECT 'La factura no existe' AS mensaje;
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `rol_usuario` (IN `p_rol_id` INT, IN `p_user_id` INT)   BEGIN 
SELECT facturas.*, usuarios.user_nombre, usuarios.user_apellido FROM facturas 
INNER JOIN usuarios ON usuarios.user_id = facturas.user_copiaid WHERE usuarios.rol_copiaid = p_rol_id AND user_id = p_user_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_buscar_user_rol` (IN `p_rol` VARCHAR(100))   BEGIN 
SELECT usuarios.*, roles.rol_descripcion FROM usuarios 
INNER JOIN roles ON usuarios.rol_copiaid = roles.rol_id AND roles.rol_descripcion = p_rol; 
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `SP_newuser` (IN `id` INT(11), IN `nombre` VARCHAR(100), IN `apellido` VARCHAR(100), IN `contrasena` VARCHAR(100), IN `ciudad` VARCHAR(100), IN `direccion` VARCHAR(100), IN `email` VARCHAR(100), IN `telefono` INT(11))   BEGIN
	INSERT INTO usuarios (user_id, user_nombre, user_apellido,user_password,user_ciudad,user_direccion,user_email,user_telefono)
    values (id,nombre, apellido,contraseña,ciudad,direccion,email,telefono);
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `cate_id` int(11) NOT NULL,
  `cate_descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`cate_id`, `cate_descripcion`) VALUES
(1, 'Refrigerado'),
(2, 'Congelado'),
(3, 'Seco');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `clien_id` int(11) NOT NULL,
  `clien_documento` int(11) NOT NULL,
  `clien_nombre` varchar(100) NOT NULL,
  `clien_ciudad` varchar(100) NOT NULL,
  `clien_direccion` varchar(100) NOT NULL,
  `clien_email` varchar(100) NOT NULL,
  `clien_telefono` int(11) NOT NULL,
  `clien_estado` varchar(100) NOT NULL DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`clien_id`, `clien_documento`, `clien_nombre`, `clien_ciudad`, `clien_direccion`, `clien_email`, `clien_telefono`, `clien_estado`) VALUES
(9096, 80504137, 'Pollos Hermanos', 'Bogota D.c', 'cll 54 #98 - 50', 'pollos@gmail.com', 2147483647, 'activo'),
(9103, 53131541, 'Tacos Tito', 'Bogota', 'cll 45sur #98', 'pollos@tacos.com', 2147483647, 'innactivo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entradas`
--

CREATE TABLE `entradas` (
  `ent_id` int(11) NOT NULL,
  `prov_copiaid` int(11) NOT NULL,
  `ent_detalle_producto` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`ent_detalle_producto`)),
  `ent_fecha_entrada` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `entradas`
--

INSERT INTO `entradas` (`ent_id`, `prov_copiaid`, `ent_detalle_producto`, `ent_fecha_entrada`) VALUES
(3123, 6, '{\"10\": [\"Pan\", \"12\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-27'),
(637235, 6, '{\"10\": [\"Pan\", \"2\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(724562, 6, '{\"10\": [\"Pan\", \"12\", \"Unidad\"], \"8\": [\"Carne\", \"12\", \"Kilogramo\"]}', '2024-08-29'),
(2147483647, 6, '{\"10\": [\"Pan\", \"2\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-28');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `fact_id` int(11) NOT NULL,
  `clien_copiaid` int(11) NOT NULL,
  `fact_detalle_productos` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`fact_detalle_productos`)),
  `fact_fecha_emision` date NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `facturas`
--

INSERT INTO `facturas` (`fact_id`, `clien_copiaid`, `fact_detalle_productos`, `fact_fecha_emision`) VALUES
(1, 9103, '{\"8\": [\"Carne\", \"10\", \"Kilogramo\"]}', '2024-08-24'),
(2, 9096, '{\"10\": [\"Pan\", \"12\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(3, 9096, '{\"10\": [\"Pan\", \"12\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(4, 9096, '{\"10\": [\"Pan\", \"12\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(5, 9096, '{\"10\": [\"Pan\", \"12\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(6, 9096, '{\"10\": [\"Pan\", \"1\", \"Unidad\"], \"8\": [\"Carne\", \"1\", \"Kilogramo\"]}', '2024-08-29'),
(7, 9096, '{\"10\": [\"Pan\", \"1\", \"Unidad\"], \"8\": [\"Carne\", \"1\", \"Kilogramo\"]}', '2024-08-29'),
(8, 9096, '{\"8\": [\"Carne\", \"1\", \"Kilogramo\"]}', '2024-08-29'),
(9, 9096, '{\"10\": [\"Pan\", \"1\", \"Unidad\"], \"8\": [\"Carne\", \"1\", \"Kilogramo\"]}', '2024-08-29'),
(10, 9096, '{\"10\": [\"Pan\", \"1\", \"Unidad\"], \"8\": [\"Carne\", \"1\", \"Kilogramo\"]}', '2024-08-29'),
(11, 9096, '{\"10\": [\"Pan\", \"2\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(12, 9096, '{\"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(13, 9096, '{\"10\": [\"Pan\", \"2\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(14, 9096, '{\"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(15, 9096, '{\"10\": [\"Pan\", \"2\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(16, 9096, '{\"10\": [\"Pan\", \"2\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29'),
(17, 9096, '{\"10\": [\"Pan\", \"2\", \"Unidad\"], \"8\": [\"Carne\", \"2\", \"Kilogramo\"]}', '2024-08-29');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `prod_id` int(11) NOT NULL,
  `prod_descripcion` varchar(255) NOT NULL,
  `cate_copiaid` int(11) NOT NULL,
  `prod_unidad_medida` varchar(100) NOT NULL,
  `prod_precio` int(11) NOT NULL,
  `prod_estado` varchar(100) NOT NULL DEFAULT 'agotado',
  `prod_stock` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`prod_id`, `prod_descripcion`, `cate_copiaid`, `prod_unidad_medida`, `prod_precio`, `prod_estado`, `prod_stock`) VALUES
(8, 'Carne', 1, 'Kilogramo', 1500, 'disponible', 11),
(10, 'Pan', 3, 'Unidad', 1500, 'disponible', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedor`
--

CREATE TABLE `proveedor` (
  `prov_id` int(11) NOT NULL,
  `prov_nit` int(11) NOT NULL,
  `prov_razonsocial` varchar(100) NOT NULL,
  `prov_email` varchar(100) NOT NULL,
  `prov_telefono` int(11) NOT NULL,
  `prov_estado` varchar(100) NOT NULL DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedor`
--

INSERT INTO `proveedor` (`prov_id`, `prov_nit`, `prov_razonsocial`, `prov_email`, `prov_telefono`, `prov_estado`) VALUES
(6, 42, 'Proveedor de Maiz', 'maiz@gmail.com', 51234123, 'activo'),
(7, 123, 'Proveedor Carne', 'carne@gmail.com', 32133421, 'activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_usuario`
--

CREATE TABLE `tipo_usuario` (
  `rol_id` int(11) NOT NULL,
  `rol_descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tipo_usuario`
--

INSERT INTO `tipo_usuario` (`rol_id`, `rol_descripcion`) VALUES
(1, 'administrador'),
(2, 'usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `user_id` int(11) NOT NULL,
  `user_nombre` varchar(100) NOT NULL,
  `user_apellido` varchar(100) NOT NULL,
  `user_password` char(102) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `user_telefono` int(11) NOT NULL,
  `rol_copiaid` int(11) NOT NULL,
  `user_estado` varchar(100) NOT NULL DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`user_id`, `user_nombre`, `user_apellido`, `user_password`, `user_email`, `user_telefono`, `rol_copiaid`, `user_estado`) VALUES
(123, 'Juan David', 'Figueroa', '1$k9phlL3jK4wjcPHR$4972014ced28bbb3b8376bda50de594a01633eee2b2a8a494199b39f053dc05625d2a188c1983d8d66d', 'juan@gmail.com', 312312, 1, 'innactivo'),
(321, 'Prueba ', '1', '$2b$12$2LVC8XE/PY75gb.ppBkvjeeaWlKMElybCOv1NhmDAUUZldF8MZmZK', 'fabio@mail.com', 412341235, 1, 'activo'),
(1013101334, 'Juan', 'Cuvides', '$2b$12$q1XxKREfnVgQgCx0APT5BegOcvsZsHWGLypRA58nRMpkOpSlxvhz6', 'juanDavid@gmail.com', 2147483647, 1, 'activo');

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `v_estado_factura`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `v_estado_factura` (
);

-- --------------------------------------------------------

--
-- Estructura Stand-in para la vista `v_estado_user`
-- (Véase abajo para la vista actual)
--
CREATE TABLE `v_estado_user` (
);

-- --------------------------------------------------------

--
-- Estructura para la vista `v_estado_factura`
--
DROP TABLE IF EXISTS `v_estado_factura`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_estado_factura`  AS SELECT `facturas`.`fact_id` AS `ID`, `facturas`.`clien_copiaid` AS `IdUser`, `facturas`.`fact_estado` AS `Estado` FROM `facturas` ;

-- --------------------------------------------------------

--
-- Estructura para la vista `v_estado_user`
--
DROP TABLE IF EXISTS `v_estado_user`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `v_estado_user`  AS SELECT `facturas`.`fact_id` AS `ID`, `facturas`.`clien_copiaid` AS `UsuarioID`, `facturas`.`fact_estado` AS `Estado` FROM `facturas` ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`cate_id`);

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`clien_id`);

--
-- Indices de la tabla `entradas`
--
ALTER TABLE `entradas`
  ADD PRIMARY KEY (`ent_id`),
  ADD KEY `prov_copiaid` (`prov_copiaid`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`fact_id`),
  ADD KEY `idx_Facturas_ID_Factura` (`fact_id`),
  ADD KEY `fk_cliente_copia` (`clien_copiaid`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`prod_id`),
  ADD KEY `FK_cate_copiaid` (`cate_copiaid`);

--
-- Indices de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  ADD PRIMARY KEY (`prov_id`);

--
-- Indices de la tabla `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
  ADD PRIMARY KEY (`rol_id`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`user_id`),
  ADD KEY `rol_copiaid` (`rol_copiaid`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias`
--
ALTER TABLE `categorias`
  MODIFY `cate_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `clien_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9107;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `fact_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `prod_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT de la tabla `proveedor`
--
ALTER TABLE `proveedor`
  MODIFY `prov_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `entradas`
--
ALTER TABLE `entradas`
  ADD CONSTRAINT `entradas_ibfk_1` FOREIGN KEY (`prov_copiaid`) REFERENCES `proveedor` (`prov_id`),
  ADD CONSTRAINT `fk_preveedor_copia` FOREIGN KEY (`prov_copiaid`) REFERENCES `proveedor` (`prov_id`);

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `fk_cliente_copia` FOREIGN KEY (`clien_copiaid`) REFERENCES `clientes` (`clien_id`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `FK_cate_copiaid` FOREIGN KEY (`cate_copiaid`) REFERENCES `categorias` (`cate_id`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`rol_copiaid`) REFERENCES `tipo_usuario` (`rol_id`),
  ADD CONSTRAINT `usuarios_roles_fk` FOREIGN KEY (`rol_copiaid`) REFERENCES `tipo_usuario` (`rol_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
