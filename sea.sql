/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50550 (5.5.50)
 Source Host           : localhost:3306
 Source Schema         : sea

 Target Server Type    : MySQL
 Target Server Version : 50550 (5.5.50)
 File Encoding         : 65001

 Date: 05/05/2024 17:55:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `forum_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` int(11) NOT NULL,
  `comment_time` datetime NOT NULL,
  `likes` int(11) NULL DEFAULT NULL,
  `score` float NULL DEFAULT NULL,
  `user_id_like` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL COMMENT '点赞用户ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for comment_new
-- ----------------------------
DROP TABLE IF EXISTS `comment_new`;
CREATE TABLE `comment_new`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `status` int(1) NULL DEFAULT NULL,
  `comment_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for forum
-- ----------------------------
DROP TABLE IF EXISTS `forum`;
CREATE TABLE `forum`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `time` datetime NULL DEFAULT NULL,
  `section` int(1) NULL DEFAULT NULL COMMENT '1普通帖子，2信息，3新闻',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for marine_life
-- ----------------------------
DROP TABLE IF EXISTS `marine_life`;
CREATE TABLE `marine_life`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `species` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `habitat_region` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `quantity` int(11) NULL DEFAULT NULL,
  `status` int(11) NOT NULL,
  `time` datetime NULL DEFAULT NULL,
  `originalscientificname` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `kingdom` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `date_year` int(11) NULL DEFAULT NULL,
  `decimallongitude` float NULL DEFAULT NULL,
  `decimallatitude` float NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `index_status`(`status`) USING BTREE,
  INDEX `index_status_name`(`name`, `status`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 50595 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for marine_life_comment
-- ----------------------------
DROP TABLE IF EXISTS `marine_life_comment`;
CREATE TABLE `marine_life_comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marine_life_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` int(11) NOT NULL,
  `comment_time` datetime NOT NULL,
  `likes` int(11) NULL DEFAULT NULL,
  `score` float NULL DEFAULT NULL,
  `user_id_like` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for marine_life_comment_new
-- ----------------------------
DROP TABLE IF EXISTS `marine_life_comment_new`;
CREATE TABLE `marine_life_comment_new`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `marine_life_comment_id` int(11) NULL DEFAULT NULL COMMENT '海洋生物评论表id',
  `user_id` int(11) NULL DEFAULT NULL,
  `comment` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `status` int(1) NULL DEFAULT NULL,
  `comment_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for ocean_region
-- ----------------------------
DROP TABLE IF EXISTS `ocean_region`;
CREATE TABLE `ocean_region`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `location` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `temperature` float NOT NULL,
  `salinity` float NULL DEFAULT NULL,
  `status` int(1) NULL DEFAULT NULL,
  `time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for ocean_region_feature_comment
-- ----------------------------
DROP TABLE IF EXISTS `ocean_region_feature_comment`;
CREATE TABLE `ocean_region_feature_comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ocean_region_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` text CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `status` int(11) NOT NULL,
  `comment_time` datetime NOT NULL,
  `likes` int(11) NOT NULL,
  `score` float NULL DEFAULT NULL,
  `user_id_like` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for ocean_region_feature_comment_new
-- ----------------------------
DROP TABLE IF EXISTS `ocean_region_feature_comment_new`;
CREATE TABLE `ocean_region_feature_comment_new`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ocean_region_feather_comment_id` int(11) NULL DEFAULT NULL COMMENT '海洋区域特征评论表id',
  `user_id` int(11) NULL DEFAULT NULL,
  `comment` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `status` int(1) NULL DEFAULT NULL,
  `comment_time` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `role` int(11) NOT NULL,
  `full_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone_number` varchar(15) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `status` int(1) NULL DEFAULT NULL COMMENT '1正常，2禁用',
  `imageUrl` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE,
  UNIQUE INDEX `phone_number`(`phone_number`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 24 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

SET FOREIGN_KEY_CHECKS = 1;
